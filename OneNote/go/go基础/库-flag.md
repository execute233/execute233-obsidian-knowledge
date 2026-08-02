---
title: 库-flag
tags: [go, flag, 命令行参数]
aliases: []
---

# 库-flag

日志中常用命令行 flag,见 [[go/go基础/库-log]];环境配置相关见 [[go/go基础/环境搭建]]。

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

```go
flag.Args()   //返回命令行参数后的其他参数,以[]string类型
flag.NArg()   //返回命令行参数后的其他参数个数
flag.NFlag()  //返回使用的命令行参数个数
```

## 示例

```go
func main() {
    //定义命令行参数方式1
    var name string
    var age int
    var married bool
    var delay time.Duration
    flag.StringVar(&name, "name", "张三", "姓名")
    flag.IntVar(&age, "age", 18, "年龄")
    flag.BoolVar(&married, "married", false, "婚否")
    flag.DurationVar(&delay, "d", 0, "延迟的时间间隔")

    //解析命令行参数
    flag.Parse()
    fmt.Println(name, age, married, delay)
    //返回命令行参数后的其他参数
    fmt.Println(flag.Args())
    //返回命令行参数后的其他参数个数
    fmt.Println(flag.NArg())
    //返回使用的命令行参数个数
    fmt.Println(flag.NFlag())
}
```
