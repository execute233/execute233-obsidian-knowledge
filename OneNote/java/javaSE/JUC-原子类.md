---
title: JUC-原子类
tags: [java, javaSE]
aliases: [JUC-原子类]
---

# JUC-原子类

前面我们说到,如果要保证 `i++` 的原子性,那么我们的唯一选择就是加锁,那么,除了加锁之外,还有没有其他更好的解决方法呢?JUC 为我们提供了原子类,底层采用 CAS 算法,它是一种用法简单、性能高效、线程安全地更新变量的方式。

所有的原子类都位于 `java.util.concurrent.atomic` 包下。

## 原子类介绍

常用基本数据类,有对应的原子类封装:

| 原子类 | 功能 |
| --- | --- |
| `AtomicInteger` | 原子更新 int |
| `AtomicLong` | 原子更新 long |
| `AtomicBoolean` | 原子更新 boolean |
| `AtomicIntegerArray` | 原子更新 int 数组 |
| `AtomicLongArray` | 原子更新 long 数组 |
| `AtomicBooleanArray` | 原子更新 boolean 数组 |

ABA 类问题可以使用版本号来解决,Java 提供了 `AtomicStampedReference<T>` 类来提供带版本的支持。