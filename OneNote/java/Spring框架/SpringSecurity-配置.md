---
title: SpringSecurity-配置
tags: [java, Spring框架]
aliases: [SpringSecurity-配置]
---

# SpringSecurity-配置

导入两个包：
spring-security-config与spring-security-web，在org.springframework.security
接着配置初始化器
public class SecurityInitializer extends AbstractSecurityWebApplicationInitializer {
// 不重写任何内容
// 实际上会自动注册个Filter，其底层就是靠N个过滤器实现
}
创建配置类来配置SpringSecurity
```python
@Configuration
@EnableWebSecurity // 开启WebSecurity相关功能
public class SecurityConfiguration {
```

}
接着在根容器添加此配置文件即可
```python
@Override
protected Class<?>[] getRootConfigClasses() {
return new Class[]{WebConfiguration.class, SecurityConfiguration.class}; // 基本的Spring配置类,一般用于业务配置
```
}