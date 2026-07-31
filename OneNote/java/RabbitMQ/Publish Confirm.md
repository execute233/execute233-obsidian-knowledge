# Publish Confirm

![[_assets/Publish-Confirm/Publish-Confirm__09-22-42-0.png]]

Publish Return一般是代码层面的问题
配置中使用
```yaml
spring:
rabbitmq:
publisher-confirm-type: _correlated_ _# none -_ _关闭，_ _simple -_ _同步阻塞等待__MQ__的回执消息，_ _correlated - MQ__异步回调方式返回回执消息_
publisher-returns: true
```
在实际的代码里可以
```python
@Configuration
public class RabbitMQConfig implements ApplicationContextAware {
@Override
public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
```
// 获取RabbitTemplate
RabbitTemplate template = applicationContext.getBean(RabbitTemplate.class);
// 设置ReturnCallback
```text
template.setReturnsCallback(returnMessage -> {
System._out_.println("ReturnCallback: " + returnMessage.getMessage());
```
});
// 设置ConfirmCallback
```text
template.setConfirmCallback((correlationData, ack, cause) -> {
System._out_.println("ConfirmCallback: " + correlationData + " " + ack + " " + cause);
```
});
}
}