---
title: 第 17 课：View Transitions、导航与脚本生命周期
tags: ["Astro", "frontend", "课程", "课程-17"]
aliases: ["第 17 课", "View Transitions、导航与脚本生命周期", "第 17 课：View Transitions、导航与脚本生命周期"]
---
# 第十七课：View Transitions、导航与脚本生命周期

### 17.1 启用 ClientRouter

把 ClientRouter 放在所有页面共享的 Layout 的 head 中：

~~~astro
---
import { ClientRouter } from 'astro:transitions';
---

<html lang="zh-CN">
  <head>
    <ClientRouter />
  </head>
  <body>
    <slot />
  </body>
</html>
~~~

这会让站内标准链接拥有客户端导航与 View Transition 能力。没有它时，Astro 仍是正常的多页网站。

官方依据：[View transitions](https://docs.astro.build/en/guides/view-transitions/)

### 17.2 元素过渡

两个页面中对应元素使用同一名称：

~~~astro
<img
  src={cover.src}
  alt=""
  transition:name={'cover-' + post.id}
  transition:animate="slide"
/>
~~~

内置动画包括 fade、initial、slide。动画只是增强，页面必须在无动画时仍可用。

### 17.3 保持状态

~~~astro
<AudioPlayer
  client:load
  transition:persist
/>
~~~

只要新页面也存在对应组件，旧 Island 可保留内部状态。也可让 video、audio 等原生元素继续播放。

不要滥用：

- 页面间的内容已经不同，却强行持久化；
- 让持久化掩盖真正应该进入 URL 或持久 store 的状态；
- 忽略不同页面 Props 更新。

默认情况下，持久 Island 保留状态，但会接收新 Props。若加 <code>transition:persist-props</code>，连旧 Props 也保留。

### 17.4 脚本生命周期

ClientRouter 不做完整页面刷新，因此旧的 <code>DOMContentLoaded</code> 思维可能失效。需要在每次 Astro 页面导航后初始化：

~~~astro
<script>
  function setupCopyButtons() {
    document.querySelectorAll<HTMLButtonElement>('[data-copy]').forEach((button) => {
      if (button.dataset.ready === 'true') return;
      button.dataset.ready = 'true';

      button.addEventListener('click', async () => {
        await navigator.clipboard.writeText(button.dataset.copy ?? '');
      });
    });
  }

  document.addEventListener('astro:page-load', setupCopyButtons);
</script>
~~~

<code>astro:page-load</code> 在首次加载和后续客户端导航完成时都会触发。

> [!important]
> 初始化函数要幂等。每次导航都运行时，不能重复绑定同一 DOM 元素。可以通过 data 标记、AbortController 或 Web Component 生命周期清理。

### 17.5 主题闪烁

主题类应在首次绘制和页面 swap 前及时应用。若使用 inline 脚本，监听 <code>astro:after-swap</code> 并同时首次执行。

### 17.6 Prefetch

Astro 支持预取可能即将访问的页面。预取会消耗网络流量，不应把所有链接都设置为激进预取。优先对高概率下一步、同源、成本可控的页面启用。

官方依据：[Prefetch](https://docs.astro.build/en/guides/prefetch/)

### 17.7 可访问性

- 尊重 <code>prefers-reduced-motion</code>；
- 页面 title 与主标题在导航后正确变化；
- 保留可见焦点；
- 不让动画阻碍键盘操作；
- 异步结果用 <code>aria-live</code>；
- 不用动画隐藏路由状态。
