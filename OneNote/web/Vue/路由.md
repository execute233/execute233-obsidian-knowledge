---
title: Vue 路由
tags: [vue, vue-router, 路由]
aliases: []
---

# Vue 路由

## 安装与项目结构

```bash
npm i vue-router
```

约定：路由文件放在 `src/router` 目录，可创建 `index.ts`：

```ts
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: () => import('@/pages/About.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

然后在 `main.ts` 中加载路由：

```ts
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

一般约定：路由主键放在 `pages` 或 `views` 文件夹，通用组件放在 `components` 文件夹。

## 路由器的工作模式

| 模式 | 创建函数 | 说明 |
| --- | --- | --- |
| `history` | `createWebHistory()` | 路径中不带 `#`，更接近传统 URL |
| `hash` | `createWebHashHistory()` | 路径中带 `#`，无需服务端配合 |

## `to` 的两种写法

```html
<!-- 字符串 -->
<RouterLink to="/home">首页</RouterLink>

<!-- 对象 -->
<RouterLink :to="{ path: '/about' }">关于</RouterLink>
<RouterLink :to="{ name: 'home' }">首页</RouterLink>
```

## 命名路由

给路由起一个名字，便于 `to` 通过 `name` 跳转：

```ts
const routes = [
  { path: '/', name: 'home', component: Home },
]
```

```html
<RouterLink :to="{ name: 'home' }">首页</RouterLink>
```

## 嵌套路由

在子页面里再嵌套一个页面：

```ts
const routes = [
  {
    path: '/user',
    component: UserLayout,
    children: [
      { path: 'profile', component: UserProfile },
      { path: 'settings', component: UserSettings },
    ],
  },
]
```

父组件用 `<RouterView />` 渲染子路由。

## query 参数

直接在 `to` 里写 `query` 即可：

```html
<RouterLink :to="{ path: '/search', query: { keyword: 'vue' } }">搜索</RouterLink>
```

子路由中获取：

```ts
import { useRoute } from 'vue-router'

const route = useRoute()
console.log(route.query.keyword)
```

## params 参数

需要在路由里写占位（占位符格式为 `:name`）：

```ts
const routes = [
  { path: '/user/:id', name: 'user', component: User },
]
```

> 注意：用对象写法传 `params` 时必须使用 `name`，不能用 `path`。

```html
<RouterLink :to="{ name: 'user', params: { id: 1 } }">用户 1</RouterLink>
```

## props 配置

**第一种方式**：把 `params` 直接作为 `props` 传给路由组件。

```ts
{ path: '/user/:id', component: User, props: true }
```

```html
<script setup lang="ts">
defineProps<{ id: string }>()
</script>
```

**第二种方式**：自定义 `props` 函数返回对象：

```ts
{
  path: '/user/:id',
  component: User,
  props: route => ({ id: route.params.id, role: 'guest' }),
}
```

## `replace` 属性

`<RouterLink>` 默认是 `push`，加上 `replace` 后会替换当前历史记录：

```html
<RouterLink to="/home" replace>首页（replace）</RouterLink>
```

## 编程式导航

通过 `useRouter()` 拿到路由实例后命令式跳转：

```ts
import { useRouter } from 'vue-router'

const router = useRouter()

router.push('/home')
router.push({ name: 'home' })
router.replace('/home')
router.go(-1)
```

## 路由重定向

```ts
const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home },
]
```