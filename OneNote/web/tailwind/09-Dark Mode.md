---
title: 第 9 课：Dark Mode
tags: [Tailwind, CSS, frontend, 课程-9]
aliases: ["第 9 课", "第 9 课：Dark Mode"]
---

# 第九课：Dark Mode

## 9.1 默认行为

<code>dark:</code> 可以应用于任何 utility：

~~~html
<article class="bg-white text-slate-950 dark:bg-slate-900 dark:text-white">
  <p class="text-slate-600 dark:text-slate-300">正文</p>
</article>
~~~

默认情况下，dark variant 使用 <code>prefers-color-scheme</code>。如果只需要跟随系统，无需自定义。

## 9.2 手动切换

如果需要用户主动选择，在全局 CSS 中覆盖 dark variant：

~~~css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
~~~

当根元素带 <code>dark</code> class 时，所有 <code>dark:*</code> 生效：

~~~html
<html class="dark">
  ...
</html>
~~~

也可以选择 data attribute：

~~~css
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
~~~

来源：[Dark mode 官方文档](https://tailwindcss.com/docs/dark-mode)。

## 9.3 Vue 三态主题：light / dark / system

<code>src/composables/useTheme.ts</code>：

~~~ts
import { onBeforeUnmount, ref } from "vue"

export type Theme = "light" | "dark" | "system"

const STORAGE_KEY = "theme"

function getStoredTheme(): Theme {
  const value = localStorage.getItem(STORAGE_KEY)
  return value === "light" || value === "dark" ? value : "system"
}

const theme = ref<Theme>("system")
let media: MediaQueryList | undefined

function applyTheme(value: Theme) {
  const prefersDark =
    window.matchMedia("(prefers-color-scheme: dark)").matches

  document.documentElement.classList.toggle(
    "dark",
    value === "dark" || (value === "system" && prefersDark),
  )

  document.documentElement.style.colorScheme =
    value === "system" ? "light dark" : value
}

function setTheme(value: Theme) {
  theme.value = value

  if (value === "system") {
    localStorage.removeItem(STORAGE_KEY)
  } else {
    localStorage.setItem(STORAGE_KEY, value)
  }

  applyTheme(value)
}

function handleSystemChange() {
  if (theme.value === "system") {
    applyTheme("system")
  }
}

export function useTheme() {
  theme.value = getStoredTheme()
  media = window.matchMedia("(prefers-color-scheme: dark)")
  media.addEventListener("change", handleSystemChange)
  applyTheme(theme.value)

  onBeforeUnmount(() => {
    media?.removeEventListener("change", handleSystemChange)
  })

  return {
    theme,
    setTheme,
  }
}
~~~

主题选择器：

~~~vue
<script setup lang="ts">
import { useTheme, type Theme } from "./composables/useTheme"

const { theme, setTheme } = useTheme()

const options: Array<{ value: Theme; label: string }> = [
  { value: "light", label: "浅色" },
  { value: "dark", label: "深色" },
  { value: "system", label: "跟随系统" },
]
</script>

<template>
  <div class="inline-flex rounded-xl bg-slate-100 p-1 dark:bg-slate-800">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      :aria-pressed="theme === option.value"
      :class="[
        'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
        theme === option.value
          ? 'bg-white text-slate-950 shadow-sm dark:bg-slate-700 dark:text-white'
          : 'text-slate-600 hover:text-slate-950 dark:text-slate-300 dark:hover:text-white',
      ]"
      @click="setTheme(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>
~~~

上面所有 Tailwind 类名都是完整静态字符串，扫描器可以识别。

> [!note] SSR 提醒
> 该 composable 面向普通客户端 Vite 应用。若以后放进 Astro SSR、Nuxt 或其他服务端渲染环境，需要保护 <code>window</code>、<code>localStorage</code> 和 <code>document</code> 的访问，并尽量在服务器或页面 head 中提前决定主题。

## 9.4 避免首屏闪烁

应用 JS 挂载后才添加 <code>dark</code>，可能先显示浅色再闪到深色。将最短的主题初始化脚本放入页面 head，使它在首次绘制前同步执行：

~~~html
<script>
  const stored = localStorage.getItem("theme")
  const dark =
    stored === "dark" ||
    (stored === null &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)

  document.documentElement.classList.toggle("dark", dark)
</script>
~~~

真实项目还应根据 CSP 选择 nonce、外部脚本或服务端渲染 class。

## 9.5 深色模式不是机械反色

逐项考虑：

- 页面背景和表面层级。
- 主文字、次文字和禁用文字。
- 边框是否过亮。
- 阴影在深色背景上是否仍有意义。
- 品牌色在深色背景上的对比度。
- 表单、滚动条和浏览器原生控件的 <code>color-scheme</code>。
