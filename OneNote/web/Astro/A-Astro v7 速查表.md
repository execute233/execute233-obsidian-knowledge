---
title: Astro v7 速查表
tags: ["Astro", "frontend", "速查表", "附录"]
aliases: ["Astro v7 速查表"]
---
# Astro v7 速查表

## .astro 常用 API

| API | 用途 |
|---|---|
| <code>Astro.props</code> | 组件 / getStaticPaths Props |
| <code>Astro.params</code> | 动态路由参数 |
| <code>Astro.url</code> | 当前 URL |
| <code>Astro.site</code> | 配置的站点基础 URL |
| <code>Astro.cookies</code> | 按需渲染时操作 cookie |
| <code>Astro.locals</code> | 当前请求的 Middleware 数据 |
| <code>Astro.session</code> | Session 数据 |
| <code>Astro.cache</code> | 当前动态响应缓存策略 |
| <code>Astro.redirect()</code> | 跳转并改变 URL |
| <code>Astro.rewrite()</code> | 渲染另一条路由但保留 URL |
| <code>Astro.slots.has()</code> | 检查 Slot |

## 指令

| 指令 | 作用 |
|---|---|
| <code>class:list</code> | 组合动态 class |
| <code>set:text</code> | 设置纯文本 |
| <code>set:html</code> | 插入 HTML；需自行保证可信 |
| <code>is:global</code> | 全局 CSS |
| <code>is:inline</code> | script / style 原样输出 |
| <code>define:vars</code> | 将 JS 值传入 CSS / script 变量 |
| <code>client:load</code> | 尽快 hydration |
| <code>client:idle</code> | 空闲时 hydration |
| <code>client:visible</code> | 可见时 hydration |
| <code>client:media</code> | media query 匹配时 hydration |
| <code>client:only</code> | 仅客户端渲染 |
| <code>server:defer</code> | 延迟服务器岛 |
| <code>transition:persist</code> | 页面导航间保留元素 / Island |

## Content Collections

~~~ts
import { defineCollection, getCollection, getEntry, render } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';
~~~

| 操作 | API |
|---|---|
| 定义集合 | <code>defineCollection()</code> |
| 多文件加载 | <code>glob()</code> |
| 单数据文件 | <code>file()</code> |
| 查询集合 | <code>getCollection()</code> |
| 查询一项 | <code>getEntry()</code> |
| 渲染 Markdown / MDX | <code>render(entry)</code> |

## 渲染选择

~~~text
默认 static
├── 普通页面：构建时生成
├── export const prerender = false：按请求生成
└── server:defer：独立服务器岛

output: server
├── 普通页面：按请求生成
└── export const prerender = true：构建时生成
~~~

## Vue Island 选择

~~~text
需要立即交互？       client:load
非关键但很快会用？   client:idle
滚到那里才会用？     client:visible
只在某媒体条件使用？ client:media
完全不能 SSR？       client:only="vue"
~~~

---
