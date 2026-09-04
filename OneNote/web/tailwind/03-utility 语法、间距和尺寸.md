---
title: utility 语法、间距和尺寸
tags: [Tailwind, CSS, frontend]
aliases: ["utility 语法、间距和尺寸"]
---

# utility 语法、间距和尺寸

## 3.1 从 CSS 属性推导 utility

高频 utility 通常遵循“属性缩写 + 主题值”：

| Tailwind               | 对应 CSS 意图           |
| ---------------------- | ------------------- |
| <code>p-4</code>       | 四边 padding          |
| <code>px-6</code>      | inline 方向 padding   |
| <code>py-3</code>      | block 方向 padding    |
| <code>mt-8</code>      | margin-top          |
| <code>mx-auto</code>   | 水平自动 margin         |
| <code>w-full</code>    | width: 100%         |
| <code>max-w-3xl</code> | 最大宽度取主题值            |
| <code>min-h-dvh</code> | 最小高度为动态视口高度         |
| <code>size-10</code>   | 同时设置 width 与 height |

在默认主题中，常用 spacing 基准是 <code>--spacing: 0.25rem</code>，所以：

~~~text
p-1  → 0.25rem
p-2  → 0.5rem
p-4  → 1rem
p-6  → 1.5rem
p-8  → 2rem
~~~

v4 能动态推导许多 spacing utility，因此 <code>w-17</code> 这类不在传统固定表里的数值也可以成立。工程中仍应优先选择稳定、重复的节奏，别因为“能写任意数字”就破坏视觉一致性。

## 3.2 方向缩写

~~~text
m   margin
p   padding

t   top
r   right
b   bottom
l   left
x   left + right
y   top + bottom

s   inline-start
e   inline-end
~~~

面向国际化界面时，<code>ms-*</code>、<code>me-*</code>、<code>ps-*</code>、<code>pe-*</code> 等逻辑方向 utility 比硬编码 left/right 更容易支持 RTL。

## 3.3 尺寸的常见模式

页面容器：

~~~html
<main class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
  ...
</main>
~~~

头像：

~~~html
<img class="size-12 shrink-0 rounded-full object-cover" src="..." alt="..." />
~~~

允许 Flex 子项正确省略文字：

~~~html
<div class="flex min-w-0 items-center gap-3">
  <img class="size-10 shrink-0 rounded-full" src="..." alt="" />
  <p class="min-w-0 truncate">一段可能非常长的标题</p>
</div>
~~~

<code>min-w-0</code> 是 Flex/Grid 中非常高频的排错类：子项默认最小尺寸可能阻止它收缩，导致 <code>truncate</code> 不生效或布局溢出。

## 3.4 任意值

设计系统没有某个一次性值时，用方括号：

~~~html
<div class="w-[372px]"></div>
<div class="top-[117px]"></div>
<div class="grid-cols-[14rem_minmax(0,1fr)]"></div>
<div class="max-h-[calc(100dvh-(--spacing(6)))]"></div>
~~~

任意值里的空格用下划线：

~~~html
<div class="grid-cols-[1fr_20rem_2fr]"></div>
~~~

引用 CSS variable 时可用简写：

~~~html
<div class="bg-(--card-bg) fill-(--icon-color)"></div>
~~~

它们分别相当于 <code>bg-[var(--card-bg)]</code> 和 <code>fill-[var(--icon-color)]</code>。

## 3.5 任意属性

Tailwind 暂无某个 utility 时，可以直接表达 CSS 属性：

~~~html
<div class="[mask-type:luminance] hover:[mask-type:alpha]"></div>
<div class="[--sidebar-width:18rem] lg:[--sidebar-width:20rem]"></div>
~~~

选择规则：

| 情况 | 推荐 |
|---|---|
| 官方已有 utility | 使用官方 utility |
| 一次性设计稿数值 | 任意值 |
| 运行时值 | 内联 CSS variable + utility |
| 多处重复且有设计含义 | 加入 <code>@theme</code> |
| 项目反复使用的新能力 | <code>@utility</code> |
| 复杂选择器或第三方结构 | 自定义 CSS |

## 3.6 负值、分数和 important

~~~html
<div class="-mt-4"></div>
<div class="w-1/2"></div>
<div class="translate-x-1/2"></div>
<div class="bg-red-500!"></div>
~~~

v4 的 important 修饰符推荐放在整个类名末尾，例如 <code>hover:bg-red-600!</code>。只有确实无法通过组件 API、层级或冲突清理解决时才使用它。

## 3.7 一个资料卡

~~~vue
<template>
  <article
    class="mx-auto flex max-w-md items-center gap-4 rounded-2xl bg-white p-6 shadow-lg ring-1 ring-black/5"
  >
    <img
      class="size-16 shrink-0 rounded-full object-cover"
      src="/avatar.jpg"
      alt="用户头像"
    />

    <div class="min-w-0">
      <h2 class="truncate text-lg font-semibold text-slate-950">
        execute233
      </h2>
      <p class="mt-1 truncate text-sm text-slate-500">
        AI Agent 与全栈开发
      </p>
    </div>
  </article>
</template>
~~~
