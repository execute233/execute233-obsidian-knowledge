---
title: Publish-Subscribe
tags: [java, RabbitMQ]
aliases: [Publish-Subscribe]
---

# Publish-Subscribe

## 1. 模式说明

```
P  ──▶  X (Exchange)  ──▶  Queue1  ──▶  C1
                   └──▶  Queue2  ──▶  C2
```

在订阅模型中,多了一个 Exchange 角色,而且过程略有变化:

- **P**:生产者,也就是要发送消息的程序,但是不再发送到队列中,而是发给 X(交换机)。
- **C**:消费者,消息的接收者,会一直等待消息到来。
- **Queue**:消息队列,接收消息、缓存消息。
- **Exchange**:交换机(X)。一方面,接收生产者发送的消息。另一方面,知道如何处理消息,例如递交给某个特别队列、递交给所有队列、或是将消息丢弃。到底如何操作,取决于 Exchange 的类型。Exchange 有常见以下 3 种类型:
  - **Fanout**:广播,将消息交给所有绑定到交换机的队列。
  - **Direct**:定向,把消息交给符合指定 routing key 的队列。
  - **Topic**:通配符,把消息交给符合 routing pattern(路由模式)的队列。

**Exchange**(交换机)只负责转发消息,不具备存储消息的能力,因此如果没有任何队列与 Exchange 绑定,或者没有符合路由规则的队列,那么消息会丢失!按路由规则转发可使用 [[Routing]] 模式。

类型 `FANOUT`。

## 生产者示例

```java
// 创建交换机,指定的交换机名称与类型
channel.exchangeDeclare("exchange", BuiltinExchangeType.FANOUT, false, true, null);

// 创建队列
channel.queueDeclare("1", false, false, true, null);
channel.queueDeclare("2", false, false, true, null);

// 绑定队列与交换机,参数分别为队列名称,交换机名称,路由键(交换机为 FANOUT 则设置为 "")
channel.queueBind("1", "exchange", "");
channel.queueBind("2", "exchange", "");

// 发送消息...
```

消费者只需要获取对应的队列即可。