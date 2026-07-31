# Task for scout

只读分析 E:/个人知识/OneNote/kotlin/ 下 11 篇 .md,报告 markdown 格式偏离。

## 已完成清理(勿再报告)
行尾空格✅ / 反斜杠转义✅ / 代码块语言标签✅ / 空 Untitled✅ / 图片 wikilink 化✅

## 检查维度
1. 标题层级
2. Frontmatter
3. 列表风格 (-/*/+,1. 2.?,缩进)
4. 强调 (**xx**/__xx__, *xx*/_xx_)
5. 表格 (GFM 一致?)
6. 链接 ([[]] 内部, [text](url) 外部,损坏?)
7. HTML 残留
8. 图片 (![[]] vs ![](path))
9. 中文/英文标点
10. [TOC]、[ ]、emoji 乱码
11. 结构异常

## 输出格式
```
# kotlin 目录 markdown 格式审计

## 概况
- 文件总数: 11
- 影响笔记数: X
- 子目录: 基础 / 库 / 程序设计中级 / 程序设计高级

## 偏离清单
### 高优
- ...
### 中优
- ...

## 自动修复可行性
- 完全可自动: X 类
- 需人工判断: Y 类
- 不可自动: Z 类

## 推荐处理顺序
1. ...
2. ...
```

## 约束
**只读取,绝对不要修改任何文件**。
用 read/grep/find 等只读工具。

## 工作目录
E:/个人知识/

---
Update progress at: E:\个人知识\.pi-subagents\artifacts\progress\f6ea5cfd\progress.md

---
**Output:**
Write your findings to exactly this path: E:\个人知识\.pi-subagents\artifacts\outputs\f6ea5cfd\.scout-reports\kotlin.md
This path is authoritative for this run.
Ignore any other output filename or output path mentioned elsewhere, including output destinations in the base agent prompt, system prompt, or task instructions.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

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