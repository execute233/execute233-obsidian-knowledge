---
title: 迭代器和iter包
tags: [go, 迭代器, iter]
aliases: []
---

# 迭代器和 iter 包

## Push 迭代器(标准迭代器)

![Exported image](_assets/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85__13-02-06-0.png)

使用迭代器就可以使用 `for/range` 写法。

## Pull 迭代器(用于并行迭代两个容器)

标准库里有把标准迭代器转为 Pull 迭代器的方法。

![Exported image](_assets/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85__13-02-08-1.png)

返回两个函数:

- 第一个是 Pull 迭代器:每次调用时都会返回序列中的下一个值和一个布尔值,该布尔值表示该值是否有效
- 第二个是停止函数,应在完成 Pull 迭代器后调用

下面是一个示例,将一个迭代器中的两个连续值对作为一个元素,返回一个新的迭代器。

![Exported image](_assets/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85/%E8%BF%AD%E4%BB%A3%E5%99%A8%E5%92%8Citer%E5%8C%85__13-02-16-2.png)
