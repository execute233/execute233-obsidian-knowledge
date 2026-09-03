---
title: Flex 弹性盒子
tags: [css, 布局, flex]
aliases: []
---

# Flex 弹性盒子

Flex 是 CSS3 的一维布局模型，专注于控制单个方向（主轴）上的排列。把容器设为 `display: flex` 后，其直接子元素自动变为弹性项目。

## 基础

```css
.flex {
  display: flex;
  gap: 10px;                  /* 盒子间的间隙 */
  flex-wrap: wrap;            /* 容纳不下时是否换行 */
  flex-direction: row;        /* 主轴方向 */
}
```

## 主轴与交叉轴

Flex 布局有两个轴：

- **主轴**：由 `flex-direction` 决定，项目沿主轴排列
- **交叉轴**：与主轴垂直的另一个轴

### flex-direction 主轴方向

| 取值 | 含义 |
| --- | --- |
| `row`（默认） | 水平，起点在左 |
| `row-reverse` | 水平，起点在右 |
| `column` | 垂直，起点在上 |
| `column-reverse` | 垂直，起点在下 |

## 对齐

- `justify-*`：**主轴**方向上的对齐
- `align-*`：**交叉轴**方向上的对齐

`content` 控制所有项目的整体对齐；`items` 是单个项目在单元格内的默认对齐；`self` 是单个项目的单独对齐。

```css
.flex {
  justify-content: center;   /* 主轴居中 */
  align-items: center;       /* 交叉轴居中（常用于垂直居中） */
}
```

## 弹性项目属性

```css
.item {
  flex-grow: 1;      /* 主轴剩余空间的瓜分比例；0 不放大 */
  flex-shrink: 1;    /* 空间不足时的收缩比例；0 保持原始大小 */
  flex-basis: auto;  /* 分配多余空间前占据的主轴空间 */
  flex: 1 1 auto;    /* grow / shrink / basis 的简写 */
  order: 0;          /* 排序，越小越靠前 */
}
```

### 常用简写

```css
.item {
  flex: 1;           /* flex: 1 1 0%，等分剩余空间 */
}
```

## 典型应用

### 水平垂直居中

```css
.box {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### 等分布局

```css
.container {
  display: flex;
}
.container > * {
  flex: 1;
}
```

### 圣杯式顶栏 + 内容

```css
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main {
  flex: 1;          /* 中间内容撑满剩余高度 */
}
```

二维网格布局用 [[08-Grid网格]]。