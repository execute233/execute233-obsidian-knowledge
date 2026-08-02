---
title: Spring-IoC
tags: [java, Spring框架]
aliases: [Spring-IoC]
---

# Spring-IoC

## IoC（Inversion of Control，控制反转）

一种设计原则，将对象的创建、配置和依赖管理的控制权从应用程序代码中"反转"到外部容器。

Spring 为我们提供了一个 IoC 容器，用于去存放我们需要使用的对象，我们可以将对象交给 IoC 容器进行管理。

一般配置文件是 xml，这样的一个内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean class="xxxx"/>
</beans>
```

可以通过 `ApplicationContext` 来获取 IoC 容器。

## Bean 配置

`<bean>` 标签有以下属性：此外，IoC 容器还提供了 BeanFactoryPostProcessor 机制用于扩展配置(详见 [[BeanFactory后处理器]])。

- class：必填，全限定类名。
- id：唯一标识符。
- name：bean 的名称。
- scope：bean 的作用域，`singleton`（单例，默认），`prototype`。
- lazy-init：是否懒加载。
- init-method：bean 初始化后调用的方法名。
- destroy-method：bean 销毁前调用的方法名。
- depends-on：指定当前 bean 依赖其他 bean，控制加载顺序。
- parent：指定继承的 bean，但是继承里面的字段。
- abstract：指示这是个抽象的 bean，只能被继承使用。

`<bean>` 内部可以嵌入 `<property>` 标签，有以下属性：

- name：字段名。
- value：相应的值。
- ref：相应的 Bean 对象名。

如果字段是集合，可以内嵌 `<list>` 等标签，再内嵌多个 `<value>` 指定默认值。

`<bean>` 内部可以嵌入 `<constructor-arg>` 标签，来设置构造方法的参数，属性同上。有多个构造方法时，还有 `type` 字段可以指定构造方法。

## 依赖注入

对 bean 中的字段自动配置，前面已经提到。

前面 `property` 是手动 `ref` 来指定装配，但可以使用 `autowire` 对 bean 中的对象字段自动装配。

`autowire` 有几个值：

- `byType`
- `byName`
- `constructor`
- `default`
- `no`

如果自动装配的目标有多个，则需要指定 `<bean>` 设置：

- 取消：`autowire-candidate="false"`。
- 主要：`primary="true"`。

## 自动装配

对 bean 中的对象字段自动装配，前面已经提到。

## 生命周期与继承

只有单例模式的 bean 才能被管理生命周期。参考上面的 `init-method`、`destroy-method`。Bean 还可以实现 [[Aware与Scope]] 接口来获取容器信息和定义作用域。

继承参考上面的 `parent`。

## 工厂 Bean

如：

```xml
<bean class="com.test.bean.StudentFactory" factory-method="getStudent"/>
```

注意，这里的 Bean 类型需要填写为 Student 类的工厂类，并且添加 `factory-method` 指定对应的工厂方法，但是最后注册的是工厂方法的返回类型，所以说依然是 Student 的 Bean。

如果要使用工厂类对象来得到 bean，可以先注册工厂 bean，再指定 Bean 的工厂 Bean，如：

```xml
<bean name="studentfactory" class="com.test.bean.StudyFactory"/>
<bean factory-bean="studentfactory" factory-method="getStudent"/>
```

注意，可以直接输入工厂 Bean 的名称来得到其生产的 Bean，要得到工厂 Bean 则需要名称前加 `&`。

## 注解开发

xml 太复杂了，但我们可以使用 `@Configuration` 来修饰类：

- `@Configuration` 修饰类，该类可传给 `AnnotationConfigApplicationContext` 使用来获取 IoC 容器。
- 同时该类可以使用 `@Import` 来导入其他配置。

然后，我们可以在被修饰的类里面的成员方法打上 `@Bean("bean名称")` 注解，该成员方法返回的对象会自动交由 IoC 容器管理，同时 `@Bean` 也有属性可配置。

配置该成员方法，可像 xml 一样用注解配置，如：

```java
@Lazy
@Scope
@DependsOn
```

对于需要其他 Bean 进行的注入，可直接把 Bean 形参拿过来，再 `@Bean`，会自动装配，如：

```java
@Bean
public Student getStudent(Teacher teacher) {
    return new Student(teacher);
}
```

对于类的字段，使用 `@Autowired`（优先 byType）/ `@Resource`（优先 byName）注解可以自动装配，如果有多个可用的 bean 来装配，使用 `@Qualifier` 来指定要的 Bean 的名字。

同时可以给 Bean 类的方法打上注解：

```java
@PostConstruct  // 构造完毕后
@PreDestroy     // 销毁前
```

但这样还是太麻烦了，我们可以告诉 Spring 扫描哪些包下的类是需要自动装配的。

使用 `@Component("名字")` 修饰类来表示这个类是个 Bean 对象，并自动交由 IoC 管理。

可以在 `@Configuration` 继续添加 `@ComponentScan` / `@ComponentScans` 来标记扫描的包。