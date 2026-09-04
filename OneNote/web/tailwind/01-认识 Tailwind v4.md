---
title: 认识 Tailwind v4
tags: [Tailwind, CSS, frontend]
aliases: ["认识 Tailwind v4"]
---

# 认识 Tailwind v4

## 1.1 Tailwind 到底是什么

Tailwind 是一个 utility-first CSS framework。你在模板中组合单一职责的类名，构建工具扫描源码，再只生成被识别到的 CSS。最终产物是普通静态 CSS，浏览器端没有 Tailwind runtime。[官方核心概念](https://tailwindcss.com/docs/styling-with-utility-classes)和[安装文档](https://tailwindcss.com/docs/installation/using-vite)都以这个模型为基础。

传统 CSS：

~~~html
<button class="submit-button">保存</button>
~~~

~~~css
.submit-button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background: #0284c7;
  color: white;
  font-weight: 600;
}

.submit-button:hover {
  background: #0369a1;
}
~~~

Tailwind：

~~~html
<button
  class="rounded-lg bg-sky-600 px-4 py-2 font-semibold text-white hover:bg-sky-700"
>
  保存
</button>
~~~

二者最终都在写 CSS。Tailwind 改变的是样式的组织方式：

| 问题 | 传统 CSS 常见做法 | Tailwind 常见做法 |
|---|---|---|
| 给样式命名 | 创建语义类名 | 组合单用途 utility |
| 约束取值 | 团队约定或变量 | theme variables 驱动的统一尺度 |
| 状态 | 编写选择器 | <code>hover:</code>、<code>focus-visible:</code> |
| 响应式 | 编写媒体查询 | <code>md:</code>、<code>max-lg:</code> |
| 复用 UI | CSS 类或模板 | 优先封装 Vue 组件 |
| 特殊值 | 自定义声明 | 任意值、CSS 变量或自定义 CSS |

## 1.2 Tailwind 不等于内联样式

utility 和 <code>style</code> 属性看起来都贴近元素，但 utility 仍有几个关键能力：

- 它从设计系统的有限取值中选择，例如 <code>p-4</code>、<code>text-lg</code>。
- 它可以表达伪类、媒体查询和复杂选择器，例如 <code>hover:</code>、<code>md:</code>、<code>group-hover:</code>。
- 同一个 utility 会被多个元素复用，最终 CSS 不必随页面元素数量线性增长。
- 它在构建时生成，无需把框架运行时代码发到浏览器。

动态值来自数据库或 API 时，普通内联样式仍然合理：

~~~vue
<script setup lang="ts">
defineProps<{
  accent: string
}>()
</script>

<template>
  <button
    :style="{ '--accent': accent }"
    class="rounded-lg bg-(--accent) px-4 py-2 text-white"
  >
    动态品牌色
  </button>
</template>
~~~

这里让 Vue 提供运行时 CSS 变量，让 Tailwind 负责布局、状态和固定视觉规则。

## 1.3 读懂一个完整类名

~~~text
dark:md:hover:bg-sky-700/80!
~~~

从右向左拆解：

| 片段 | 含义 |
|---|---|
| <code>bg-sky-700</code> | 设置背景色 |
| <code>/80</code> | 颜色使用 80% 不透明度 |
| <code>hover:</code> | 支持 hover 且元素正被悬停 |
| <code>md:</code> | 视口宽度达到 md 断点 |
| <code>dark:</code> | dark variant 生效 |
| <code>!</code> | v4 写法：将 important 修饰符放在类名末尾 |

通常不该写得这么复杂，但你要能读懂它。variant 可以堆叠，格式始终是：

~~~text
条件:条件:utility
~~~

## 1.4 v4 的核心变化

Tailwind v4 在 2025-01-22 发布，官方将其描述为一次重写。入门时最重要的变化是：

- 一行 <code>@import "tailwindcss";</code> 完成所有引入。
- 默认自动检测源码，不再要求先写 <code>content</code> 数组。
- 通过 <code>@theme</code> 在 CSS 中配置设计令牌。
- 提供第一方 <code>@tailwindcss/vite</code> 插件。
- 内置 CSS import 处理和 vendor prefixing。
- 主题值同时暴露为原生 CSS variables。
- container queries 进入核心，无需旧插件。
- spacing 等很多 utility 能从统一尺度动态推导。

来源：[Tailwind CSS v4.0 发布说明](https://tailwindcss.com/blog/tailwindcss-v4)。

## 1.5 编译过程

~~~text
Vue / HTML / TS / Astro 源码
          ↓
以纯文本方式扫描可能的类名
          ↓
识别合法 utility 与 variant
          ↓
只生成需要的 CSS
          ↓
Vite 输出静态 CSS
~~~

这解释了两个现象：

1. <code>bg-red-500</code> 能生成，是因为完整字符串出现在源码中。
2. <code>"bg-" + color + "-500"</code> 通常不能生成，因为完整类名从未出现在源码文本中。

源码检测详见[[13-源码检测、冲突与调试|源码检测、冲突与调试]]。

## 1.6 Preflight

导入 Tailwind 时，[Preflight](https://tailwindcss.com/docs/preflight) 会自动进入 base layer。它基于 modern-normalize，并包含一些有意的重置，例如：

- 移除标题、段落等元素的默认 margin。
- 将所有元素设为 <code>box-sizing: border-box</code>。
- 重置默认 border，使 <code>border</code> 能稳定表示实线 1px 边框。
- 图片和其他媒体默认成为 block 并限制最大宽度。

因此刚接入 Tailwind 后，原本“有默认字号和间距”的标题可能变得像普通文本。这不是 Tailwind 失效，而是你需要显式设计它。

> [!warning] 第三方组件的样式异常
> 地图、富文本编辑器等第三方 UI 可能依赖浏览器默认样式。先在 DevTools 中检查是否被 Preflight 命中，再在 <code>@layer base</code> 或组件作用域内有针对性地覆盖。
