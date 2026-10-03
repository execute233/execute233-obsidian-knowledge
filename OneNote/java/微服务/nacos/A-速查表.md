---
title: Nacos 速查表
tags: [java, nacos, 速查]
aliases: [Nacos端口速查, Nacos参数速查]
---

# Nacos 速查表

本表汇总 Nacos 3.2.4 与本课程 Spring Cloud Alibaba 2025.1 示例的常用入口和参数。

## 端口与路径

| 入口 | 默认值 / 路径 | 用途 |
| --- | --- | --- |
| Console | <code>http://&lt;NACOS_HOST&gt;:8080</code> | 浏览器管理；替换主机占位符 |
| Server 主端口 | <code>8848</code> | HTTP 与 SDK server-addr |
| SDK gRPC | 主端口 <code>+1000</code>，默认 <code>9848</code> | 应用长连接 |
| 节点间 gRPC | 主端口 <code>+1001</code>，默认 <code>9849</code> | 内部通信 |
| JRaft | 主端口 <code>-1000</code>，默认 <code>7848</code> | 内部持久协议 |
| Client API | <code>/nacos/v3/client</code> | 运行时请求 |
| Admin API | <code>/nacos/v3/admin</code> | 管理请求 |
| Console API | <code>/v3/console</code> | Console 页面请求 |
| 登录 | <code>/nacos/v3/auth/user/login</code> | 默认鉴权插件的 Token 获取 |
| 指标 | <code>/nacos/actuator/prometheus</code> | 启用后抓取 |

## Server 配置

| 配置 | 3.2.4 默认 / 要求 | 本课做法 |
| --- | --- | --- |
| <code>nacos.server.main.port</code> | <code>8848</code> | 按需要调整派生端口 |
| <code>nacos.console.port</code> | <code>8080</code> | 与业务应用端口区分 |
| <code>nacos.core.auth.enabled</code> | 发行配置 <code>false</code> | 显式 <code>true</code> |
| <code>nacos.core.auth.admin.enabled</code> | <code>true</code> | 保持开启 |
| <code>nacos.core.auth.console.enabled</code> | <code>true</code> | 保持开启 |
| <code>nacos.core.auth.plugin.nacos.token.secret.key</code> | 填入随机 Base64 密钥 | 集群一致，解码前的随机材料不少于 32 字节 |
| <code>nacos.core.auth.server.identity.key/value</code> | 非空自定义值 | 集群一致；JRaft 也会校验 |
| <code>spring.sql.init.platform</code> | 按存储方案设置 | 外置 MySQL 使用 <code>mysql</code> |
| <code>management.endpoints.web.exposure.include</code> | 按需暴露 | 加入 <code>prometheus</code> |
| <code>nacos.console.ai.mcp.import.allowed-private-addresses</code> | 管理员维护的允许列表 | 填写 <code>&lt;MCP_TARGET_IP_OR_CIDR&gt;</code>，只允许需要的目标 |

## Spring 接入配置

| 配置 | 用途 |
| --- | --- |
| <code>spring.application.name</code> | 默认服务名 |
| <code>spring.cloud.nacos.discovery.server-addr</code> | 注册中心主端口地址 |
| <code>spring.cloud.nacos.discovery.namespace</code> | 服务命名空间 ID |
| <code>spring.cloud.nacos.discovery.group</code> | 服务分组 |
| <code>spring.cloud.nacos.discovery.cluster-name</code> | 实例集群名 |
| <code>spring.cloud.nacos.discovery.ephemeral</code> | 临时 / 持久类型 |
| <code>spring.cloud.nacos.config.server-addr</code> | 配置中心主端口地址 |
| <code>spring.cloud.nacos.config.namespace</code> | 配置命名空间 ID |
| <code>spring.config.import</code> | 显式导入远程配置 |
| <code>refreshEnabled</code> | import 条目的动态刷新开关 |
| <code>spring.cloud.loadbalancer.nacos.enabled</code> | 是否使用 Nacos 选择策略 |

Discovery / Config 的用户名与密码分别用环境变量配置。连接地址填写主端口，不填写 <code>8080</code> 或浏览器页面路径。

## PowerShell 操作

先定义 <code>$nacosDir</code> 为实际发行包目录：

```powershell
& "$nacosDir\bin\startup.cmd" -m standalone
Test-NetConnection -ComputerName '<NACOS_HOST>' -Port 9848
Get-Content -LiteralPath "$nacosDir\logs\nacos.log" -Tail 50 -Wait
```

| 操作 | 说明 |
| --- | --- |
| <code>startup.cmd -m standalone</code> | 本机单机；从 PowerShell 直接调用脚本 |
| <code>startup.cmd -m cluster</code> | 集群；先配置数据库、成员与身份 |
| <code>-f microservice</code> | 只加载 Config / Naming，AI 课不能使用 |
| <code>shutdown.cmd</code> | Windows 脚本可能结束多个 Nacos 进程 |

## 身份与版本

| 项目 | 规则 |
| --- | --- |
| 服务身份 | <code>namespace + group + serviceName</code> |
| 配置身份 | <code>namespace + group + dataId</code> |
| Prompt 身份 | <code>namespace + promptKey</code>，读取时选择版本或标签 |
| Spring BOM | <code>Boot 4.0.0 / Cloud 2025.1.0 / Alibaba 2025.1.0.0</code> |
| Nacos Server / Client | <code>3.2.4 / 3.1.1</code>，职责不同，不要求同号 |

详见 [[00-课程总览|课程总览]]、[[B-常见问题|排查问题]]、[[官方资料索引|参数官方依据]]。
