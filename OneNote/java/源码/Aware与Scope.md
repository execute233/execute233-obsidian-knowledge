---
title: Aware与Scope
tags: [java, 源码]
aliases: [Aware与Scope]
---

# Aware与Scope

## Aware

Aware 接口用于注入与容器相关的信息，例如：

- `BeanNameAware` 注入 Bean 的名字
- `BeanFactoryAware` 注入 BeanFactory 容器
- `ApplicationContextAware` 注入 ApplicationContext 容器
- `EmbeddedValueResolverAware` 注入 `${}`

Aware 属于 Spring 容器内置的回调机制，而 `@Autowired` 等注解的解析依赖 Bean 后处理器，相关原理见 [[Bean及其后处理器]] 与 [[BeanFactory后处理器]]。

### 举例

```java
class MyBean implements BeanNameAware, ApplicationContextAware, InitializingBean {
    /*
    这些功能用 @Autowired 也可以实现，但与 Aware 接口还有区别
    @Autowired 的解析需要 bean 后处理器，属于扩展功能
    Aware 是内置功能，不添加扩展，Spring 就能识别
    在一些情况下会用到 Aware，比如 bean 加载顺序是：
        Configuration -> beanFactoryPostProcessor
        -> beanPostProcessor -> bean
    这种情况下 Configuration 里面的注解便会失效
    */
    @Override
    public void setBeanName(String name) {
        log.info("setBeanName"); // Bean 名称设置后
    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        log.info("setApplicationContext"); // 设置 ApplicationContext 后
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        log.info("afterPropertiesSet"); // Bean 初始化后
    }
}
```

## Scope

目前有以下 Scope：

- `singleton`
- `prototype`
- `request`
- `session`
- `application`

### 单例注入多例失效

对于单例对象来讲，依赖注入仅发生了一次，后续没有用到多例，因此使用的始终是第一次依赖注入的多例。

解决办法是使用 `@Lazy` 生成代理，每次使用单例方法都由代理生成新的多例对象。

另一种方法是指定 `@Scope(proxyMode = ScopedProxyMode.TARGET_CLASS)`。

还有种方法是注入 `ObjectFactory<Object>` 对象，每次使用都利用工厂对象拿到 Object 的多例。

Bean 的作用域由 IoC 容器统一管理，详见 [[Spring-IoC]]。
