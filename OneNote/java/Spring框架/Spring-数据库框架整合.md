---
title: Spring-数据库框架整合
tags: [java, Spring框架]
aliases: [Spring-数据库框架整合]
---

# Spring-数据库框架整合

## 整合 Mybatis 框架

Spring 整合 MyBatis 的详细配置步骤可参考 [[mb使用]]。底层 JDBC 连接通过 [[JDBC-连接数据库]] 实现。

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

## MyBatis 事务管理

来看看存在的问题：

当两个事务同时在执行，并且同时在操作同一个数据，这样很容易出现并发相关的问题，比如一个事务先读取了某条数据，而另一个事务此时修改了此数据，当前一个事务紧接着再次读取时，会导致和前一次读取的数据不一致，这就是一种典型的数据虚读现象。

因此，为了解决这些问题，事务之间实际上是存在一些隔离级别的：

- `ISOLATION_READ_UNCOMMITTED`（读未提交）：其他事务会读取当前事务尚未更改的提交（相当于读取的是这个事务暂时缓存的内容，并不是数据库中的内容）。
- `ISOLATION_READ_COMMITTED`（读已提交）：其他事务会读取当前事务已经提交的数据（也就是直接读取数据库中已经发生更改的内容）。
- `ISOLATION_REPEATABLE_READ`（可重复读）：其他事务会读取当前事务已经提交的数据并且其他事务执行过程中不允许再进行数据修改（注意这里仅仅是不允许修改数据）。
- `ISOLATION_SERIALIZABLE`（串行化）：它完全服从 ACID 原则，一个事务必须等待其他事务结束之后才能开始执行，相当于挨个执行，效率很低。

- **读未提交**：最后事务 B 出现问题发生回滚，但这时事务 A 获取的是未更新的数据（毫无意义的数据），即是脏读。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-25-1.png]]

- **读已提交**：如果事件 B 修改并提交了数据，那么实际上事务 A 之前读取到的数据依然不是最新的数据，直接导致两次读取的数据不一致，这种现象称为**虚读**或**不可重复读**。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-27-2.png]]

- **可重复读（MySQL 默认）**：这里仅仅是禁止了事务执行过程中的 UPDATE 操作，但是它并没有禁止 INSERT 这类操作，因此，如果事务 A 执行过程中事务 B 插入了新的数据，那么 A 这时是毫不知情的，这就是**幻读**。

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-32-3.png]]

总结就是：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---|---|---|---|
| 读未提交 | 可能 | 可能 | 可能 |
| 读已提交 | 不可能 | 可能 | 可能 |
| 可重复读 | 不可能 | 不可能 | 可能 |
| 串行化 | 不可能 | 不可能 | 不可能 |

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

代码示例：

```java
@Component
public class TestServiceImpl implements TestService {

    @Resource
    TestMapper mapper;

    @Transactional   // 此注解表示事务，之后执行的所有方法都会在同一个事务中执行
    public void test() {
        mapper.insertStudent();
        if(true) throw new RuntimeException("我是测试异常！");
        mapper.insertStudent();
    }
}
```

详细看下 `@Transactional`：

- `transactionManager`：指定事务管理器。
- `propagation`：事务传播规则，一个事务可以包括 N 个子事务。
- `isolation`：事务隔离级别，不多说了。
- `timeout`：事务超时时间。
- `readOnly`：是否为只读事务，不同的数据库会根据只读属性进行优化，比如 MySQL 一旦声明事务为只读，那么久不允许增删改操作了。
- `rollbackFor` 和 `noRollbackFor`：发生指定异常时回滚或是不回滚，默认发生任何异常都回滚。

如果这个事务方法调用了另一个事务方法，此时事务传播规则生效。事务的传播规则如下：

| 传播行为 | 说明 |
|---|---|
| `PROPAGATION_REQUIRED` | 表示当前方法必须运行在事务中。如果当前事务存在，方法将会在该事务中运行。否则，会启动一个新的事务。 |
| `PROPAGATION_SUPPORTS` | 表示当前方法不需要事务上下文，但是如果存在当前事务的话，那么该方法会在这个事务中运行。 |
| `PROPAGATION_MANDATORY` | 表示该方法必须在事务中运行，如果当前事务不存在，则会抛出一个异常。 |
| `PROPAGATION_REQUIRED_NEW` | 表示当前方法必须运行在它自己的事务中。一个新的事务将被启动。如果存在当前事务，在该方法执行期间，当前事务会被挂起。如果使用 JTA TransactionManager 的话，则需要访问 TransactionManager。 |
| `PROPAGATION_NOT_SUPPORTED` | 表示该方法不应该运行在事务中。如果存在当前事务，在该方法运行期间，当前事务将被挂起。如果使用 JTA TransactionManager 的话，则需要访问 TransactionManager。 |
| `PROPAGATION_NEVER` | 表示当前方法不应该运行在事务上下文中。如果当前正有一个事务在运行，则会抛出异常。 |
| `PROPAGATION_NESTED` | 表示如果当前已经存在一个事务，那么该方法将会在嵌套事务中运行。嵌套的事务可以独立于当前事务进行单独地提交或回滚。如果当前事务不存在，那么其行为与 `PROPAGATION_REQUIRED` 一样。注意各厂商对这种传播行为的支持是有所差异的，可以参考资源管理器的文档来确认它们是否支持嵌套事务。 |

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