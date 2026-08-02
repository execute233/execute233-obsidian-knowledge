---
title: mb使用
tags: [java, Mybatis]
aliases: [mb使用]
---

# mb使用

## 配置

1. 先用 SqlSessionFactoryBuilder 导入配置文件
2. 得到 SqlSessionFactory 后,就可以 openSession,但要自己关闭,可用 try-with-resource
3. 要在配置文件里引用 mapper
4. 编写 mapper.xml,一般格式是这样的

配置用的是 xml 文件,文件一般是这个内容:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${driver}"/>
                <property name="url" value="jdbc:mysql://…:3306/…"/>
                <property name="username" value="${mysql.username}"/>
                <property name="password" value="${mysql.password}"/>
            </dataSource>
        </environment>
    </environments>
</configuration>
```

SqlSessionFactory 通过 `build()` 方法创建:

```java
// 输入是 xml 文件
SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(inputStream);
// 可以指定环境
SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(inputStream, environment);
```

SqlSession 中有很多方法可以使用。

## 使用

由于 Mybatis 并不知道具体需要执行的 SQL 语句,以及需要返回哪些数据作为结果,因此同样需要编写 mapper 配置文件。

在 `<configuration>` 中通过 `<mappers>` 下的 `<mapper>` 指定 mapper 文件,属性有 `class`、`resource`、`url`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="testMapper">
    <select id="selectStudent" parameterType="int" resultType="你的实体类">
        SELECT * FROM user WHERE id = #{id}
    </select>
</mapper>
```
