---
title: SpringSecurity-配置
tags: [java, Spring框架]
aliases: [SpringSecurity-配置]
---

# SpringSecurity-配置

## 导入依赖

导入两个包：`spring-security-config` 与 `spring-security-web`，在 `org.springframework.security`。

```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-config</artifactId>
    <version>6.2.11</version>
</dependency>
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-web</artifactId>
    <version>6.2.11</version>
</dependency>
```

## 配置初始化器

```java
public class SecurityInitializer extends AbstractSecurityWebApplicationInitializer {
    // 不重写任何内容
    // 实际上会自动注册个 Filter，其底层就是靠 N 个过滤器实现
}
```

这里和 [[SpringMVC-配置]] 中的 `WebApplicationInitializer` 机制类似，都是通过 `ServletContainerInitializer` 自动发现的。

## 创建配置类

创建配置类来配置 SpringSecurity：

```java
@Configuration
@EnableWebSecurity  // 开启 WebSecurity 相关功能
public class SecurityConfiguration {
    // ...
}
```

接着在根容器添加此配置文件即可（根容器即 [[Spring-IoC]] 中的 IoC 容器）：

```java
@Override
protected Class<?>[] getRootConfigClasses() {
    return new Class[]{WebConfiguration.class, SecurityConfiguration.class};  // 基本的 Spring 配置类，一般用于业务配置
}
```

认证与授权分别见 [[SpringSecurity-认证]] 与 [[SpringSecurity-授权]]。
