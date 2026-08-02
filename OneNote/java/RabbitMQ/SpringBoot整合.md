---
title: SpringBoot整合
tags: [java, RabbitMQ]
aliases: [SpringBoot整合]
---

# SpringBoot整合

前置基础: [[RabbitMQ基础]] 中介绍了六大消息模式,本篇专注于 SpringBoot 项目的工程化整合。

导入相关依赖:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
    <version>3.5.7</version>
</dependency>
```

然后配置:

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: admin
    password: password
    virtual-host: /
```

编写对应的配置类:

```java
@Configuration
public class RabbitMQConfig {

    // 可能涉及多个交换机与队列,这里使用名字区分不同 Exchange 与 Queue

    // 交换机配置
    @Bean("bootExchange1")
    public Exchange bootExchange() {
        // 这个 Builder 有各种类型的路由可以构建
        return ExchangeBuilder.topicExchange("exchange").autoDelete().durable(false).build();
    }

    // 队列配置
    @Bean("bootQueue1")
    public Queue bootQueue() {
        return QueueBuilder.nonDurable("1").build();
    }

    // 队列与交换机绑定
    @Bean
    public Binding bootBinding(@Qualifier("bootQueue1") Queue queue,
                               @Qualifier("bootExchange1") Exchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with("mysql.#").noargs();
    }
}
```

然后我们便可以注入对应的对象使用:

```java
@Autowired
private RabbitTemplate template;

void test() {
    template.convertAndSend("exchange", "mysql.1", "hello world");
}
```

对于消费者,我们需要自定义一个监听类,使用 `@RabbitListener`:

```java
@Component
@Slf4j
public class RabbitMQListener {

    @RabbitListener(queues = "1")
    // 如果自己配置了消息转换器,这里参数可以使任何对象
    public void listener(Message message) {
        log.info("接收到消息: " + new String(message.getBody()));
    }
}
```

如果要自定义消息转换器,写 Bean 即可:

```java
@Bean
public MessageConverter messageConverter() {
    return new Jackson2JsonMessageConverter();
}
```
