---
title: SpringBoot-Log
tags: [java, Spring框架]
aliases: [SpringBoot-Log]
---

# SpringBoot-Log

![[_assets/SpringBoot-Log/SpringBoot-Log__09-24-09-0.png]]

所以，SpringBoot 为了统一日志框架的使用，做了这些事情：

- 直接将其他依赖以前的日志框架剔除。
- 导入对应日志框架的 Slf4j 中间包。
- 导入自己官方指定的日志实现，并作为 Slf4j 的日志实现层。

## 打印项目日志信息

SpringBoot 使用的是 Slf4j 作为日志门面，Logback 作为日志实现，对应的依赖为：

```xml
spring-boot-starter-logging
```

（此依赖项已经被包含了）

然后就可以 `LoggerFactory.getLogger()` 了，也可以使用 Lombok 的 `@Slf4j`。

## 配置 logback 日志

SpringBoot 推荐其配置文件名称命名为 `logback-spring.xml`，可以使用高级 Profile 功能。

我们可使用默认配置的文件中已有的东西自己配置，如：

```xml
<?xml version="1.0" encoding="utf-8" ?>
<!-- 该标签会覆盖 spring 的默认配置 -->
<configuration>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>

    <!-- ch.qos.logback.core.ConsoleAppender 是专用于控制台的 Appender -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern>
            <pattern>${CONSOLE_LOG_CHARSET}</pattern>
        </encoder>
    </appender>

    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <encoder>
            <pattern>${CONSOLE_LOG_PATTERN}</pattern>
            <pattern>${CONSOLE_LOG_CHARSET}</pattern>
        </encoder>
        <rollingPolicy class="cn.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <!-- 日志文件输出路径，以及命名规则 -->
            <fileNamePattern>logs/app-log-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <!-- 单个日志文件大小上限 -->
            <maxFileSize>10MB</maxFileSize>
            <!-- 到期自动清理日志文件 -->
            <cleanHistoryOnStart>true</cleanHistoryOnStart>
            <!-- 保留最近 30 天的日志文件 -->
            <maxHistory>30</maxHistory>
            <!-- 总日志文件大小上限 -->
            <totalSizeCap>50MB</totalSizeCap>
        </rollingPolicy>
    </appender>

    <!-- 指定日志输出级别，和启用的 Appender -->
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

Logback 内置的日志字段还是比较少，可以使用其 MDC 机制获取日志打印上下文。这个在 `org.slf4j.MDC` 中，需要自定义丢 key-value（基于 ThreadLocal），然后在配置文件中写 `%X{key}` 占位符。

## 自定义 Banner

在 `resource` 文件夹下使用 `banner.txt` 即可自定义，替换掉 SpringBoot 原来的 Banner。

可以在里面使用颜色，比如：

```text
${AnsiColor.RED}
```

设置后面输出颜色，当然也是 Spring 占位符。