---
title: 第 04 课：组件组合、Slots 与 Fragment
tags: ["Astro", "frontend", "课程", "课程-4"]
aliases: ["第 04 课", "组件组合、Slots 与 Fragment", "第 04 课：组件组合、Slots 与 Fragment"]
---
# 第四课：组件组合、Slots 与 Fragment

### 4.1 Props 传数据，Slots 传结构

| 需求 | 推荐 |
|---|---|
| 标题、状态、URL、尺寸 | Props |
| 一段任意 HTML | 默认 Slot |
| 页头操作区、页脚区 | 命名 Slot |
| 没传内容时显示占位 | Slot fallback |

~~~astro
<!-- src/components/Card.astro -->
---
interface Props {
  title: string;
}

const { title } = Astro.props;
---

<article class="card">
  <header>
    <h2>{title}</h2>
    <div class="actions">
      <slot name="actions" />
    </div>
  </header>

  <div class="content">
    <slot>
      <p>暂无内容</p>
    </slot>
  </div>
</article>
~~~

调用：

~~~astro
<Card title="Astro Islands">
  <a slot="actions" href="/edit">编辑</a>
  <p>只给需要交互的部分发送 JavaScript。</p>
</Card>
~~~

### 4.2 Fragment

向同一个命名 Slot 传多个同级节点，而不希望多出包装元素：

~~~astro
<Card title="文章">
  <Fragment slot="actions">
    <a href="/preview">预览</a>
    <button>收藏</button>
  </Fragment>

  <p>正文一</p>
  <p>正文二</p>
</Card>
~~~

命名 Slot 必须是组件的直接子级，不能隔着普通包装元素。

### 4.3 检查 Slot 是否存在

~~~astro
---
const hasAside = Astro.slots.has('aside');
---

<main class:list={{ 'with-aside': hasAside }}>
  <article><slot /></article>
  {hasAside && <aside><slot name="aside" /></aside>}
</main>
~~~

官方依据：[Components — Slots](https://docs.astro.build/en/basics/astro-components/#slots)
