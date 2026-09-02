---
title: 第 01 课：Astro 到底是什么
tags: ["Astro", "frontend", "课程", "课程-1"]
aliases: ["第 01 课", "Astro 到底是什么", "第 01 课：Astro 到底是什么"]
---
# 第一课：Astro 到底是什么

### 1.1 一句话定义

Astro 是面向内容型网站的 Web Framework。它倾向先在构建阶段或服务器生成 HTML，只在真正需要交互的位置发送浏览器 JavaScript。

适合：

- 博客、文档、知识库、作品集；
- 营销页、企业官网、新闻与内容平台；
- 电商展示页面；
- “大部分是内容，少部分有交互”的站点。

不一定是首选：

- 绝大多数页面都依赖复杂客户端状态的后台；
- Figma、在线 IDE、图片编辑器这类高交互应用；
- 整站本质就是一个大型 Vue SPA。

官方定位：[Why Astro](https://docs.astro.build/en/concepts/why-astro/)

### 1.2 与 Vue 的关键差异

| 问题 | Vue SPA | Astro |
|---|---|---|
| 组件默认在哪里运行 | 浏览器 | 构建时或服务器 |
| 默认发送组件 runtime | 会 | 不会 |
| 页面导航 | 通常由 Router 接管 | 默认标准 HTML 链接和多页导航 |
| 主要优化目标 | 应用交互 | 内容交付与少量交互 |
| 响应式状态 | Vue ref / reactive | Astro 组件本身没有客户端响应式状态 |
| 使用 Vue | 整个应用 | 通常只作为交互 Island |

> [!important] 第一原则：永远先问“这段代码在哪里运行？”
> - <code>.astro</code> frontmatter：构建时或服务器。
> - <code>.astro</code> 模板：生成 HTML。
> - 普通 <code>&lt;script&gt;</code>：浏览器。
> - 带 <code>client:*</code> 的 Vue 组件：先生成 HTML，再在浏览器 hydration。
> - 带 <code>server:defer</code> 的组件：由服务器独立延迟渲染。

### 1.3 三种组件形态

#### Astro Component：默认零客户端 runtime

~~~astro
---
const createdAt = new Date();
---

<article>
  <h2>服务器生成的内容</h2>
  <time>{createdAt.toISOString()}</time>
</article>
~~~

这段 TypeScript 不会原样进入浏览器。最终用户拿到的是 HTML。

#### Client Island：只让一个 Vue 组件交互

~~~astro
---
import SearchBox from '../components/SearchBox.vue';
---

<main>
  <h1>知识库</h1>
  <SearchBox client:visible />
</main>
~~~

#### Server Island：动态区域不阻塞整个页面

~~~astro
---
import UserMenu from '../components/UserMenu.astro';
---

<UserMenu server:defer>
  <span slot="fallback">正在加载用户信息…</span>
</UserMenu>
~~~

官方概念：[Islands architecture](https://docs.astro.build/en/concepts/islands/) · [Server islands](https://docs.astro.build/en/guides/server-islands/)

### 1.4 Hydration 是什么

服务器先输出 Vue 组件的 HTML，浏览器随后下载 Vue 相关 JavaScript，将事件、状态和已有 HTML 连接起来，这个过程叫 hydration。

如果不写客户端指令：

~~~astro
<Counter />
~~~

它只渲染 HTML，不会在浏览器变成可交互的 Vue 组件。

写了客户端指令：

~~~astro
<Counter client:load />
~~~

浏览器才会加载所需 JavaScript 并 hydration。
