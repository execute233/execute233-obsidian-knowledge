# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是一个 **Obsidian 个人知识库（vault）**，不是代码项目：没有构建、测试、lint、包管理器。仓库根目录 `E:\个人知识` 就是 vault 根目录，用 Obsidian 打开即可预览。所有工作都是 Markdown 笔记的编写、重组、链接维护与归档。

## 目录结构

- `OneNote/<主题>/<子主题>/<笔记>.md` — 全部笔记（约 360 篇），15 个主题：java / python / web / SQL / c / go / liunx / kotlin / docker / computer / build_tools / unity / windows / AI / copilot。
- `OneNote/_MOC/` — 16 个知识地图：`MOC-Index.md`（总入口）+ 每主题一个 `MOC-<主题>.md`。**新增、删除、重命名笔记后必须同步对应 MOC**，`MOC-Index.md` 里的「N 篇」计数也要一起改。
- 系统化课程用「编号课程」组织：`00-课程总览.md`（课程地图 + wiki 链接导航）→ `01-…`、`02-…` 按学习顺序编号 → 附录 `A-速查表` / `B-常见问题` / `C-自测题` → `官方资料索引.md`。见 `OneNote/web/CSS/`、`OneNote/web/tailwind/`、`OneNote/web/Astro/`、`OneNote/python/LangGraph/`。
- 被课程重写替换的旧笔记移入该目录的 `archive/` 子目录，**内容不改**，原文件名写进新课的 `aliases` 以兼容旧链接。
- 图片放在笔记同级 `_assets/<笔记名>/<笔记名>__HH-MM-SS-N.png`。
- `docs/specs/`、`docs/plans/` — 设计文档与实现计划，已被 gitignore，**不提交**（可用作写作前的方案载体）。
- `copilot/` — Copilot 插件自动产物（OA-file-hider 已在 Obsidian 中隐藏）；`Copilot-Indexed-Files-*.md` 被忽略。
- `.obsidian/` 配置入库（社区插件清单、图谱视图、外观）；`workspace.json`、插件 `data.json`、`.smart-env/`、`.trash/`、`.pi-subagents/` 被忽略。

## 如何写一篇好的笔记

### frontmatter 三件套（必须）

```yaml
---
title: 中文标题
tags: [主题, 子主题, 关键词]
aliases: [旧文件名, 英文别名]
---
```

- `tags` 参考同目录既有风格（如 `[css, 盒模型, 边框]`、`[java, javaSE]`），不要堆无关标签。
- `aliases` 用于检索与旧链接兼容：重命名笔记时把**旧名留在 aliases**（如 `05-CSS盒模型.md` 保留 aliases `CSS 盒子模型`）。
- 正文一级标题 `#` 与 frontmatter `title` 同名，其余一律用 `##`。

### 结构

- 开篇一句话说清「这是什么 / 解决什么问题」，再进入内容；不要一上来就贴代码。
- 长笔记（课程、WSL、PowerShell 等）在开篇用 callout 列本课重点：
  ```markdown
  > [!abstract]
  > 本课重点：
  >
  > * 要点一
  > * 要点二
  ```
- callout 惯用类型：`[!abstract]` 开篇摘要、`[!tip]` 技巧、`[!note]` 备注、`[!info]` 适用场景、`[!warning]` 易错点、`[!danger]` 高危误区。
- 属性、取值、对比一律用**表格**；示例用**短代码块**并标语言（```` ```css ````/```` ```java ````/```` ```text ````）；块内还要嵌围栏时外层用 `~~~`。
- 表格单元格里放行内代码/类名时用 `<code>xx</code>`，避免管道符与反引号冲突（tailwind 笔记的做法）。
- 结尾用 wiki 链接交叉引用相关笔记（「详见 [[…]]」），让知识网连起来。

### 内容原则

- **精炼速查 + 适量示例**：这是全库统一风格，不要写成教程长文。
- **不照搬原文**：写作前用 WebFetch / 搜索核对知识覆盖范围（CSS 课程要求逐章抓 runoob 对应章节，并对照 MDN 补现代主题），再用自己的话压缩成要点。
- 不确定的内容先查再写；第三方来源要核对版本（如 Tailwind v4 vs v3、Astro 版本差异），库内笔记已多次因此返工。

### 链接

- 库内笔记只用 Obsidian wiki 链接 `[[文件名|显示文本]]`，**不要**用 markdown 链接指向库内笔记。
- 同目录写短名 `[[JUC-锁]]`；跨目录写相对/库根路径，如 `[[java/javaSE/NIO]]`、`[[../web/Sass/Sass函数]]`。
- 链接一律带显示别名，避免渲染出 `01-CSS简介与引入` 这类文件名。
- `alwaysUpdateLinks` 已开启：在 Obsidian 里重命名会自动改链，但**用脚本/git 重命名后必须 Grep 全库手工修链**（历史上多次 `moc: 修正错链` 提交都是这个原因）。

## 行尾与编码

- 全库 UTF-8 无 BOM、**LF 行尾**（仓库以 LF 为准，工作区可能是 CRLF）。
- 改笔记用 Edit 做局部替换，**不要整文件重写**：历史上多次因整文件重写把 LF 变成 CRLF，产生整篇无意义 diff 后返工重来。

## Git 约定

- 提交信息用中文，格式 `<范围>: <动作>`：
  - `web/css: 新增 05 课 (盒模型)`
  - `moc: 修正 alwaysUpdateLinks 触发的错链`
  - `gitignore: 忽略 docs/specs 与 docs/plans`
  - 跨主题的杂项改动用 `kb:` 前缀。
- 小步提交：一个任务一个 commit，新增课程常按 2 篇一组。
- 不要在笔记里写明文 API key / token（`langchain.md` 曾出现明文 key，已重写历史清除）。

## 常用操作

- 找笔记用 Grep / Glob，不要用 `Get-ChildItem -Recurse`（中文路径与体量都不友好）。
- 校验 wiki 链接：Grep 出 `[[目标]]`，再 Glob 确认同名文件存在。
- 清理图片前**同时**搜 `![[` 和 `![` 两种引用形式——曾因只查一种误删 60 张图片。
- 读写路径含中文，PowerShell 下记得加引号；仓库根目录已是工作目录，无需 `cd`。
