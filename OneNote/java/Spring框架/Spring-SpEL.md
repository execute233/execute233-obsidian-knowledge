---
title: Spring-SpEL
tags: [java, Spring框架]
aliases: [Spring-SpEL]
---

# Spring-SpEL

SpEL是一种强大，简洁的装配Bean的方式，它可以通过运行期间执行的表达式将值装配到我们的属性或构造函数当中，更可以调用JDK中提供的静态常量，获取外部Properties文件中的的配置。
 3. 外部属性注入
4. SpEL

用的是properties文件
在使用@Configuration的类添加@PropertySource（有字符集属性）注解，注意类路径下的文件前面要加classpath：
接着，我们就可以在Bean对象（被@Conponent修饰）中的字段/构造方法字段使用@Value（"${属性名}"）即可