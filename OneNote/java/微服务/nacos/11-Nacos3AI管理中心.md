---
title: Nacos 3 AI 管理中心
tags: [java, nacos, AI, MCP]
aliases: [Nacos AI Registry, Nacos3新特性]
---

# Nacos 3 AI 管理中心

AI 管理中心把 MCP Server、Agent、Prompt、Skill 和 AgentSpec 作为独立资源管理，提供发现、版本和发布治理。

> [!abstract]
> 本课重点：五类资源；运行时角色；发布生命周期；与微服务模型的关系。

## 资源类型

| 资源 | 保存什么 | 应用怎样使用 |
| --- | --- | --- |
| MCP Server | 协议、端点、工具 / 资源定义、版本 | MCP Client 发现后连接并调用 |
| Agent | AgentCard、调用端点、版本 | 按 A2A 等集成方式发现和调用 Agent |
| Prompt | 模板、变量、版本、标签 | 查询模板后渲染，送给模型 |
| Skill | 可复用能力包及元数据 | Agent 或工具链下载并加载 |
| AgentSpec | Agent 规范包、manifest 和相关文件 | 平台或开发工具读取与分发 |

Agent 是可调用入口，AgentSpec 是规范包。MCP Server 的工具定义和 Nacos Prompt 模板也不是同一种资源。

## MCP 链路

```text
MCP Server → Nacos：登记服务描述、工具和地址
MCP Client → Nacos：发现所需资源与可用端点
MCP Client → MCP Server：初始化、列出工具、调用工具
LLM / Agent → MCP Client：根据任务决定是否调用工具
```

模型不是 MCP 服务发现的必需条件。本课程先用 Java MCP Client 验证通信，能更清楚地判断问题是注册、协议还是模型选择。

| 组件 | 职责 |
| --- | --- |
| Nacos | 资源登记、治理、发现 |
| MCP Server | 实现工具和资源，处理协议请求 |
| MCP Client | 发起 MCP 通信 |
| MCP Router / 网关 | 按部署方式提供代理、路由或协议转换 |
| LLM | 推理和选择调用；由应用接入 |

Nacos 登记一个 MCP 地址，不会自动让该地址实现 MCP 协议。若接入 Router / 网关，调用路径会包含对应组件，需要按该组件的文档配置。

## 版本与发布状态

```text
创建草稿 → 修改 → 提交审核 → 发布 → 上线
                                   → 下线 / 重新上线
```

Prompt、Skill、AgentSpec 等资源具备版本和发布生命周期。是否需要审核取决于 Pipeline 配置；管理员强制发布可能绕过校验，因此要有明确的操作和审计约定。

| 概念 | 含义 |
| --- | --- |
| 版本 | 一次可追溯的资源内容 |
| 标签 | 指向版本的可变指针，例如 <code>latest</code> |
| 业务标签 | 分类、检索和治理信息 |
| 可见性 | 哪些调用者能在列表 / 详情等入口看到资源 |
| 权限 | 调用者是否允许执行读取、写入等操作 |

标签更新不会修改已发布的版本内容。生产应用需要确定使用固定版本还是跟随标签，并建立对应的验证与回退方式。

## 与配置、服务发现的关系

AI 资源可能复用 Config 或 Naming 的底层存储和发现能力，但操作时使用对应 AI 资源模型。不要绕过 AI API 直接修改底层配置记录。

Namespace 继续用于环境 / 租户隔离。应用读取所需资源，管理平台承担资源发布、审核、批量查询和权限维护。

## 功能模式

| 模式 | 本课程用途 |
| --- | --- |
| 默认 <code>all</code> | 同时学习 Config、Naming 与 AI 管理中心 |
| <code>-f microservice</code> | 只加载微服务模块，MCP / Prompt 实操不可用 |
| Console 独立部署 | 按真实身份和后端权限访问 Server；另行配置拓扑 |

使用本课程部署命令的默认模式即可。3.2.4 对内网 MCP 工具导入增加允许列表限制，详见下一课及 [[14-版本升级与旧文纠偏|升级说明]]。

详见 [[12-MCP注册发现与工具调用|MCP 实操]]、[[13-Prompt版本发布与读取实操|Prompt 实操]]。
