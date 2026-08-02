---
title: 迭代器和iter包
tags: [go, 迭代器, iter]
aliases: []
---

# 迭代器和 iter 包

迭代器常用于遍历 slice/map,见 [[go/go基础/中级|中级]];泛型是迭代器的基础,见 [[go/go基础/泛型|泛型]]。

## Push 迭代器(标准迭代器)

```go
// All 返回一个迭代器,迭代集合中的所有元素
func (s *Set[E]) All() iter.Seq[E] {
    return func(yield func(E) bool) {
        for v := range s.m {
            if !yield(v) {
                return
            }
        }
    }
}
```

使用迭代器就可以使用 `for/range` 写法。

## Pull 迭代器(用于并行迭代两个容器)

标准库里有把标准迭代器转为 Pull 迭代器的方法。

```go
func Pull[V any](seq Seq[V]) (next func() (V, bool), stop func())

func Pull2[K, V any](seq Seq2[K, V]) (next func() (K, V, bool), stop func())
```

返回两个函数:

- 第一个是 Pull 迭代器:每次调用时都会返回序列中的下一个值和一个布尔值,该布尔值表示该值是否有效
- 第二个是停止函数,应在完成 Pull 迭代器后调用

下面是一个示例,将一个迭代器中的两个连续值对作为一个元素,返回一个新的迭代器。

```go
// Pairs 返回一个迭代器,遍历 seq 中连续的值对。
func Pairs[V any](seq iter.Seq[V]) iter.Seq2[V, V] {
    return func(yield func(V, V) bool) {
        next, stop := iter.Pull(seq)
        defer stop()
        for {
            v1, ok1 := next()
            if !ok1 {
                return
            }
            v2, ok2 := next()
            // If ok2 is false, v2 should be the
            // zero value; yield one last pair.
            if !yield(v1, v2) {
                return
            }
            if !ok2 {
                return
            }
        }
    }
}
```
