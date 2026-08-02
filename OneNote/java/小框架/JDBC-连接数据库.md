---
title: JDBC-连接数据库
tags: [java, 小框架]
aliases: [JDBC-连接数据库]
---

# JDBC-连接数据库

## 从 Maven 导入

```xml
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <version>9.4.0</version>
</dependency>
```

## 查看依赖是否导入成功

```java
// DriverManager 是管理数据驱动的工具类,可以通过它来查看当前已经引入的驱动列表
DriverManager.drivers().forEach(System.out::println);
```

## 创建数据库连接

```java
// 从 DriverManager 中获取连接,一般用 try-with-resource 包围
Connection con = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/study", "用户名", "密码");
```

## 执行 SQL 操作

```java
// 获取 Statement 对象,这也一般用 try-with-resource 包围
Statement statement = con.createStatement();

// 使用 executeQuery 来执行一个查询 SQL 语句
ResultSet set = statement.executeQuery("select * from user");

// ResultSet 是个迭代器,类似于游标,一般这样遍历
while (set.next()) {
    System.out.println(set.getString("name"));
}

// 注意:执行下一个 execute 语句获得 ResultSet 对象后,之前的 ResultSet 对象会被关闭,无法使用
```

## 增删改操作

```java
// 执行添加、修改、删除操作,返回的是修改的行数
int rows = statement.executeUpdate("insert into user (name) values ('test')");
```

## 通用执行方法

```java
// 直接使用 execute,如果得到 ResultSet 对象则返回 true,更新计数或无结果则为 false
boolean hasResultSet = statement.execute("select * from user");

// 在这之后可使用 statement.getResultSet() 主动获取
if (hasResultSet) {
    ResultSet rs = statement.getResultSet();
}
```
