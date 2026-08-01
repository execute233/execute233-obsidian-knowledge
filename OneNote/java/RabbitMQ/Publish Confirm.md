---
title: Publish Confirm
tags: [java, RabbitMQ]
aliases: [Publish Confirm]
---

# Publish Confirm

![[_assets/Publish-Confirm/Publish-Confirm__09-22-42-0.png]]

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