---
title: Grid 网格
tags: [css, 布局, grid]
aliases: []
---

# Grid 网格

Grid 是 CSS3 的二维布局模型，通过划分行和列，把元素（网格项）依次放入网格中，适合整体页面与卡片布局。

## 基础

默认网格只有一列，通过 `grid-template-columns` 与 `grid-template-rows` 设置行列尺寸：

```css
.grid {
  display: grid;
  grid-template-columns: 50px 50px 50px 50px;   /* 固定列宽 */
  grid-template-columns: 1fr 1fr 1fr 1fr;       /* 等分列宽 */
  grid-template-columns: repeat(4, 1fr);        /* 函数写法 */
  gap: 10px;                                     /* 格子间距 */
}
```

## 自适应列数

```css
.grid {
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
```

- `minmax(200px, 1fr)`：每列最窄不少于 200px，若还有剩余空间则等分拉伸
- `auto-fill`：在不换行的前提下尽可能多地往一行里塞入列

## 显式网格 vs 隐式网格

- **显式网格**：由 `grid-template-*` 定义的网格
- **隐式网格**：内容超出显式网格时，浏览器自动创建的新行 / 列
- `grid-auto-rows` / `grid-auto-columns`：规定自动生成格子的大小
- `grid-auto-flow`：规定网格项的排列方向（`row` / `column` / `dense`）

## 对齐

| 属性 | 作用 |
| --- | --- |
| `justify-items` | 每个网格项在行上的对齐 |
| `justify-content` | 整个网格在行上的对齐 |
| `align-items` | 每个网格项在列上的对齐 |
| `align-content` | 整个网格在列上的对齐 |

## 网格项属性

```css
.grid-item {
  grid-column: 1 / 3;     /* 从第 1 列开始到第 3 列结束 */
  grid-column: span 2;    /* 跨 2 列 */
  grid-column: 1 / -1;    /* 占满整行 */
  grid-row: 2 / 4;        /* 占第 2~4 行 */
  justify-self: center;   /* 单独控制行对齐 */
  align-self: center;     /* 单独控制列对齐 */
}
```

## 网格区域

给每个网格项起名字，父容器即可使用 `grid-template-areas` 排版：

```css
.layout {
  display: grid;
  grid-template-areas:
    'header header'
    'sidebar main'
    'footer footer';
  grid-template-columns: 200px 1fr;
  grid-template-rows: 60px 1fr 40px;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

效果上可以拼出类似管理后台的「顶栏 + 侧栏 + 内容 + 底栏」版面。

## Flex vs Grid 选择

- 一维排列（一行或一列、按钮组、导航条）→ [[07-Flex弹性盒子]]
- 二维布局（卡片网格、完整页面骨架）→ Grid