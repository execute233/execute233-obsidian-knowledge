---
title: CSS 布局
tags: [css, 布局, 定位, 浮动]
aliases: [CSS 布局]
---

# CSS 布局

## display 显示类型

`display` 决定元素的盒类型，常用取值：

| 取值 | 含义 |
| --- | --- |
| `inline` | 行内元素，不独占一行，不可设宽高 |
| `block` | 块级元素，独占一行，可设宽高 |
| `inline-block` | 行内块，不换行但可设宽高 |
| `flex` | 弹性布局容器 |
| `grid` | 网格布局容器 |
| `none` | 不显示，且不占空间（区别于 `visibility: hidden`） |

`visibility` 控制可见性：`visible` 显示、`hidden` 隐藏（仍占空间）。

## position 定位

`position` 控制元素的定位方式，默认 `static`（正常文档流）。非 `static` 时可通过 `top` / `right` / `bottom` / `left` 调整位置。

| 取值         | 说明                                           |
| ---------- | -------------------------------------------- |
| `static`   | 默认，正常文档流，不受偏移属性影响                            |
| `relative` | 相对元素**自身原位置**偏移，不脱离文档流（原空间保留）；常作为绝对定位的容器块    |
| `absolute` | 脱离文档流，相对**最近的已定位祖先**（无则相对 html/body）定位       |
| `fixed`    | 脱离文档流，相对**浏览器视口**定位，滚动不移动                    |
| `sticky`   | 未达到阈值前表现如 relative，达到后表现如 fixed（需设置 top 等阈值） |

```css
.parent {
  position: relative;   /* 作为 absolute 子元素的定位参考 */
}
.child {
  position: absolute;
  top: 0;
  right: 0;
}
```

绝对/固定定位元素脱离文档流、不占空间，会与其他元素重叠。

## z-index 与层叠上下文

`z-index` 控制定位元素的堆叠顺序，数值越大越靠前：

```css
z-index: 999;
```

`z-index` 仅在同一个层叠上下文内比较。以下情况会创建新的层叠上下文：

- `position` 不为 `static` 且设置了 `z-index`
- `position: fixed`
- `position: sticky` 且处于粘滞状态
- 使用了 `filter` / `perspective` / `clip-path` / `isolation: isolate` / `will-change`
- 使用了 `transform`
- 使用了 `opacity`（非 1）

没有 `z-index` 时，后面定位的元素显示在前。

## float 浮动

使元素向左或向右移动，周围元素重新排列、环绕它：

```css
img {
  float: right;
}
```

- 浮动元素只能左右移动，会尽量靠到包含框或另一浮动框边缘
- 多个浮动元素有空间时会彼此相邻
- 浮动元素之后的元素会围绕它

### 清除浮动 clear

浮动会导致父元素高度塌陷、后续元素错位，用 `clear` 指定某侧不允许浮动元素：

```css
.clearfix {
  clear: both;
}
```

`clear` 取值：`left` / `right` / `both` / `none`。现代布局中多用 flex / grid 替代 float，但清除浮动仍是处理历史代码的必备技能。

## 水平 & 垂直对齐

常用对齐方式：

```css
/* 块级元素水平居中 */
.block {
  margin: 0 auto;
}

/* 行内元素水平居中 */
.parent {
  text-align: center;
}

/* 单行文本垂直居中：行高等于容器高度 */
.line {
  height: 50px;
  line-height: 50px;
}

/* 定位方式垂直水平居中 */
.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

## 块级格式化上下文 BFC

BFC 像一个「结界」，具有以下特性：

- 隔离的独立容器：BFC 内部元素的布局不会影响外部（如 margin 折叠）
- 垂直外边距合并：同一个 BFC 内相邻块级盒子的垂直外边距会合并
- 包含浮动元素：可解决因浮动元素导致父元素高度塌陷的问题
- 不与浮动元素重叠：可用 BFC 实现两栏或多栏布局

触发 BFC 的方式：

- 根元素 `<html>`
- 浮动元素（`float` 不为 `none`）
- 绝对定位元素（`position` 为 `absolute` 或 `fixed`）
- `display` 为 `inline-block` / `table-cell` / `table-caption` / `flex` / `inline-flex` / `grid` / `inline-grid`
- `overflow` 不为 `visible` 的块级元素（如 `hidden` / `auto` / `scroll`）

单方向布局用 [[07-Flex弹性盒子]]，二维布局用 [[08-Grid网格]]。