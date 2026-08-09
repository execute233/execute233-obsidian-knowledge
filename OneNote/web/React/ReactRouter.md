---
title: React Router
tags: [react, router, 路由]
aliases: []
---

# React Router

## What is it?

一个路径 `path` 对应一个组件 `component`，当在浏览器中访问某个 `path` 时，对应的组件会在页面中渲染。

```jsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/about" element={<About />} />
  </Routes>
</BrowserRouter>
```

## 安装

```bash
npm install react-router-dom
```

## 快速开始

最简单的用法是在入口里直接创建：

```jsx
// index.jsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

const router = createBrowserRouter([
  { path: '/', element: <Home /> },
  { path: '/about', element: <About /> },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <RouterProvider router={router} />
)
```

实际项目中通常把 router 逻辑放在 `src/router/index.js`，再在 `src/index.js` 中使用它导出的内容：

```jsx
// src/router/index.jsx
import App from '@/App'
import Home from '@/pages/Home'

export const router = createBrowserRouter([
  { path: '/', element: <App />, children: [
    { path: 'home', element: <Home /> },
  ] },
])
```

## 路由导航

### 声明式导航

通过 `<Link>` 组件描述要跳转到哪里去。常见场景：后台管理系统的左侧菜单。

```jsx
import { Link } from 'react-router-dom'

<Link to="/about">关于我们</Link>
<Link to={`/user/${user.id}`}>用户详情</Link>
```

语法说明：通过 `to` 属性指定路由 `path`，组件会被渲染为 `<a>` 链接。如果需要传参，可以直接在 `to` 中通过字符串拼接参数。

### 编程式导航

通过 `useNavigate` 钩子得到导航方法，命令式进行跳转，适合登录后跳转等场景：

```jsx
import { useNavigate } from 'react-router-dom'

function LoginButton() {
  const navigate = useNavigate()

  const handleLogin = async () => {
    await login()
    navigate('/home')
  }

  return <button onClick={handleLogin}>登录</button>
}
```

## 路由导航传参

### searchParams 传参

```jsx
<Link to="/search?keyword=vue">搜索</Link>

// 组件内
import { useSearchParams } from 'react-router-dom'

const [params] = useSearchParams()
console.log(params.get('keyword'))
```

### params 传参

需要在 router 路径里写占位符，格式为 `:id`：

```jsx
{ path: '/user/:id', element: <User /> }

// 跳转
<Link to="/user/1">用户 1</Link>

// 组件内
import { useParams } from 'react-router-dom'

const { id } = useParams()
```

## 嵌套路由

1. 在父路由用 `children` 配置嵌套关系：

```jsx
{
  path: '/',
  element: <Layout />,
  children: [
    { path: 'home', element: <Home /> },
    { path: 'about', element: <About /> },
  ],
}
```

2. 在父组件里用 `<Outlet />` 配置二级路由渲染位置：

```jsx
import { Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div>
      <header>顶栏</header>
      <Outlet />     {/* 子路由渲染到这里 */}
    </div>
  )
}
```

默认二级路由：去掉 `path`，设置 `index` 属性为 `true`：

```jsx
{ index: true, element: <Home /> }
```

## 404 路由

使用 `*` 作为 path 即可：

```jsx
{ path: '*', element: <NotFound /> }
```

## 路由模式

```jsx
import { createBrowserRouter, createHashRouter } from 'react-router-dom'

// history 模式（推荐，需要服务端配合）
createBrowserRouter([...])

// hash 模式（路径带 #，无需服务端配置）
createHashRouter([...])
```