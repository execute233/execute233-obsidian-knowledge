---
title: 附录 A：v4 与 v3 教程辨认表
tags: [Tailwind, CSS, frontend]
aliases: ["附录 A：v4 与 v3 教程辨认表"]
---

# 附录 A：v4 与 v3 教程辨认表

你在搜索时仍会遇到大量 v3 内容。下面用于快速辨认，不代表所有旧 API 都立刻完全不可用。

| 主题 | v3 常见写法 | v4 主线 |
|---|---|---|
| CSS 入口 | 三条 <code>@tailwind</code> 指令 | <code>@import "tailwindcss";</code> |
| 配置 | <code>tailwind.config.js</code> | CSS 中 <code>@theme</code> |
| 源码范围 | <code>content: [...]</code> | 自动检测；必要时 <code>@source</code> |
| Vite | 通常走 PostCSS | 第一方 <code>@tailwindcss/vite</code> |
| PostCSS 包 | <code>tailwindcss</code> | <code>@tailwindcss/postcss</code> |
| import / prefix | 常配额外插件 | v4 构建工具内置处理 |
| 主题访问 | <code>theme(...)</code> | 优先原生 CSS theme variables |
| container query | 常需插件 | 核心能力 |
| 渐变方向 | <code>bg-gradient-to-r</code> | <code>bg-linear-to-r</code> |
| important class | <code>!flex</code> | <code>flex!</code> |
| prefix | 传统字符串前缀 | 类似 variant：<code>tw:flex</code> |
| 默认 ring | 3px | 1px；明确 3px 用 <code>ring-3</code> |
| outline 隐藏兼容 | <code>outline-none</code> 旧语义 | 原旧效果改名 <code>outline-hidden</code> |
| Vue scoped CSS | 旧配置上下文 | 自定义项配合 <code>@reference</code> |
| 浏览器目标 | 较宽松 | Chrome 111、Safari 16.4、Firefox 128 起 |

## 从旧项目升级

官方升级工具：

~~~bash
npx @tailwindcss/upgrade
~~~

工具要求 Node.js 20 或更高。官方建议在新分支运行，审查 diff，并逐页进行视觉测试；复杂项目仍可能需要手动调整。参考完整的[v3 → v4 Upgrade guide](https://tailwindcss.com/docs/upgrade-guide)。

> [!warning] 不要机械替换
> ring、outline、shadow、gradient、Preflight、hover-on-touch 和 transform properties 都存在行为变化。迁移不是只改安装包和入口指令。

---
