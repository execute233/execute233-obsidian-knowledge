---
title: React Redux
tags: [react, redux, 状态管理]
aliases: []
---

# React Redux

Redux 是一个集中状态管理工具，类似于 Pinia。React 推荐使用 `@reduxjs/toolkit` 配合 `react-redux`。

## 安装

```bash
npm install @reduxjs/toolkit react-redux
```

## 一个使用 Redux Toolkit 的标准子 store

```ts
// store/modules/counter.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment(state) {
      state.value += 1
    },
    addBy(state, action: PayloadAction<number>) {
      state.value += action.payload
    },
  },
})

export const { increment, addBy } = counterSlice.actions
export default counterSlice.reducer
```

## 总根 store

```ts
// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './modules/counter'

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
})

export type RootState   = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

## 注入 Provider

使用 `react-redux` 内置的 `Provider` 把根 store 注入应用：

```jsx
import { Provider } from 'react-redux'
import { store } from './store'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Provider store={store}>
    <App />
  </Provider>
)
```

## 读取与修改 store

读取数据：使用 `useSelector`，把 store 的数据映射到组件中。

```jsx
import { useSelector } from 'react-redux'
import type { RootState } from './store'

function Counter() {
  const count = useSelector((state: RootState) => state.counter.value)
  return <p>{count}</p>
}
```

修改数据：使用 `useDispatch`，生成提交 action 的 dispatch 函数。

```jsx
import { useDispatch } from 'react-redux'
import { increment, addBy } from './store/modules/counter'

function Buttons() {
  const dispatch = useDispatch()

  return (
    <>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(addBy(5))}>+5</button>
    </>
  )
}
```

## action 传参

在 reducer 的同步修改方法中通过 `action.payload` 接收参数。调用 action creator 时传递的值会自动放在 `payload` 上：

```ts
addBy(state, action: PayloadAction<number>) {
  state.value += action.payload
}
```

## 异步操作

借助 Redux Toolkit 自带的 `createAsyncThunk` 处理异步：

```ts
// store/modules/todos.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

export const fetchTodos = createAsyncThunk('todos/fetch', async () => {
  const res = await fetch('/api/todos')
  return res.json() as Promise<{ id: number; text: string }[]>
})

const todosSlice = createSlice({
  name: 'todos',
  initialState: { list: [] as { id: number; text: string }[], loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => { state.loading = true })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.loading = false
        state.list = action.payload
      })
  },
})
```

组件中使用方式不变：

```jsx
const dispatch = useDispatch()
useEffect(() => { dispatch(fetchTodos()) }, [dispatch])
```