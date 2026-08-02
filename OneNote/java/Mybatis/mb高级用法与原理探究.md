---
title: mb高级用法与原理探究
tags: [java, Mybatis]
aliases: [mb高级用法与原理探究]
---

# mb高级用法与原理探究

## 类型处理器

从数据库的数据类型到 Java 的一些数据类型,Mybatis 都自定义好了,而对于我们自定义的类型,需要自定义 Handler,可以这样定义:

```java
@MappedJdbcTypes(JdbcType.VARCHAR) // 要打上注解,声明接受什么数据库的类型
class MyTypeHandler extends BaseTypeHandler<MyType> {
    // 继承,设置自定义处理器,泛型是要处理的 Java 类型
}
```

要重写以下方法:

```java
// 将非空的 Java 类型参数转换为 JDBC 类型并设置到 PreparedStatement 中
void setNonNullParameter(PreparedStatement ps, int i, Student parameter, JdbcType jdbcType);

// 根据列名从 ResultSet 中获取值并转换为 Java 类型
Student getNullableResult(ResultSet rs, String columnName);

// 根据列索引从 ResultSet 中获取值并转换为 Java 类型
Student getNullableResult(ResultSet rs, int columnIndex);

// 从 CallableStatement(存储过程)中根据列索引获取值并转换为 Java 类型
Student getNullableResult(CallableStatement cs, int columnIndex);
```

然后应用 Handler:

**XML 方式**: 在 `<configuration>` 里的 `<typeHandlers>` 下打 `<typeHandler>`。

**注解方式**: 在 `@Result` 里配置 `typeHandler` 属性。
