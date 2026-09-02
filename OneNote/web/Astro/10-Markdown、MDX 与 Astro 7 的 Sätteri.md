---
title: 第 10 课：Markdown、MDX 与 Astro 7 的 Sätteri
tags: ["Astro", "frontend", "课程", "课程-10"]
aliases: ["第 10 课", "Markdown、MDX 与 Astro 7 的 Sätteri", "第 10 课：Markdown、MDX 与 Astro 7 的 Sätteri"]
---
# 第十课：Markdown、MDX 与 Astro 7 的 Sätteri

### 10.1 三种内容方式

| 方式 | 优点 | 适用 |
|---|---|---|
| <code>src/pages/*.md</code> | 文件直接变路由，简单 | 少量独立页面 |
| MDX | Markdown 中导入组件 | 富交互文档 |
| Content Collections | Schema、类型、查询、Loader | 正式博客 / 文档内容层 |

本课程主线使用 Content Collections。不要把大量正式文章全塞进 <code>src/pages</code>。

### 10.2 Astro 7 的 Markdown

Astro 7 默认使用 Rust 驱动的 Sätteri 处理 Markdown 和 MDX。默认提供 GitHub-Flavored Markdown 与智能标点等常用能力。

如果项目依赖 remark / rehype 插件，可安装 <code>@astrojs/markdown-remark</code> 并切回 unified 管线；不要只复制旧教程中的 remark 配置后假设它仍会自动生效。

官方依据：[Astro 7 发布说明](https://astro.build/blog/astro-7/#markdown--mdx-in-rust) · [Upgrade to Astro 7 — Sätteri](https://docs.astro.build/en/guides/upgrade-to/v7/#new-default-markdown-processor-s%C3%A4tteri)

### 10.3 MDX

安装：

~~~bash
pnpm astro add mdx
~~~

MDX 示例：

~~~mdx
---
title: Vue Island 演示
---

import Counter from '../components/Counter.vue';

# 文章标题

下面只有 Counter 会在浏览器 hydration：

<Counter client:visible />
~~~

MDX 很强，但不要把每篇普通文章都写成组件程序。纯内容优先 Markdown。

### 10.4 Markdown 图片

位于 <code>src</code> 的本地 Markdown 图片可以被 Astro 处理：

~~~md
![群岛架构](../assets/islands.png)
~~~

位于 public：

~~~md
![群岛架构](/images/islands.png)
~~~

public 图片不会被优化。

官方依据：[Markdown in Astro](https://docs.astro.build/en/guides/markdown-content/) · [Images in Markdown](https://docs.astro.build/en/guides/images/#images-in-markdown-files)
