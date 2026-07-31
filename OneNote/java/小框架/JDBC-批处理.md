# JDBC-批处理

```java
多次执行SQL语句插入会造成网络开销，可以将批量插入操作封装，如
for (…) {
statemen.addBatch("insert into user (name, age) values ('" + user + "', 18)");
}
int[] results = statement.executeBatch(); // 统一执行处理
```