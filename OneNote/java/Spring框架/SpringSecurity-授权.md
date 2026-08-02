---
title: SpringSecurity-授权
tags: [java, Spring框架]
aliases: [SpringSecurity-授权]
---

# SpringSecurity-授权

## 基于角色授权

仍然可以在 `filterChain` 里配置（配置方式见 [[SpringSecurity-配置]]）：

```java
auth.requestMatchers("static/**").permitAll();  // 静态资源全部放行
auth.requestMatchers("/").hasAnyRole("USER", "ADMIN");
auth.anyRequest().hasAnyRole("ADMIN");  // 其他请求需要 ADMIN 角色
auth.anyRequest().authenticated();  // 依然所有请求要验证
```

同时，实现 `UserDetailsService` 的类返回的 `UserDetail` 要有 `.roles`（用户认证见 [[SpringSecurity-认证]]）。

## 基于注解授权

首先要开启方法安全校验 `@EnableMethodSecurity`。

然后就可以在方法打这些注解：

```java
@PreAuthorize(写 SpEL 表达式)   // 方法执行前，详细可在 SecurityExpressionRoot 查看（SpEL 见 [[Spring-SpEL]]）
@PostAuthorize                  // 这个是方法执行之后
@Secured                         // 不支持 SpEL，并需要 ROLE_ 前缀
@PreFilter 与 @PostFilter        // 对于集合类型的参数或返回值过滤
```

## 基于权限授权

通过 `.authorities("...")` 给用户授予具体权限，路径匹配使用 `.hasAuthority(...)`。
