---
title: Topic
tags: [java, RabbitMQ]
aliases: [Topic]
---

# Topic

![[_assets/Topic/Topic__09-22-35-0.png]]

类型 `TOPIC`。

类似于 Routing,这个的 routing key 是可以进行模糊匹配的,`*` 代表某个字符,`#` 代表 0 个或多个字符,这个要在 `.` 前面后面使用才有效。

## 生产者示例

```java
// 创建交换机,指定的交换机名称与类型
channel.exchangeDeclare("exchange", BuiltinExchangeType.TOPIC, false, true, null);

// 创建队列
channel.queueDeclare("1", false, false, true, null);
channel.queueDeclare("2", false, false, true, null);

// 绑定队列与交换机,参数分别为队列名称,交换机名称,路由键
// 队列 1 绑定,绑 routing key
channel.queueBind("1", "exchange", "mysql.#");

// 队列 2 绑定,绑 routing key
channel.queueBind("2", "exchange", "redis.#");

// 发送消息...
for (int i = 0; i < 1000; i++) {
    channel.basicPublish("exchange", "mysql." + i, null, Integer.toString(i).getBytes());
    TimeUnit.SECONDS.sleep(1);
}
```