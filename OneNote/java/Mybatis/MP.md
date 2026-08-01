---
title: MP
tags: [java, Mybatis]
aliases: [MP]
---

# MP

## 导入

`mybatis-plus-spring-boot3-starter` / `mybatis-plus-spring-boot4-starter`

## 快速使用

依然是实体类,可以直接映射到数据库中的表:

```java
@Data
@TableName("user")
public class User {
    @TableId(type = IdType.AUTO)
    int id;

    @TableField("username")
    String name;

    @TableField("password")
    String password;
}
```

然后是 mapper:

```java
@Mapper
public interface UserMapper extends BaseMapper<User> {
    // 使用方式与 JPA 极为相似,也一样预设了大量的方法
}
```