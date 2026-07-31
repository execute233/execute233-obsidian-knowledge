![[_assets/Routing/Routing__09-21-57-0.png]]

类型DIRECT
生产者示例：
// 创建交换机，指定的交换机名称与类型
channel.exchangeDeclare("exchange", BuiltinExchangeType._DIRECT_, false, true, null);
// 创建队列
channel.queueDeclare("1", false, false, true, null);
channel.queueDeclare("2", false, false, true, null);
// 绑定队列与交换机，参数分别为队列名称，交换机名称，路由键
// 队列1绑定，可以绑多个routing key
channel.queueBind("1", "exchange", "error");
channel.queueBind("1", "exchange", "exception");
// 队列2绑定，可以绑多个routing key
channel.queueBind("2", "exchange", "info");
channel.queueBind("2", "exchange", "warn");
// 发送消息...
for (int i = 0; i < 1000; i++) {
channel.basicPublish("exchange", "info", null, Integer._toString_(i).getBytes());
TimeUnit._SECONDS_.sleep(1);
}
消费者只需要拿到队列1即可，上述代码中会让队列2不会有消息