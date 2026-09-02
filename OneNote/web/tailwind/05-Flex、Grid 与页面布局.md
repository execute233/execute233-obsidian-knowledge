---
title: 第 5 课：Flex、Grid 与页面布局
tags: [Tailwind, CSS, frontend, 课程-5]
aliases: ["第 5 课", "第 5 课：Flex、Grid 与页面布局"]
---

# 第五课：Flex、Grid 与页面布局

## 5.1 先选布局模型

| 场景 | 优先考虑 |
|---|---|
| 单行或单列排列、对齐、分配剩余空间 | Flexbox |
| 同时控制行和列 | Grid |
| 元素覆盖、角标、浮层 | position |
| 普通文档流 | block / inline |

Tailwind 不替你选择布局模型，它只是把 CSS 映射为短类名。

## 5.2 Flex 高频组合

水平居中并分隔：

~~~html
<header class="flex items-center justify-between gap-4">
  <div>Logo</div>
  <nav>...</nav>
</header>
~~~

移动端纵向、较大屏横向：

~~~html
<div class="flex flex-col gap-4 md:flex-row md:items-center">
  ...
</div>
~~~

固定侧栏与可收缩内容：

~~~html
<div class="flex min-h-dvh">
  <aside class="hidden w-64 shrink-0 border-r border-slate-200 lg:block">
    ...
  </aside>
  <main class="min-w-0 flex-1">
    ...
  </main>
</div>
~~~

需要记住的几个细节：

- <code>flex-1</code> 常用于取得剩余空间。
- <code>shrink-0</code> 防止图标、头像、侧栏被压缩。
- <code>min-w-0</code> 允许内容区真正收缩。
- 优先用 <code>gap-*</code> 表达子元素间距，通常比给每个子项加 margin 更稳定。

## 5.3 Grid 高频组合

固定列数：

~~~html
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-4">
  ...
</div>
~~~

十二列仪表盘：

~~~html
<div class="grid grid-cols-12 gap-6">
  <section class="col-span-12 lg:col-span-8">主内容</section>
  <aside class="col-span-12 lg:col-span-4">辅助内容</aside>
</div>
~~~

自适应卡片，不依赖固定断点：

~~~html
<div class="grid grid-cols-[repeat(auto-fit,minmax(16rem,1fr))] gap-6">
  ...
</div>
~~~

最后一种写法使用任意值直接表达原生 Grid，适合真正由可用空间驱动的列表。

## 5.4 position、inset 与层级

角标：

~~~html
<div class="relative">
  <img class="rounded-xl" src="..." alt="..." />
  <span
    class="
      absolute top-3 right-3
      rounded-full bg-red-600 px-2 py-1 text-xs font-bold text-white
    "
  >
    NEW
  </span>
</div>
~~~

全屏浮层：

~~~html
<div class="fixed inset-0 z-50 grid place-items-center bg-black/50 p-4">
  <div class="w-full max-w-lg rounded-2xl bg-white p-6">...</div>
</div>
~~~

<code>inset-0</code> 同时设置四个方向为 0；<code>z-50</code> 只在正确的 stacking context 中有效。若 z-index “不听话”，应检查父元素是否因 transform、opacity、isolation 等创建了新的 stacking context。

## 5.5 溢出、图片和比例

横向滚动表格：

~~~html
<div class="overflow-x-auto">
  <table class="min-w-full">...</table>
</div>
~~~

固定比例封面：

~~~html
<img class="aspect-video w-full rounded-xl object-cover" src="..." alt="..." />
~~~

滚动容器：

~~~html
<section class="max-h-[70dvh] overflow-y-auto overscroll-contain">
  ...
</section>
~~~

## 5.6 应用外壳

~~~vue
<template>
  <div class="min-h-dvh bg-slate-50 text-slate-950">
    <div class="flex min-h-dvh">
      <aside
        class="
          hidden w-64 shrink-0 border-r border-slate-200 bg-white
          lg:block
        "
      >
        <div class="sticky top-0 p-6">
          <p class="text-lg font-bold">Learning Hub</p>
        </div>
      </aside>

      <div class="min-w-0 flex-1">
        <header
          class="
            sticky top-0 z-10
            flex h-16 items-center justify-between
            border-b border-slate-200 bg-white/85 px-4 backdrop-blur
            sm:px-6 lg:px-8
          "
        >
          <h1 class="truncate font-semibold">Tailwind 课程</h1>
          <button class="rounded-lg border border-slate-300 px-3 py-2">
            菜单
          </button>
        </header>

        <main class="mx-auto max-w-7xl p-4 sm:p-6 lg:p-8">
          <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
            <section class="xl:col-span-2">主区域</section>
            <aside>侧栏</aside>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>
~~~
