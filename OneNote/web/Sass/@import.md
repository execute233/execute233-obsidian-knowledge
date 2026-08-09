---
title: Sass @import
tags: [sass, @import]
aliases: []
---

# Sass @import

可以使用 `@import` 导入外部的 `.scss` 文件：

```scss
@import 'variables';
@import 'mixins';
```

> [!tip] 注意
> 在较新版本的 Sass（`@use` / `@forward`）中，推荐使用 `@use` 替代 `@import` 来组织样式模块。