---
title: Sass @mixin 与 @include
tags: [sass, @mixin, @include]
aliases: []
---

# Sass @mixin 与 @include

`@mixin` 定义整个样式表中可重复使用的样式段，`@include` 把 mixin 引入到选择器中。

## 无参 mixin

```scss
@mixin important-text {
  color: red;
  font-size: 25px;
  font-weight: bold;
  border: 1px solid blue;
}

.selector {
  @include important-text;
}
```

## 带参数的 mixin

```scss
// 混入接收两个参数
@mixin bordered($color, $width) {
  border: $width solid $color;
}

.myArticle {
  @include bordered(blue, 1px);
}
```

## 可变参数 mixin

```scss
@mixin box-shadow($shadows...) {
  -moz-box-shadow: $shadows;
  -webkit-box-shadow: $shadows;
  box-shadow: $shadows;
}

.shadows {
  @include box-shadow(0px 4px 5px #666, 2px 6px 10px #999);
}
```