---
title: 库-log
tags: [go, log, 日志]
aliases: []
---

# 库-log

## log

log 包提供了各种方法,如 `Print` 系列、`Fatal` 系列、和 `Panic` 系列。

## 配置 logger

默认情况下的 logger 只会提供日志的时间信息,但是很多情况下我们希望得到更多信息,比如记录该日志的文件名和行号等。log 标准库中为我们提供了定制这些设置的方法。

log 标准库中的 `Flags` 函数会返回标准 logger 的输出配置,而 `SetFlags` 函数用来设置标准 logger 的输出配置。

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-02-0.png)

## flag 选项

提供了以下 flag 选项。

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-04-1.png)

可以这样使用:

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-05-2.png)

## 配置日志前缀

提供了关于日志信息前缀的两个方法:`Prefix` 查看标准 logger 的输出前缀,`SetPrefix` 函数用来设置输出前缀。

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-08-3.png)

## 配置日志输出位置

用来设置标准 logger 的输出目的地,默认是标准错误输出。

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-10-4.png)

## 创建 logger

库中还提供了一个创建新 logger 对象的构造函数,支持我们创建自己的 logger 实例。

![Exported image](_assets/%E5%BA%93-log/%E5%BA%93-log__13-01-11-5.png)
