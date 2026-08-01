---
title: Spring-数据库框架整合
tags: [java, Spring框架]
aliases: [Spring-数据库框架整合]
---

# Spring-数据库框架整合

## 整合 Mybatis 框架

将数据源交给 IoC 容器管理。

首先导入 `mybatis-spring`（ver：3.0.5）和 `spring-jdbc`。

然后在 Spring 配置类的 `sqlSessionTemplate()` 方法上打 `@Bean`，一般是：

```java
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder()
    .build(Resources.getResourceAsReader("mybatis-config.xml"));
return new SqlSessionTemplate(sqlSessionFactory);
```

或者自己单独创建 `DataSource`（方便后续更换），然后返回 `SqlSessionFactoryBean`，如：

```java
@Bean
public DataSource dataSource() {
    return new PooledDataSource(…);
}

@Bean
public SqlSessionTemplate sqlSessionTemplate(DataSource source) throws Exception {
    SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
    bean.setDataSource(source);
    return new SqlSessionTemplate(bean.getObject());
}
```

后面就可以 `getBean(SqlSessionTemplate)`。

## HikariCP 连接池

POM 导入 `HikariCP`（ver：5.0.1，groupId：`com.zaxxer`）。

将前面的 `dataSource` 换为 `HikariDataSource` 即可。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-23-0.png]]

## MyBatis 事务管理

来看看存在的问题：

- **读未提交**：最后事务 B 出现问题发生回滚，但这时事务 A 获取的是未更新的数据（毫无意义的数据），即是脏读。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-25-1.png]]

- **读已提交**：如果事件 B 修改并提交了数据，那么实际上事务 A 之前读取到的数据依然不是最新的数据，直接导致两次读取的数据不一致，这种现象称为**虚读**或**不可重复读**。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-27-2.png]]

- **可重复读（MySQL 默认）**：这里仅仅是禁止了事务执行过程中的 UPDATE 操作，但是它并没有禁止 INSERT 这类操作，因此，如果事务 A 执行过程中事务 B 插入了新的数据，那么 A 这时是毫不知情的，这就是**幻读**。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-32-3.png]]

总结就是：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-34-4.png]]

## Spring 事务管理

`<environment>` 下的 `<transaction>` 即是管理事务，分为两种：

- **JDBC**：使用 JDBC 的事务管理机制，即利用对应数据库的驱动生成的 `Connection` 对象完成事务操作。
- **MANAGED**：让程序容器来实现对事务的管理。

在配置类打上 `@EnableTransactionManagement` 启用。

写上：

```java
@Bean
public TransactionManager transactionManager(DataSource dataSource) {
    return new DataSourceTransactionManager(dataSource);
}
```

便可以使用了。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-36-5.png]]

详细看下 `@Transactional`：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-37-6.png]]

如果这个事务方法调用了另一个事务方法，此时事务传播规则生效。事务的传播规则如下：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-39-7.png]]

## JUnit 整合

Spring 提供了 Test 模块，会自动集成 JUnit 进行测试，导入：

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>6.2.11</version>
</dependency>
```

然后测试类打上：

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = 配置类.class)
```

然后这个类就可以直接 `@Test` 运行，使用自动装配。