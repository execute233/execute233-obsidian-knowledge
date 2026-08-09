---
title: Vue 其它常用 API
tags: [vue, api, 响应式]
aliases: []
---

# Vue 其它常用 API

## shallowRef 与 shallowReactive

### shallowRef

- **作用**：创建一个响应式数据，但只对 `.value` 本身进行响应式处理。
- **特点**：只跟踪引用值的变化，不关心值内部属性的变化。

```ts
const state = shallowRef({ count: 0 })
// state.value = { count: 1 }   // 触发响应
// state.value.count = 1        // 不会触发响应
```

### shallowReactive

- **作用**：创建一个浅层响应式对象。
- **特点**：最外层属性是响应式的，但嵌套对象的内部属性不是。

```ts
const obj = shallowReactive({
  foo: { bar: 1 },
})
obj.foo = { bar: 2 }     // 触发响应
obj.foo.bar = 2          // 不会触发响应
```

## readonly 与 shallowReadonly

### readonly

`readonly` 创建一个对象的**深层只读副本**：

```ts
const original = reactive({ count: 0 })
const copy = readonly(original)

original.count = 1  // OK
copy.count = 2      // 警告，且修改无效
```

### shallowReadonly

只对对象最外层属性做只读处理，嵌套属性仍可写：

```ts
const obj = shallowReadonly({ foo: { bar: 1 } })
obj.foo = { bar: 2 }      // 警告
obj.foo.bar = 2            // 可以
```

## toRaw 与 markRaw

### toRaw

把响应式对象转为**原始对象**，脱离代理。常用于读取响应式对象后想拿到原始数据：

```ts
import { reactive, toRaw } from 'vue'

const state = reactive({ a: 1 })
const raw = toRaw(state)
console.log(raw === state)  // true（同一个对象，但已脱离代理）
```

### markRaw

标记一个对象，使其**永远不会**被 `reactive` / `shallowReactive` 转成响应式。适合挂载第三方类实例（例如 Vue Router 的 router 对象）：

```ts
import { markRaw } from 'vue'

const router = markRaw(createRouter(/* ... */))
app.use(router)
```

## customRef

自定义响应处理，可以精细控制 `track`（追踪依赖）与 `trigger`（触发更新）的时机。常用于实现防抖 ref：

```ts
import { customRef } from 'vue'

function useDebouncedRef<T>(value: T, delay = 300) {
  let timer: ReturnType<typeof setTimeout> | null = null
  return customRef<T>((track, trigger) => ({
    get() {
      track()
      return value
    },
    set(newValue: T) {
      if (timer) clearTimeout(timer)
      timer = setTimeout(() => {
        value = newValue
        trigger()
      }, delay)
    },
  }))
}

// 使用：搜索框输入 300ms 后才触发更新
const keyword = useDebouncedRef('', 300)
```