# Task for worker

[Read from: E:\个人知识\context.md, E:\个人知识\plan.md]

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:在 E:/个人知识/ 这个 vault 里,给 OneNote/ 下 159 篇 .md 笔记(不含 _assets/)批量加 frontmatter。

## 目标 schema
每个 .md 文件顶部加:
```
---
title: {filename 去 .md}
tags: [{dir1}, {dir2}]
aliases: [{filename 去 .md}]
---
```

示例:
- `OneNote/java/javaSE/NIO.md` → `tags: [java, javaSE]`
- `OneNote/SQL/Redis/基本操作.md` → `tags: [SQL, Redis]`
- `OneNote/unity/脚本开发/触摸.md` → `tags: [unity, 脚本开发]`

## 规则
1. **跳过已有 frontmatter** (以 `---` 开头)
2. **跳过 _assets/ 目录**
3. **跳过空文件** (0 字节)
4. **不修改正文内容**
5. 全库统一用这套 schema,不要挑

## 写脚本 + 跑
- 写一个 `.add-frontmatter.py` (Python 3.12 可用)
- 脚本先 dry-run 列出打算改的 5 个样例
- 然后实际执行
- 输出统计:处理笔记数、已加 frontmatter 数、跳过数

## 提交
- 完成后 git commit,信息:`frontmatter: 159 篇笔记统一加 title/tags/aliases`
- commit 前输出 git status 确认

## 约束
- 不要碰其他文件
- 工作树变干净后完成
- cwd: E:/个人知识/

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\64deeb2f\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\64deeb2f\OneNote.log1.md
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