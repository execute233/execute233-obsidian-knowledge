# Task for worker

[Read from: E:\个人知识\context.md, E:\个人知识\plan.md]

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:在 E:/个人知识/ 里,把 OneNote/ 下所有 .md 笔记里的编号列表 `1. xxx` `2. yyy` 转成层级标题。

## 目标
把假装章节的 `1. xxx` 这种行,转成 `## xxx` 标题。
- 原文: `1. **Lambda 表达式**` → 新文: `## Lambda 表达式`
- 原文: `2. xxx` 同级 → 跳过 (`##` 比 `1.` 更高优先级表示同级)
- 残缺编号 `1. xxx`、`3. yyy`(缺 2) → 保留

## 规则
1. **只处理代码块外的编号列表**
2. **只处理文件首的 H1 之后、第一个非空行前的连续编号列表**
3. **不修改代码块内**
4. **不修改嵌套编号列表** (已经是列表的一部分)
5. **空行的`数字.`不算**
6. **不修改正文散文中的 `1. xxx` 之类**(只针对"用来假装章节"的连续编号列表段)

## 启发式
- 找到文件 H1 后面、`## xxxx` 前面,或文件末尾
- 找到连续 >= 2 行的 `^\d+\. xxx` 段
- 把这段每行:
  - `1. xxx` → `## xxx`
  - `2. xxx` → `## xxx`
  - ... (都同级 ##)

## 写脚本 + 跑
- 写 `.restructure-titles.py`
- dry-run 列出 5 个样本思路
- 真实执行
- 输出:处理笔记数、改了多少 `1. xxx` → `## xxx`

## 提交
- git commit:`重构: 编号列表 1. xxx 转 ## h2 标题 (251 行 → X 个二级标题)`
- commit 前 git status 确认

## 约束
- 不在 fenced code 内替换
- 不修改 python 缩进格式
- 工作目录: E:/个人知识/

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\64deeb2f\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\64deeb2f\OneNote.log2.md
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