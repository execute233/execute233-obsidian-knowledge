---
title: 附录 C：自测题与答案
tags: [Tailwind, CSS, frontend]
aliases: ["附录 C：自测题与答案"]
---

# 附录 C：自测题与答案

## 概念题

1. Tailwind 为什么不等同于 inline style？
2. v4 的源码扫描器会执行 TypeScript 吗？
3. 为什么 <code>"bg-" + color + "-500"</code> 不可靠？
4. <code>sm:hidden</code> 是隐藏手机还是隐藏 640px 及以上？
5. <code>md:max-lg:grid</code> 表示什么范围？
6. viewport breakpoint 与 container query 分别回答什么问题？
7. <code>@theme</code> 与 <code>:root</code> 的关键差异是什么？
8. 为什么 Vue 组件比大量 <code>@apply</code> 更常作为复用边界？
9. v4 important modifier 写在哪里？
10. 为什么改变 class 属性中的先后顺序不一定解决冲突？
11. <code>group</code>、<code>peer</code>、<code>has</code> 分别观察什么关系？
12. 手动 dark mode 为什么需要 <code>@custom-variant</code>？
13. Vue scoped style 中使用自定义 <code>@apply</code> 为什么可能需要 <code>@reference</code>？
14. Preflight 为什么会让 h1 看起来像普通文本？
15. 什么时候任意值应升级为 token？

## 代码题

### 题 1：找错

~~~vue
<div :class="'text-' + (error ? 'red' : 'green') + '-600'">
  状态
</div>
~~~

### 题 2：改成 mobile-first

目标：手机单列，md 两列，xl 四列。

~~~html
<div class="md:grid-cols-2 xl:grid-cols-4">...</div>
~~~

### 题 3：实现卡片自身响应

目标：卡片容器小于 md 时纵向，达到容器 md 时横向；不得使用 viewport <code>md:</code>。

### 题 4：解释冲突

~~~html
<div class="flex grid">...</div>
~~~

为什么不能只把 <code>flex</code> 移到最后？

### 题 5：选择扩展方式

分别为以下需求选择任意值、<code>@theme</code>、<code>@utility</code>、普通 CSS：

1. 只在一个页面出现的 372px 宽度。
2. 全站品牌色。
3. 项目中反复使用的 content-visibility。
4. 不可修改 HTML 的第三方富文本结构。

<details>
<summary>展开参考答案</summary>

1. Utility 可以使用设计系统约束、伪类、媒体查询和复杂 variants，并由构建器复用生成 CSS；inline style 没有这些完整能力。
2. 不会。它把文件视为纯文本。
3. 完整候选类名没有出现在源码中。应把 prop 映射到完整静态字符串。
4. 隐藏 640px 及以上；无前缀才是手机基础规则。
5. 从 md 开始，到 lg 之前。
6. viewport 依据视口宽度；container query 依据组件所在容器宽度。
7. <code>@theme</code> 变量会影响 utility/variant API，并输出 CSS variables；普通 <code>:root</code> 变量只是一段运行时 CSS 数据。
8. Vue 组件能同时封装结构、样式、行为、类型与可访问性；<code>@apply</code> 只复用声明。
9. 类名末尾，例如 <code>bg-red-500!</code>。
10. 冲突取决于生成 CSS 的规则顺序、cascade layer 和 specificity，不由 HTML class token 顺序直接决定。
11. group 观察祖先状态；peer 观察前面的同级元素状态；has 根据元素是否包含匹配后代或条件。
12. 默认 dark variant 基于系统媒体查询；手动模式需要把它改成根 class 或 data attribute 选择器。
13. 独立 style 上下文不知道全局自定义 theme、utility 和 variant；<code>@reference</code> 无重复输出地提供这些信息。
14. Preflight 移除了用户代理样式的默认 margin、字号等依赖，要求设计者显式添加样式。
15. 多处重复、有稳定语义、需要全局联动或跨 CSS/JS 复用时。

代码题：

1. 改为两个完整候选：<code>:class="error ? 'text-red-600' : 'text-green-600'"</code>。
2. <code>class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4"</code>。
3. 外层 <code>@container</code>，卡片 <code>flex flex-col @md:flex-row</code>。
4. 删除冲突并用真实状态条件只选择 <code>flex</code> 或 <code>grid</code>。
5. 依次为任意值、<code>@theme</code>、<code>@utility</code>、普通 CSS。

</details>

---
