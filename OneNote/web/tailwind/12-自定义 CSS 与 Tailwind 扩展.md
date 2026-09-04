---
title: 自定义 CSS 与 Tailwind 扩展
tags: [Tailwind, CSS, frontend]
aliases: ["自定义 CSS 与 Tailwind 扩展"]
---

# 自定义 CSS 与 Tailwind 扩展

## 12.1 决策顺序

遇到官方 utility 无法直接满足的样式时，按以下顺序判断：

1. 是否已有官方 utility，只是还没查到？
2. 是否只是一次性的任意值或任意属性？
3. 是否应当成为 design token？
4. 是否是可复用的新单用途能力，适合 <code>@utility</code>？
5. 是否是组件或第三方结构，适合普通 CSS？

Tailwind 不禁止 CSS。[Adding custom styles](https://tailwindcss.com/docs/adding-custom-styles)正是官方核心文档的一部分。

## 12.2 Cascade layers

~~~css
@import "tailwindcss";

@layer base {
  body {
    background: var(--color-slate-50);
    color: var(--color-slate-950);
  }

  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}

@layer components {
  .markdown-content {
    max-width: 70ch;
  }
}
~~~

理解层次：

| layer | 用途 |
|---|---|
| theme | 设计令牌 |
| base | 元素默认规则、Preflight 补充 |
| components | 较复杂且可被 utility 覆盖的组件规则 |
| utilities | 单用途规则 |

## 12.3 @utility

简单 custom utility：

~~~css
@utility content-auto {
  content-visibility: auto;
}
~~~

使用时自动支持 variants：

~~~html
<section class="content-auto lg:content-auto">...</section>
~~~

带嵌套选择器：

~~~css
@utility scrollbar-hidden {
  &::-webkit-scrollbar {
    display: none;
  }
}
~~~

函数型 utility：

~~~css
@theme {
  --tab-size-github: 8;
}

@utility tab-* {
  tab-size: --value(--tab-size-*, integer, [integer]);
}
~~~

于是可以使用：

~~~html
<pre class="tab-github"></pre>
<pre class="tab-4"></pre>
<pre class="tab-[12]"></pre>
~~~

函数型 utility 属于进阶能力。只有项目确实需要一组参数化 utility 时再创建，避免构造一套没人理解的小框架。

## 12.4 @custom-variant

为产品状态建立 variant：

~~~css
@custom-variant theme-midnight (&:where([data-theme="midnight"], [data-theme="midnight"] *));
@custom-variant hocus (&:is(:hover, :focus-visible));
~~~

使用：

~~~html
<button class="hocus:bg-sky-700 theme-midnight:bg-slate-950">
  保存
</button>
~~~

如果只是一个元素的一次性复杂选择器，任意 variant 更轻；如果同一条件反复出现并有业务含义，再创建 custom variant。

## 12.5 @variant

在普通 CSS 中复用 Tailwind variant：

~~~css
.external-widget {
  background: white;

  @variant dark {
    background: black;
  }

  @variant hover, focus-visible {
    outline: 2px solid var(--color-sky-500);
  }
}
~~~

v4.3 支持在 <code>@variant</code> 中堆叠或以逗号表达多个 variant。

## 12.6 @apply

~~~css
@layer components {
  .select2-dropdown {
    @apply rounded-b-lg bg-white shadow-md;
  }
}
~~~

合理场景：

- 覆盖第三方组件已有 class。
- 你无法修改 HTML。
- 在现有 CSS 中需要复用 Tailwind token 和少量 utility。

不推荐把每个 Vue 组件都改成：

~~~css
.button {
  @apply rounded-lg bg-sky-600 px-4 py-2 text-white;
}
~~~

然后模板只写 <code>button</code>。这会把你重新带回频繁命名和跨文件跳转，同时失去直接组合 variants 的优势。Vue 组件本身已经是更完整的复用边界。

## 12.7 build-time functions

在普通 CSS 中复用主题能力：

~~~css
.panel {
  margin: --spacing(4);
  color: --alpha(var(--color-sky-600) / 80%);
}
~~~

<code>--spacing()</code> 根据主题 spacing 计算值；<code>--alpha()</code> 调整颜色透明度。旧 <code>theme()</code> 函数仍为迁移兼容存在，但官方建议 v4 优先使用 CSS theme variables。

## 12.8 prefix 与全局 important

接入遗留项目发生命名冲突时：

~~~css
@import "tailwindcss" prefix(tw);
~~~

类名前缀在 v4 中像 variant 一样位于最前：

~~~html
<div class="tw:flex tw:bg-red-500 tw:hover:bg-red-600"></div>
~~~

若遗留 CSS specificity 极高，可把所有 utility 标记 important：

~~~css
@import "tailwindcss" important;
~~~

这两项是有代价的兼容工具，不应作为新项目默认设置。
