# Task for worker

[Read from: E:\个人知识\context.md, E:\个人知识\plan.md]

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:在 E:/个人知识/ 里,批量规范化笔记中的中英文标点。

## 目标
- 代码内 (fenced code `` ``` `` 块、行内 `` `xxx` ``) → 全部使用 **半角** 标点
- 中文文本段 → 全部使用 **全角** 标点
- 已有 yaml frontmatter / wikilink (`![[...]]`) / URL / 邮箱 → 跳过

## 规则
1. **不在 fenced code 内替换**(保留原文)
2. **不在行内代码内替换**(` ``xxx`` `)
3. **不在 wikilink / markdown link 内替换**(`[[...]]`、`[text](url)`)
4. **不在文件路径 / 邮箱 / URL 内替换**
5. **核心标点**:
   - 半角 → 全角: `,` → `，`,`.` → `。` (句末),`:` → `：`,`;` → `；`,`?` → `？`,`!` → `！`,`(` → `（`,`)` → `）`(注意只在文本段)
   - 全角 → 半角: `，` → `,`,`： → `:` (在 fenced code 中)
6. **保守策略**:只在置信度高的情况下替换,不动模糊的

## 写脚本 + 跑
- 写 `.normalize-punctuation.py`
- 分两遍:文本段 → 全角;代码段 → 半角
- 输出:处理笔记数、改了多少处

## 提交
- git commit:`规范化: 44 篇笔记中英文标点(代码内半角,文本内全角)`
- commit 前 git status 确认

## 约束
- 不修改 wikilink 内容
- 不修改 URL
- 不修改 frontmatter 字段值
- 工作目录: E:/个人知识/

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\64deeb2f\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\64deeb2f\OneNote.log3.md
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