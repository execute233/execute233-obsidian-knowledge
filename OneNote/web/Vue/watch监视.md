---
title: Vue watch 监视
tags: [vue, watch, 响应式]
aliases: []
---

# Vue watch 监视

## 可监视的数据

`watch` 只能监测以下四种数据：

1. `ref` 定义的数据
2. `reactive` 定义的数据
3. 一个返回值的 getter 函数
4. 一个包含上述内容的数组

## 场景一：监视 ref 值

```html
<script setup lang="ts">
import { ref, watch } from 'vue'

const count = ref(0)

watch(count, (newValue, oldValue) => {
  console.log(`count: ${oldValue} -> ${newValue}`)
})
</script>
```

监视对象时还可以开启深度监视，并决定是否上来就触发一次：

```html
<script setup lang="ts">
import { ref, watch } from 'vue'

const user = ref({ name: '张三', age: 18 })

watch(
  user,
  (newValue, oldValue) => {
    console.log(newValue, oldValue)
  },
  { deep: true, immediate: true }
)
</script>
```

> `newValue` 与 `oldValue` 是否相同，取决于是否替换了整个 `.value`。

## 场景二：监视 reactive 定义的数据

```html
<script setup lang="ts">
import { reactive, watch } from 'vue'

const person = reactive({ name: '张三', age: 18 })

watch(person, (newValue, oldValue) => {
  console.log(newValue, oldValue)
})
</script>
```

要点：

- `reactive` 定义的对象不能直接整体替换，需要用 `Object.assign(target, source)`。
- 如果只想监听对象里某个基本类型值，使用 getter 函数。

```html
<script setup lang="ts">
import { reactive, watch } from 'vue'

const person = reactive({ name: '张三', age: 18 })

// 只监听 age 字段
watch(() => person.age, (newAge, oldAge) => {
  console.log(newAge, oldAge)
})
</script>
```

## watchEffect

`watchEffect` 会自动分析回调内使用到的响应式依赖，立即运行一次，并在依赖变化时重新执行：

```html
<script setup lang="ts">
import { ref, watchEffect } from 'vue'

const count = ref(0)

watchEffect(() => {
  console.log(`count is ${count.value}`)
})
</script>
```

## 模板 ref 属性

模板中类似 `class`，但更推荐使用 `ref` 获取元素引用：

```html
<template>
  <input ref="myInput" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const myInput = ref<HTMLInputElement | null>(null)

onMounted(() => {
  myInput.value?.focus()
})
</script>
```

样式中 `scoped` 标记表示样式只在当前组件生效：

```html
<style scoped>
.title { color: red; }
</style>
```