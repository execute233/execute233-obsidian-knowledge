---
title: SpringBoot-多环境配置
tags: [java, Spring框架]
aliases: [SpringBoot-多环境配置]
---

# SpringBoot-多环境配置

由于SpringBoot只会读取application.properties或是application.yml文件，那么怎么才能实现自由切换呢？SpringBoot给我们提供了一种方式，我们可以通过配置文件指定：
```yaml
spring:
profiles:
active: dev
```
接着我们分别创建两个环境的配置文件，application-dev.yml和application-prod.yml分别表示开发和生产环境的配置文件
日志也是可以配置的，<root>标签外面套<springProfile>即可，标上name属性