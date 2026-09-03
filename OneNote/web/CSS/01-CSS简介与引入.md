---
title: CSS 简介与引入
tags: [css, 基础]
aliases: [CSS 基本]
---

# CSS 简介与引入

CSS（Cascading Style Sheets，层叠样式表）是用于描述 HTML 元素如何显示的语言，核心目的是把**内容**（HTML）与**表现**（样式）分离。

现代 CSS 已无版本号——不再有 CSS3/CSS4，W3C 改为按模块独立开发发布（如「CSS 颜色模块第五版」）。

## 基本语法

CSS 规则由「选择器」和「声明块」组成：

```css
选择器 {
  属性: 值;
  属性: 值;
}
```

- 每条声明以冒号分隔属性与值，以分号 `;` 结束
- 声明块用大括号 `{}` 括起来
- 属性与值之间**不要加空格**（如 `margin-left: 20px`）

示例：

```css
p {
  color: red;
  text-align: center;
}
```

### 注释

CSS 注释以 `/*` 开始、以 `*/` 结束，浏览器会忽略：

```css
/* 这是个注释 */
p {
  text-align: center; /* 注释也可以出现在行内 */
}
```

## 引入方式

CSS 有三种引入方式：

### 1. 行内样式（Inline）

直接写在标签的 `style` 属性中，只作用于单个元素，会损失样式表复用优势，慎用：

```html
<p style="color: red; margin-left: 20px">内容</p>
```

### 2. 内部样式（Internal）

通过 `<style>` 标签写在 HTML 的 `<head>` 中，适用于单文档特殊样式：

```html
<head>
  <style>
    hr { color: sienna; }
    p { margin-left: 20px; }
  </style>
</head>
```

### 3. 外部样式（External）

通过 `<link>` 引入独立的 `.css` 文件，可跨页面复用，**一个文件改变整个站点外观**：

```html
<head>
  <link rel="stylesheet" href="mystyle.css">
</head>
```

### @import 引入

在 CSS 文件内部也可以用 `@import` 引入其他 CSS：

```css
@import url("reset.css");
@import "./common.css";
```

## 多重样式与优先级

当同一个选择器在多个样式表中定义时，属性值按优先级取用。一般情况下：

```
行内样式 > 内部样式 > 外部样式 > 浏览器默认样式
```

注意：若外部样式表在内部样式的 `<style>` **之后**引入，则外部样式会覆盖内部样式的同名属性。更精确的优先级规则见 [[02-CSS选择器]]。