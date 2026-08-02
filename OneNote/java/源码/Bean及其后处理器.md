---
title: Bean及其后处理器
tags: [java, 源码]
aliases: [Bean及其后处理器]
---

# Bean及其后处理器

## Bean 的生命周期

Bean 定义注册阶段由 [[BeanFactory后处理器]] 处理，本节关注 Bean 实例化之后的生命周期回调。

以下面为例:

```java
ConfigurableApplicationContext context = SpringApplication.run(SpringLearnApplication.class, args);
context.close();
```

```java
@Slf4j
@Component
class LifeCleanBean {
    public LifeCleanBean() {
        log.info("constructor");
    }
}
```

```java
@Autowired    // 是在构造方法完成后注入
public void autowire(@Value("${JAVA_HOME}") String home) {
    log.info("autowire: {}", home);
}
```

```java
@PostConstruct    // 在构造方法后,也在注入完成后
public void postConstruct() {
    log.info("postConstruct");
}
```

```java
@PreDestroy    // 仅在单例 bean 被销毁时调用,其他类型的销毁时机不同
public void preDestroy() {
    log.info("preDestroy");
}
```

## 扩展 Bean 处理器

```java
public class MyBeanPostProcessor    // 这些接口都实现了 BeanPostProcessor
        implements InstantiationAwareBeanPostProcessor, DestructionAwareBeanPostProcessor {

    @Nullable
    @Override
    public Object postProcessBeforeInstantiation(Class<?> beanClass, String beanName) throws BeansException {
        // 实例化之前执行,这里返回的对象会替换原本的 bean
        return null;
    }

    @Override
    public boolean postProcessAfterInstantiation(Object bean, String beanName) throws BeansException {
        // 实例化之后执行,这里返回 false 会跳过依赖注入阶段
        return true;
    }

    @Nullable
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        // 初始化之前执行,返回的对象会替换原本的 bean,如 @PostConstruct、@ConfigurationProperties 就是在这一步解析
        return bean;
    }

    @Nullable
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        // 初始化之后执行,返回的对象会替换原本的 bean,如代理增强
        return bean;
    }

    @Override
    public void postProcessBeforeDestruction(Object bean, String beanName) throws BeansException {
        // bean 销毁之前执行
    }

    @Override
    public boolean requiresDestruction(Object bean) {
        // 是否需要执行销毁方法
        return true;
    }

    @Nullable
    @Override
    public PropertyValues postProcessProperties(PropertyValues pvs, Object bean, String beanName)
            throws BeansException {
        // 依赖注入阶段执行,返回 null 会跳过属性注入阶段
        return pvs;
    }
}
```

执行顺序就是:

```text
postProcessBeforeInstantiation
constructor()
@PostConstructor
InitializingBean.afterPropertiesSet
@Bean(initMethod=)
postProcessAfterInstantiation
postProcessProperties
@Autowired
postProcessBeforeInitialization
@PostConstruct
postProcessAfterInitialization
postProcessBeforeDestruction
requiresDestruction
@PreDestroy
DisposableBean.destroy()
@Bean(destroyMethod=)
```

## 常见的 Bean 后处理器

```java
// 干净的容器,没有自己添加后处理器
GenericApplicationContext context = new GenericApplicationContext();
// 设置 BeanFactory 的 @Autowired 的参数解析器,这里添加了就可以解析参数里的 @Value 值注入
context.getDefaultListableBeanFactory()
    .setAutowireCandidateResolver(new ContextAnnotationAutowireCandidateResolver());

// 解析 @Autowired、@Value 的 Bean 处理器
context.registerBean(AutowiredAnnotationBeanPostProcessor.class);
// @Resource、@PostConstruct、@PreDestroy 的 Bean 处理器
context.registerBean(CommonAnnotationBeanPostProcessor.class);
// @ConfigurationProperties 的 Bean 处理器,要绑定
ConfigurationPropertiesBindingPostProcessor.register(context.getDefaultListableBeanFactory());

context.refresh();    // 执行 BeanFactory 后处理器,添加 Bean 后处理器,初始化所有单例
```

## @Autowired Bean 后处理器解析

```java
// 1、查看哪些属性、方法添加了 @Autowired,称为 InjectionMetadata
AutowiredAnnotationBeanPostProcessor processor = new AutowiredAnnotationBeanPostProcessor();
processor.setBeanFactory(beanFactory);
// 执行依赖注入,指定属性对(没有就找默认的),指定的 Bean 类型,指定的 Bean 名字
processor.postProcessProperties(null, Bean1.class, "bean1");
```

### postProcessProperties 的方法具体做了下面的事

```java
// findAutowiringMetadata 方法是私有的,这里通过反射来执行该方法
InjectionMetadata metadata = (InjectionMetadata) findAutowiringMetadata.invoke(
    processor, "bean1", Bean1.class, null);

// 返回的 InjectionMetadata 调用 inject 来进行注入,注入时按类型查找值
metadata.inject(bean1, "bean1", null);
```

### inject 方法里如何注入值

```java
Field bean2 = Bean1.class.getDeclaredField("bean2");    // 首先获取要注入的字段
DependencyDescriptor descriptor = new DependencyDescriptor(bean2, false);    // 包装字段,并且指示依赖是否必要,否则报错

// 根据成员变量找要注入谁,给指定的 beanName, autowiredBeanName, typeConverter
// 因为是根据类型来找值的,后面 3 个参数都可以为 null
beanFactory.doResolveDependency(descriptor, null, null, null);
```

### inject 方法里如何注入方法

```java
Method setBean2 = Bean1.class.getDeclaredMethod("setBean2", Bean2.class);    // 首先获取注入的方法
DependencyDescriptor descriptor = new DependencyDescriptor(new MethodParameter(setBean2, 0), false);
beanFactory.doResolveDependency(descriptor, null, null, null);
```

总的来说:

![[_assets/Bean及其后处理器/Bean及其后处理器__09-26-21-0.png]]
