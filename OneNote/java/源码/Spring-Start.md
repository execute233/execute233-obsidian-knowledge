---
title: Spring-Start
tags: [java, 源码]
aliases: [Spring-Start]
---

# Spring-Start

## BeanFactory 与 ApplicationContext

我们从 `SpringApplication.run` 返回 `ConfigurableApplicationContext` 的开始研究接口关系。

![[_assets/Spring-Start/Spring-Start__09-26-15-0.png]]

BeanFactory 是 ApplicationContext 的父接口，是 Spring 的核心容器，主要的 ApplicationContext 实现了组合它的功能。Spring 中 BeanFactory 默认实现是用 DefaultListableBeanFactory。

![[_assets/Spring-Start/Spring-Start__09-26-17-1.png]]

可以通过反射拿到里面的 BeanFactory 字段。

```java
ConfigurableApplicationContext context = SpringApplication.run(SpringLearnApplication.class);
Field singletonObjects = DefaultSingletonBeanRegistry.class.getDeclaredField("singletonObjects");
singletonObjects.setAccessible(true);

ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
Map<String, Object> map = (Map<String, Object>) singletonObjects.get(beanFactory);
map.forEach((k, v) -> {
    log.info(k + ": " + v);
});
```

ApplicationContext 比 BeanFactory 多的功能主要体现在以下接口：

### MessageSource（国际化资源处理）

通用的翻译在 `messages.properties` 中，国家翻译以 `messages_en.properties` 为文件存储键值对。

当对应的键不存在对应的语言环境时，会去默认语言找。

IDEA 在 resources 目录下创建资源包即可，添加语言文件。

可以注入 MessageSource 该 Bean 在任何地方用：

```java
// 里面的文本可以嵌入 {0} 类似的，使用 args 传参
r = context.getMessage("key", null, Locale.CHINA);
// 找不到就用默认的消息
r = context.getMessage("key", null, "defaultMessage", Locale.CHINA);
```

### ResourcePatternResolver（通过通配符匹配资源）

```java
// 返回资源路径下的文件，有多个则返回第一个找到的
context.getResource("classpath:application.yml");
// 返回在 jar 包中的资源路径下的所有文件
context.getResources("classpath*:META_INF/spring.factories");
```

### EnvironmentCapable（处理环境信息）

```java
// 获取环境变量
ConfigurableEnvironment environment = context.getEnvironment();
// 获取的是系统环境变量，不区分大小写
environment.getProperty("java_home");
// Spring 中的配置文件的环境变量
environment.getProperty("server.port");
```

### ApplicationEventPublish（发布事件对象）

```java
// 发送事件
context.publishEvent(new ApplicationEvent("test") {});
```

我们可以在任意一个 Bean 中的方法打上 `@EventListener` 注解来监听事件。

```java
@EventListener
public void test(ApplicationEvent event) {
    Object source = event.getSource();
}
```

## BeanFactory 的实现

```java
// 创建 BeanFactory
DefaultListableBeanFactory beanFactory = new DefaultListableBeanFactory();

// 得到 Bean 的定义（class, scope, 初始化, 销毁）
AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder.genericBeanDefinition(Config.class)
    .setScope("singleton").getBeanDefinition();
// 添加到 BeanFactory
beanFactory.registerBeanDefinition("config", beanDefinition);

// 给 BeanFactory 添加常用的后处理器，包括注解处理以及事件处理
AnnotationConfigUtils.registerAnnotationConfigProcessors(beanFactory);

// 拿到该 BeanFactory 里面的所有 BeanFactory 后处理器
Collection<BeanFactoryPostProcessor> postProcessors =
    beanFactory.getBeansOfType(BeanFactoryPostProcessor.class).values();
// 让每个 BeanFactory 后处理器去处理这个 BeanFactory
for (BeanFactoryPostProcessor beanFactoryPostProcessor : postProcessors) {
    beanFactoryPostProcessor.postProcessBeanFactory(beanFactory);
}

// 还有 Bean 的后处理器，针对 Bean 的各个阶段提供扩展，比如 @Autowired
beanFactory.getBeansOfType(BeanPostProcessor.class).values().forEach(beanFactory::addBeanPostProcessor);

// beanFactory 默认是 lazy-init，可以调用下面方法来预先实例化所有的单例 Bean
beanFactory.preInstantiateSingletons();

// 获取所有 bean 的名字
for (String name : beanFactory.getBeanDefinitionNames()) {
    log.info(name);
}

/**
 * beanFactory 不会自动：
 *   主动调用 BeanFactory 后处理器
 *   主动添加 Bean 后处理器
 *   主动初始化单例 Bean
 *   解析 beanFactory、${} 和 #{}
 * bean 的后处理器有排序的逻辑
 */
```

## ApplicationContext 的实现

它主要实现了类似于上面代码的功能，扩展 BeanFactory。

主要是这种：

- `ClassPathXmlApplicationContext` — 基于 classpath 下 xml 格式的配置文件来创建
- `FileSystemXmlApplicationContext` — 基于磁盘路径下 xml 格式配置文件来创建
- `AnnotationApplicationContext` — 基于 java 注解配置来创建
- `AnnotationConfigServletWebServerApplicationContext` — 基于 java 注解来创建，用于 web 环境

### 基于 xml 格式的配置文件原理

```java
// 一样创建个 BeanFactory
DefaultListableBeanFactory beanFactory = new DefaultListableBeanFactory();
// 得到 BeanDefinition 读取器
XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(beanFactory);
// 加载配置文件，把 Bean 添加到 BeanFactory 里
reader.loadBeanDefinitions(new ClassPathResource("application.xml"));
```

### 基于注解的配置

```java
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(Config.class);
```

### 基于注解 + Web 的配置

```java
new AnnotationConfigServletWebServerApplicationContext(WebConfig.class);
```

```java
@Configuration
static class WebConfig {
    @Bean
    public ServletWebServerFactory servletWebServerFactory() {
        return new TomcatServletWebServerFactory(); // tomcat
    }

    @Bean
    public DispatcherServlet dispatcherServlet() {
        return new DispatcherServlet(); // dispatcherServlet
    }

    @Bean
    public DispatcherServletRegistrationBean registrationBean(DispatcherServlet servlet) {
        return new DispatcherServletRegistrationBean(servlet, "/"); // 绑定
    }

    @Bean("/") // 另类的 Controller 配置方法,Bean 名字就是 Web 路径
    public Controller controller1() {
        return (Controller) (request, response) -> {
            response.getWriter().print("helloWorld");
            return null;
        };
    }
}
```