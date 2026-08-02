---
title: Spring-SpEL
tags: [java, Spring框架]
aliases: [Spring-SpEL]
---

# Spring-SpEL

SpEL 是一种强大、简洁的装配 Bean 的方式，它可以通过运行期间执行的表达式将值装配到我们的属性或构造函数当中，更可以调用 JDK 中提供的静态常量，获取外部 Properties 文件中的配置。

前置基础: Bean 装配的整体机制见 [[Spring-IoC]],本篇专注于 SpEL 表达式语法。

## 外部属性注入

用的是 properties 文件。

在使用 `@Configuration` 的类添加 `@PropertySource`（有字符集属性）注解，注意类路径下的文件前面要加 `classpath:`。

接着，我们就可以在 Bean 对象（被 `@Component` 修饰）中的字段/构造方法字段使用 `@Value("${属性名}")` 即可。

## SpEL

语法：`#{表达式}`，常用形式：

- 引用 Bean：`#{beanName.prop}`。
- 调用静态方法：`#{T(java.lang.Math).random()}`。
- 字符串拼接：`#{'hello ' + name}`。
- 运算与三元：`#{age > 18 ? 'adult' : 'minor'}`。

示例：

```java
@Value("#{T(System).currentTimeMillis()}")
private long startTime;

@Value("#{'Hello, ' + user.name}")
private String greeting;
```
