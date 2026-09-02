---
title: 第 12 课：SSG、按需渲染与 Adapters
tags: ["Astro", "frontend", "课程", "课程-12"]
aliases: ["第 12 课", "SSG、按需渲染与 Adapters", "第 12 课：SSG、按需渲染与 Adapters"]
---
# 第十二课：SSG、按需渲染与 Adapters

### 12.1 默认：静态预渲染

Astro 默认在 build 时生成 HTML：

~~~text
源代码 + 内容
      ↓ pnpm build
dist/index.html
dist/about/index.html
dist/blog/astro-islands/index.html
~~~

优点：

- 请求时无需执行服务器代码；
- 部署简单；
- 易缓存；
- 内容首屏快；
- 攻击面较小。

适合博客、文档和基本营销站。

### 12.2 单路由按需渲染

先添加部署平台 Adapter，例如 Node：

~~~bash
pnpm astro add node
~~~

然后在需要动态渲染的页面：

~~~astro
---
export const prerender = false;

const visitCookie = Astro.cookies.get('visits');
const visits = (visitCookie?.number() ?? 0) + 1;

Astro.cookies.set('visits', String(visits), {
  httpOnly: true,
  sameSite: 'lax',
  path: '/',
});
---

<h1>你已访问 {visits} 次</h1>
~~~

其他未标记页面仍然静态生成。这种“一部分静态，一部分按需”的策略通常最适合内容站。

### 12.3 整站 server output

~~~js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
});
~~~

在 server output 中，页面默认按请求渲染。个别稳定页面可以重新预渲染：

~~~astro
---
export const prerender = true;
---

<h1>关于我们</h1>
~~~

> [!important]
> <code>output: 'server'</code> 不会解锁额外能力，它只是反转默认值。官方建议从默认 static 开始，直到大多数路由确实需要按需渲染。

官方依据：[On-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/)

### 12.4 决策表

| 需求 | 推荐 |
|---|---|
| 内容发布后才变化 | SSG |
| 可接受 webhook 触发重新构建 | SSG |
| 每个用户看到不同内容 | 按需渲染 |
| 使用 request cookie / header | 按需渲染 |
| 个别动态账户页 | static 默认 + <code>prerender=false</code> |
| 大多数页面都动态 | <code>output='server'</code> |
| Server Island | 需要 Adapter |

### 12.5 Adapter 不是通用包

Astro 官方维护 Node、Cloudflare、Netlify、Vercel Adapter。部署到哪个 runtime，就读对应 Adapter 文档，因为文件系统、缓存、sessions、edge 能力可能不同。

### 12.6 Streaming 与响应头

按需渲染会流式发送 HTML，但慢数据请求仍可能阻塞所在渲染路径。响应头必须在页面级代码中尽早设置，不能等深层组件渲染后才修改。
