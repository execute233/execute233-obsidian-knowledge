---
title: CSS 颜色与背景
tags: [css, 颜色, 背景]
aliases: []
---

# CSS 颜色与背景

## 颜色表示法

| 写法 | 示例 | 说明 |
| --- | --- | --- |
| 颜色关键字 | `red`、`white` | 预定义颜色名 |
| 十六进制 | `#FF0000`、`#FFF` | `#RRGGBB`，可简写为 3 位 |
| 十六进制含 alpha | `#FFFFFFFF` | `#RRGGBBAA` |
| RGB | `rgb(255, 0, 0)` | 红绿蓝三通道，各 0~255 |
| RGBA | `rgba(255, 0, 0, 0.5)` | 多一个 alpha 透明度，0 透明 ~ 1 不透明 |

## 背景属性

```css
background-color: #f5f5f5;            /* 背景颜色 */
background-image: url(./bg.png);       /* 背景图片 */
background-repeat: no-repeat;          /* 是否平铺：repeat / repeat-x / repeat-y / no-repeat */
background-position: right top;        /* 背景位置 */
background-attachment: fixed;          /* 背景是否随页面滚动 */
background-size: cover;                /* 背景尺寸 */
```

### background-size 取值

| 取值 | 含义 |
| --- | --- |
| `auto`（默认） | 保持原图尺寸 |
| `cover` | 保持高宽比完全覆盖背景（可能裁切） |
| `contain` | 保持高宽比完整放入背景区域内（可能留白） |
| `200px 100px` | 固定宽高 |

### 简写属性

`background` 可以把多个属性合并为一条，顺序为：颜色 → 图片 → 重复 → 附件 → 位置（不必全部写出）：

```css
body {
  background: #fff url(./bg.png) no-repeat right top;
}
```

背景图片默认平铺，常需配合 `no-repeat` 与 `background-position` 定位。

## 渐变 Gradients

CSS3 渐变由浏览器生成，不需要图片资源，支持线性与径向两种。

### 线性渐变 linear-gradient

```css
background-image: linear-gradient(#e66465, #9198e5);       /* 默认从上到下 */
background-image: linear-gradient(to right, red, yellow);   /* 方向：to bottom / to top / to right / to left */
background-image: linear-gradient(to bottom right, red, yellow);  /* 对角 */
background-image: linear-gradient(45deg, red, yellow, green);     /* 角度 + 多颜色节点 */
background-image: linear-gradient(to right, rgba(255,0,0,0), rgba(255,0,0,1)); /* 透明度过渡 */
```

### 径向渐变 radial-gradient

由中心向四周扩散：

```css
background-image: radial-gradient(red, yellow, green);         /* 默认椭圆、中心点 */
background-image: radial-gradient(circle, red, yellow, green); /* 圆形 */
background-image: radial-gradient(red 5%, yellow 15%, green 60%); /* 不均匀分布 */
```

## 滤镜 filter

| 函数 | 作用 |
| --- | --- |
| `blur(5px)` | 高斯模糊 |
| `brightness(1.5)` | 亮度（0~∞，1 为原图） |
| `contrast(2)` | 对比度 |
| `grayscale(1)` | 灰度（0~1，1 为完全灰） |
| `opacity(0.5)` | 透明度 |
| `saturate(2)` | 饱和度 |

```css
img {
  filter: grayscale(1);
}
```

`backdrop-filter` 只对元素**后方背景**生效，元素自身内容不受影响（毛玻璃效果）。