---
title: Routing
tags: [java, RabbitMQ]
aliases: [Routing]
---

# Routing

![[_assets/Routing/Routing__09-21-57-0.png]]

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