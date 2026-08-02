---
title: MP-条件构造器
tags: [java, Mybatis]
aliases: [MP-条件构造器]
---

# MP-条件构造器

对于复杂查询,可以构造 QueryWrapper 用于复杂查询:

```java
QueryWrapper<User> wrapper = new QueryWrapper<>(); // 复杂查询使用此完成
wrapper.select("id", "username")                   // 可自定义哪些字段
    .ge("id", 2)                                   // 选择判断 id 大于等于 2 的所有数据
    .orderByDesc("id");                            // 按照 id 降序排列
mapper.selectList(wrapper);                        // Mapper 同样支持使用 QueryWrapper 查询
```

等价于下面的 SQL 语句:

```sql
select id, username from user where id >= 2 order by id desc
```

关联基础: [[MP]] 的 CRUD 操作通常只处理简单条件,复杂场景需要 QueryWrapper / LambdaQueryWrapper / UpdateWrapper 等构造器。

有很多方法可以使用,如 `eq`、`ne`、`gt`、`lt`、`like`、`between`、`isNull` 等。

有时候会遇到批处理的情况,比如快速删除多个指定用户:

```java
mapper.deleteBatchIds(Arrays.asList(1, 2, 3));
```

也可以快速进行分页操作,不过需要提前配置:

```java
Page<User> page = new Page<>(1, 10); // 第 1 页,每页 10 条
mapper.selectPage(page, null);
```
