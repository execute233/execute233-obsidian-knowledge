# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你是 markdown 笔记格式化专家。本任务处理 `OneNote/build_tools/` 目录下 5 篇笔记。

## 严禁(硬性约束)
- ❌ 任何 .py 脚本(不能写不能跑)
- ❌ 用 `edit` 做正则替换批量改
- ❌ 用 `bash` 跑自动化命令(sed/awk/grep 等批量改)
- ✅ 唯一工具: `read` 读全文, `write` 完整重写整个文件

## 5 个文件(必须全部处理,无遗漏)
- E:/个人知识/OneNote/build_tools/Git/使用.md
- E:/个人知识/OneNote/build_tools/Git/安装 配置 初始化.md
- E:/个人知识/OneNote/build_tools/IDEA/快捷键操作.md
- E:/个人知识/OneNote/build_tools/maven/依赖管理.md
- E:/个人知识/OneNote/build_tools/maven/操作.md

## 每个文件你必须做

### 第一步:read 完整读文件
调用 `read` 工具,不带 offset/limit,读到 EOF。看完后记住所有内容(语义不要改)。

### 第二步:逐项分析(写下你的判断)
- frontmatter(YAML 头部)是否存在?字段是否完整?
- H1 标题是否等于文件名(去 .md)?
- 标题层级:是否有 `1. xxx` 单行实际是 H2?是否有 `**xxx**` 单行实际是 H3?
- 代码块:是否都有语言标签?(` ```java ` / ` ```bash ` 等)
- 表格:是否有 ``` 在表格内打断 GFM 解析?
- 标点:代码内是否混了全角 / 文本内是否混了半角?

### 第三步:用 write 工具整体重写
**完整覆盖**,不要用 `edit`。重写时严格按以下规则:

1. **frontmatter**: 必须有完整 YAML 头
```yaml
---
title: <文件名去 .md>
tags: [build_tools, <子目录>]
aliases: [<文件名去 .md>]
---
```

2. **H1**: `# <文件名去 .md>`(frontmatter 之后第一行正文)

3. **标题重构**:
   - 单独一行的 `1. xxx` 且后续不是 `2. xxx` 的 → 转 `## xxx`
   - 单独一行的 `**xxx**` → 转 `### xxx`
   - 连续编号列表(1./2./3. 有连贯内容)保留

4. **代码块**:
   - 必须有语言标签,没有就按内容猜(java/python/bash/sql/yaml/json/cs/cpp/xml/properties/http/dockerfile 等)
   - 表格内不能有 ``` 打断,合并到单元格用行内 `` `code` ``

5. **标点**:
   - 中文文本段落:全角(，。；：？！（）)
   - 代码块 / 行内代码 / wikilink / URL:半角(,.;:?!())

6. **保留不动**:
   - 所有 `[[xxx]]` wikilink
   - 所有 `![[...]]` 图片引用  
   - 所有 URL(http/https)
   - 内容语义(不能改字、删段、加段)

### 第四步:报告
每个文件处理完,记录到你的最终回复中:
```
[文件名]
  - frontmatter: 已有 → 补全 X 字段 / 无 → 新加
  - H1: 已是 `# 文件名` / 已校正
  - 标题重构: N 个伪子标题 / 编号列表 → ## 或 ###
  - 代码块标签: N 个补标签 / N 个改语言
  - 表格修复: N 处(如有)
  - 标点: N 处全→半 / N 处半→全
  - 总修改: X 处
```

完成后给我总结:处理了多少文件,共改了多少处。

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