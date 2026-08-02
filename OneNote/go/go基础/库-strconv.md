---
title: 库-strconv
tags: [go, strconv, 类型转换]
aliases: []
---

# 库-strconv

字符串格式化见 [[go/go基础/库-fmt|库-fmt]];基本数据类型见 [[go/go基础/基础|基础]]。

实现了基本类型与其字符串表示的转换。

## string 与 int 类型转换

`Atoi()` 函数用于将字符串类型的整数转换为 int 类型。

```go
func Atoi(s string) (i int, err error)
```

`Itoa()` 函数用于将 int 类型数据转换为对应的字符串表示。

![Exported image](_assets/%E5%BA%93-strconv/%E5%BA%93-strconv__13-01-39-1.png)

## Parse 系列函数

用于转换字符串为给定类型的值:`ParseBool()`、`ParseFloat()`、`ParseInt()`、`ParseUint()`。

## Format 系列函数

实现了将给定类型数据格式化为 string 类型数据的功能。
