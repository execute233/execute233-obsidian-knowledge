---
title: ControllerAdvice之@InitBinder
tags: [java, 源码]
aliases: [ControllerAdvice之@InitBinder]
---

# ControllerAdvice之@InitBinder

## ControllerAdvice 功能

对所有的 Controller 增强，有下面：

- `@ExceptionHandler` 抛出异常处理
- `@ModelAttribute` 返回值作为 Model 数据补充到 Controller 执行过程中
- `@InitBinder` 补充自定义类型转换器

加在 `@ControllerAdvice` 是全局的，加在 `@Controller` 是局部的。

（WebDataBinder）