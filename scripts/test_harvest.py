#!/usr/bin/env python3
"""留言收割流水线的测试套件(stdlib unittest,零依赖)。

严格只在 tempfile 临时目录(系统 /tmp 下)构造沙箱仓库结构跑测试,
不读写 /home/ubuntu/study-notes 的任何真实文件。

覆盖合同要求的断言类别:
  1. 幂等(重跑零变化)
  2. 空转(零留言)
  3. 多留言多段(锚号递增不冲突)
  4. canonical 匹配命中
  5. canonical 匹配未命中降级(不失败)
  6. 非目标字节零改动(哈希/切片断言)
  7. 指针替换正确
  8. 蒸馏标记识别与路由
  9. 蒸馏标记重复处理幂等
  10. 蒸馏队列追加格式
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_PATH = Path(__file__).resolve().parent / "harvest_annotations.py"
_spec = importlib.util.spec_from_file_location("harvest_annotations", SCRIPT_PATH)
ha = importlib.util.module_from_spec(_spec)
sys.modules["harvest_annotations"] = ha
_spec.loader.exec_module(ha)  # type: ignore[union-attr]


BVID = "BV1testXXXX"
BVID_LOWER = BVID.lower()
MID = "999999999"
PART = 1
TODAY = "2026-07-16"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class HarvestSandbox:
    """在临时目录里搭建一个最小但结构合法的 study-notes 仓库切片。"""

    def __init__(self, tmp_root: Path):
        self.root = tmp_root
        self.mid_dir = self.root / "sources" / "bilibili" / MID
        self.transcripts_dir = self.mid_dir / "transcripts" / "2026"
        self.annotations_dir = self.root / "annotations" / "bilibili" / MID
        self.distill_path = self.root / "wiki" / "_candidates" / "_distill-queue.md"

        self.transcripts_dir.mkdir(parents=True)
        self.annotations_dir.mkdir(parents=True)
        (self.root / "wiki" / "_candidates").mkdir(parents=True, exist_ok=True)

        self.canonical_path = self.transcripts_dir / f"2026-07-16__test__{BVID}__P01.md"
        self.cr_path = self.transcripts_dir / f"2026-07-16__test__{BVID}__P01__连续阅读.md"
        self.annotation_path = self.annotations_dir / f"{BVID}.md"

        self._write_canonical()

    def _write_canonical(self):
        segments = [
            ("00:00:00.000", "00:00:02.000", "这是第一段测试文本用来验证匹配"),
            ("00:00:02.000", "00:00:04.500", "这是第二段测试文本继续讲解流程"),
            ("00:00:04.500", "00:00:07.000", "这是第三段完全不同的收尾内容"),
        ]
        lines = [
            "---",
            "title: 测试视频",
            "type: transcript",
            f"bvid: {BVID}",
            f"mid: {MID}",
            f"part: {PART}",
            "---",
            "",
        ]
        for idx, (s, e, txt) in enumerate(segments, start=1):
            ms = idx * 1000
            lines.append(f"- [{s}–{e}] {txt}")
            lines.append(f"  ^{BVID_LOWER}-p{PART:02d}-{ms:09d}-{idx:03d}")
            lines.append("")
        self.canonical_path.write_text("\n".join(lines), encoding="utf-8")

    def write_continuous(self, body_paragraphs_and_callouts: str):
        text = (
            "---\n"
            "title: 测试视频（连续阅读版）\n"
            "type: transcript\n"
            f"bvid: {BVID}\n"
            f"mid: {MID}\n"
            f"part: {PART}\n"
            "---\n\n"
            + body_paragraphs_and_callouts
        )
        self.cr_path.write_text(text, encoding="utf-8")

    def read_continuous(self) -> str:
        return self.cr_path.read_text(encoding="utf-8")

    def write_existing_annotation(self, max_seq: int = 1):
        text = (
            "---\n"
            "title: 既有留言页\n"
            "type: annotation\n"
            f"bvid: {BVID}\n"
            f"mid: {MID}\n"
            f"part: {PART}\n"
            "author: user\n"
            "---\n\n"
            "# 视频留言与思考\n\n"
            "## 阅读状态\n\n"
            "- [x] 已阅读\n\n"
            "## 留言栏（用户原话）\n\n"
            "### 2026-07-10 · 已阅读\n\n"
            "> 这是一条既有的手写留言，脚本不得改动。\n\n"
            f"^an-{BVID_LOWER}-p{PART:02d}-{max_seq:03d}\n\n"
            "## 蒸馏状态\n\n"
            "## See Also\n\n"
            "- 占位\n"
        )
        self.annotation_path.write_text(text, encoding="utf-8")

    def read_annotation(self) -> str:
        return self.annotation_path.read_text(encoding="utf-8")

    def read_distill(self) -> str:
        return self.distill_path.read_text(encoding="utf-8") if self.distill_path.exists() else ""

    def run(self, dry_run: bool = False, today: str = TODAY):
        return ha.run(self.root, today, dry_run)


class BaseHarvestTest(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory(prefix="harvest-test-")
        self.sandbox = HarvestSandbox(Path(self._tmpdir.name))

    def tearDown(self):
        self._tmpdir.cleanup()


# ---------------------------------------------------------------------------
# 1. 空转:零留言 -> 零改动
# ---------------------------------------------------------------------------


class TestEmptyRun(BaseHarvestTest):
    def test_no_callouts_means_no_changes(self):
        sb = self.sandbox
        body = "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n这是第三段完全不同的收尾内容。\n"
        sb.write_continuous(body)
        before = sb.read_continuous()
        before_hash = sha256(before)

        changed = sb.run()

        self.assertEqual(changed, [], "零留言应零改动")
        after_hash = sha256(sb.read_continuous())
        self.assertEqual(before_hash, after_hash)
        self.assertFalse(sb.annotation_path.exists(), "不应凭空创建 annotation 页")
        self.assertFalse(sb.distill_path.exists(), "不应凭空创建 distill 队列")


# ---------------------------------------------------------------------------
# 2. canonical 匹配命中 + 3. 匹配未命中降级
# ---------------------------------------------------------------------------


class TestAnchorMatching(BaseHarvestTest):
    def test_match_hit_produces_backlink_with_timestamp(self):
        sb = self.sandbox
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 这段能对上原文\n\n"
            "这是第三段完全不同的收尾内容。\n"
        )
        sb.write_continuous(body)

        sb.run()

        ann = sb.read_annotation()
        self.assertIn(f"{sb.canonical_path.name}", ann)
        self.assertIn(f"#^{BVID_LOWER}-p01-000001000-001", ann)
        self.assertIn("|00:00]]", ann)
        self.assertIn("这段能对上原文", ann)

    def test_match_miss_degrades_without_crash(self):
        sb = self.sandbox
        body = (
            "完全不存在于canonical里的一段随意文字用来测试降级路径。\n\n"
            "> [!留] 这段对不上原文，应当降级\n"
        )
        sb.write_continuous(body)

        changed = sb.run()  # 不应抛异常

        self.assertIn(sb.annotation_path, changed)
        ann = sb.read_annotation()
        self.assertIn("这段对不上原文，应当降级", ann)
        self.assertIn("未匹配到 canonical 锚点", ann)
        self.assertNotIn("#^", ann.split("原文引文")[-1].split("\n")[0])


# ---------------------------------------------------------------------------
# 4. 多留言多段 + 锚号递增不冲突
# ---------------------------------------------------------------------------


class TestMultipleCommentsAnchors(BaseHarvestTest):
    def test_two_comments_get_sequential_anchors_continuing_existing_max(self):
        sb = self.sandbox
        sb.write_existing_annotation(max_seq=1)  # 已有 ^an-...-001
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 第一条随文留言\n\n"
            "这是第三段完全不同的收尾内容。\n\n"
            "> [!留] 第二条随文留言\n"
        )
        sb.write_continuous(body)

        sb.run()

        ann = sb.read_annotation()
        self.assertIn(f"^an-{BVID_LOWER}-p01-001", ann, "既有锚点不能被破坏")
        self.assertIn(f"^an-{BVID_LOWER}-p01-002", ann, "第一条新留言应为 002")
        self.assertIn(f"^an-{BVID_LOWER}-p01-003", ann, "第二条新留言应为 003,不与 002 冲突")
        self.assertIn("第一条随文留言", ann)
        self.assertIn("第二条随文留言", ann)
        # 既有手写留言原文必须逐字保留
        self.assertIn("这是一条既有的手写留言，脚本不得改动。", ann)

    def test_adjacent_callouts_do_not_merge(self):
        """紧邻的两条 `> [!留]` 之间没有空行分隔时,不应被续行收集吞并成一条。"""
        sb = self.sandbox
        sb.write_existing_annotation(max_seq=1)  # 已有 ^an-...-001
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 第一条相邻留言\n"
            "> [!留] 第二条相邻留言\n\n"
            "这是第三段完全不同的收尾内容。\n"
        )
        sb.write_continuous(body)

        sb.run()

        ann = sb.read_annotation()
        cr_text = sb.read_continuous()

        # 两条相邻留言必须各自产出独立条目,锚号连续递增(002, 003)
        self.assertIn(f"^an-{BVID_LOWER}-p01-002", ann, "第一条相邻留言应为 002")
        self.assertIn(f"^an-{BVID_LOWER}-p01-003", ann, "第二条相邻留言应为 003")
        self.assertIn("第一条相邻留言", ann)
        self.assertIn("第二条相邻留言", ann)

        # 正文互不污染:002 条目正文里不能出现"第二条相邻留言",反之亦然
        entry_002 = ann.split(f"^an-{BVID_LOWER}-p01-002")[0].rsplit("### ", 1)[-1]
        self.assertNotIn("第二条相邻留言", entry_002)

        # 连续阅读稿里两条 callout 都应各自被替换为指针行,不留 `[!留]` 字面泄漏
        self.assertNotIn("[!留] 第一条相邻留言\n> [!留] 第二条相邻留言", cr_text)
        self.assertEqual(
            cr_text.count("[!留] ✓ 已收录"),
            2,
            "两条相邻留言应各自替换为两条独立的指针行",
        )
        self.assertNotIn("第一条相邻留言", cr_text, "原始留言正文不应残留在连续阅读稿里")
        self.assertNotIn("第二条相邻留言", cr_text, "原始留言正文不应残留在连续阅读稿里")


# ---------------------------------------------------------------------------
# 5. 非目标字节零改动(哈希/切片断言)
# ---------------------------------------------------------------------------


class TestNonTargetBytesUnchanged(BaseHarvestTest):
    def test_only_callout_lines_change_in_continuous_reading_file(self):
        sb = self.sandbox
        para1 = "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。"
        para2 = "这是第三段完全不同的收尾内容。"
        body = f"{para1}\n\n> [!留] 留言正文\n\n{para2}\n"
        sb.write_continuous(body)
        before_lines = sb.read_continuous().split("\n")

        sb.run()

        after_lines = sb.read_continuous().split("\n")
        # 找到 before 里 callout 起始行的位置
        callout_idx = next(i for i, l in enumerate(before_lines) if l.startswith("> [!留]"))

        prefix_before = "\n".join(before_lines[:callout_idx])
        prefix_after = "\n".join(after_lines[:callout_idx])
        self.assertEqual(
            sha256(prefix_before), sha256(prefix_after), "callout 之前的字节必须逐字节相同"
        )

        # callout 之后剩余内容(跳过被替换的单行)必须原样保留
        suffix_before = "\n".join(before_lines[callout_idx + 1 :])
        suffix_after = "\n".join(after_lines[callout_idx + 1 :])
        self.assertEqual(
            sha256(suffix_before), sha256(suffix_after), "callout 之后的字节必须逐字节相同"
        )

        # canonical 转写稿必须原封不动
        canonical_before = sb.canonical_path.read_text(encoding="utf-8")
        sb.run()  # 幂等重跑
        canonical_after = sb.canonical_path.read_text(encoding="utf-8")
        self.assertEqual(sha256(canonical_before), sha256(canonical_after))


# ---------------------------------------------------------------------------
# 6. 指针替换正确
# ---------------------------------------------------------------------------


class TestPointerReplacement(BaseHarvestTest):
    def test_callout_replaced_with_correct_pointer_line(self):
        sb = self.sandbox
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 留言正文\n\n"
            "这是第三段完全不同的收尾内容。\n"
        )
        sb.write_continuous(body)

        sb.run()

        cr_text = sb.read_continuous()
        expected_anchor = f"an-{BVID_LOWER}-p01-001"
        expected_rel = f"../../../../../annotations/bilibili/{MID}/{BVID}.md"
        expected_line = f"> [!留] ✓ 已收录 → [[{expected_rel}#^{expected_anchor}]]"
        self.assertIn(expected_line, cr_text)
        self.assertNotIn("留言正文", cr_text, "callout 原文应被替换,不再残留于连续阅读稿")

        ann = sb.read_annotation()
        self.assertIn(f"^{expected_anchor}", ann)


# ---------------------------------------------------------------------------
# 7. 幂等:重跑零变化
# ---------------------------------------------------------------------------


class TestIdempotency(BaseHarvestTest):
    def test_rerun_after_harvest_makes_no_further_changes(self):
        sb = self.sandbox
        sb.write_existing_annotation(max_seq=1)
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 留言正文\n\n"
            "这是第三段完全不同的收尾内容。\n\n"
            "> [!留] 批准蒸馏 备注甲\n"
        )
        sb.write_continuous(body)

        first_changed = sb.run()
        self.assertTrue(first_changed)

        snapshot = {
            p: p.read_text(encoding="utf-8")
            for p in (sb.cr_path, sb.annotation_path, sb.distill_path)
            if p.exists()
        }

        second_changed = sb.run()

        self.assertEqual(second_changed, [], "已收割/已入队后重跑不应再产生任何改动")
        for p, content in snapshot.items():
            self.assertEqual(content, p.read_text(encoding="utf-8"), f"{p} 不应在重跑后变化")

    def test_dry_run_never_writes_files(self):
        sb = self.sandbox
        body = "这是第一段测试文本，用来验证匹配。\n\n> [!留] 试探性留言\n"
        sb.write_continuous(body)

        changed = sb.run(dry_run=True)

        self.assertTrue(changed, "dry-run 也应报告将改动的文件列表")
        self.assertFalse(sb.annotation_path.exists(), "dry-run 不得真的写文件")
        cr_text = sb.read_continuous()
        self.assertIn("试探性留言", cr_text, "dry-run 不得改动源文件")


# ---------------------------------------------------------------------------
# 8/9/10. 「批准蒸馏」标记:识别路由 / 重复幂等 / 队列格式
# ---------------------------------------------------------------------------


class TestDistillQueue(BaseHarvestTest):
    def test_distill_marker_routes_to_queue_not_annotation(self):
        sb = self.sandbox
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 批准蒸馏 这一段值得沉淀\n\n"
            "这是第三段完全不同的收尾内容。\n"
        )
        sb.write_continuous(body)

        changed = sb.run()

        self.assertIn(sb.distill_path, changed)
        self.assertNotIn(sb.annotation_path, changed, "批准蒸馏标记不应进入 annotation 留言栏")
        self.assertFalse(sb.annotation_path.exists())

        distill = sb.read_distill()
        self.assertIn(BVID, distill)
        self.assertIn("这一段值得沉淀", distill)

        cr_text = sb.read_continuous()
        self.assertIn("> [!留] ✓ 已入蒸馏队列", cr_text)
        self.assertNotIn("批准蒸馏", cr_text)

    def test_distill_marker_idempotent_on_rerun(self):
        sb = self.sandbox
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 批准蒸馏 备注乙\n"
        )
        sb.write_continuous(body)

        sb.run()
        first_distill = sb.read_distill()
        occurrences_first = first_distill.count("备注乙")

        second_changed = sb.run()

        self.assertEqual(second_changed, [], "重复标记不应再次追加队列条目")
        second_distill = sb.read_distill()
        self.assertEqual(second_distill, first_distill)
        self.assertEqual(occurrences_first, 1)
        self.assertEqual(second_distill.count("备注乙"), 1)

    def test_distill_queue_entry_format(self):
        sb = self.sandbox
        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 批准蒸馏 格式校验备注\n"
        )
        sb.write_continuous(body)

        sb.run(today="2026-07-20")

        distill = sb.read_distill()
        self.assertIn("2026-07-20", distill)
        self.assertIn(BVID, distill)
        self.assertIn(f"P{PART:02d}", distill)
        self.assertIn("格式校验备注", distill)
        self.assertIn("段落引文", distill)
        self.assertIn("mid:", distill)
        self.assertIn(MID, distill)


# ---------------------------------------------------------------------------
# annotation 页缺失时按模板建页
# ---------------------------------------------------------------------------


class TestAnnotationTemplateCreation(BaseHarvestTest):
    def test_creates_annotation_page_with_expected_skeleton_when_missing(self):
        sb = self.sandbox
        self.assertFalse(sb.annotation_path.exists())
        body = "这是第一段测试文本，用来验证匹配。\n\n> [!留] 新页留言\n"
        sb.write_continuous(body)

        sb.run()

        self.assertTrue(sb.annotation_path.exists())
        ann = sb.read_annotation()
        self.assertIn("type: annotation", ann)
        self.assertIn(f"bvid: {BVID}", ann)
        self.assertIn(f"mid: {MID}", ann)
        self.assertIn("留言栏（用户原话）", ann)
        self.assertIn("阅读状态", ann)
        self.assertIn("蒸馏状态", ann)
        self.assertIn("See Also", ann)
        self.assertIn("新页留言", ann)
        self.assertIn(f"^an-{BVID_LOWER}-p01-001", ann)


# ---------------------------------------------------------------------------
# 11. 写入原子化:flush 中途故障注入,目标文件不得半写
# ---------------------------------------------------------------------------


class TestAtomicWrite(BaseHarvestTest):
    def test_flush_failure_leaves_target_file_with_original_content(self):
        sb = self.sandbox
        sb.write_existing_annotation(max_seq=1)
        original_annotation_text = sb.read_annotation()

        body = (
            "这是第一段测试文本，用来验证匹配。这是第二段测试文本，继续讲解流程。\n\n"
            "> [!留] 会触发写入的留言\n\n"
            "这是第三段完全不同的收尾内容。\n"
        )
        sb.write_continuous(body)
        original_cr_text = sb.read_continuous()

        # 让 os.replace 在 flush 循环里第一次被调用时就抛异常,
        # 模拟"临时文件已写完,正准备原子替换时进程被打断"的故障点。
        with mock.patch("os.replace", side_effect=OSError("模拟故障注入:写入中途被打断")):
            with self.assertRaises(OSError):
                sb.run()

        # 目标文件必须保持故障注入前的原始字节,不能出现半写/截断/损坏。
        self.assertEqual(
            sb.read_annotation(),
            original_annotation_text,
            "flush 中途失败后,annotation 页必须保持原内容,不允许半写",
        )
        self.assertEqual(
            sb.read_continuous(),
            original_cr_text,
            "flush 中途失败后,连续阅读稿必须保持原内容,不允许半写",
        )

        # 失败路径必须清理掉未完成的临时文件,不能残留 .tmp 垃圾文件。
        leftover_tmp = [
            p
            for p in sb.annotations_dir.iterdir()
            if p.name != sb.annotation_path.name and ".tmp" in p.name
        ]
        self.assertEqual(leftover_tmp, [], "故障注入后不应残留未清理的临时文件")

    def test_successful_flush_still_uses_replace_and_leaves_no_tmp_residue(self):
        """正常路径下(不注入故障)原子写完成后,目录里不应残留任何 .tmp 文件。"""
        sb = self.sandbox
        body = "这是第一段测试文本，用来验证匹配。\n\n> [!留] 正常留言\n"
        sb.write_continuous(body)

        sb.run()

        for d in (sb.annotations_dir, sb.transcripts_dir):
            leftover_tmp = [p for p in d.iterdir() if ".tmp" in p.name]
            self.assertEqual(leftover_tmp, [], f"{d} 下不应残留 .tmp 临时文件")


if __name__ == "__main__":
    unittest.main(verbosity=2)
