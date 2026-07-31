# Task for worker

You are a delegated subagent running from a fork of the parent session. Treat the inherited conversation as reference-only context, not a live thread to continue. Do not continue or answer prior messages as if they are waiting for a reply. Your sole job is to execute the task below and return a focused result for that task using your tools.

Task:
你的任务:重写 3 篇 Kotlin 笔记里的灾难表格。

## 现状
3 篇笔记里的 markdown 表格被 OneNote 导出时插入了独立的代码块栅栏,导致 GFM 表格解析失败:
1. `OneNote/kotlin/基础/基础知识.md` — 第 15-76 行附近有 1 张大表被 42 个独立 ` ```kotlin ` 栅栏切碎
2. `OneNote/kotlin/程序设计中级/封装，继承和多态.md` — 编辑函数说明表第 43-73 行被切碎
3. `OneNote/kotlin/程序设计中级/类与对象.md` — 3 张运算符表(第 24-103、107-170、181-207、233-251 行)被 37 处代码块插入

## 读 + 写策略
**这是内容级别的修复**,需要你:
1. 读每篇文件的完整内容
2. 识别 3 个表格的"原本结构"(表头 + 数据行)
3. 把栅栏之间的代码块内容**合并回正确的表格单元格**
4. 保留表格的所有行(包括带 `[[ ]]` wikilink 的)
5. 代码块外的散文内容不动

## 工具
- 用 `read` 读完整文件
- 用 `edit` 做精确替换
- 不写 Python 脚本

## 重要原则
- ⚠️ **不要重写内容语义** — 只把结构还原成正确的 GFM 表格
- ⚠️ **不要删除任何代码示例** — 全部塞进表格里
- ⚠️ **表头要保留**,不要清空
- ⚠️ **保留所有 `[[xxx]]` 的图片 wikilink**

## 表格合并示例
**原文(坏)**:
```
|列1|列2|列3|
|---|---|---|
|值1|```
```kotlin
code1
```
```|值3|
```

**目标(好)**:
```
|列1|列2|列3|
|---|---|---|
|值1|`code1`|值3|
```

或者用 fenced code 块在单元格内:
```
|列1|列2|列3|
|---|---|---|
|值1|<pre>code1</pre>|值3|
```

## 输出
- 改完后用 `git diff --stat` 给我统计
- 报告:每篇文件改了多少行,删了多少行,新增多少行
- 报告:每篇文件的"原表格行数 vs 新表格行数"

## 约束
- cwd: E:/个人知识/
- 工作树最终保持干净
- 不要碰其他文件
- 不要 commit(我后面会统一 commit)

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\23b56f5d\OneNote.kotlin-tables.md
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