---
title: mb使用
tags: [java, Mybatis]
aliases: [mb使用]
---

# mb使用

## 配置
## 使用
    1. 先用SqlSessionFactoryBuilder导入配置文件
    2. 得到SqlSessionFactory后，就可以openSession，但要自己关闭，可用try-with-resource
    3. 要在配置文件里引用mapper
    4. 编写mapper.xml，一般格式是这样的


配置用的是xml文件，文件一般是这个内容
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
"[http://mybatis.org/dtd/mybatis-3-config.dtd](http://mybatis.org/dtd/mybatis-3-config.dtd)">
<configuration>
<environments default="development">
<environment id="development">
<transactionManager type="JDBC"/>
<dataSource type="POOLED">
<property name="driver" value="${driver}"/>
<property name="url" value="jdbs:mysql://…:3306/…"/>
<property name="username" value="${mysql.username}"/>
<property name="password" value="${mysql.password}"/>
</dataSource>
</environment>
</environments>
</configuration>
build(各种输入流) // 输入是xml文件
build(各种输入流,String environment) // 指定环境
```
SqlSession中有很多方法可以使用
由于Mybatis并不知道具体需要执行的SQL语句，以及需要返回哪些数据作为结果，因此同样需要编写配置文件。
```xml
在<configuration>中打<mappers>打<mapper>指定mapper文件,属性有class,resource,url
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "[http://mybatis.org/dtd/mybatis-3-mapper.dtd](http://mybatis.org/dtd/mybatis-3-mapper.dtd)">
<mapper namespace="testMapper">
<select id="selectStudent" parameterType="int" resultType="你的实体类">
SELECT * FROM user WHERE id = #{id}
</select>
</mapper>
```