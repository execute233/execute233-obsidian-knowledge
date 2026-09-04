---
title: Vue 中的组件化
tags: [Tailwind, CSS, frontend]
aliases: ["Vue 中的组件化"]
---

# Vue 中的组件化

## 11.1 长 class 并不自动等于坏代码

Tailwind 把样式决策放回模板，所以 class 较长是正常现象。判断是否需要抽象，不要看字符数，而要看：

- 结构和样式是否跨文件重复。
- 这段 UI 是否有独立语义和行为。
- 修改时是否需要保持多个实例一致。
- 是否需要定义清晰的 props、slots 和 events。

官方建议在 React、Vue 等框架中优先用组件管理跨文件重复，而不是立刻把每组 utility 抽成 CSS 类。参考[Managing duplication](https://tailwindcss.com/docs/styling-with-utility-classes#managing-duplication)。

## 11.2 用完整静态字符串映射 props

错误做法：

~~~ts
const buttonClass = "bg-" + props.color + "-600"
~~~

扫描器看不到最终的 <code>bg-sky-600</code>，因而可能不生成 CSS。

正确做法：

~~~ts
const toneClasses = {
  primary: "bg-sky-600 text-white hover:bg-sky-700",
  danger: "bg-red-600 text-white hover:bg-red-700",
  neutral: "bg-white text-slate-900 ring-1 ring-slate-300 hover:bg-slate-50",
} as const
~~~

所有候选类名都以完整文本存在，且不同变体可以拥有不同的视觉逻辑。

## 11.3 BaseButton.vue

~~~vue
<script setup lang="ts">
import { computed } from "vue"

type Tone = "primary" | "danger" | "neutral"
type Size = "sm" | "md" | "lg"

const props = withDefaults(
  defineProps<{
    tone?: Tone
    size?: Size
    loading?: boolean
    disabled?: boolean
    type?: "button" | "submit" | "reset"
  }>(),
  {
    tone: "primary",
    size: "md",
    loading: false,
    disabled: false,
    type: "button",
  },
)

const baseClasses = [
  "inline-flex items-center justify-center gap-2 rounded-lg font-semibold",
  "transition-colors duration-200",
  "focus-visible:outline-2 focus-visible:outline-offset-2",
  "focus-visible:outline-sky-600",
  "disabled:cursor-not-allowed disabled:opacity-50",
  "motion-reduce:transition-none",
]

const toneClasses: Record<Tone, string> = {
  primary: "bg-sky-600 text-white hover:bg-sky-700 active:bg-sky-800",
  danger: "bg-red-600 text-white hover:bg-red-700 active:bg-red-800",
  neutral:
    "bg-white text-slate-900 ring-1 ring-slate-300 hover:bg-slate-50 active:bg-slate-100",
}

const sizeClasses: Record<Size, string> = {
  sm: "min-h-8 px-3 text-sm",
  md: "min-h-10 px-4 text-sm",
  lg: "min-h-12 px-5 text-base",
}

const classes = computed(() => [
  baseClasses,
  toneClasses[props.tone],
  sizeClasses[props.size],
])
</script>

<template>
  <button
    :type="type"
    :class="classes"
    :disabled="disabled || loading"
    :aria-busy="loading || undefined"
  >
    <span
      v-if="loading"
      class="size-4 animate-spin rounded-full border-2 border-current border-r-transparent"
      aria-hidden="true"
    />
    <slot />
  </button>
</template>
~~~

这个组件的关注点：

- 视觉变体通过受控 props 暴露。
- 所有 Tailwind 类名静态可检测。
- loading 同时影响视觉、disabled 和 <code>aria-busy</code>。
- 固定最小高度让触控目标更稳定。
- 用户仍然能通过 slot 提供内容。

## 11.4 避免无约束的 class 冲突

Vue 会合并组件根元素上的外部 class。如果调用方传入 <code>bg-red-500</code>，组件内部又有 <code>bg-sky-600</code>，谁生效不由 class 属性的书写先后简单决定。

优先方案：

1. 用 <code>tone</code>、<code>size</code>、<code>block</code> 等语义 props 暴露允许的变化。
2. 对布局位置让父容器负责，例如父级设置宽度或 wrapper。
3. 如果必须开放 class 覆盖，明确记录哪些区域允许覆盖，并用测试验证。
4. 不要把 important 当成组件 API。

## 11.5 Vue 的 class 数组与对象

~~~vue
<script setup lang="ts">
defineProps<{
  active: boolean
  disabled?: boolean
}>()
</script>

<template>
  <button
    :class="[
      'rounded-lg px-3 py-2 text-sm font-medium',
      active
        ? 'bg-sky-100 text-sky-800'
        : 'text-slate-600 hover:bg-slate-100',
      {
        'cursor-not-allowed opacity-50': disabled,
      },
    ]"
  >
    <slot />
  </button>
</template>
~~~

Vue 的动态绑定没有问题；问题只发生在你把类名拆碎后拼接。完整候选字符串依然存在于源码中。

## 11.6 scoped style 中的 @reference

直接在 Vue 的 <code>&lt;style scoped&gt;</code> 中使用自定义 theme token、<code>@apply</code> 或 <code>@variant</code> 时，该样式块是独立处理上下文。v4 提供 <code>@reference</code>，只引用主样式中的主题、custom utilities 和 variants，不重复输出 CSS：

~~~vue
<template>
  <div class="legacy-widget">
    <slot />
  </div>
</template>

<style scoped>
@reference "../style.css";

.legacy-widget {
  @apply rounded-card bg-surface p-6 text-content shadow-card;
}
</style>
~~~

若完全使用默认主题且无自定义项，可引用：

~~~css
@reference "tailwindcss";
~~~

来源：[Functions and directives：@reference](https://tailwindcss.com/docs/functions-and-directives#reference-directive)。

> [!tip] 优先模板 utility
> 普通 Vue 元素优先直接在 template 使用 utility。<code>@reference + @apply</code> 更适合必须写 CSS 的第三方结构、伪元素密集样式或迁移代码。
