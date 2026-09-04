---
title: 附录 B：高频速查表
tags: [Tailwind, CSS, frontend]
aliases: ["附录 B：高频速查表"]
---

# 附录 B：高频速查表

## 布局

| 目标 | 常用 utility |
|---|---|
| 隐藏/显示 | <code>hidden</code>、<code>block</code>、<code>inline</code>、<code>inline-block</code> |
| Flex | <code>flex</code>、<code>flex-col</code>、<code>flex-wrap</code>、<code>flex-1</code> |
| 对齐 | <code>items-center</code>、<code>justify-between</code>、<code>place-items-center</code> |
| Grid | <code>grid</code>、<code>grid-cols-*</code>、<code>col-span-*</code> |
| 间距 | <code>gap-*</code>、<code>space-x-*</code>、<code>space-y-*</code> |
| 定位 | <code>relative</code>、<code>absolute</code>、<code>fixed</code>、<code>sticky</code> |
| 方向 | <code>inset-0</code>、<code>top-*</code>、<code>right-*</code> |
| 层级 | <code>z-*</code>、<code>isolate</code> |
| 溢出 | <code>overflow-hidden</code>、<code>overflow-x-auto</code> |

## 尺寸与间距

| 目标 | 常用 utility |
|---|---|
| 宽高 | <code>w-*</code>、<code>h-*</code>、<code>size-*</code> |
| 范围 | <code>min-w-*</code>、<code>max-w-*</code>、<code>min-h-*</code>、<code>max-h-*</code> |
| 视口 | <code>min-h-screen</code>、<code>min-h-dvh</code> |
| 外边距 | <code>m-*</code>、<code>mx-*</code>、<code>my-*</code>、<code>mx-auto</code> |
| 内边距 | <code>p-*</code>、<code>px-*</code>、<code>py-*</code> |
| 比例 | <code>aspect-square</code>、<code>aspect-video</code> |

## 排版

| 目标 | 常用 utility |
|---|---|
| 字号 | <code>text-sm</code> 到 <code>text-9xl</code> |
| 字重 | <code>font-normal</code>、<code>font-medium</code>、<code>font-semibold</code>、<code>font-bold</code> |
| 行高 | <code>leading-*</code> 或 <code>text-base/7</code> |
| 字距 | <code>tracking-tight</code>、<code>tracking-wide</code> |
| 截断 | <code>truncate</code>、<code>line-clamp-*</code> |
| 换行 | <code>whitespace-nowrap</code>、<code>break-words</code>、<code>text-balance</code> |

## 外观

| 目标    | 常用 utility                                                              |
| ----- | ----------------------------------------------------------------------- |
| 背景/文字 | <code>bg-*</code>、<code>text-*</code>                                   |
| 边框    | <code>border</code>、<code>border-*</code>                               |
| 圆角    | <code>rounded-*</code>                                                  |
| 焦点环   | <code>ring-*</code>、<code>outline-*</code>                              |
| 阴影    | <code>shadow-*</code>、<code>inset-shadow-*</code>                       |
| 透明    | <code>opacity-*</code> 或颜色 <code>/数字</code>                             |
| 图片    | <code>object-cover</code>、<code>object-contain</code>                   |
| 滤镜    | <code>blur-*</code>、<code>grayscale</code>、<code>backdrop-blur-*</code> |

## 响应式与状态

~~~text
sm: md: lg: xl: 2xl:
max-md: md:max-lg:
@container @sm: @lg:

hover: focus: focus-visible: active: disabled:
checked: invalid: open:
first: last: odd: even: empty:
group-hover: peer-checked: has-checked:
data-active: aria-expanded:
dark:
motion-reduce: contrast-more: forced-colors:
~~~

## v4 CSS API

| API | 用途 |
|---|---|
| <code>@import</code> | 导入 Tailwind 与其他 CSS |
| <code>@theme</code> | 定义 design tokens 与 utility API |
| <code>@source</code> | 控制源码检测和 safelist |
| <code>@utility</code> | 注册 custom utility |
| <code>@custom-variant</code> | 注册 custom variant |
| <code>@variant</code> | 在 CSS 中应用 variant |
| <code>@apply</code> | 将 utility 内联到自定义 CSS |
| <code>@reference</code> | 为 Vue/Svelte style 或 CSS Module 引用上下文 |
| <code>--spacing()</code> | 在 CSS 中使用 spacing scale |
| <code>--alpha()</code> | 在 CSS 中调整颜色透明度 |

---
