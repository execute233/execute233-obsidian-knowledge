---
title: Spring-高级特性
tags: [java, Spring框架]
aliases: [Spring-高级特性]
---

# Spring-高级特性

## Bean Aware

在 Spring 中提供了一些以 Aware 结尾的接口，实现了 Aware 接口的 bean 在被初始化之后，可以获取相应资源。

简单来说，它就是一个标识，实现此接口的类会获得某些感知能力，Spring 容器会在 Bean 被加载时，根据类实现的感知接口，会调用类中实现的对应感知方法，有这些接口和更多的使用：

- `BeanNameAware`：获取该 Bean 名称。
- `ApplicationContextAware`：获得 `ApplicationContext` 引用，但会导致代码与 Spring 框架耦合。
- `BeanFactoryAware`：获得 `BeanFactory` 引用。
- `EnvironmentAware`：获得 `Environment` 对象。
- `ResourceLoaderAware`：获得 `ResourceLoader`。
- `MessageSourceAware`：获得 `MessageSource`，用于国际化消息。
- `ApplicationEventPublisherAware`：获得 `ApplicationEventPublisher`，用于发布事件。

## 任务调度

为了执行某些任务，我们可能需要一些非常规的操作，比如我们希望使用线程来处理我们的结果或是执行一些定时任务，到达指定时间后再去执行。这时我们首先想到的就是创建一个新的线程来处理，或是使用 `TimerTask` 来完成定时任务，但是我们有了 Spring 框架之后，就不用这样了，因为 Spring 框架为我们提供了更加便捷的方式进行任务调度。

### 异步方法调用

首先要开启异步支持，在 `@Configuration` 修饰类再修饰 `@EnableAsync`。

然后在 Bean 类的成员方法（返回 `void` 或 `Future`）打上 `@Async`，之后得到该 Bean 对象调用相应的方法就可以异步执行了。

### 定时任务

首先要开启定时任务支持，在 `@Configuration` 修饰类再修饰 `@EnableScheduling`。

然后在 Bean 类的成员方法打上 `@Scheduled`，无需主动调用就可以定时运行这个方法了：

- `fixedRate`：固定速率执行，单位毫秒。
- `fixedDelay`：固定延迟执行（前一次完成后延迟指定时间到下一次），单位毫秒。
- `initialDelay`：应用启动一段时间后开始第一次执行。
- `cron`：复杂时间规则。

cron 表达式由 6 或 7 个字段组成：

```text
秒 分 时 日 月 周 [年]
```

有以下字段：

| 字段 | 含义 |
| --- | --- |
| `*` | 任意值 |
| `,` | 多个值 |
| `-` | 指定范围 |
| `/` | 指定步长 |
| `?` | 不指定值（只在日期和星期有效） |
| `L` | 最后一个，通常用于月份和星期字段 |
| `W` | 最近的工作日，仅在日期字段有效 |
| `#` | 每个月的第几个星期几，比如 `2#3` 是每个月第三个星期二 |

例子：

- `0 0 6 * * ?`：每天早上 6 点。
- `0 0 */1 * *`：每个小时整点。
- `0 0 0 1 * ?`：每月一号午夜进行。

## 监听器

要编写监听器，我们只需要让 Bean 继承 `ApplicationListener<T>` 就可以了，并且将类型指定为对应的 Event 事件，这样，当发生某个事件时就会通知我们，比如 `ContextRefreshedEvent`，这个事件会在 Spring 容器初始化完成会触发一次。