---
title: BeanFactory后处理器
tags: [java, 源码]
aliases: [BeanFactory后处理器]
---

# BeanFactory后处理器

## BeanFactoryPostProcessor

BeanFactory 扫描 Bean 注解的后处理器。与之对应，作用于单个 Bean 生命周期各阶段的处理器见 [[Bean及其后处理器]]。

```java
GenericApplicationContext context = new GenericApplicationContext();
// 注册 BeanFactory 后处理器， 用于解析 @Configuration
// 可以处理 @ComponentScan、@Bean、@Import、@ImportResource
context.registerBean(ConfigurationClassPostProcessor.class);
```

## ConfigurationClassPostProcessor 中组件扫描原理

```java
// 工具类，查找某个类上面是否有某个注解，这里以 Config 类上是否有 @ComponentScan 为例
ComponentScan componentScan = AnnotationUtils.findAnnotation(Config.class, ComponentScan.class);
if (componentScan != null) {
    // 获取包名属性
    for (String basePackage : componentScan.basePackages()) {
        // 拿到要扫描的包，转换为路径，比如
        // com.execute233.springlearn.controller -> classpath*:com/execute233/springlearn/controller/**/*.class
        String path = "classpath:" + basePackage.replace('.', '/') + "/**/*.class";

        // 用于缓存类信息的工厂
        CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();

        // 通过注解构建 bean 名器
        AnnotationBeanNameGenerator generator = new AnnotationBeanNameGenerator();
        Resource[] resources = context.getResources(path);

        // 拿到所有要扫描的类的路径
        for (Resource resource : resources) {
            // 得到每个类的元信息，检查是否加了 @Component
            MetadataReader reader = factory.getMetadataReader(resource);
            AnnotationMetadata annotationMetadata = reader.getAnnotationMetadata();

            // 如果该类添加了 @Component 或其派生
            if (annotationMetadata.hasAnnotation(Component.class.getName())
                || annotationMetadata.hasMetaAnnotation(Component.class.getName())) {
                // 构建 BeanDefinition 并注册到 BeanFactory 中
                AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder
                    .genericBeanDefinition(reader.getClassMetadata().getClassName()).getBeanDefinition();
                DefaultListableBeanFactory beanFactory = context.getDefaultListableBeanFactory();
                String beanName = generator.generateBeanName(beanDefinition, beanFactory);
                beanFactory.registerBeanDefinition(beanName, beanDefinition);
            }
        }
    }
}
```

## ConfigurationClassPostProcessor 中 @Bean 扫描原理

```java
// 用于缓存类信息的工厂
CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();
MetadataReader reader = factory.getMetadataReader(Config.class.getName());

// 拿到被 @Bean 修饰的方法
Set<MethodMetadata> methods = reader.getAnnotationMetadata().getAnnotatedMethods(Bean.class.getName());
for (MethodMetadata method : methods) {
    // 这里是工厂方法得到的 Bean，就不用指定类名了
    BeanDefinitionBuilder builder = BeanDefinitionBuilder.genericBeanDefinition();
    // 你要拿到方法的 bean 肯定要一个实例化的对象给它访问，这里指定工厂方法名称与工厂 Bean 名称
    builder.setFactoryMethodOnBean(method.getMethodName(), Config.class.getName());
    // 我们还要定义工厂方法参数的装配形式
    builder.setAutowireMode(AbstractBeanDefinition.AUTOWIRE_CONSTRUCTOR);

    // 这样就拿到 BeanDefinition
    AbstractBeanDefinition beanDefinition = builder.getBeanDefinition();
    context.getDefaultListableBeanFactory().registerBeanDefinition(method.getMethodName(), beanDefinition);
}
```

## Mapper 接口的管理

### 单个 Mapper 可以如此管理

```java
// 返回的是工厂对象，但最后还是 Mapper1 的 Bean
@Bean
public MapperFactoryBean<Mapper1> mapper1(SqlSessionFactory sqlSessionFactory) {
    MapperFactoryBean<Mapper1> factory = new MapperFactoryBean<>(Mapper1.class);
    factory.setSqlSessionFactory(sqlSessionFactory);
    return factory;
}
```

### 多个 Mapper 可以模拟 ComponentScan 做的事

```java
class MapperPostProcessor implements BeanDefinitionRegistryPostProcessor {
    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry beanfactory) throws BeansException {
        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        AnnotationBeanNameGenerator generator = new AnnotationBeanNameGenerator();

        // 拿到 Mapper 路径下的所有资源
        Resource[] resources = resolver.getResources(path);
        CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();
        for (Resource resource : resources) {
            MetadataReader reader = factory.getMetadataReader(resource);
            ClassMetadata metadata = reader.getClassMetadata();
            if (metadata.isInterface()) {
                // 拿到接口
                AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder.genericBeanDefinition(MapperFactoryBean.class)
                    .addConstructorArgValue(metadata.getClassName())
                    .setAutowireMode(AbstractBeanDefinition.AUTOWIRE_BY_TYPE)
                    .getBeanDefinition();
                // 这里 bean 名字是个问题，直接丢给生成器是拿到 MapperFactoryBean 的名字，会覆盖容器已有的东西
                // Spring 源码里是另起一个 beanDefinition 来生成名字的
                AbstractBeanDefinition beanNameDefinition = BeanDefinitionBuilder
                    .genericBeanDefinition(metadata.getClassName()).getBeanDefinition();
                String beanName = generator.generateBeanName(beanNameDefinition, beanfactory);
                beanfactory.registerBeanDefinition(beanName, beanDefinition);
            }
        }
    }
}
```
