---
title: Spring整合Swagger或Knife4j
tags: [java, Spring框架]
aliases: [Spring整合Swagger或Knife4j]
---

# Spring 整合 Swagger 或 Knife4j

## Swagger 常用注解

| 注解 | 用法 | 属性 |
| --- | --- | --- |
| `@Api` | 用在 Controller，表示对类的说明 | `tag`：标签 |
| `@ApiOperation` | 用在方法上，说明方法的用途、作用 | `value`：方法的业务功能 |
| `@ApiModel` | 用在 Entity、DTO、VO 等 | `description`：描述 |
| `@ApiModelProperty` | 用在属性上，描述属性信息 | — |

## 集成步骤

### 1. 添加依赖

```xml
<!-- Knife4j（推荐） -->
<dependency>
    <groupId>com.github.xiaoymin</groupId>
    <artifactId>knife4j-openapi3-jakarta-spring-boot-starter</artifactId>
    <version>4.4.0</version>
</dependency>
```

### 2. 配置类

```java
@Configuration
public class Knife4jConfig {
    @Bean
    public OpenAPI openAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("API 文档")
                .description("SpringBoot 集成 Knife4j")
                .version("1.0.0"));
    }
}
```

### 3. 访问

启动应用后访问 `http://localhost:8080/doc.html`。