---
title: 库-flag
tags: [go, flag, 命令行参数]
aliases: []
---

# 库-flag

该库实现了命令行参数的解析。

## os.Args

获取命令行参数,这是一个数组,每个元素以空格分开。

## flag 参数类型

| flag 参数 | 有效值 |
| --- | --- |
| 字符串 flag | 合法字符串 |
| 整数 flag | 1234、0664、0x1234 等类型,也可以是负数 |
| 浮点数 flag | 合法浮点数 |
| bool 类型 flag | 1, 0, t, f, T, F, true, false, TRUE, FALSE, True, False |
| 时间段 flag | 任何合法的时间段字符串,如 "300ms"、"-1.5h"、"2h45m";合法的单位有 ns、us、µs、ms、s、m、h |

## 定义和使用命令行 flag 参数

```go
flag.Type(flag 名, 默认值, 帮助信息) *Type
flag.TypeVar(指针, flag 名, 默认值, 帮助信息)
```

通过以上两种方法定义好命令行 flag 参数后,需要通过调用 `flag.Parse()` 来对命令行参数进行解析。

支持的形式有以下几种:

```bash
-flag xxx
--flag xxx
-flag=xxx
--flag=xxx
```

> 其中,布尔类型的参数必须使用等号的方式指定。

## 其它函数

![Exported image](_assets/%E5%BA%93-flag/%E5%BA%93-flag__13-00-55-0.png)

## 示例

![Exported image](_assets/%E5%BA%93-flag/%E5%BA%93-flag__13-00-56-1.png)
