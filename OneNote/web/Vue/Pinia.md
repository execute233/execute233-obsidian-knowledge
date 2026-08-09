---
title: Vue Pinia
tags: [vue, pinia, 状态管理]
aliases: []
---

# Vue Pinia

Pinia 是 Vue 官方推荐的状态管理库，类似 Vuex 但更轻量、类型推断更友好。

## 安装与挂载

```bash
npm install pinia
```

在 `main.ts` 中挂载：

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
```

## 定义 Store

通常把每个 store 放在 `src/store/<name>.ts`，文件名与组件名一致：

```ts
// src/store/count.ts
import { defineStore } from 'pinia'

export const useCountStore = defineStore('count', {
  state: () => ({
    sum: 6,
  }),

  getters: {
    doubleSum: (state) => state.sum * 2,
  },

  actions: {
    increment() {
      this.sum += 1
    },
  },
})
```

## 在组件中使用

```html
<script setup lang="ts">
import { useCountStore } from '@/store/count'

const count = useCountStore()

// 直接读写 state（响应式）
count.sum      // 6
count.sum = 10 // 修改
count.increment()
</script>

<template>
  <div>{{ count.sum }}</div>
  <button @click="count.increment">+1</button>
</template>
```

> 注意：`reactive` 中的 `ref` 会自动解包。

## 修改数据的两种风格

```ts
// 1. 直接修改（state 视为可变）
count.sum += 1

// 2. 通过 $patch 批量修改
count.$patch({ sum: 10, name: 'vue' })

// 3. 通过 $patch 函数形式（推荐用于复杂更新）
count.$patch((state) => {
  state.sum += 1
})
```

## storeToRefs

将 store 解构为响应式，**只对 state / getters 包裹 ref**，方法保持不变：

```html
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCountStore } from '@/store/count'

const count = useCountStore()
const { sum, doubleSum } = storeToRefs(count)  // 响应式
const { increment } = count                    // 方法直接拿
</script>
```

## getters

对 state 进行派生，写在 `defineStore` 中；使用时不需要当作方法调用：

```ts
getters: {
  doubleSum: (state) => state.sum * 2,
}
```

```html
<div>{{ count.doubleSum }}</div>
```

## $subscribe

类似 `watch`，用于监听 store 中 state 的变化：

```html
<script setup lang="ts">
import { useCountStore } from '@/store/count'

const count = useCountStore()

count.$subscribe((mutation, state) => {
  console.log('变化:', mutation.type)
  console.log('当前 state:', state)
})
</script>
```

## 组合式写法（Setup Store）

也可以在 `defineStore` 中传入一个 setup 函数，更接近 Composition API：

```ts
export const useCountStore = defineStore('count', () => {
  const sum = ref(6)

  const doubleSum = computed(() => sum.value * 2)
  const increment = () => { sum.value += 1 }

  return { sum, doubleSum, increment }
})
```

这种写法中：

- `ref` / `reactive` 会被自动解包，等价于 `state`。
- `computed` 等价于 `getters`。
- 普通函数等价于 `actions`。