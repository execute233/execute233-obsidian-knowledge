![[Publish-Subscribe__09-21-49-0.png]]

类型FANOUT  
生产者示例：  
// 创建交换机，指定的交换机名称与类型  
channel.exchangeDeclare("exchange", BuiltinExchangeType._FANOUT_, false, true, null);  
// 创建队列  
channel.queueDeclare("1", false, false, true, null);  
channel.queueDeclare("2", false, false, true, null);  
// 绑定队列与交换机，参数分别为队列名称，交换机名称，路由键(交换机为FANOUT则设置为”“)  
channel.queueBind("1", "exchange", "");  
channel.queueBind("2", "exchange", "");  
// 发送消息...  
消费者只需要获取对应的队列即可