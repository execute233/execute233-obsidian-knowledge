---
title: 第 09 课：Vue Islands 与 client:* 指令
tags: ["Astro", "frontend", "课程", "课程-9"]
aliases: ["第 09 课", "Vue Islands 与 client:* 指令", "第 09 课：Vue Islands 与 client:* 指令"]
---
# 第九课：Vue Islands 与 client:* 指令

### 9.1 安装 Vue

~~~bash
pnpm astro add vue
~~~

官方集成：[Astro Vue integration](https://docs.astro.build/en/guides/integrations-guide/vue/)

一个 Vue 搜索组件：

~~~vue
<!-- src/components/SearchBox.vue -->
<script setup lang="ts">
import { computed, ref } from 'vue';

interface Item {
  title: string;
  href: string;
}

const props = defineProps<{
  items: Item[];
}>();

const query = ref('');

const results = computed(() => {
  const keyword = query.value.trim().toLowerCase();
  if (!keyword) return props.items;

  return props.items.filter((item) =>
    item.title.toLowerCase().includes(keyword),
  );
});
</script>

<template>
  <section>
    <label>
      搜索文章
      <input v-model="query" type="search" />
    </label>

    <ul>
      <li v-for="item in results" :key="item.href">
        <a :href="item.href">{{ item.title }}</a>
      </li>
    </ul>
  </section>
</template>
~~~

在 Astro 页面中：

~~~astro
---
import SearchBox from '../components/SearchBox.vue';

const items = [
  { title: 'Astro Islands', href: '/blog/astro-islands' },
  { title: 'Tailwind v4', href: '/blog/tailwind-v4' },
];
---

<SearchBox items={items} client:visible />
~~~

### 9.2 五种 client 指令

| 指令 | 何时加载 / hydration | 适合 |
|---|---|---|
| <code>client:load</code> | 页面加载后尽快 | 首屏关键交互 |
| <code>client:idle</code> | 页面初始加载后浏览器空闲 | 低优先级按钮、非核心控件 |
| <code>client:visible</code> | 进入视口时 | 评论、图表、页面下方搜索 |
| <code>client:media</code> | 媒体查询匹配时 | 只在特定屏幕存在的交互 |
| <code>client:only="vue"</code> | 不做服务器渲染，只在客户端渲染 | 严重依赖浏览器 API 且无法 SSR |

~~~astro
<HeaderMenu client:load />
<AnalyticsPanel client:idle />
<Comments client:visible={{ rootMargin: '200px' }} />
<MobileNav client:media="(max-width: 48rem)" />
<MapEditor client:only="vue" />
~~~

官方依据：[Template directives — client directives](https://docs.astro.build/en/reference/directives-reference/#client-directives)

> [!important] 选择优先级
> 能用 HTML / CSS → 不发 JS；能用小脚本 → 不引入 Vue；必须状态化交互 → Vue Island；能延迟 → 不用 client:load。

### 9.3 没有 client:* 会怎样

~~~astro
<SearchBox items={items} />
~~~

Vue 会在构建时或服务器生成 HTML，但浏览器没有 Vue runtime，因此输入不会触发响应式过滤。这不是 bug，是 Astro 的默认行为。

### 9.4 Props 必须跨网络边界

传给 hydrated framework component 的 Props 需要可序列化。函数、服务器连接、数据库客户端不能作为 Props 发送到浏览器。

推荐：

~~~astro
<SearchBox
  items={posts.map((post) => ({
    title: post.data.title,
    href: '/blog/' + post.id,
  }))}
  client:visible
/>
~~~

不要把完整、敏感、用不到的数据交给 Island。

### 9.5 Islands 之间共享状态

优先考虑：

- URL query；
- localStorage；
- 自定义 DOM Event；
- Nano Stores 等外部小型 store；
- 把强耦合交互合并成同一个 Vue Island。

不要期待两个独立 Island 像同一棵 Vue 组件树那样自动共享 provide / inject。

### 9.6 常见误用

~~~astro
<!-- 不推荐：整页都变成客户端 Vue -->
<App client:only="vue" />
~~~

如果整站都这样写，Astro 的内容优先与零 JS 默认优势基本消失。此时应重新评估是否直接使用 Nuxt / Vue 更自然。
