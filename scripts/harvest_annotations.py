#!/usr/bin/env python3
"""留言收割流水线 -- 把连续阅读稿里的 `> [!留]` 留言收割进 annotation 真源页。

纯 stdlib,零依赖。设计与验收依据:
  - 合同 /home/ubuntu/.claude/jobs/fc51b3d3/tmp/CONTRACT-harvest.md
  - 方案 /home/ubuntu/.claude/plans/effervescent-wiggling-hopcroft.md

硬边界(见合同):只写 annotations/、wiki/_candidates/_distill-queue.md 与连续阅读稿本身
的 `> [!留]` callout 块;不动 sources/**/raw、canonical 转写稿正文、annotation 既有内容;
除本次新增/替换的字节外,连续阅读稿其余字节零改动。

用法:
    python3 scripts/harvest_annotations.py [--root PATH] [--dry-run] [--date YYYY-MM-DD]

--root      仓库根目录(默认:本脚本所在目录的上一级)
--dry-run   只打印将要发生的改动,不写任何文件
--date      覆盖"今天"的日期(测试用;默认取系统当前日期)
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# 正则与常量
# ---------------------------------------------------------------------------

CALLOUT_START_RE = re.compile(r"^> \[!留\]\s*(.*)$")
CANONICAL_TEXT_RE = re.compile(
    r"^- \[(\d{2}:\d{2}:\d{2}\.\d+)[–-](\d{2}:\d{2}:\d{2}\.\d+)\] (.*)$"
)
CANONICAL_ANCHOR_RE = re.compile(r"^\s*\^([\w-]+)\s*$")
CR_FILENAME_RE = re.compile(r"__(BV\w+)__P(\d+)__连续阅读\.md$")
TITLE_LINE_RE = re.compile(r"^title:\s*(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")

DISTILL_MARK = "批准蒸馏"
ANNOTATION_SECTION_HEADING = "## 留言栏（用户原话）"

REPORT_LINES: List[str] = []


def log(msg: str) -> None:
    REPORT_LINES.append(msg)


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------


def strip_punct(s: str) -> str:
    """去掉标点与空白(含全角),只保留可比较的核心字符。"""
    return "".join(ch for ch in s if not unicodedata.category(ch).startswith(("P", "Z")))


def strip_quote_prefix(line: str) -> str:
    return re.sub(r"^>\s?", "", line)


def ts_to_mmss(ts: str) -> str:
    h, m, s = ts.split(":")
    total = int(h) * 3600 + int(m) * 60 + float(s)
    total_int = int(total)
    mm, ss = divmod(total_int, 60)
    return f"{mm:02d}:{ss:02d}"


# ---------------------------------------------------------------------------
# canonical 转写稿解析
# ---------------------------------------------------------------------------


@dataclass
class Segment:
    text: str
    anchor: Optional[str]
    start_ts: str


def parse_canonical(path: Path) -> List[Segment]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").split("\n")
    segments: List[Segment] = []
    i = 0
    while i < len(lines):
        m = CANONICAL_TEXT_RE.match(lines[i])
        if m:
            start_ts, _end_ts, txt = m.groups()
            anchor = None
            if i + 1 < len(lines):
                am = CANONICAL_ANCHOR_RE.match(lines[i + 1])
                if am:
                    anchor = am.group(1)
            segments.append(Segment(text=txt, anchor=anchor, start_ts=start_ts))
            i += 2
        else:
            i += 1
    return segments


def build_corpus(segments: List[Segment]) -> Tuple[str, List[Tuple[int, int]]]:
    parts = []
    offsets: List[Tuple[int, int]] = []
    pos = 0
    for seg in segments:
        s = strip_punct(seg.text)
        offsets.append((pos, pos + len(s)))
        parts.append(s)
        pos += len(s)
    return "".join(parts), offsets


def find_segment_for_paragraph(
    paragraph: str,
    segments: List[Segment],
    corpus: str,
    offsets: List[Tuple[int, int]],
    cursor: int,
) -> Tuple[Optional[Segment], int]:
    """用段首 ~15 字(标点无关)在 corpus 里找起点,映射回所在 segment。

    命中失败时依次缩短匹配长度做容错;仍失败则返回 (None, cursor)(降级不失败)。
    """
    target_full = strip_punct(paragraph)
    if not target_full:
        return None, cursor
    for length in (15, 12, 10, 8, 6):
        if len(target_full) < length:
            continue
        target = target_full[:length]
        idx = corpus.find(target, cursor)
        if idx == -1:
            idx = corpus.find(target)
        if idx != -1:
            seg_idx = None
            for k, (s, e) in enumerate(offsets):
                if s <= idx < e or (idx == s == e):
                    seg_idx = k
                    break
            if seg_idx is None:
                for k, (s, e) in enumerate(offsets):
                    if idx <= s:
                        seg_idx = k
                        break
            if seg_idx is not None:
                return segments[seg_idx], idx
    return None, cursor


# ---------------------------------------------------------------------------
# 文件缓存(统一 dry-run / 写盘)
# ---------------------------------------------------------------------------


class FileCache:
    def __init__(self) -> None:
        self.cache: dict = {}
        self.dirty: set = set()

    def get(self, path: Path, default_factory=None) -> str:
        if path not in self.cache:
            if path.exists():
                self.cache[path] = path.read_text(encoding="utf-8")
            elif default_factory is not None:
                self.cache[path] = default_factory()
            else:
                self.cache[path] = ""
        return self.cache[path]

    def set(self, path: Path, text: str) -> None:
        self.cache[path] = text
        self.dirty.add(path)

    def flush(self, dry_run: bool) -> List[Path]:
        changed = sorted(self.dirty, key=str)
        if not dry_run:
            for path in changed:
                path.parent.mkdir(parents=True, exist_ok=True)
                self._atomic_write(path, self.cache[path])
        return changed

    @staticmethod
    def _atomic_write(path: Path, text: str) -> None:
        """同目录 tempfile 写入 + os.replace 原子替换,避免半写截断。"""
        import os
        import tempfile

        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            os.replace(tmp_name, path)
        except BaseException:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise


# ---------------------------------------------------------------------------
# Markdown 小节插入
# ---------------------------------------------------------------------------


def heading_level(line: str) -> Optional[int]:
    m = HEADING_RE.match(line)
    return len(m.group(1)) if m else None


def find_heading_index(lines: List[str], heading_text: str) -> Optional[int]:
    for i, l in enumerate(lines):
        if l.strip() == heading_text.strip():
            return i
    return None


def section_end(lines: List[str], start_idx: int) -> int:
    level = heading_level(lines[start_idx])
    for j in range(start_idx + 1, len(lines)):
        lvl = heading_level(lines[j])
        if lvl is not None and lvl <= level:
            return j
    return len(lines)


def insert_in_section(
    text: str, heading_text: str, sub_heading_text: Optional[str], block_lines: List[str]
) -> str:
    """在 heading_text 小节末尾插入 block_lines;若给了 sub_heading_text,
    优先插入到已存在的同名子标题末尾,否则新建子标题再插入。"""
    lines = text.split("\n")
    h_idx = find_heading_index(lines, heading_text)
    if h_idx is None:
        raise ValueError(f"heading not found: {heading_text}")
    end_idx = section_end(lines, h_idx)

    if sub_heading_text:
        sub_idx = None
        for k in range(h_idx + 1, end_idx):
            if lines[k].strip() == sub_heading_text.strip():
                sub_idx = k
                break
        if sub_idx is not None:
            sub_end = section_end(lines, sub_idx)
            insert_at = sub_end
            new_lines = lines[:insert_at] + [""] + block_lines + [""] + lines[insert_at:]
        else:
            insert_at = end_idx
            new_lines = (
                lines[:insert_at]
                + ["", sub_heading_text, ""]
                + block_lines
                + [""]
                + lines[insert_at:]
            )
    else:
        insert_at = end_idx
        new_lines = lines[:insert_at] + [""] + block_lines + [""] + lines[insert_at:]
    result = "\n".join(new_lines)
    return collapse_blank_lines(result)


def collapse_blank_lines(text: str) -> str:
    """把 3+ 个连续换行(2+ 个空行)收敛为 1 个空行,只影响本脚本插入造成的多余空行。"""
    return re.sub(r"\n{3,}", "\n\n", text)


def append_flat(text: str, block_lines: List[str]) -> str:
    if not text.endswith("\n"):
        text += "\n"
    if not text.endswith("\n\n"):
        text += "\n"
    return collapse_blank_lines(text + "\n".join(block_lines) + "\n")


# ---------------------------------------------------------------------------
# annotation 页模板与锚号
# ---------------------------------------------------------------------------


def next_seq(text: str, bvid: str, part: int) -> int:
    pattern = re.compile(rf"\^an-{re.escape(bvid.lower())}-p{part:02d}-(\d+)\b")
    nums = [int(m) for m in pattern.findall(text)]
    return (max(nums) + 1) if nums else 1


def render_new_annotation(
    bvid: str,
    mid: str,
    part: int,
    title: str,
    cr_relpath: str,
    canonical_relpath: str,
    index_relpath: str,
    today: str,
) -> str:
    tags = "[bilibili, 阅读批注]"
    fm = (
        "---\n"
        f'title: "视频留言与思考：{title}"\n'
        "type: annotation\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        f"tags: {tags}\n"
        f"sources:\n  - {canonical_relpath}\n"
        f"related:\n  - {cr_relpath}\n  - {index_relpath}\n"
        "confidence: high\n"
        "author: user\n"
        f"bvid: {bvid}\n"
        f"mid: {mid}\n"
        f"part: {part}\n"
        "---\n"
    )
    body = (
        "\n# 视频留言与思考\n\n"
        "> [!note] 留言规则\n"
        "> 本页保存主人的阅读留言。AI 不得覆盖或静默改写用户原话；"
        "AI 的回应必须放在独立的 `[!ai-note]` 区块。主人可以直接在"
        "“留言栏（用户原话）”末尾继续追加。\n\n"
        "## 阅读状态\n\n"
        f"- [ ] 已阅读（{today}）\n\n"
        f"{ANNOTATION_SECTION_HEADING}\n\n"
        "## 蒸馏状态\n\n"
        "## See Also\n\n"
        f"- [连续阅读版]({cr_relpath})\n"
        f"- [带时间戳原话]({canonical_relpath})\n"
        f"- [视频索引]({index_relpath})\n"
    )
    return fm + body


# ---------------------------------------------------------------------------
# 段落定位
# ---------------------------------------------------------------------------


def find_paragraph_above(lines: List[str], idx: int) -> str:
    i = idx - 1
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    while i >= 0 and lines[i].lstrip().startswith(">"):
        i -= 1
        while i >= 0 and lines[i].strip() == "":
            i -= 1
    if i < 0:
        return ""
    end = i
    start = i
    while start >= 0 and lines[start].strip() != "" and not lines[start].lstrip().startswith(">"):
        start -= 1
    start += 1
    if end < start:
        return ""
    para_lines = lines[start : end + 1]
    return "".join(l.strip() for l in para_lines)


# ---------------------------------------------------------------------------
# 主处理逻辑
# ---------------------------------------------------------------------------


def relpath(target: Path, start: Path) -> str:
    import os

    return os.path.relpath(target, start=start).replace("\\", "/")


def process_continuous_file(
    cr_path: Path, root: Path, today: str, cache: FileCache
) -> bool:
    m = CR_FILENAME_RE.search(cr_path.name)
    if not m:
        log(f"跳过(文件名不含 BVID/P 号): {cr_path}")
        return False
    bvid, part_str = m.group(1), m.group(2)
    part = int(part_str)
    mid = cr_path.parents[2].name

    canonical_path = cr_path.parent / cr_path.name.replace("__连续阅读.md", ".md")
    segments = parse_canonical(canonical_path)
    corpus, offsets = build_corpus(segments)

    annotation_path = root / "annotations" / "bilibili" / mid / f"{bvid}.md"
    distill_path = root / "wiki" / "_candidates" / "_distill-queue.md"
    index_path = root / "sources" / "bilibili" / mid / "视频索引.md"

    text = cache.get(cr_path)
    trailing_nl = text.endswith("\n")
    lines = text.split("\n")
    if trailing_nl:
        lines = lines[:-1]

    title = bvid
    for l in lines[:30]:
        tm = TITLE_LINE_RE.match(l)
        if tm:
            t = tm.group(1).strip().strip('"')
            title = t.replace("（连续阅读版）", "").strip()
            break

    modified = False
    cursor = 0
    i = 0
    while i < len(lines):
        cm = CALLOUT_START_RE.match(lines[i])
        if cm and not cm.group(1).strip().startswith("✓"):
            start = i
            first_remainder = cm.group(1)
            j = i + 1
            cont: List[str] = []
            while (
                j < len(lines)
                and lines[j].startswith(">")
                and not CALLOUT_START_RE.match(lines[j])
            ):
                cont.append(strip_quote_prefix(lines[j]))
                j += 1
            content_parts = [first_remainder.strip()] + [c.strip() for c in cont]
            content = "\n".join(p for p in content_parts if p != "")

            paragraph = find_paragraph_above(lines, start)
            quote = paragraph.strip()[:60]

            seg, idx = find_segment_for_paragraph(paragraph, segments, corpus, offsets, cursor)
            if seg is not None:
                cursor = idx

            if content.strip().startswith(DISTILL_MARK):
                note = content.strip()[len(DISTILL_MARK) :].strip(" :：-\n")
                link_md = None
                if seg is not None and seg.anchor:
                    link_md = (
                        f"[[{relpath(canonical_path, distill_path.parent)}#^{seg.anchor}"
                        f"|{ts_to_mmss(seg.start_ts)}]]"
                    )
                block = [
                    f"## {today} · {bvid} P{part:02d}",
                    "",
                    f"- mid: {mid}",
                    f"- 留言备注：{note if note else '(无备注)'}",
                    f"- 段落引文：{quote}…" if quote else "- 段落引文：（未能定位到段落）",
                ]
                if link_md:
                    block.append(f"- 定位：{link_md}")
                else:
                    block.append("- 定位：（未匹配到 canonical 锚点，仅存段落引文）")
                distill_text = cache.get(
                    distill_path,
                    default_factory=lambda: (
                        "# 蒸馏候选队列\n\n"
                        "> 本文件由 `scripts/harvest_annotations.py` 自动追加"
                        "（来自连续阅读稿里的「批准蒸馏」标记）。队列的消费"
                        "（生成 `wiki/_candidates/` 正式候选、走 D0–D5 审批）"
                        "不在本次收割流水线范围内。\n"
                    ),
                )
                distill_text = append_flat(distill_text, block)
                cache.set(distill_path, distill_text)

                new_line = "> [!留] ✓ 已入蒸馏队列"
                lines[start:j] = [new_line]
                modified = True
                i = start + 1
                continue
            else:
                ann_text = cache.get(
                    annotation_path,
                    default_factory=lambda: render_new_annotation(
                        bvid,
                        mid,
                        part,
                        title,
                        relpath(cr_path, annotation_path.parent),
                        relpath(canonical_path, annotation_path.parent),
                        relpath(index_path, annotation_path.parent),
                        today,
                    ),
                )
                seq = next_seq(ann_text, bvid, part)
                anchor_full = f"an-{bvid.lower()}-p{part:02d}-{seq:03d}"

                link_md = None
                if seg is not None and seg.anchor:
                    link_md = (
                        f"[[{relpath(canonical_path, annotation_path.parent)}#^{seg.anchor}"
                        f"|{ts_to_mmss(seg.start_ts)}]]"
                    )
                quote_line = (
                    f"> 原文引文：{quote}… {link_md}"
                    if link_md
                    else f"> 原文引文：{quote}…（未匹配到 canonical 锚点）"
                    if quote
                    else "> 原文引文：（未能定位到段落，仅保留留言正文）"
                )
                entry_lines = [quote_line, ">"]
                for cl in content.split("\n"):
                    entry_lines.append(f"> {cl}" if cl else ">")
                entry_lines.append("")
                entry_lines.append(f"^{anchor_full}")

                sub_heading = f"### {today} · 随文留言"
                ann_text = insert_in_section(
                    ann_text, ANNOTATION_SECTION_HEADING, sub_heading, entry_lines
                )
                cache.set(annotation_path, ann_text)

                rel_to_ann = relpath(annotation_path, cr_path.parent)
                new_line = f"> [!留] ✓ 已收录 → [[{rel_to_ann}#^{anchor_full}]]"
                lines[start:j] = [new_line]
                modified = True
                i = start + 1
                continue
        i += 1

    if modified:
        new_text = "\n".join(lines) + ("\n" if trailing_nl else "")
        cache.set(cr_path, new_text)
        log(f"收割: {cr_path}")
    return modified


def iter_continuous_files(root: Path):
    bilibili_dir = root / "sources" / "bilibili"
    if not bilibili_dir.exists():
        return
    for mid_dir in sorted(bilibili_dir.iterdir()):
        tdir = mid_dir / "transcripts"
        if not tdir.exists():
            continue
        for f in sorted(tdir.rglob("*连续阅读.md")):
            yield f


def run(root: Path, today: str, dry_run: bool) -> List[Path]:
    cache = FileCache()
    any_modified = False
    for cr_path in iter_continuous_files(root):
        if process_continuous_file(cr_path, root, today, cache):
            any_modified = True
    changed = cache.flush(dry_run)
    if not any_modified:
        log("空转:未发现待收割的 `> [!留]` 留言。")
    return changed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None, help="仓库根目录(默认 scripts/ 的上一级)")
    parser.add_argument("--dry-run", action="store_true", help="只打印改动,不写文件")
    parser.add_argument("--date", default=None, help="覆盖今天日期 YYYY-MM-DD(测试用)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    today = args.date or date.today().isoformat()

    changed = run(root, today, args.dry_run)

    for l in REPORT_LINES:
        print(l)
    if changed:
        verb = "将写入" if args.dry_run else "已写入"
        print(f"{verb} {len(changed)} 个文件:")
        for p in changed:
            print(f"  - {p}")
    else:
        print("无文件改动。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
