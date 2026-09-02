---
title: 第 7 课：状态与结构 variants
tags: [Tailwind, CSS, frontend, 课程-7]
aliases: ["第 7 课", "第 7 课：状态与结构 variants"]
---

# 第七课：状态与结构 variants

## 7.1 基本交互状态

~~~html
<button
  class="
    rounded-lg bg-sky-600 px-4 py-2 font-semibold text-white
    hover:bg-sky-700
    active:bg-sky-800
    focus-visible:outline-2 focus-visible:outline-offset-2
    focus-visible:outline-sky-600
    disabled:cursor-not-allowed disabled:opacity-50
  "
>
  保存
</button>
~~~

常见状态：

| variant | 对应意图 |
|---|---|
| <code>hover:</code> | 指针悬停 |
| <code>focus:</code> | 元素获得焦点 |
| <code>focus-visible:</code> | 浏览器判断应显示焦点提示 |
| <code>active:</code> | 正在激活 |
| <code>disabled:</code> | 表单控件不可用 |
| <code>checked:</code> | checkbox/radio 被选中 |
| <code>invalid:</code> | 表单验证失败 |
| <code>placeholder-shown:</code> | placeholder 正显示 |
| <code>open:</code> | details、dialog 或 popover 打开 |

v4 的 <code>hover:</code> 默认放在 <code>@media (hover: hover)</code> 中，因此只在主要输入设备真的支持 hover 时触发。不要依赖“触摸一下触发 hover”来完成关键功能。来源：[v4 Upgrade guide](https://tailwindcss.com/docs/upgrade-guide#hover-styles-on-mobile)。

## 7.2 结构状态

~~~html
<ul>
  <li class="border-b py-3 first:pt-0 last:border-b-0 last:pb-0">...</li>
  <li class="border-b py-3 first:pt-0 last:border-b-0 last:pb-0">...</li>
</ul>
~~~

表格斑马纹：

~~~html
<tr class="odd:bg-white even:bg-slate-50">...</tr>
~~~

空状态：

~~~html
<div class="empty:hidden">...</div>
~~~

## 7.3 group：由父元素状态影响子元素

~~~html
<a
  href="#"
  class="group block rounded-xl p-5 hover:bg-sky-600"
>
  <h3 class="font-semibold text-slate-950 group-hover:text-white">
    新建项目
  </h3>
  <p class="mt-1 text-sm text-slate-600 group-hover:text-sky-100">
    从模板开始创建。
  </p>
</a>
~~~

嵌套 group 时可以命名：

~~~html
<div class="group/card">
  <button class="group/action">
    <span class="group-hover/action:underline">操作</span>
  </button>
  <p class="group-hover/card:text-sky-700">卡片说明</p>
</div>
~~~

## 7.4 peer：由同级表单状态影响后续元素

~~~html
<label class="block">
  <span class="text-sm font-medium">邮箱</span>
  <input
    type="email"
    class="
      peer mt-2 w-full rounded-lg border border-slate-300 px-3 py-2
      invalid:border-red-500
    "
  />
  <span class="mt-1 hidden text-sm text-red-600 peer-invalid:block">
    请输入有效邮箱。
  </span>
</label>
~~~

<code>peer</code> 基于 CSS 后续同级选择器，因此目标通常必须写在 peer 元素之后，不能反向影响前面的兄弟节点。

## 7.5 has、data 与 aria

父元素中包含 checked 控件时：

~~~html
<label
  class="
    flex items-center gap-3 rounded-xl border p-4
    has-checked:border-sky-600 has-checked:bg-sky-50
  "
>
  <input type="radio" name="plan" class="accent-sky-600" />
  <span>Pro 计划</span>
</label>
~~~

根据 data attribute：

~~~html
<button data-active class="text-slate-500 data-active:text-sky-700">
  概览
</button>
~~~

根据 ARIA：

~~~html
<button
  aria-expanded="false"
  class="rounded-lg px-3 py-2 aria-expanded:bg-slate-100"
>
  菜单
</button>
~~~

ARIA 不是为了“触发 CSS”才添加的。它首先应准确表达可访问状态，Tailwind 只是复用这个真实状态。

## 7.6 任意 variant 和后代

你不控制 Markdown 或第三方 HTML 时：

~~~html
<article
  class="
    [&_h2]:mt-10 [&_h2]:text-2xl [&_h2]:font-bold
    [&_p]:mt-4 [&_p]:text-slate-700
    [&_a]:text-sky-700 [&_a]:underline
  "
>
  ...
</article>
~~~

<code>&</code> 表示当前元素，下划线代表选择器中的空格。复杂到难以阅读时，应转为清晰的自定义 CSS。

## 7.7 用户环境 variants

~~~html
<div class="transition motion-reduce:transition-none"></div>
<p class="text-slate-500 contrast-more:text-slate-950"></p>
<input class="appearance-none forced-colors:appearance-auto" />
<button class="p-2 pointer-coarse:p-3">触屏上扩大点击区域</button>
~~~

参考[官方状态 variants 文档](https://tailwindcss.com/docs/hover-focus-and-other-states)。
