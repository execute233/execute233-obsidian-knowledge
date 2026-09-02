---
title: 常见问题与排错
tags: ["Astro", "frontend", "排错", "附录"]
aliases: ["常见问题与排错"]
---
# 常见问题与排错

## 为什么 class / Tailwind 不生效

1. 类名是否动态拼接，导致扫描器看不到完整候选？
2. 全局 Tailwind CSS 是否被 Layout 导入？
3. scoped style 是否试图穿透子组件？
4. class 是否正确透传到子组件根元素？
5. 组件是不是来自 MDX / Slot，需要 <code>:global()</code> 或 Typography？

## 为什么点击没反应

1. Vue 组件是否缺少 <code>client:*</code>？
2. 是否本来该用浏览器 script？
3. ClientRouter 导航后脚本是否重新初始化？
4. querySelector 是否只绑定了第一个实例？
5. 事件是否在正确执行环境中注册？

## 为什么动态路由构建失败

1. static 模式是否遗漏 <code>getStaticPaths()</code>？
2. params 名称是否与文件中的 <code>[param]</code> 一致？
3. params 值是否为 string 或 undefined？
4. Content Collection id 是否与你生成的 URL 一致？
5. 是否把 SSG 的 props 写法搬进按需动态路由？

## 为什么代码报 window is not defined

浏览器 API 被放进 frontmatter、服务器组件、Endpoint 或 Action。移到：

- 普通 <code>&lt;script&gt;</code>；
- Vue 的 mounted / 浏览器事件；
- <code>client:only</code>，仅当组件确实不能 SSR。

## 为什么缓存没有生效

1. 是否在 dev 模式测试？开发模式不实际缓存。
2. 是否配置 cache provider？
3. 是否为按需响应？
4. <code>Astro.cache.enabled</code> 是否为 true？
5. Adapter 是否支持对应 provider？
6. 响应是不是个性化而被主动 opt out？

## 为什么旧教程代码不工作

优先排查：

- <code>src/content/config.ts</code> → 当前 <code>src/content.config.ts</code>；
- 旧 Content Collections API → Loader API；
- <code>@astrojs/tailwind</code> → Tailwind v4 Vite plugin；
- remark / rehype 默认存在 → Astro 7 默认 Sätteri；
- 把 Advanced Routing 当实验 flag → Astro 7 已稳定；
- 依赖 <code>@astrojs/db</code> → Astro 7 已移除。

---
