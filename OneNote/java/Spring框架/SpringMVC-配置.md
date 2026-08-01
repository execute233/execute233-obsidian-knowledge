---
title: SpringMVC-配置
tags: [java, Spring框架]
aliases: [SpringMVC-配置]
---

# SpringMVC-配置

## MVC 的三层架构

![[_assets/SpringMVC-配置/SpringMVC-配置__09-23-42-0.png]]

MVC 详细解释如下：

- **M** 是指业务模型（Model）：通俗的讲就是我们之前用于封装数据传递的实体类。
- **V** 是指用户界面（View）：一般指的是前端页面。
- **C** 则是控制器（Controller）：控制器就相当于 Servlet 的基本功能，处理请求，返回响应。

![[_assets/SpringMVC-配置/SpringMVC-配置__09-23-44-1.png]]

## 传统 XML 配置

### POM 添加依赖 spring-webmvc

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>6.2.11</version>
</dependency>
```

### 配置 spring 的 Servlet

在 `web.xml` 中注册 `DispatcherServlet`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee
        https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
    version="6.0">

    <servlet>
        <servlet-name>mvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>mvc</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

### 配置 Spring 上下文（比如 spring.xml）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        https://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 需要引入 context 命名空间，配置 base-package -->
    <context:component-scan base-package=""/>
</beans>
```

### 为 DispatcherServlet 配置初始化参数

在步骤 2 里，`<servlet>` 标签里写：

```xml
<init-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring.xml</param-value>
</init-param>
```

## 注解配置

Tomcat 会在类路径中查找实现 `ServletContainerInitializer` 接口的类，如果发现的话，就用它来配置 Servlet 容器，Spring 提供了这个接口的实现类 `SpringServletContainerInitializer`，通过 `@HandlesTypes(WebApplicationInitializer.class)` 来设置，这个类反过来会查找实现 `WebApplicationInitializer` 的类，并将配置的任务交给他们来完成，因此直接实现接口即可：

```java
public class WebInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{WebInitializer.class};  // 基本的 Spring 配置类，一般用于业务配置
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[0];  // DispatcherServlet 的配置类，用于 Controller 等配置
    }

    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};  // 匹配路径
    }
}
```