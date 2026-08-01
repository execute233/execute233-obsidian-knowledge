# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你是 markdown 笔记格式化专家。本任务处理 `OneNote/windows/` 目录下 1 篇笔记。

## 严禁
- ❌ .py 脚本
- ❌ edit 正则替换
- ❌ bash 批量改
- ✅ `read` + `write`(整体重写)

## 1 个文件
- E:/个人知识/OneNote/windows/可选功能/WSL.md

## 流程
1. read 全文
2. 分析 frontmatter / H1 / 标题层级 / 代码块 / 表格 / 标点
3. write 整体重写:
   - frontmatter YAML 头(title/tags/aliases)
   - H1 = `# 文件名`
   - 单独 `1. xxx` → `## xxx`
   - 单独 `**xxx**` → `### xxx`
   - 代码块带语言标签
   - 文本全角,代码半角
   - 保留 wikilink / 图片引用 / URL / 语义
4. 报告修改

## Acceptance Contract
Acceptance level: checked
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope
- criterion-2: Return evidence sufficient for an independent acceptance review

Required evidence: changed-files, tests-added, commands-run, residual-risks, no-staged-files

Review gate: required by reviewer.

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
    },
    {
      "id": "criterion-2",
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