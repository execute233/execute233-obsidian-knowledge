---
title: Publish Confirm
tags: [java, RabbitMQ]
aliases: [Publish Confirm]
---

# Publish Confirm

RabbitMQ 了 **Publisher Confirm** 和 **Publisher Return** 两种确认机制。开启确认机制后,在 MQ 成功收到消息后会返回确认消息给生产者。返回的结果有以下几种情况:

- 消息投递到了 MQ,但是路由失败。此时会通过 Publisher Return 返回路由异常原因,然后返回 **ACK**,告知投递成功。
- 临时消息投递到了 MQ,并且入队成功,返回 **ACK**,告知投递成功。
- 持久消息投递到了 MQ,并且入队完成持久化,返回 **ACK**,告知投递成功。
- 其它情况都会返回 **NACK**,告知投递失败。

## 架构示意

```
publisher  ──[ack]──▶  topic exchange  ──▶  queue1 (non durable)  ──▶  consumer1
                          │
                          └────────────▶  queue2 (durable)  ──▶  consumer2
                                                                  │
                                                                  ▼
                                                               (磁盘)
publisher  ──[return/ack]──▶  exchange2  (路由失败,回退)
```

Publish Return 一般是代码层面的问题。

## 配置中使用

```yaml
spring:
  rabbitmq:
    # none - 关闭,simple - 同步阻塞等待 MQ 的回执消息,correlated - MQ 异步回调方式返回回执消息
    publisher-confirm-type: correlated
    publisher-returns: true
```

## 在实际的代码里可以

```java
@Configuration
public class RabbitMQConfig implements ApplicationContextAware {

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        // 获取 RabbitTemplate
        RabbitTemplate template = applicationContext.getBean(RabbitTemplate.class);

        // 设置 ReturnCallback
        template.setReturnsCallback(returnMessage -> {
            System.out.println("ReturnCallback: " + returnMessage.getMessage());
        });

        // 设置 ConfirmCallback
        template.setConfirmCallback((correlationData, ack, cause) -> {
            System.out.println("ConfirmCallback: " + correlationData + " " + ack + " " + cause);
        });
    }
}
```