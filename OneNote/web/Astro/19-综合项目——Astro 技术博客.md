---
title: 第 19 课：综合项目——Astro 技术博客
tags: ["Astro", "frontend", "课程", "课程-19"]
aliases: ["第 19 课", "综合项目——Astro 技术博客", "Capstone"]
---
# 第十九课：综合项目——Astro 技术博客

## 项目目标

交付一个能部署的内容站，覆盖 Astro 最重要能力，但保持合理 JavaScript 预算。

### 必做功能

- [ ] BaseLayout、PostLayout、SEO metadata；
- [ ] Tailwind CSS v4 主题 token、响应式和暗色模式；
- [ ] Content Collection Schema；
- [ ] 博客首页、文章详情动态路由；
- [ ] draft 过滤、日期排序、标签；
- [ ] Astro Image；
- [ ] 自动文章目录；
- [ ] Vue 搜索 Island；
- [ ] 无 Vue 的主题切换与复制按钮；
- [ ] 自定义 404；
- [ ] RSS 与 Sitemap；
- [ ] View Transitions；
- [ ] 无障碍与生产构建检查；
- [ ] 静态部署。

### 进阶功能

- [ ] 评论 Action；
- [ ] Middleware + Session 登录状态；
- [ ] UserMenu Server Island；
- [ ] 一个公开动态路由的 Route Cache；
- [ ] 搜索 URL query 同步；
- [ ] 标签分页；
- [ ] 端到端测试。

## 推荐目录

~~~text
src/
├── actions/
│   └── index.ts
├── assets/
│   └── covers/
├── components/
│   ├── BaseHead.astro
│   ├── Header.astro
│   ├── Footer.astro
│   ├── PostCard.astro
│   ├── ThemeToggle.astro
│   ├── UserMenu.astro
│   └── SearchBox.vue
├── data/
│   └── blog/
├── layouts/
│   ├── BaseLayout.astro
│   └── PostLayout.astro
├── pages/
│   ├── index.astro
│   ├── 404.astro
│   ├── about.astro
│   ├── rss.xml.ts
│   └── blog/
│       ├── index.astro
│       └── [id].astro
├── styles/
│   └── global.css
├── content.config.ts
├── env.d.ts
└── middleware.ts
~~~

## 架构决策

| 功能 | 技术选择 | 原因 |
|---|---|---|
| 文章正文 | Astro + Content Collection | 静态、类型安全、零客户端 JS |
| 布局 | Astro Layout | 生成 HTML，无需 runtime |
| 样式 | Tailwind v4 | 复用已有课程与 token |
| 搜索 | Vue Island + client:visible | 需要响应式输入 |
| 主题切换 | 小型 script | 不需要 Vue runtime |
| 用户菜单 | Server Island | 个性化但不阻塞静态正文 |
| 评论提交 | Action | 站内类型安全调用与验证 |
| 评论开放 API | Endpoint | 需要标准 HTTP 接口时才添加 |

## 里程碑

### Milestone 1：静态骨架

- 页面、路由、Layout；
- Tailwind；
- Header / Footer；
- SEO。

完成定义：关闭 JavaScript后，所有核心页面仍可阅读和导航。

### Milestone 2：内容系统

- Content Collection；
- 三篇文章；
- 动态详情页；
- 目录、标签、排序。

完成定义：错误 frontmatter 会在构建时失败。

### Milestone 3：渐进增强

- 主题切换；
- 复制按钮；
- Vue 搜索 Island；
- View Transitions。

完成定义：JavaScript 只出现在有明确交互需求的位置。

### Milestone 4：生产质量

- Image；
- RSS、Sitemap；
- 404、redirect；
- 检查、构建、预览；
- Lighthouse 与键盘测试；
- 部署。

### Milestone 5：可选全栈

- Adapter；
- Action；
- Middleware；
- Session；
- Server Island；
- Route Caching。

完成定义：个性化响应不进入共享缓存，授权在服务器执行。

### RSS 与 Sitemap 最小实现

先确保 <code>astro.config.mjs</code> 已配置 <code>site</code>。

~~~bash
pnpm add @astrojs/rss
pnpm astro add sitemap
~~~

~~~ts
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  return rss({
    title: 'Astro Notes',
    description: 'Astro 与现代前端学习笔记',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: '/blog/' + post.id + '/',
    })),
  });
}
~~~

在 Layout 的 head 加 RSS 自动发现：

~~~astro
<link
  rel="alternate"
  type="application/rss+xml"
  title="Astro Notes"
  href={new URL('rss.xml', Astro.site)}
/>
~~~

官方依据：[RSS recipe](https://docs.astro.build/en/recipes/rss/) · [Sitemap integration](https://docs.astro.build/en/guides/integrations-guide/sitemap/)

## 项目评分表

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| HTML / A11y | 结构或键盘不可用 | 基本可用 | 语义、焦点、标签完整 |
| Astro 边界 | 整页 Vue | 部分合理 | HTML、脚本、Island 选择清晰 |
| 内容类型 | 无 Schema | 有基本 Schema | 验证、筛选、排序完整 |
| 渲染策略 | 全部动态 | 能运行 | 每路由策略有依据 |
| 性能 | JS 与图片失控 | 基本优化 | Island 延迟、图片和 CLS 优化 |
| 安全 | 信任客户端 | 验证输入 | 验证 + 认证 + 授权 + 缓存隔离 |
| 工程质量 | 不能构建 | 可构建 | check、build、preview、部署全通过 |

总分 12 分；达到 10 分即可认为主线课程完成。

---
