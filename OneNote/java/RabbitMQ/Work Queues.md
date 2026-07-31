# Work Queues

**轮训分发消息**

![[_assets/Work-Queues/Work-Queues__09-21-42-0.png]]

使用多个消费者即可
**消息应答**
为了保证消息在发送过程中不丢失，引入了该机制，消费者收到消息并处理后告诉rabbimq它已经处理了，可以把消息删除了
**自动应答**
没有对传递的消息数量进行限制，可能会导致极高的内存占用，只适合消费者可以搞笑并以某种速率处理的情况下使用
**手动应答方法**
// 肯定确认，第一个是消息tag，第二个是是否确认多个（即确认当前channel中所有的消息）
channel.basicAck(message.getEnvelope().getDeliveryTag(), false);
// 否定确认，第一个是消息tag，第二个是是否确认多个（即否定当前channel中所有的消息）,第三个是是否重新入队
channel.basicNack(message.getEnvelope().getDeliveryTag(), false, true);
// 否定确认，第一个是消息tag，第二个是是否重新入队
channel.basicReject(message.getEnvelope().getDeliveryTag(), false);
**消息自动重新入队**
如果消费者丢失连接并未发送ACK，则消息会对其重新排队

![[_assets/Work-Queues/Work-Queues__09-21-45-1.png]]

持久化
队列持久化（只是队列不会消失）
创建队列时设置持久化即可，非持久化的队列变为持久化队列必须先把原队列删除再重新创建
消息持久化（发送的消息不回消失）
需要在生产者发布消息时配置
channel.basicPublish("", _QUEUE_NAME_, MessageProperties._PERSISTENT_TEXT_PLAIN_, _CONTENT_.getBytes());
不公平分发与预取值
需要在consumer设置
// 设置不公平分发，默认0就是轮训，差不多是优先级
channel.basicQos(1);