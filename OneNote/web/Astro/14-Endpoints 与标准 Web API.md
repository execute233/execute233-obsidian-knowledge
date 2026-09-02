---
title: 第 14 课：Endpoints 与标准 Web API
tags: ["Astro", "frontend", "课程", "课程-14"]
aliases: ["第 14 课", "Endpoints 与标准 Web API", "第 14 课：Endpoints 与标准 Web API"]
---
# 第十四课：Endpoints 与标准 Web API

### 14.1 静态 Endpoint

~~~ts
// src/pages/site-info.json.ts
import type { APIRoute } from 'astro';

export const GET = (() => {
  return Response.json({
    name: 'Astro Notes',
    version: '1.0.0',
  });
}) satisfies APIRoute;
~~~

默认 static 模式会在构建时生成 <code>/site-info.json</code>。

### 14.2 服务器 Endpoint

~~~ts
// src/pages/api/comments.ts
import type { APIRoute } from 'astro';

export const prerender = false;

export const GET = (async () => {
  const comments = await listComments();
  return Response.json(comments);
}) satisfies APIRoute;

export const POST = (async ({ request }) => {
  if (request.headers.get('content-type') !== 'application/json') {
    return Response.json(
      { message: 'Content-Type 必须是 application/json' },
      { status: 415 },
    );
  }

  const body = await request.json();

  if (typeof body.content !== 'string' || body.content.trim() === '') {
    return Response.json(
      { message: 'content 不能为空' },
      { status: 400 },
    );
  }

  const comment = await createComment(body.content);
  return Response.json(comment, { status: 201 });
}) satisfies APIRoute;
~~~

Astro 支持导出 <code>GET</code>、<code>POST</code>、<code>PUT</code>、<code>PATCH</code>、<code>DELETE</code>、<code>OPTIONS</code>、<code>HEAD</code> 和 <code>ALL</code>。

官方依据：[Endpoints](https://docs.astro.build/en/guides/endpoints/)

### 14.3 Endpoint vs Action

| 需求 | Endpoint | Action |
|---|---|---|
| 给第三方或移动端公开 HTTP API | 推荐 | 不适合 |
| RSS、sitemap、JSON、图片文件 | 推荐 | 不适合 |
| 精确控制 HTTP、header、body | 推荐 | 可做但不是强项 |
| Astro 页面 / Island 调服务器函数 | 可用 fetch | 推荐 |
| 自动验证表单 / JSON | 手动 | 推荐 |
| 类型安全调用 | 自行建立 | 自动生成 |

### 14.4 安全清单

- [ ] 所有输入都验证。
- [ ] 验证 content-type 和 body 大小。
- [ ] 做身份认证与权限检查。
- [ ] 返回正确 HTTP status。
- [ ] 不在响应中泄露堆栈和秘密。
- [ ] 对公开写接口考虑 CSRF、CORS、rate limit。
