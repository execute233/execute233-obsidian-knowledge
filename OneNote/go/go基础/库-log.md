---
title: 库-log
tags: [go, log, 日志]
aliases: []
---

# 库-log

基础格式化输出见 [[go/go基础/库-fmt|库-fmt]];日志中常记录时间,见 [[go/go基础/库-time|库-time]];命令行标志见 [[go/go基础/库-flag|库-flag]]。

## log

log 包提供了各种方法,如 `Print` 系列、`Fatal` 系列、和 `Panic` 系列。

## 配置 logger

默认情况下的 logger 只会提供日志的时间信息,但是很多情况下我们希望得到更多信息,比如记录该日志的文件名和行号等。log 标准库中为我们提供了定制这些设置的方法。

log 标准库中的 `Flags` 函数会返回标准 logger 的输出配置,而 `SetFlags` 函数用来设置标准 logger 的输出配置。

```go
func Flags() int
func SetFlags(flag int)
```

## flag 选项

提供了以下 flag 选项。

```go
const (
    // 控制输出日志信息的细节,不能控制输出的顺序和格式。
    // 输出的日志在每一项后会有一个冒号分隔:例如2009/01/23 01:23:23.123123 /a/b/c/d.go:23: message
    Ldate         = 1 << iota             // 日期:2009/01/23
    Ltime                                 // 时间:01:23:23
    Lmicroseconds                         // 微秒级别的时间:01:23:23.123123(用于增强Ltime位)
    Llongfile                             // 文件全路径名+行号:/a/b/c/d.go:23
    Lshortfile                            // 文件名+行号:d.go:23(会覆盖掉Llongfile)
    LUTC                                  // 使用UTC时间
    LstdFlags     = Ldate | Ltime         // 标准logger的初始值
)
```

可以这样使用:

```go
func main() {
    log.SetFlags(log.Llongfile | log.Lmicroseconds | log.Ldate)
    log.Println("这是一条很普通的日志。")
}
```

## 配置日志前缀

提供了关于日志信息前缀的两个方法:`Prefix` 查看标准 logger 的输出前缀,`SetPrefix` 函数用来设置输出前缀。

```go
func Prefix() string
func SetPrefix(prefix string)
```

## 配置日志输出位置

用来设置标准 logger 的输出目的地,默认是标准错误输出。

```go
func SetOutput(w io.Writer)
```

## 创建 logger

库中还提供了一个创建新 logger 对象的构造函数,支持我们创建自己的 logger 实例。

```go
func New(out io.Writer, prefix string, flag int) *Logger
```
