---
title: Sass @extend
tags: [sass, @extend]
aliases: []
---

# Sass @extend

`@extend` 让一个选择器继承另一个选择器的样式规则。

```scss
.button-basic {
  border: none;
  padding: 15px 30px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
}

.button-report {
  @extend .button-basic;
  background-color: red;
}
```

编译结果会将 `.button-basic` 与 `.button-report` 合并到同一个规则集中，适合表示「变体」的继承关系。

> [!warning] 注意
> `@extend` 会跨选择器拼接 CSS，可能造成意料之外的覆盖；现代 Sass 推荐使用 `@use` 与 mixin 来组织可复用样式。