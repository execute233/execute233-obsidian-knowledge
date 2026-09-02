---
title: 第 11 课：Content Collections 完整实战
tags: ["Astro", "frontend", "课程", "课程-11"]
aliases: ["第 11 课", "Content Collections 完整实战", "第 11 课：Content Collections 完整实战"]
---
# 第十一课：Content Collections 完整实战

### 11.1 文件结构

~~~text
src/
├── content.config.ts
├── data/
│   └── blog/
│       ├── astro-islands.md
│       └── tailwind-v4.md
├── layouts/
│   └── PostLayout.astro
└── pages/
    └── blog/
        ├── index.astro
        └── [id].astro
~~~

> [!warning]
> 当前主线配置文件是根于 src 的 <code>src/content.config.ts</code>，不是旧教程常见的 <code>src/content/config.ts</code>。

### 11.2 定义集合

~~~ts
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({
    base: './src/data/blog',
    pattern: '**/*.{md,mdx}',
  }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    cover: z.string().optional(),
  }),
});

export const collections = { blog };
~~~

官方依据：[Content collections](https://docs.astro.build/en/guides/content-collections/)

### 11.3 创建文章

~~~md
---
title: 理解 Astro Islands
description: 为什么 Astro 默认几乎不发送 JavaScript。
pubDate: 2026-09-01
tags:
  - Astro
  - Architecture
draft: false
---

# Islands

Astro 先输出 HTML，再只对需要交互的区域 hydration。
~~~

Schema 不匹配时，开发或构建会直接报错。把内容错误变成构建错误，是 Content Collections 的主要价值之一。

### 11.4 查询、过滤、排序

~~~astro
<!-- src/pages/blog/index.astro -->
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';

const posts = (
  await getCollection('blog', ({ data }) => {
    return import.meta.env.PROD ? !data.draft : true;
  })
).sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
---

<BaseLayout title="文章">
  <h1>文章</h1>

  <ul>
    {posts.map((post) => (
      <li>
        <a href={'/blog/' + post.id}>{post.data.title}</a>
        <time datetime={post.data.pubDate.toISOString()}>
          {post.data.pubDate.toLocaleDateString('zh-CN')}
        </time>
      </li>
    ))}
  </ul>
</BaseLayout>
~~~

> [!important]
> <code>getCollection()</code> 的顺序不保证稳定。需要按日期展示时，必须自己排序。

### 11.5 生成详情页

~~~astro
<!-- src/pages/blog/[id].astro -->
---
import type { CollectionEntry } from 'astro:content';
import { getCollection, render } from 'astro:content';
import PostLayout from '../../layouts/PostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  return posts.map((post) => ({
    params: { id: post.id },
    props: { post },
  }));
}

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;
const { Content, headings } = await render(post);
---

<PostLayout
  title={post.data.title}
  description={post.data.description}
  pubDate={post.data.pubDate}
  tags={post.data.tags}
>
  <aside slot="toc">
    <ul>
      {headings
        .filter((heading) => heading.depth <= 3)
        .map((heading) => (
          <li>
            <a href={'#' + heading.slug}>{heading.text}</a>
          </li>
        ))}
    </ul>
  </aside>

  <Content />
</PostLayout>
~~~

### 11.6 id 与自定义 slug

<code>glob()</code> 会按文件生成 URL 友好的 id。内容 frontmatter 中可用 <code>slug</code> 覆盖单条内容的生成 id，包括带斜线的路径。

URL 设计要稳定。文章发布后不要随意改变 id；确实改变时配置 redirect。

### 11.7 不只加载 Markdown

内置 Loader：

- <code>glob()</code>：从多个 Markdown、MDX、JSON、YAML、TOML 等文件加载；
- <code>file()</code>：从单个 JSON 等数据文件生成集合；
- 自定义 Loader：从 CMS、API、数据库加载。

Astro 7 文档还提供 Live Content Collections，按请求读取远程内容，使用 <code>src/live.config.ts</code> 与 <code>getLiveCollection()</code>。这是进阶选修，先掌握 build-time collection。
