---
title: CSS 变量与嵌套
tags: [css, 变量, 嵌套]
aliases: []
---

# CSS 变量与嵌套

## CSS 自定义属性（变量）

自定义属性由 CSS 作者定义，可在整个文档中重复使用，解决大量重复值难以维护的问题，同时提供语义化命名（`--main-text-color` 比 `#00ff00` 更易理解）。

### 声明与获取

属性名以两个减号 `--` 开头，值可以是任何有效 CSS 值：

```css
:root {
  --main-bg-color: brown;
}

.one {
  background-color: var(--main-bg-color);
}
```

- 通常定义在 `:root` 伪类下，全文档可访问；也可按需限定作用域（选择器即作用域）。
- **自定义属性名大小写敏感**：`--my-color` 与 `--My-color` 是两个不同变量。

### 继承与备用值

自定义属性会继承：子元素未设置时使用父元素的值。

`var()` 可提供备用值，当变量未定义或无效时生效（**不是**浏览器兼容兜底）：

```css
.two {
  color: var(--my-var, red); /* --my-var 未定义时用 red */
}
```

### 无效变量

若 `var()` 代换出无效值，该属性不会报错，而是使用继承值或初始值：

```css
:root {
  --text-color: 16px;   /* 16px 不是 color 的合法值 */
}
p {
  color: var(--text-color); /* 结果为黑色（初始值），非语法错误 */
}
```

### JavaScript 读写

```js
element.style.getPropertyValue("--my-var");
getComputedStyle(element).getPropertyValue("--my-var");
element.style.setProperty("--my-var", jsVar + 4);
```

## CSS 原生嵌套

CSS 嵌套由浏览器直接解析（无需 Sass 等预处理器），使样式表更易读、更模块化，不再重复选择器。

### 子选择器

可以省略 `&` 或显式使用：

```css
parent {
  child { }      /* 等价于 parent child */
  & child { }    /* 显式写法，含义相同 */
}
```

### 组合选择器必须用 &

不带组合器时浏览器会自动在两个选择器间添加空格；组合选择器（同时匹配多个类）必须用 `&`：

```css
.a {
  .b { }   /* 等价于 .a .b（后代） */
  &.b { }  /* 等价于 .a.b（同时具备两个类） */
}
```

### 后附嵌套选择器（反转上下文）

`&` 可加在后方，使子元素根据父元素状态变化：

```css
.card {
  & h2 {
    color: slateblue;
    .featured & {   /* 等价于 :is(.card h2):is(.featured h2) */
      color: tomato;
    }
  }
}
```

### 拼接不可行

**不能**像 Sass 那样拼接字符串创建类名（如 `&__child`），嵌套选择器会被当作类型选择器导致规则无效：

```css
.component {
  &__child {}   /* 无效：CSS 嵌套不支持字符串拼接 */
}
```

### 优先级

嵌套选择器的优先级类似 `:is()`，取选择器列表中优先级最高的项。无效的嵌套规则整体被忽略，不影响父级及后续规则。