---
title: 自测题与答案
tags: ["Astro", "frontend", "自测题", "附录"]
aliases: ["自测题与答案"]
---
# 自测题

先独立回答，再展开答案。

1. 为什么普通 Astro Component 不需要 hydration？
2. <code>&lt;Counter /&gt;</code> 和 <code>&lt;Counter client:load /&gt;</code> 有什么差异？
3. 为什么静态动态路由需要 <code>getStaticPaths()</code>？
4. 什么情况下用 <code>client:visible</code> 比 <code>client:load</code> 更合理？
5. Props 和 Slots 分别适合什么？
6. <code>src/assets</code> 和 <code>public</code> 的区别？
7. Content Collection 查询为什么要显式排序？
8. <code>prerender=false</code> 与 <code>output='server'</code> 的关系？
9. Client Island 和 Server Island 的运行位置有何不同？
10. Action 和 Endpoint 如何选择？
11. Middleware locals 能否跨请求保存购物车？
12. 为什么 <code>PUBLIC_</code> 不能放 secret？
13. View Transition 后，为什么 DOMContentLoaded 代码可能不再运行？
14. 哪些页面绝不能进入公共 Route Cache？
15. 普通博客是否需要 <code>src/fetch.ts</code>？

> [!success]- 参考答案
> 1. 它在构建时或服务器渲染成 HTML，本身没有客户端 runtime。
> 2. 前者只输出 HTML；后者还加载框架 JavaScript并 hydration。
> 3. 构建阶段必须提前知道要生成哪些 URL。
> 4. 组件在首屏下方或用户可能永远看不到时。
> 5. Props 传数据与选项，Slots 传 HTML 结构。
> 6. src 会处理、优化、打包；public 原样复制。
> 7. 官方说明生成集合顺序不稳定且依平台而异。
> 8. 前者让单条路由按需渲染；后者让按需渲染成为全站默认。
> 9. Client Island 在浏览器 hydration；Server Island 在服务器延迟渲染。
> 10. 站内类型安全调用与表单优先 Action；公开标准 HTTP / 文件输出优先 Endpoint。
> 11. 不能。locals 只存在于当前请求，跨请求使用 Session 或数据库。
> 12. 带 PUBLIC_ 的值会进入客户端代码，发送后不再是秘密。
> 13. ClientRouter 替换 DOM 而不是完整刷新，应监听 astro:page-load。
> 14. 含用户身份、账户、购物车、权限差异或其他私密内容的响应。
> 15. 通常不需要。默认请求管线已覆盖普通需求。

---
