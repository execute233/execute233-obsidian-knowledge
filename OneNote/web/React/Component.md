---
title: React Component
tags: [react, component, hook]
aliases: []
---

# React Component

## 组件定义

一个组件就是首字母大写的函数，内部存放了组件的逻辑和视图 UI。渲染组件只需要把组件当标签书写：

```jsx
function Hello(props) {
  return <h1>Hello, {props.name}!</h1>
}

// 使用
<Hello name="张三" />
```

```jsx
// 也可以是箭头函数
const Hello = ({ name }) => <h1>Hello, {name}!</h1>
```

## useState

`useState` 是一个 React Hook 函数，允许向组件添加状态变量，影响组件的渲染：

```jsx
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      点击次数：{count}
    </button>
  )
}
```

### 修改状态的规则

- **状态不可变**：状态被认为是只读的，应该始终替换它而不是修改它。直接修改不能引发视图更新。
- 对于对象，应该 `set` 一个全新的对象来进行修改：

```jsx
const [user, setUser] = useState({ name: '张三', age: 18 })

// 正确：传一个新对象
setUser({ ...user, age: 19 })

// 错误：直接修改（不会触发更新）
user.age = 19
```

## 样式控制

### 行内样式

```jsx
function Box() {
  return <div style={{ color: 'red', fontSize: 18 }}>红色文字</div>
}
```

或者写成变量：

```jsx
const boxStyle = { color: 'red', fontSize: 18 }
return <div style={boxStyle}>红色文字</div>
```

### 类名控制

```jsx
function Button({ primary }) {
  // 根据条件拼接类名
  return <button className={`btn ${primary ? 'btn-primary' : ''}`}>按钮</button>
}
```

### classnames 优化类名控制

```bash
npm install classnames
```

```jsx
import classNames from 'classnames'

function Button({ primary, disabled }) {
  return (
    <button
      className={classNames('btn', { 'btn-primary': primary, disabled })}
    >
      按钮
    </button>
  )
}
```

## lodash 实用工具库

参考：[Lodash 中文文档](https://www.lodashjs.com/)

## 受控表单绑定

使用 React 组件的 `useState` 控制表单的状态。不同于 Vue 的双向绑定，两个数据流都要手动指定：

```jsx
function Form() {
  const [value, setValue] = useState('')

  return (
    <input
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  )
}
```

## 获取 DOM

使用 `useRef` 钩子函数：

```jsx
import { useRef } from 'react'

function FocusInput() {
  const inputRef = useRef(null)

  return (
    <>
      <input ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>聚焦</button>
    </>
  )
}
```

## uuid 实用库

```bash
npm install uuid
```

```jsx
import { v4 as uuid } from 'uuid'

const id = uuid()
```

当成可执行的方法调用即可，会生成随机的 UUID。

## dayjs 日期处理

```bash
npm install dayjs
```

参考：[Day.js 解析文档](https://day.js.org/docs/zh-CN/parse/parse)

## 组件通信

### 父传子

父组件在子组件标签上绑定属性，子组件通过 `props` 接收：

```jsx
function Child({ name, age }) {
  return <p>{name} - {age}</p>
}

function Parent() {
  return <Child name="张三" age={18} />
}
```

> `props` 可传递任意类型数据，但子组件只读 props 数据，不能直接修改，只能由父组件修改。

### 父传子 — props.children

当内容嵌在子组件标签时，父组件会自动在 `props.children` 中接收：

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>
}

<Card>
  <h1>标题</h1>
  <p>内容</p>
</Card>
```

### 子传父

在子组件中调用父组件中的函数并传递参数：

```jsx
function Child({ onAdd }) {
  return <button onClick={() => onAdd('hello')}>添加</button>
}

function Parent() {
  const handleAdd = (msg) => console.log(msg)

  return <Child onAdd={handleAdd} />
}
```

### 兄弟通信

使用「子传父 + 父传子」组合实现兄弟组件通信：子 A 通过回调把数据传给父，父再把数据传给子 B。

### Context 跨组件通信

1. 使用 `createContext()` 创建上下文对象
2. 在顶层组件用 `ctx.Provider` 提供数据
3. 在底层组件用 `useContext()` 钩子函数消费数据

```jsx
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext(null)

function App() {
  const [theme, setTheme] = useState('light')

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Toolbar />
    </ThemeContext.Provider>
  )
}

function Toolbar() {
  const { theme, setTheme } = useContext(ThemeContext)

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      当前：{theme}
    </button>
  )
}
```