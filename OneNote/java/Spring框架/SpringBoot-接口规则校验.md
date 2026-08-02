---
title: SpringBoot-接口规则校验
tags: [java, Spring框架]
aliases: [SpringBoot-接口规则校验]
---

# SpringBoot-接口规则校验

## 导入依赖

在 [[SpringBoot-Start]] 工程中，导入以下依赖即可开启参数校验：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

## 使用

`@Validated` 打在 [[SpringMVC-Controller]] 上启用验证，我们可以使用以下注解来对参数校验：

| 验证注解 | 验证的数据类型 | 说明 |
| --- | --- | --- |
| `@AssertFalse` | `boolean`/装箱 | 值必须是 false |
| `@AssertTrue` | `boolean`/装箱 | 值必须是 true |
| `@NotNull` | Any | 不能是 null |
| `@Null` | Any | 必须是 null |
| `@Min` | `Number` 或 `CharSequence` | 大于等于指定值 |
| `@Max` | `Number` 或 `CharSequence` | 小于等于指定值 |
| `@DecimalMax` / `@DecimalMin` | 同上 | 同上（高精度） |
| `@Size` | 字符串、`Collection`、`Map`、数组 | 长度在指定区间内 |
| `@Past` | `Date`、`Calendar` | 值比当前时间早 |
| `@Future` | 同上 | 值比当前时间晚 |
| `@NotBlank` | `CharSequence` | 值不为空，比较时会去除字符串的首位空格 |
| `@Length` | `CharSequence` | 长度在指定区间内 |
| `@NotEmpty` | `CharSequence`、`Collection`、`Map`、数组 | 值不为 null 且长度不为空 |
| `@Range` | `BigDecimal`、`BigInteger`、`CharSequence` 等数值 | 值在指定区间内 |
| `@Email` | `CharSequence` | 值必须是邮件格式 |
| `@Pattern` | `CharSequence` | 必须匹配正则表达式 |
| `@Valid` | 非原子类型 | 验证对象属性 |

## 异常处理

对于异常不是很友好，可以单独使用 `@ControllerAdvice` 打上类（异常处理详见 [[SpringMVC-other]]），给方法打 `@ExceptionHandler(要处理的 Controller.class)` 即可，方法参数是 `Exception`。

如果方法传入的参数是自定义对象需要验证，可以给参数打 `@Valid`，在自定义对象的类中的属性打注解即可。
