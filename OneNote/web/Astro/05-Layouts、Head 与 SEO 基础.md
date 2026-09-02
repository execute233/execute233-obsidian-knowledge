---
title: 第 05 课：Layouts、Head 与 SEO 基础
tags: ["Astro", "frontend", "课程", "课程-5"]
aliases: ["第 05 课", "Layouts、Head 与 SEO 基础", "第 05 课：Layouts、Head 与 SEO 基础"]
---
# 第五课：Layouts、Head 与 SEO 基础

### 5.1 BaseLayout

~~~astro
<!-- src/layouts/BaseLayout.astro -->
---
import '../styles/global.css';

interface Props {
  title: string;
  description?: string;
  image?: string;
}

const {
  title,
  description = '我的 Astro 学习站',
  image = '/og-default.png',
} = Astro.props;

const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <meta name="generator" content={Astro.generator} />

    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonicalURL} />

    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={new URL(image, Astro.site)} />

    <slot name="head" />
  </head>

  <body>
    <header>
      <a href="/">Astro Notes</a>
      <nav aria-label="主导航">
        <a href="/blog">文章</a>
        <a href="/about">关于</a>
      </nav>
    </header>

    <main>
      <slot />
    </main>

    <footer>© {new Date().getFullYear()}</footer>
  </body>
</html>
~~~

页面使用：

~~~astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="首页" description="学习 Astro v7">
  <link slot="head" rel="preconnect" href="https://fonts.example.com" />
  <h1>欢迎</h1>
</BaseLayout>
~~~

### 5.2 Layout 与 Vue Layout 的差别

组合方式很像，但 Astro Layout：

- 默认不在浏览器保持运行；
- 没有响应式状态或生命周期；
- 每次渲染输出 HTML；
- 可以在 frontmatter 安全访问服务器数据；
- 可以包住 Astro、Markdown、MDX 或框架组件。

### 5.3 Astro.site

<code>Astro.site</code> 来自配置：

~~~js
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://example.com',
});
~~~

生产站点应设置它，用于 canonical、RSS、sitemap、绝对社交分享 URL。

官方依据：[Layouts](https://docs.astro.build/en/basics/layouts/)
