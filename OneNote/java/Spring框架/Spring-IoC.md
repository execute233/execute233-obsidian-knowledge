---
title: Spring-IoC
tags: [java, Spring框架]
aliases: [Spring-IoC]
---

# Spring-IoC

## IoC（Inversion of Control，控制反转）
## Bean配置
## 依赖注入
## 自动装配
## 生命周期与继承
## 工厂bean
## 注解开发

一种设计原则，将对象的创建、配置和依赖管理的控制权从应用程序代码中“反转”到外部容器
Spring为我们提供了一个IoC容器，用于去存放我们需要使用的对象，我们可以将对象交给IoC容器进行管理。

一般配置文件是xml，这样的一个内容
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.springframework.org/schema/beans
```
[http://www.springframework.org/schema/beans/spring-beans.xsd](http://www.springframework.org/schema/beans/spring-beans.xsd)">

```xml
<bean class="xxxx"/>
</beans>
```

可以通过ApplicationContext来获取IoC容器

<bean>标签有以下属性
class - 必填，全限定类名
id - 唯一标识符
name - bean的名称
scope - bean的作用域，singleton（单例，默认），prototype
lazy-init - 是否懒加载
init-method - bean初始化后调用的方法名
destory-method - bean销毁前调用的方法名
depends-on - 指定当前bean依赖其他bean，控制加载顺序
parent - 指定继承的bean，但是继承里面的字段
```csharp
abstract - 指示这是个抽象的bean,只能被继承使用
<bean>内部可以嵌入<property>标签,有以下属性
```
name - 字段名
value - 相应的值
ref - 相应的Bean对象名
如果字段是集合，可以内嵌<list>等标签，再内嵌多个<value>指定默认值
<bean>内部可以嵌入<constructor-arg>标签，来设置构造方法的参数，属性同上
有多个构造方法时，还有type字段可以指定构造方法
对bean中的字段自动配置，前面已经提到
前面property是手动ref来指定装配，但可以使用autowire对bean中的对象字段自动装配。
autowire有几个值：
byType
byName
constructor
default
no
自己体会
如果自动装配的目标有多个，则需要指定<bean>设置
取消autowire-candidate="false"
主要primary="true"
只有单例模式的bean才能被管理生命周期
参考上面的init-method， destory-method
继承参考上面的parent
如
<bean class="com.test.bean.StudentFactory" factory-method="getStudent"/>
注意，这里的Bean类型需要填写为Student类的工厂类，并且添加factory-method指定对应的工厂方法，但是最后注册的是工厂方法的返回类型，所以说依然是Student的Bean
如果要使用工厂类对象来得到bean，可以先注册工厂bean，再指定Bean的工厂Bean，如
```xml
<bean name="studentfactory" class="com.test.bean.StudyFactory"/>
<bean factory-bean="studentfactory" factory-method="getStudent">
```
注意，可以直接输入工厂Bean的名称来得到其生产的Bean，要得到工厂Bean则需要名称前加&
xml太复杂了，但我们可以使用@Configuration来修饰类
@Configuration修饰类，该类可传给AnnotationConfigApplicationContext使用来获取IoC容器
同时该类可以使用@Import来导入其他配置
然后，我们可以在被修饰的类里面的成员方法打上@Bean（"bean名称"）注解，该成员方法返回的对象会自动交由IoC容器管理，同时@Bean也有属性可配置
配置该成员方法，可像xml一样用注解配置，如
```python
@Lazy
@Scope
@DependsOn
```
对于需要其他Bean进行的注入，可直接把Bean形参拿过来，再@Bean，会自动装配，如
```python
@Bean
public Student getStudent(Teacher teacher) {
return new Student(teacher);
```
}
对于类的字段，使用@Autowired（优先byType）/@Resource（优先byName）注解可以自动装配，如果有多个可用的bean来装配，使用@Qualifier来指定要的Bean的名字
同时可以给Bean类的方法打上注解
```python
@PostConstruct - 构造完毕后
@PreDestroy - 销毁前
```

但这样还是太麻烦了，我们可以告诉Spring扫描哪些包下的类是需要自动装配的
使用@Component（"名字"）修饰类来表示这个类是个Bean对象，并自动交由IoC管理
可以在@Configuration继续添加@ConponentScan/@ConponentScans来标记扫描的包