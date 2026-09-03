---
title: CSS 盒模型
tags: [css, 盒模型, 边框]
aliases: [CSS 盒子模型]
---

# CSS 盒模型

所有 HTML 元素都可以看作一个盒子，盒模型用于设计和布局。盒由 4 部分组成：

```
┌─ Margin 外边距 ─────────────────────────────┐
│ ┌─ Border 边框 ──────────────────────────┐ │
│ │ ┌─ Padding 内边距 ───────────────────┐ │ │
│ │ │ ┌─ Content 内容区域 ──────────────┐ │ │ │
│ │ │ │                                │ │ │ │
│ │ │ └────────────────────────────────┘ │ │ │
│ │ └─────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

- **Content**：内容区域，显示文本和图像
- **Padding**：内容周围的透明内边距
- **Border**：内边距和内容外的边框
- **Margin**：边框外、元素之间的透明外边距

## box-sizing

`width` / `height` 设置的是内容区域的尺寸。默认（`content-box`）下，元素**实际总尺寸 = width + padding + border + margin**，容易把盒子撑大。

| 取值 | 说明 |
| --- | --- |
| `content-box`（默认） | `width` / `height` 只包含 content，加 padding / border 会撑大盒子 |
| `border-box` | 边框和内边距算入盒子总宽高，`width` 即最终可见宽度 |

推荐全局启用 `border-box`，布局更直观：

```css
* {
  box-sizing: border-box;
}
```

## 行内 vs 块级宽高

- **行内元素**：盒子宽度由内部文本或其他行内元素的总宽度决定，高度由字体大小与行高决定。
- **块级元素**：盒子宽度默认直接占满整行，高度由内部元素高度总和决定。
- **行内块**（`inline-block`）：可设置宽高，但不独占一行。

## 边框 border

```css
border-width: 2px;
border-style: solid;   /* 实线 */
border-color: #333;
border-radius: 8px;    /* 圆角，使用 % 时按两边算半径，过大会变胶囊 */
```

`border-style` 可选值：`solid`（实线）、`dashed`（虚线）、`dotted`（点线）、`double`（双实线）。

`border-radius` 可写 4 个值，从左上顺时针排列；也可单独设置某一角，如 `border-top-left-radius`。

单边边框：

```css
border-top: 1px solid #000;
border-left: 2px dashed red;
border-bottom: 3px dotted #ccc;
border-right: 4px double #888;
```

## 内边距 padding

四值顺序为**上 右 下 左**（顺时针）：

```css
padding: 10px 20px 30px 40px;  /* 上 右 下 左 */
padding: 10px 20px;            /* 上下 10px，左右 20px */
padding: 10px;                 /* 四周 10px */
```

## 外边距 margin

控制元素与其他元素的距离，写法与 `padding` 相同：

```css
margin: 10px 20px;
```

注意：相邻块级元素的垂直外边距会**合并**（取较大者），水平不合并；`margin: 0 auto` 可使块级元素水平居中。

## 轮廓 outline

`outline` 绘制在边框之外，**不占据空间**，仅作装饰：

```css
outline: 2px solid blue;
outline-offset: 4px;   /* 与边框的距离 */
```

## 盒子阴影 box-shadow

```css
box-shadow: offset-x offset-y blur-radius spread-radius color;
box-shadow: 2px 2px 8px 2px rgba(0, 0, 0, 0.2);
```

## 尺寸约束

```css
max-width: 1200px;
min-width: 320px;
max-height: 800px;
min-height: 200px;
```

`width` / `height` 可用百分比，相对于父盒子。

## 溢出 overflow

内容超出盒子大小时控制滚动与裁切：

```css
overflow: auto;       /* 溢出自动出现滚动条 */
overflow: hidden;     /* 溢出隐藏 */
overflow: scroll;     /* 始终显示滚动条 */
overflow: clip;       /* 溢出裁切（不会创建滚动容器） */
```

## 用户代理样式

浏览器自带默认样式（如 `body` 自带 `margin`），可通过引入 `normalize.css` 等重置库统一，也可用 `* { margin: 0; padding: 0; }` 手动清零。