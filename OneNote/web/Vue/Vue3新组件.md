---
title: Vue3 新组件
tags: [vue, vue3, 组件, teleport, suspense]
aliases: []
---

# Vue3 新组件

## `<Teleport>`

`<Teleport>` 用于将子组件渲染到指定的 DOM 节点，常用于弹窗、Toast、全屏遮罩等需要脱离父组件布局的场景。

`to` 指定目标选择器，里面的内容会以指定标签为父节点渲染：

```html
<template>
  <button @click="open = true">打开弹窗</button>

  <Teleport to="body">
    <div v-if="open" class="modal">
      <p>这是弹窗内容</p>
      <button @click="open = false">关闭</button>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const open = ref(false)
</script>
```

> 即使 `<Teleport>` 写在深层组件里，最终也会被渲染到 `body` 下。

## `<Suspense>`

`<Suspense>` 用于包裹存在**异步 setup** 的子组件，并在等待期间显示加载状态。

提供两个插槽：

| 插槽 | 含义 |
| --- | --- |
| 默认插槽 | 异步子组件的实际内容 |
| `#fallback` | 加载中显示的占位内容 |

```html
<template>
  <Suspense>
    <AsyncUser />

    <template #fallback>
      <div>加载中...</div>
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

const AsyncUser = defineAsyncComponent(() => import('./User.vue'))
</script>
```

`<Suspense>` 还可以监听内部的 `resolve` / `reject` 事件做更细粒度的控制。