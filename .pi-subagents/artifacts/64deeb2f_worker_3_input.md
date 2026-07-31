# Task for worker

[Read from: E:\个人知识\context.md, E:\个人知识\plan.md]

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:清理 Unity 8 篇笔记 cs 代码块内的 `**Symbol**` 残留。

## 现状
- OneNote/unity/脚本开发/ 下 8 篇 .md 文件
- 整篇已在前几轮被包成 ` ```cs ` 围栏
- 但代码块内部还有 `**Start**`、`**Update**`、`**Log**` 等 `**Symbol**` 形式的 markdown 强调标记
- 这些在 cs 代码块内是无意义的星号,会让 Obsidian 阅读视图看起来奇怪

## 目标
在 cs fenced code block 内,把 `**Symbol**` 中的 `**` 移除,只保留 `Symbol`。
- 原文: `void **Start**()` → 新文: `void Start()`
- 原文: `Debug._Log_("...")` → **不动** (这里是单 `_` 不是 `**`)
- 原文: `public class **ScenesTest**` → `public class ScenesTest`

## 规则
1. **只在 ```cs (不区分大小写) 代码块内替换**
2. **不修改 md 文本段**
3. **模式: `\*\*[A-Za-z_]\w*\*\*` → 单字符名**(只 strip 包围的 `**`)
4. **不修改 `_Symbol_` 形式的下划线**
5. **不修改 `*` 单星号**(只 `**` 双星号)

## 写脚本 + 跑
- 写 `.cleanup-unity-emphasis.py`
- 输出:处理笔记数、清理 `**Symbol**` 总数

## 提交
- git commit:`清理: Unity 8 篇 cs 代码块内 **Symbol** 共 11 处`
- commit 前 git status 确认

## 约束
- 工作目录: E:/个人知识/
- 只动 OneNote/unity/ 上层的 8 篇 .md

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\64deeb2f\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\64deeb2f\OneNote.log4.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
`criteriaSatisfied[].status` must be exactly one of: satisfied, not-satisfied, not-applicable.
`commandsRun[].result` must be exactly one of: passed, failed, not-run.
`manualNotes` and `notes` are optional strings; an empty string means no note and does not satisfy `manual-notes` evidence.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```