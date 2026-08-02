---
title: JDBC-批处理
tags: [java, 小框架]
aliases: [JDBC-批处理]
---

# JDBC-批处理

多次执行 SQL 语句插入会造成网络开销,可以将批量插入操作封装:

```java
// 批量添加 SQL 语句
for (int i = 0; i < users.size(); i++) {
    statement.addBatch(
        "insert into user (name, age) values ('" + users.get(i) + "', 18)");
}

// 统一执行处理
int[] results = statement.executeBatch();
```
