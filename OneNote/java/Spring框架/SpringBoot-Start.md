---
title: SpringBoot-Start
tags: [java, Spring框架]
aliases: [SpringBoot-Start]
---

# SpringBoot-Start

## 常用模块快速整合

导入 SpringBoot 直接写：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
    <version>3.5.7</version>
</dependency>
```

所有的 Spring 依赖都是以 starter 的形式命名的，类似于 `spring-boot-starter-xxx`。

比如一些常见的：

- **web**：内置 Tomcat 的 SpringMVC 模块。
  - 包含 starter、json、tomcat、spring-web、spring-webmvc。

要注意的是：

- 不需要手动添加包扫描，会自动扫描。
- Controller 返回的对象可以直接变为 JSON 文本返回（需要 Restful 风格）。

可以添加下面这些依赖：

- `spring-boot-starter-security`
- `mybatis-spring-boot-starter`（注意还是得要数据库相关依赖，配置数据源）

## 自定义运行器

只需要实现 `ApplicationRunner` 并注册为 Bean 即可，在 SpringBoot 启动完后自动调用其中的 `run`。

也可以使用 `CommandLineRunner`，支持 `@Order` 或实现 `Ordered` 接口设置优先级。

## 配置文件

在 `resource` 文件夹中的 `application.properties`（或者 `application.yml`）。

## 打包运行

- 导出 jar 包：

  ```bash
  mvn package
  ```

- 导出 war 包：

  ```xml
  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
      <!-- 排除内嵌 tomcat -->
      <exclusions>
          <exclusion>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-tomcat</artifactId>
          </exclusion>
      </exclusions>
  </dependency>
  <!-- 添加 Servlet 依赖 -->
  <dependency>
      <groupId>jakarta.servlet</groupId>
      <artifactId>jakarta.servlet-api</artifactId>
      <scope>provided</scope>
  </dependency>
  ```

  记得在 `<project>` 里设置 `<packaging>` 为 war 包。

  运行主类继承 `SpringBootServletInitializer`，实现方法返回参数调用 `builder` 使用主类 `class`。