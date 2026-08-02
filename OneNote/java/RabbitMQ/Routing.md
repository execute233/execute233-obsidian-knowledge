---
title: Routing
tags: [java, RabbitMQ]
aliases: [Routing]
---

# Routing

队列与交换机的绑定,不能是任意绑定了,而是要指定一个 RoutingKey(路由 key)。

消息的发送方在向 Exchange 发送消息时,也必须指定消息的 RoutingKey。

Exchange 不再把消息交给每一个绑定的队列,而是根据消息的 RoutingKey 进行判断,只有队列的 RoutingKey 与消息的 RoutingKey 完全一致,才会接收到消息。需要通配符路由可使用 [[Topic]] 模式。

## 路由示意

```
       error  ──────────▶  Queue1  ──▶  C1
P ──▶  X  ───info ───────▶  Queue2  ──▶  C2
       error  ──────────▶
       warning───────────▶
```

类型 `DIRECT`。

## 生产者示例

```java
// 创建交换机,指定的交换机名称与类型
channel.exchangeDeclare("exchange", BuiltinExchangeType.DIRECT, false, true, null);

// 创建队列
channel.queueDeclare("1", false, false, true, null);
channel.queueDeclare("2", false, false, true, null);

// 绑定队列与交换机,参数分别为队列名称,交换机名称,路由键
// 队列 1 绑定,可以绑多个 routing key
channel.queueBind("1", "exchange", "error");
channel.queueBind("1", "exchange", "exception");

// 队列 2 绑定,可以绑多个 routing key
channel.queueBind("2", "exchange", "info");
channel.queueBind("2", "exchange", "warn");

// 发送消息...
for (int i = 0; i < 1000; i++) {
    channel.basicPublish("exchange", "info", null, Integer.toString(i).getBytes());
    TimeUnit.SECONDS.sleep(1);
}
```

消费者只需要拿到队列 1 即可,上述代码中会让队列 2 不会有消息。