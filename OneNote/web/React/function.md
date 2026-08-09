---
title: React Hook (useEffect / 自定义 Hook)
tags: [react, hook, useeffect]
aliases: [React function]
---

# React Hook (useEffect / 自定义 Hook)

## useEffect

`useEffect` 是一个 Hook 函数，用来创建**不是由事件引起而是由渲染本身引起**的操作（副作用）。

```jsx
useEffect(() => {
  // 副作用逻辑
}, [])
```

- 参数 1：副作用函数，放要执行的操作
- 参数 2（可选）：依赖项数组，影响副作用函数的执行时机，为空时只在组件渲染完毕后执行一次

### 依赖项与执行时机

| 依赖项 | 副作用函数执行时机 |
| --- | --- |
| 没有依赖项 | 组件初始渲染 + 任意组件更新时 |
| 空数组依赖 | 只在初始渲染时执行一次 |
| 添加特定依赖项（如 `useState` 返回的变量） | 初始渲染 + 该依赖项变化时执行 |

```jsx
useEffect(() => {
  console.log('count 变了：', count)
}, [count])
```

### 清除副作用

在组件卸载时执行的清理逻辑，只要 `return` 一个函数即可：

```jsx
useEffect(() => {
  const timer = setInterval(() => console.log('tick'), 1000)

  return () => clearInterval(timer)   // 卸载时清理
}, [])
```

## 自定义 Hook

以 `use` 打头的函数，自己实现逻辑的封装与复用。

通用思路：

1. 声明一个以 `use` 打头的函数
2. 在函数体内封装可复用的逻辑
3. 把组件中用到的状态或者回调 `return` 出去
4. 在哪个组件中要用到这个逻辑，就执行这个函数，解构出状态和回调

```jsx
import { useState, useEffect } from 'react'

function useWindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight })

  useEffect(() => {
    const onResize = () => setSize({ width: window.innerWidth, height: window.innerHeight })
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  return size
}

// 使用
function MyComponent() {
  const { width, height } = useWindowSize()
  return <p>{width} x {height}</p>
}
```

## React Hooks 使用规则

- 只能在**组件中**或者其他**自定义 Hook 函数**中调用
- 只能在组件的**顶层**调用，不能嵌套在 `if`、`for`、其他函数中