# Task for worker

[Read from: E:\个人知识\context.md, E:\个人知识\plan.md]

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:在 E:/个人知识/ 里,删除 6 个空的顶层子目录骨架。

## 待删除目录(每个目录只有空的 `_assets/` 子目录或彻底空)
1. OneNote/computer/密码学/
2. OneNote/computer/操作系统/
3. OneNote/computer/汇编原理/
4. OneNote/computer/组成原理/
5. OneNote/java/JVM/
6. OneNote/unity/各种组件/

## 步骤
1. `ls -la` 每个目录,确认里面只有 `_assets/` (可能是空的或有些图片)或彻底空
2. 如果只是骨架,可以删除整个目录
3. 如果 `_assets/` 有真实文件 (.png/.jpeg),**保留** 这个目录,只删除该目录里 0 字节笔记
4. 用 `git rm -r` 删目录,或 `rmdir` 删空目录

## 决定规则
- 如果目标目录里 _assets 是空的 → 整个目录 `git rm -r`
- 如果 _assets 里有 .png/.jpeg → 保留 _assets 子目录,只删里面的 .md 骨架笔记

## 验证
- 删除后用 `ls OneNote/computer/` 确认
- 如果有保留情况,说明一下

## 提交
- git commit:`清理: 删除 6 个空目录(空骨架位置)`
- update-mode 详细说哪些是 0 字节 + 哪些是带 _assets 保留

## 约束
- 工作目录: E:/个人知识/
- 不动 OneNote/ 下的内容笔记
- 不动图片文件

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\64deeb2f\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\64deeb2f\OneNote.log5.md
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