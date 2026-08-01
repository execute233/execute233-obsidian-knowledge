---
title: Hello World
tags: [java, RabbitMQ]
aliases: [Hello World]
---

# Hello World

![[_assets/Hello-World/Hello-World__09-21-39-0.png]]

P 是生产者,C 是消费者,中间的队列是消息缓冲区。

## 生产者与消费者

### 生产者

```java
void producer() throws Exception {
    // 创建连接工厂
    ConnectionFactory factory = new ConnectionFactory();
    // 工厂 IP 连接 RabbitMQ 的队列
    factory.setHost(HOST_NAME);
    // 用户名密码
    factory.setUsername(USER_NAME);
    factory.setPassword(PASSWORD);
    // 创建连接
    Connection connection = factory.newConnection();
    // 获取信道
    Channel channel = connection.createChannel();
    // 创建队列,参数为
    // 队列名、是否持久化、是否独占、是否自动删除队列、其它参数
    channel.queueDeclare(QUEUE_NAME, false, false, false, null);
    // 发送消息,参数为
    // 交换机、路由键、其它参数、消息内容
    channel.basicPublish("", QUEUE_NAME, null, CONTENT.getBytes());
    // 上面方法是异步的,如果不需要再发送就需要关闭连接防止阻塞主线程
    connection.close();
}
```

### 消费者

```java
void consumer() throws Exception {
    ConnectionFactory factory = new ConnectionFactory();
    factory.setHost(HOST_NAME);
    factory.setUsername(USER_NAME);
    factory.setPassword(PASSWORD);

    Connection connection = factory.newConnection();
    Channel channel = connection.createChannel();

    // 消费数据,该方法不会阻塞,参数分别为
    // 消费队列、是否自动确认、消费的回调、消费取消回调
    channel.basicConsume(QUEUE_NAME, true,
        (consumerTag, message) -> System.out.println("接收到消息:" + new String(message.getBody())),
        (consumerTag) -> System.out.println("取消消费:" + consumerTag)
    );
    // 上面方法是异步的,主线程退出仍会监听,不需要再使用则需关闭连接
    connection.close();
}
```