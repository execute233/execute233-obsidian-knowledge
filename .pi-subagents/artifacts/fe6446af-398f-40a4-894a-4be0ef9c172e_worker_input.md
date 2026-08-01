# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你是 markdown 笔记格式化专家。本任务处理 `OneNote/python/` 目录下 7 篇笔记。

## 严禁(硬性约束)
- ❌ 任何 .py 脚本
- ❌ 用 `edit` 做正则替换批量改
- ❌ 用 `bash` 跑自动化命令
- ✅ 唯一工具: `read` 读全文, `write` 完整重写整个文件

## 7 个文件(必须全部处理)
- E:/个人知识/OneNote/python/conda/包管理.md
- E:/个人知识/OneNote/python/conda/环境管理.md
- E:/个人知识/OneNote/python/conda/管理conda.md
- E:/个人知识/OneNote/python/基础/内置函数.md
- E:/个人知识/OneNote/python/基础/基础.md
- E:/个人知识/OneNote/python/基础/字符串相关.md
- E:/个人知识/OneNote/python/基础/类.md

## 每个文件你必须做

### 第一步:read 完整读文件

### 第二步:逐项分析
- frontmatter 是否完整?
- H1 是否等于文件名?
- 标题层级
- 代码块:python/bash/sql/yaml/json 等
- 表格
- 标点
- **特殊**: 字符串相关.md 含 `graph.microsoft.com` 远程图片(OneNote Graph 鉴权),这种引用会过期失效。建议保留(它们是历史内容)但要在报告里指出。

### 第三步:用 write 工具整体重写

1. frontmatter 完整
2. H1 = `# 文件名`
3. 标题重构
4. 代码块带语言标签
5. 标点规范化
6. 保留 wikilink、图片、URL、语义

### 第四步:报告
每个文件记录修改。完成后给总结。

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