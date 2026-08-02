---
title: SpringBoot-多环境配置
tags: [java, Spring框架]
aliases: [SpringBoot-多环境配置]
---

# SpringBoot-多环境配置

前置: SpringBoot 基础见 [[SpringBoot-Start]],日志配置见 [[SpringBoot-Log]]。

由于 SpringBoot 只会读取 `application.properties` 或是 `application.yml` 文件，那么怎么才能实现自由切换呢？SpringBoot 给我们提供了一种方式，我们可以通过配置文件指定：

```yaml
spring:
  profiles:
    active: dev
```

接着我们分别创建两个环境的配置文件，`application-dev.yml` 和 `application-prod.yml` 分别表示开发和生产环境的配置文件。

日志也是可以配置的，`<root>` 标签外面套 `<springProfile>` 即可，标上 `name` 属性：

```xml
<springProfile name="dev">
    <root level="DEBUG">
        <appender-ref ref="CONSOLE"/>
    </root>
</springProfile>
<springProfile name="prod">
    <root level="INFO">
        <appender-ref ref="FILE"/>
    </root>
</springProfile>
```
