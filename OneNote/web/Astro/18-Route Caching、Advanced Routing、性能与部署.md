---
title: 第 18 课：Route Caching、Advanced Routing、性能与部署
tags: ["Astro", "frontend", "课程", "课程-18"]
aliases: ["第 18 课", "Route Caching、Advanced Routing、性能与部署", "第 18 课：Route Caching、Advanced Routing、性能与部署"]
---
# 第十八课：Route Caching、Advanced Routing、性能与部署

### 18.1 Route Caching

Route Caching 只用于按需渲染的响应。先配置 provider：

~~~js
// astro.config.mjs
import { defineConfig, memoryCache } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  adapter: node({ mode: 'standalone' }),
  cache: {
    provider: memoryCache(),
  },
  routeRules: {
    '/api/[...path]': { swr: 600 },
    '/products/[...slug]': {
      maxAge: 3600,
      tags: ['products'],
    },
  },
});
~~~

页面中：

~~~astro
---
export const prerender = false;

if (Astro.cache.enabled) {
  Astro.cache.set({
    maxAge: 120,
    swr: 60,
    tags: ['home'],
  });
}
---

<h1>缓存页面</h1>
~~~

含义：

- <code>maxAge</code>：响应保持新鲜的秒数；
- <code>swr</code>：过期内容仍可暂时提供，同时后台重新验证；
- <code>tags</code>：用于定向失效。

失效：

~~~ts
// Endpoint 中
await context.cache.invalidate({ tags: ['products'] });
await context.cache.invalidate({ path: '/products/astro-book' });
~~~

官方依据：[Route caching](https://docs.astro.build/en/guides/caching/)

> [!warning] 缓存安全
> 只要响应含用户身份、账户信息、购物车或权限差异，就不要放进公共共享缓存。先证明缓存 key 能隔离用户，再考虑更复杂方案。

开发模式不会真正缓存，<code>cache.enabled</code> 为 false。要用 build + preview 测试缓存。

Astro 7 的 Netlify、Vercel、Cloudflare CDN cache provider 仍由官方标为实验性，需要显式启用。生产采用前先阅读对应 Adapter 文档。

### 18.2 Advanced Routing

Astro 7 把 <code>src/fetch.ts</code> 设为特殊入口，可以替换或包裹默认请求管线。

保留默认行为，只加日志与响应头：

~~~ts
// src/fetch.ts
import { FetchState, astro } from 'astro/fetch';

export default {
  async fetch(request: Request): Promise<Response> {
    const state = new FetchState(request);
    const startedAt = performance.now();

    const response = await astro(state);
    response.headers.set(
      'Server-Timing',
      'app;dur=' + (performance.now() - startedAt).toFixed(1),
    );

    return response;
  },
};
~~~

官方依据：[Advanced routing](https://docs.astro.build/en/guides/routing/#advanced-routing) · [astro/fetch API](https://docs.astro.build/en/reference/modules/astro-fetch/)

> [!danger] 不要急着用
> 默认管线已经依次处理 trailing slash、redirect、session、action、middleware、page、i18n、cache。大多数项目不需要替换它。只有需要精确改变执行顺序、接入 Hono、代理部分请求或包住整个管线时再用 Advanced Routing。

官方特别提醒：不要仅通过字符串检查传入 URL pathname 来做授权，因为传入 pathname 不保证就是 Astro 最终匹配的内部路由。保护路由应交给拥有路由匹配能力的 router，或在实际 Action / Endpoint / Page 授权。

如果项目本来有普通 <code>src/fetch.ts</code>，请重命名，或设置 <code>fetchFile: null</code>。

### 18.3 Astro 7 迁移要点

- Rust 编译器是唯一编译器，未闭合标签会报错；
- 不再自动修正不合法 HTML 嵌套；
- 默认 JSX 风格空白压缩；
- Markdown / MDX 默认 Sätteri；
- <code>src/fetch.ts</code> 是保留入口；
- Route Caching 与 Advanced Routing 已稳定；
- <code>@astrojs/db</code> 已从 Astro 7 移除；
- 旧 Astro 项目可运行 <code>npx @astrojs/upgrade</code>。

### 18.4 构建质量门

~~~bash
pnpm astro check
pnpm build
pnpm preview
~~~

手动检查：

- [ ] 所有路由都能打开；
- [ ] 404、redirect、动态路由正确；
- [ ] 无意外 hydration；
- [ ] 浏览器控制台无错误；
- [ ] 所有图片尺寸稳定；
- [ ] 键盘可操作；
- [ ] 手机、平板、桌面布局正常；
- [ ] 客户端导航后脚本仍工作；
- [ ] 秘密没有出现在客户端源码或 Network 响应；
- [ ] 动态页面在目标 Adapter 上工作。

### 18.5 性能检查

关注：

- JavaScript 总量与每个 Island 的框架成本；
- <code>client:load</code> 数量；
- LCP 图片是否正确优化和优先加载；
- CLS 是否来自图片、字体或 Server Island fallback；
- 第三方脚本；
- Content Collection 构建规模；
- 动态数据是否阻塞整个页面；
- 缓存是否正确且不泄露个性化内容。

### 18.6 部署策略

| 项目形态 | 构建 / 运行要求 |
|---|---|
| 纯静态博客 | <code>pnpm build</code>，部署 dist |
| 含 server:defer | Adapter + 服务器 / serverless runtime |
| 含 <code>prerender=false</code> | Adapter |
| <code>output='server'</code> | Adapter |
| Sessions | Adapter 和合适 session driver |
| Route Caching | cache provider 与 runtime 支持 |

官方依据：[Deployment overview](https://docs.astro.build/en/guides/deploy/) · [Adapters](https://docs.astro.build/en/guides/on-demand-rendering/#server-adapters)
