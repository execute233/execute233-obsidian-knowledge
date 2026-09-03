---
title: CSS 字体与文本
tags: [css, 字体, 文本]
aliases: [CSS 字体与文本]
---

# CSS 字体与文本

## 字体样式

### font-family

可以同时声明多个备选字体，浏览器按顺序匹配第一个可用的；字体名含空格需用引号。最后一般用通用族关键字兜底：

```css
font-family: 'Helvetica', 'Arial', sans-serif;
```

通用字体系列：

| 关键字 | 含义 |
| --- | --- |
| `serif` | 衬线字体（笔画末端有装饰，如 Times New Roman） |
| `sans-serif` | 无衬线字体（如 Arial），屏幕上更易读 |
| `monospace` | 等宽字体（每个字符同宽，如 Courier New） |
| `cursive` | 手写字体 |
| `fantasy` | 奇幻字体 |

### @font-face 自定义字体

需要使用本地或远程字体文件时，用 `@font-face` 声明后即可当作普通字体族使用：

```css
@font-face {
  font-family: genshin;
  src: url('./fonts/genshin.woff2');
}

.title {
  font-family: genshin, sans-serif;
}
```

### font-size

| 单位 | 说明 |
| --- | --- |
| `px` | 像素大小，浏览器默认 16px |
| `em` | 相对父元素字体大小（1em = 父元素 font-size） |
| `rem` | 相对根元素（html）字体大小 |
| 百分比 | 相对父元素，如 `100%` |

### font-weight

字重（粗细）：关键字 `lighter` / `normal` / `bold` / `bolder`，或数字 `100` ~ `900`（常规 `400`，加粗 `700`）。

### font-style

- `normal`：正常
- `italic`：斜体（使用字体内置的斜体字型）
- `oblique`：倾斜体（强制倾斜，可加角度，如 `oblique 30deg`）

### font 简写

```css
font: italic bold 16px/1.5 'Helvetica', sans-serif;
/*    样式   字重  大小/行高  字体族（必须放最后） */
```

## 文本样式

| 属性 | 说明 |
| --- | --- |
| `text-indent` | 首行缩进，常用 `em` 表示缩进几个字 |
| `text-align` | 对齐：`left` / `right` / `center` / `justify`（两端对齐） |
| `text-decoration` | 文本修饰（可复合颜色、样式、粗细） |
| `text-transform` | 大小写转换：`uppercase` / `lowercase` / `capitalize` |
| `line-height` | 行高，建议 `1.5` 或 `1.8`（无单位即倍数） |
| `letter-spacing` | 字符间距 |
| `word-spacing` | 单词间距 |
| `word-break` | 换行策略：`normal` 保留单词、`break-all` 强制拆词 |
| `text-wrap` | 控制如何换行 |
| `white-space` | 空格处理策略 |

### text-decoration 组合写法

```css
text-decoration: underline wavy red 2px;
/*        线条类型    样式  颜色  粗细  */
```

线条类型：`underline`（下划线）、`line-through`（删除线）、`overline`（上划线）。样式可选：`dashed`（虚线）、`wavy`（波浪线）、`dotted`（点线）、`double`（双实线）。

### white-space 取值

| 取值 | 说明 |
| --- | --- |
| `pre` | 保留全部空格与换行 |
| `pre-wrap` | 保留空格换行，但超出宽度会换行 |
| `pre-line` | 不保留空格序列，但保留源代码换行与 `<br>` |

## 颜色 color

```css
color: red;                    /* 关键字 */
color: rgb(255, 255, 255);     /* rgb */
color: #FFFFFF;                /* 16 进制 */
color: rgba(255, 255, 255, 1); /* 含 alpha 通道，1 不透明，越接近 0 越透明 */
color: #FFFFFFFF;              /* 16 进制含 alpha */
```

完整颜色表示法见 [[03-CSS颜色与背景]]。