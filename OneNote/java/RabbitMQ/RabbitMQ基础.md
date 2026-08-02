---
title: RabbitMQ基础
tags: [java, RabbitMQ]
aliases: [RabbitMQ基础]
---

# RabbitMQ基础

## 三大功能

流量削峰、应用解耦、异步处理。

## 四大核心概念

![[_assets/RabbitMQ基础/RabbitMQ基础__09-21-29-0.png]]

快递员(快递站)模型:

```
发包裹  ──快递员──▶  快递站  ──快递员──▶  收件人
```

实际 RabbitMQ 流程:

```
生产者  ──▶  交换机  ──绑定关系──▶  队列  ──▶  消费者
                  └─绑定关系──▶  队列  ──▶  消费者
```

## RabbitMQ 工作原理

![[_assets/RabbitMQ基础/RabbitMQ基础__09-21-34-2.png]]

```
Producer ──▶ Connection/Channel ──▶ Exchange ──▶ Queue ──▶ Connection/Channel ──▶ Consumer
                              ▼
                          Broker (RabbitMQ)
```

## 六种消息模式

最简单的入门模式是 [[Hello World]],随后可扩展到 [[Work Queues]]、[[Publish-Subscribe]]、[[Routing]]、[[Topic]] 等模式。消息可靠性详见 [[可靠性]]。

| # | 模式 | 描述 |
|---|---|---|
| 1 | Hello World | 最简单的消息传递,一对一单发单收 |
| 2 | Work Queues | 一个生产者对应多个消费者(竞争消费模式) |
| 3 | Publish/Subscribe | 一条消息被多个消费者同时接收 |
| 4 | Routing | 选择性接收消息(基于 routing key) |
| 5 | Topics | 基于模式(topic)的路由 |
| 6 | Publisher Confirms | 生产者发布确认 |

## 核心概念

- **Broker**:接收和分发消息的应用。
- **Virtual host**:出于多租户和安全因素设计的,把 AMQP 的基本组件划分到一个虚拟的分组中,类似于网络中的 namespace 概念。当多个不同的用户使用同一个 RabbitMQ server 提供的服务时,可以划分出多个 vhost,每个用户在自己的 vhost 创建 exchange/queue 等。
- **Connection**:publisher/consumer 和 broker 之间的 TCP 连接。
- **Channel**:在 connection 内部建立的逻辑连接,如果应用程序支持多线程,通常每个 thread 创建单独的 channel 进行通讯,AMQP method 包含了 channel id 帮助客户端和 message broker 识别 channel,所以 channel 之间是完全隔离的。Channel 作为轻量级的 Connection 极大减少了操作系统建立 TCP connection 的开销。
- **Exchange**:message 到达 broker 的第一站,根据分发规则,匹配查询表中的 routing key,分发消息到 queue 中去。常用的类型有:direct(point-to-point)、topic(publish-subscribe)和 fanout(multicast)。

## 安装

安装 web 管理插件:

```bash
rabbitmq-plugins enable rabbitmq_management
```

访问 15672 端口即可,初始账密都为 guest。

## 添加用户

创建账号:

```bash
rabbitmqctl add_user <user_name> <password>
```

设置用户角色:

```bash
rabbitmqctl set_user_tags <user_name> administrator
```

设置用户权限:

```bash
rabbitmqctl set_permissions [-p <vhostpath>] <user> <conf> <write> <read>
```

例如 `rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"` 表示用户 admin 具有 /vhost1 这所有的资源配置、读、写权限。

查询用户和角色:

```bash
rabbitmqctl list_users
```

要注意 erlang cookie 不一致问题,一般需要:

```bash
copy "C:\Windows\System32\config\systemprofile\.erlang.cookie" "C:\Users\<user>\.erlang.cookie"
```

## JAVA 相关使用配置

添加相应的 maven 坐标:

```xml
<dependency>
    <groupId>com.rabbitmq</groupId>
    <artifactId>amqp-client</artifactId>
    <version>5.28.0</version>
</dependency>
```