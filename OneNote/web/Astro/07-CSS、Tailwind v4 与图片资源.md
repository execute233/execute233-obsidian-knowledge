---
title: 第 07 课：CSS、Tailwind v4 与图片资源
tags: ["Astro", "frontend", "课程", "课程-7"]
aliases: ["第 07 课", "CSS、Tailwind v4 与图片资源", "第 07 课：CSS、Tailwind v4 与图片资源"]
---
# 第七课：CSS、Tailwind v4 与图片资源

### 7.1 默认 Scoped CSS

~~~astro
<article class="card">
  <h2>只影响本组件</h2>
</article>

<style>
  .card {
    border: 1px solid #ddd;
  }

  h2 {
    color: rebeccapurple;
  }
</style>
~~~

Astro 会给选择器和当前组件中的 HTML 加作用域标记。父组件的 scoped style 默认不会直接控制子组件内部结构。

需要全局样式时：

~~~astro
<style is:global>
  html {
    color-scheme: light dark;
  }
</style>
~~~

需要在局部容器中控制 Slot 或渲染后的 Markdown：

~~~astro
<article class="prose">
  <slot />
</article>

<style>
  .prose :global(h2) {
    margin-top: 2rem;
  }
</style>
~~~

官方依据：[Styles and CSS](https://docs.astro.build/en/guides/styling/)

### 7.2 添加 Tailwind CSS v4

Astro 5.2+ 官方命令会安装 Tailwind v4 的 Vite 插件：

~~~bash
pnpm astro add tailwind
~~~

全局样式：

~~~css
/* src/styles/global.css */
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.62 0.2 275);
  --font-sans: "Inter", system-ui, sans-serif;
}
~~~

在顶层 Layout 导入：

~~~astro
---
import '../styles/global.css';
---
~~~

> [!warning] Tailwind 版本坑
> Astro 7 + Tailwind v4 不以 <code>@astrojs/tailwind</code> 作为主线。旧集成面向 Tailwind 3。当前官方方式是 <code>astro add tailwind</code> 安装 <code>@tailwindcss/vite</code>，并在 CSS 中使用 <code>@import "tailwindcss"</code>。

你的 Tailwind 独立课程负责 utility、响应式和 design token；本课只关注它与 Astro 的边界。

### 7.3 Astro 组件中的 Tailwind

~~~astro
---
interface Props {
  title: string;
  active?: boolean;
}

const { title, active = false } = Astro.props;
---

<article
  class:list={[
    'rounded-2xl border p-6 shadow-sm',
    active
      ? 'border-brand-500 bg-brand-500/10'
      : 'border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-950',
  ]}
>
  <h2 class="text-xl font-semibold">{title}</h2>
</article>
~~~

Tailwind 扫描的是完整、静态可识别的类名。不要写：

~~~ts
// 不推荐：扫描器无法可靠发现完整类名
const color = 'red';
const className = 'bg-' + color + '-500';
~~~

应映射完整候选：

~~~ts
const variants = {
  danger: 'bg-red-500 text-white',
  success: 'bg-emerald-500 text-white',
};
~~~

### 7.4 图片优化

本地图片优先放 <code>src/assets</code>：

~~~astro
---
import { Image, Picture } from 'astro:assets';
import cover from '../assets/cover.png';
---

<Image
  src={cover}
  alt="Astro 群岛架构示意图"
  widths={[480, 768, 1200]}
  sizes="(max-width: 768px) 100vw, 768px"
/>

<Picture
  src={cover}
  formats={['avif', 'webp']}
  alt="课程封面"
/>
~~~

Astro 的 Image 会推断本地图片尺寸，减少 CLS，并能在构建时或按需渲染时转换格式、质量和大小。<code>alt</code> 是必需的。

| 场景 | 推荐 |
|---|---|
| 需要优化的本地内容图 | <code>src/assets</code> + Image |
| 多格式输出 | Picture |
| favicon、robots.txt | public |
| 必须保持原样与固定 URL | public |
| 远程图优化 | 配置允许的域名或 remotePatterns |

官方依据：[Images](https://docs.astro.build/en/guides/images/)
