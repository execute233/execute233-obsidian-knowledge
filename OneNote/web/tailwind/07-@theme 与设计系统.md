---
title: @theme 与设计系统
tags: [Tailwind, CSS, frontend]
aliases: ["@theme 与设计系统"]
---

# @theme 与设计系统

## 7.1 theme variable 不只是 CSS variable

<code>@theme</code> 中的变量既会成为原生 CSS variable，也会影响哪些 utility 或 variants 存在：

~~~css
@import "tailwindcss";

@theme {
  --color-mint-500: oklch(0.72 0.11 178);
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 120rem;
}
~~~

于是得到：

~~~html
<div class="bg-mint-500 font-display 3xl:grid-cols-6"></div>
~~~

普通 <code>:root</code> 变量不会自动创建 utility。官方因此要求 <code>@theme</code> 位于顶层。参考[Theme variables](https://tailwindcss.com/docs/theme)。

## 7.2 重要命名空间

| namespace | 生成或影响 |
|---|---|
| <code>--color-*</code> | <code>bg-*</code>、<code>text-*</code>、<code>border-*</code> 等颜色 utility |
| <code>--font-*</code> | font family |
| <code>--text-*</code> | font size |
| <code>--font-weight-*</code> | font weight |
| <code>--tracking-*</code> | letter spacing |
| <code>--leading-*</code> | line height |
| <code>--breakpoint-*</code> | viewport variants |
| <code>--container-*</code> | container variants 与部分 size utility |
| <code>--spacing-*</code> / <code>--spacing</code> | spacing 与 sizing |
| <code>--radius-*</code> | border radius |
| <code>--shadow-*</code> | box shadow |
| <code>--blur-*</code> | blur |
| <code>--ease-*</code> | easing |
| <code>--animate-*</code> | animation |

## 7.3 建立项目 token

~~~css
@import "tailwindcss";

@theme {
  --color-brand-50: oklch(0.97 0.02 240);
  --color-brand-100: oklch(0.93 0.04 240);
  --color-brand-500: oklch(0.68 0.16 240);
  --color-brand-600: oklch(0.58 0.18 240);
  --color-brand-700: oklch(0.49 0.16 240);

  --font-display: "Inter Variable", "Noto Sans SC", sans-serif;

  --radius-card: 1rem;
  --shadow-card: 0 1rem 3rem oklch(0.2 0.02 240 / 0.1);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
}
~~~

使用：

~~~html
<article class="rounded-card bg-white p-6 shadow-card">
  <h2 class="font-display text-brand-700">课程</h2>
</article>
~~~

设计 token 的名字应表达体系，而不是偶然页面：

~~~text
较好：brand、surface、danger、card、display
较差：login-blue、homepage-shadow、left-card-radius
~~~

## 7.4 语义 token 与主题切换

为了让组件不必到处同时写浅色和深色 palette，可以让语义变量随主题变化，再把它们映射为 Tailwind 颜色：

~~~css
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));

:root {
  --app-surface: oklch(1 0 0);
  --app-surface-muted: oklch(0.97 0.01 250);
  --app-text: oklch(0.2 0.02 250);
  --app-text-muted: oklch(0.5 0.02 250);
  --app-border: oklch(0.9 0.01 250);
}

.dark {
  --app-surface: oklch(0.2 0.02 250);
  --app-surface-muted: oklch(0.25 0.02 250);
  --app-text: oklch(0.96 0.01 250);
  --app-text-muted: oklch(0.72 0.02 250);
  --app-border: oklch(0.35 0.02 250);
}

@theme inline {
  --color-surface: var(--app-surface);
  --color-surface-muted: var(--app-surface-muted);
  --color-content: var(--app-text);
  --color-content-muted: var(--app-text-muted);
  --color-line: var(--app-border);
}
~~~

组件变为：

~~~html
<article class="border border-line bg-surface text-content">
  <p class="text-content-muted">次要信息</p>
</article>
~~~

使用 <code>@theme inline</code> 可让生成的 utility 直接引用右侧变量值，适合这种变量映射。

## 7.5 扩展、覆盖和重置

扩展默认主题：

~~~css
@theme {
  --font-script: "Great Vibes", cursive;
}
~~~

覆盖单个 token：

~~~css
@theme {
  --breakpoint-sm: 30rem;
}
~~~

清空某个 namespace：

~~~css
@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-brand: oklch(0.65 0.18 245);
}
~~~

清空整个默认主题：

~~~css
@theme {
  --*: initial;
  --spacing: 0.25rem;
  --color-brand: oklch(0.65 0.18 245);
  --font-body: "Inter", sans-serif;
}
~~~

最后一种是强约束设计系统的做法，不适合作为刚入门时的默认选择，因为大量默认 utility 会消失。

## 7.6 什么时候把任意值提升为 token

满足任意两项时，通常值得提升：

- 在多个文件重复出现。
- 有明确语义，例如品牌色、卡片圆角。
- 修改它应全局联动。
- 需要给设计或产品共同命名。
- 需要在自定义 CSS、JavaScript 或动画库中复用。

只出现一次的布局修正无需强行进入主题。

## 7.7 分享主题

主题可以独立为 CSS 文件：

~~~css
/* packages/brand/theme.css */
@theme {
  --color-brand-500: oklch(0.68 0.16 240);
  --font-display: "Inter Variable", sans-serif;
}
~~~

应用中导入：

~~~css
@import "tailwindcss";
@import "../packages/brand/theme.css";
~~~

这让 monorepo 中的多个应用共享 token，不必复制 JavaScript 配置。
