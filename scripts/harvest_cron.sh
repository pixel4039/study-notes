#!/bin/bash
# 留言收割 cron 包装脚本。
#
# 用途:定时(建议 */30 * * * *)在服务器上拉取 study-notes 最新提交、跑
# harvest_annotations.py 把连续阅读稿里的 `> [!留]` 留言收割进 annotation
# 真源页,有变化就单主题提交并推回。
#
# 重要:本脚本只是"写好放在 scripts/ 里"的交付物,合同明确禁止在本次任务
# 里安装 crontab——是否、何时把它接入 crontab 是 Sol 验收通过后另一步。
#
# 依据:合同 /home/ubuntu/.claude/jobs/fc51b3d3/tmp/CONTRACT-harvest.md
#      方案 /home/ubuntu/.claude/plans/effervescent-wiggling-hopcroft.md
#
# 设计:
#   1. flock 防重入(同一时刻只允许一个实例跑)。
#   2. git fetch;若本地已是最新且没有待收割的 `> [!留]` 留言,直接退出,不占用资源。
#   3. git pull --ff-only;失败(比如本地有冲突或非 ff)就退出,留到下一轮重试,不 rebase、不强推。
#   4. 跑 harvest_annotations.py(纯 stdlib,写 annotations/ 与 wiki/_candidates/_distill-queue.md)。
#   5. 有文件改动就单主题提交:"harvest: annotations from reading comments"。
#   6. git push;若被拒(与主人本地 push 撞车等)就记日志、退出,留到下一轮重试,不强推。
#   7. 全程日志写 .harvest.log(仓库 .gitignore 已排除,不进 git 历史)。

set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="${REPO_DIR}/.harvest.lock"
LOG_FILE="${REPO_DIR}/.harvest.log"
BRANCH="master"
REMOTE="origin"
COMMIT_MSG="harvest: annotations from reading comments"

log() {
    printf '[%s] %s\n' "$(date -Iseconds)" "$1" >>"${LOG_FILE}"
}

exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
    log "上一轮仍在跑,本轮跳过(flock 防重入)。"
    exit 0
fi

cd "${REPO_DIR}" || { log "无法进入仓库目录 ${REPO_DIR},退出。"; exit 1; }

if [ -n "$(git status --porcelain)" ]; then
    log "工作树不干净(有未提交改动),为安全起见本轮跳过,不做 fetch/pull/收割。"
    exit 0
fi

if ! git fetch "${REMOTE}" "${BRANCH}" --quiet; then
    log "git fetch 失败,退出待下一轮。"
    exit 1
fi

LOCAL_HEAD="$(git rev-parse HEAD)"
REMOTE_HEAD="$(git rev-parse "${REMOTE}/${BRANCH}")"

# 无新提交 且 本地没有待收割的 `> [!留]` 留言 -> 直接退出,不浪费一次 pull/跑脚本。
if [ "${LOCAL_HEAD}" = "${REMOTE_HEAD}" ]; then
    if ! grep -rlE '^> \[!留\](\s|$)' --include='*连续阅读.md' \
            "${REPO_DIR}/sources/bilibili" 2>/dev/null \
        | xargs -r grep -L '^> \[!留\] ✓' >/tmp/harvest_pending_check.$$ 2>/dev/null; then
        :
    fi
    PENDING_COUNT=0
    if [ -s /tmp/harvest_pending_check.$$ ]; then
        PENDING_COUNT=$(wc -l </tmp/harvest_pending_check.$$)
    fi
    rm -f /tmp/harvest_pending_check.$$
    if [ "${PENDING_COUNT}" -eq 0 ]; then
        log "无新提交且无待收割留言,退出。"
        exit 0
    fi
fi

if ! git pull --ff-only "${REMOTE}" "${BRANCH}" --quiet; then
    log "git pull --ff-only 失败(可能非快进),退出待下一轮,不 rebase 不强推。"
    exit 1
fi

if ! python3 "${REPO_DIR}/scripts/harvest_annotations.py" --root "${REPO_DIR}" >>"${LOG_FILE}" 2>&1; then
    log "harvest_annotations.py 执行失败,退出。"
    exit 1
fi

if [ -z "$(git status --porcelain)" ]; then
    log "本轮收割无变化。"
    exit 0
fi

git add -- annotations wiki/_candidates sources
if ! git commit -m "${COMMIT_MSG}" --quiet; then
    log "git commit 失败,退出。"
    exit 1
fi

if ! git push "${REMOTE}" "${BRANCH}" --quiet; then
    log "git push 被拒(可能与主人本地 push 竞态),留到下一轮重试,不强推。"
    exit 1
fi

log "本轮收割完成并已推送。"
exit 0
