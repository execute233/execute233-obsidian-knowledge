---
title: 第 16 课：Middleware、Sessions 与环境变量
tags: ["Astro", "frontend", "课程", "课程-16"]
aliases: ["第 16 课", "Middleware、Sessions 与环境变量", "第 16 课：Middleware、Sessions 与环境变量"]
---
# 第十六课：Middleware、Sessions 与环境变量

### 16.1 Middleware

~~~ts
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const sessionId = context.cookies.get('session')?.value;
  context.locals.user = sessionId
    ? await findUserBySession(sessionId)
    : null;

  const response = await next();
  response.headers.set('X-Frame-Options', 'DENY');
  return response;
});
~~~

页面：

~~~astro
---
const user = Astro.locals.user;
---

{user ? <p>你好，{user.name}</p> : <a href="/login">登录</a>}
~~~

<code>locals</code> 只活在当前请求，不会自动跨请求持久化。

官方依据：[Middleware](https://docs.astro.build/en/guides/middleware/)

### 16.2 类型化 Locals

~~~ts
// src/env.d.ts
type User = {
  id: string;
  name: string;
  role: 'reader' | 'author' | 'admin';
};

declare namespace App {
  interface Locals {
    user: User | null;
  }
}
~~~

### 16.3 Sessions

Sessions 在 Astro 页面用 <code>Astro.session</code>，在 Endpoint、Middleware、Action 用 <code>context.session</code>：

~~~astro
---
export const prerender = false;

const cart = (await Astro.session?.get('cart')) ?? [];
---

<a href="/cart">购物车：{cart.length}</a>
~~~

Action 中：

~~~ts
handler: async ({ productId }, context) => {
  const cart = (await context.session?.get('cart')) ?? [];
  cart.push(productId);
  await context.session?.set('cart', cart);
  return cart;
}
~~~

类型化 Session：

~~~ts
// src/env.d.ts
declare namespace App {
  interface SessionData {
    cart: string[];
    user: {
      id: string;
      name: string;
    };
  }
}
~~~

Session driver 依赖 Adapter / runtime。生产环境需确认默认 driver 是否持久、是否适合多实例、是否运行在 edge。Astro 官方文档明确说明 Sessions 不支持 edge middleware。

官方依据：[Sessions](https://docs.astro.build/en/guides/sessions/)

### 16.4 环境变量

Vite 方式：

~~~dotenv
DATABASE_URL=postgres://secret
PUBLIC_SITE_NAME=Astro Notes
~~~

- 所有环境变量可用于服务器代码；
- 只有 <code>PUBLIC_</code> 前缀变量会暴露到客户端；
- 永远不要把密码、token 加 <code>PUBLIC_</code>。

Astro 类型安全 env schema：

~~~js
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      SITE_NAME: envField.string({
        context: 'client',
        access: 'public',
        default: 'Astro Notes',
      }),
      DATABASE_URL: envField.string({
        context: 'server',
        access: 'secret',
      }),
    },
  },
});
~~~

使用：

~~~ts
import { SITE_NAME } from 'astro:env/client';
import { DATABASE_URL } from 'astro:env/server';
~~~

Secret client variable 不存在，因为发送到浏览器就不再是 secret。

官方依据：[Environment variables](https://docs.astro.build/en/guides/environment-variables/)

### 16.5 一个可靠的 Auth 请求路径

~~~mermaid
flowchart TD
  A["Request"] --> B["Middleware 读 cookie / session"]
  B --> C["context.locals.user"]
  C --> D["Page / Endpoint / Action"]
  D --> E["授权检查"]
  E --> F["Response"]
~~~

不要只在页面隐藏按钮就认为资源已受保护。真正的授权必须在 Action / Endpoint / 服务器查询处执行。
