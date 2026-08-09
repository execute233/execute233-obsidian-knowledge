---
title: React JSX
tags: [react, jsx]
aliases: []
---

# React JSX

## What's JSX?

JSX = JavaScript + XML(HTML)，表示在 JS 代码中编写 HTML 模板结构，是 React 中编写 UI 模板的方式。

```jsx
const element = <h1>Hello, JSX!</h1>
```

## The Core

JSX 并不是标准的 JS 语法，它是 JS 的语法扩展。浏览器本身不能识别，需要通过解析工具（如 Babel / SWC）做解析之后才能在浏览器中运行。

## Use JS Expression In JSX

在 JSX 中可以通过大括号 `{}` 识别 JavaScript 中的表达式，包括变量、函数调用、方法调用等：

```jsx
const name = '张三'
const element = <h1>Hello, {name}!</h1>
```

## List Render

使用原生的 `map` 方法返回 `<li>` 即可。同 Vue 一样，也需要指定不重复的 `key`：

```jsx
function TodoList({ todos }) {
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  )
}
```

## Conditional Render

可以通过逻辑运算符 `&&`（条件渲染）或三元表达式 `?:` 实现条件渲染：

```jsx
function Greeting({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn && <p>欢迎回来！</p>}
      {isLoggedIn ? <User /> : <Guest />}
    </div>
  )
}
```

## Event Bind

`on + 事件名称 = {事件处理程序}`：

```jsx
<button onClick={handleClick}>点我</button>
```

如果要传递自定义参数，需要箭头函数写法：

```jsx
<button onClick={() => handleClick(id)}>删除</button>
```

需要自定义参数**和**事件对象：

```jsx
<button onClick={(e) => handleClick(id, e)}>查看</button>
```