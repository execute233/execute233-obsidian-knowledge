---
title: mb详解
tags: [java, Mybatis]
aliases: [mb详解]
---

# mb详解

MyBatis 常用操作详见 [[mb使用]]。MyBatis-Plus 是在 MyBatis 基础上的增强工具,可简化 CRUD,详见 [[MP]]。

## 查询操作

查询操作在 XML 配置中使用一个 select 标签进行囊括,假设我们现在需要编写一个根据 ID 查询用户的操作,首先我们需要指定它的 id,建议把 id 名称起得有代表性一点:

```xml
<select id="selectUserById">
</select>
```

这个标签还有 `parameterType` 属性,指定传入参数的类型(也可以不写,会自动判断):

- 如果是基本数据类型,前面加个 `_`,如 `_int`
- 如果 JDK 内置类型,直接用类型名称,如 `String`
- 如果是自己写的类型,用自己类的全路径,如 `org.example.User`

接下来就是 SQL 语句,占位符是 `#{xxx}` 这样的形式,如:

```xml
<select id="selectUserById" parameterType="_int" resultType=""或resultMap>
    SELECT * FROM User WHERE id = #{id}
</select>
```

调用 select 方法后面接上参数就行了,多个参数使用 `Map.of()` 指定相应的参数(传入实体类也行)。

由于 `resultType` 要写全,写多个可能太累了,我们可在 `<configuration>` 里打 `<typeAliases>` 再打 `<typeAlias type="全包类名" alias="别名">`。

有时候 SQL 里获取的字段名与实体类字段名不匹配,那么这时候 Mybatis 自动封装成对象必须要有个映射表,那些不知道的字段会是默认值。需要在 `<select>` 里取消 `resultType`,使用 `resultMap` 字段,值是 `resultMap` 的 id。

`<resultMap>` 标签放在 `<mapper>` 里,id 是对应的 id,type 是相应的 Java 类,里面加 `<id column="数据库里的字段名" property="类的字段名">`。

这里对几个 select 方法解释:

- `selectList` — 查询结果是一个列表,没有则是 null
- `selectOne` — 查询结果只有一个,多个则会报错
- `selectMap` — 返回一个 Map,指定的东西为 key,对象为 value
- `selectCursor` — 返回 Cursor 对象,它是一个迭代器对象,类似于 JDBC 里的游标
- `select` — 用 lambda 处理 ResultContext 对象

## 指定构造方法

在 `<mapper>` 中的 `<resultMap>` 中打 `<constructor>`,这里面可以使用以下的单标签:

- `<idArg>` 主键才使用这个标签
  - `column` — 数据库中的键名
  - `javaType` — Java 类型
- `<arg>` 对于非主键用的,用法同上

注意参数的顺序,必须和构造方法的顺序一致,否则会无法确认。指定构造方法后,若此字段被填入了构造方法作为参数,将不会通过反射给字段单独值,而构造方法中没有传入的字段,依然会被反射赋值。

## 接口绑定

首先需要一个接口,里面有各种数据库操作的抽象方法,如:

```java
List<User> selectAllUser();          // 名字对应着配置文件中的 id
List<User> selectUserById(int id);   // 对应的语句就是用 #{id} 占位
```

然后通过 `session.getMapper(接口 class 对象)` 获得相应的接口,再调用接口即可(注意你还是得在 mapper 里写 `<select />`,同时 mapper 的 namespace 属性是接口全路径名)。

多参处理,要么 SQL 语句以 `#{param1}` 等等按传入参数顺序,要么使用 `@Param` 修饰传入参数。

## 复杂查询

查询获得的对象内的字段,还包含另一个对象,这个对象也需要通过查询获得更多的详细数据。

首先对 `<select>` 语句中的 `resultType` 替换为 `resultMap`,新建一个 resultMap。有两种不同的方式加载关联:

### 方式一: SQL 左连接

SQL 查询语句使用左连接。`<resultMap/>` 里打上 `<association/>`,property 是相应的对象字段名。不使用指定构造,使用 `<id>` `<result>` 等标签在里面或外面打。

### 方式二: 嵌套 select 查询

只要在 `<association>` 指定属性 select 到其他的 select 语句即可。

## 一对多

假设我们有 user(用户信息)和 book(图书借出信息)表:

```java
User: int id, String name, int age, List<Book> books
Book: int bid, String title, int uid
```

我们选择左联表查询:

```sql
select * from user left join book on user.id = book.uid where id = #{id}
```

查询结果如:

| id | name | age | bid | title | uid |
|---|---|---|---|---|---|
| 1 | Jack | 18 | 1 | book1 | 1 |
| 1 | Jack | 18 | 2 | book2 | 1 |

对于集合,只要在 `<resultMap>` 里使用 `<collection>`,这些属性要填:

- `property` — 字段名
- `ofType` — 集合的泛型类型

然后就可以在标签内填写对象相关的东西了,如 `<id>`、`<result>` 这些,以上面那个查询结果则该集合大小为 2。

## DML 操作

对应的 Java 操作则是使用 delete、update、insert 等方法,同时 `<mapper>` 里用相应的 `<delete>`、`<update>`、`<insert>` 标签,比如:

```xml
<insert id="insertUser" parameterType="User">
    insert into user (name, age) values (#{name}, #{age})
</insert>
```

由于字段名在运行时保存,可以直接使用 `#{name}`、`#{age}` 让其自动填充。也可以在接口中写:

```java
int insertUser(@Param("age") int age, @Param("name") String name);
```

如果插入的表有自增主键时,我们需要配置以下属性来自动生成:

- `useGeneratedKeys` — 设置为 true
- `keyColumn` — 自增主键名
- `keyProperty` — 类的主键参数字段名,SQL 操作完成后数据会回写到这个字段

## 事务操作

跟 JDBC 类似。

## 批处理

启用批处理,只要使用:

```java
SqlSession session = factory.openSession(ExecutorType.BATCH, autoCommit);
```

对于多次调用同一语句循环插入不同数据时,会优化为多个参数,启用批处理需要手动 commit。

## 动态 SQL

动态 SQL 在执行时可以进行各种条件判断以及循环拼接等操作,极大地提升了 SQL 语句编写的灵活性。

比如我们希望在根据 ID 查询用户时,如果查询的 ID 大于 3,那么必须同时要满足大于 18 岁这个条件:

```xml
<select id="selectUserById" resultType="User">
    select * from user where id = #{id}
    <if test="id > 3">
        and age > 18
    </if>
</select>
```

除了 if 操作之外,针对多分支情况提供了 choose 操作,它类似于 Java 中的 switch 语句,比如现在我们希望在查询用户时,ID 等于 1 的必须同时要满足小于 18 岁,ID 等于 2 的必须满足等于 18 岁,其他情况的必须满足大于 18 岁,我们可以像这样进行编写(注意 `<` 要用 `&lt;` 转义):

```xml
<select id="selectUserById" resultType="User">
    select * from user where id = #{id}
    <choose>
        <when test="id == 1">
            and age &lt;= 18
        </when>
        <when test="id == 2">
            and age = 18
        </when>
        <otherwise>
            and age > 18
        </otherwise>
    </choose>
</select>
```

我们也可以用 for 循环拼接,通常用在插入多条数据的时候:

```xml
<insert id="insertUsers">
    insert into user (name, age) values
    <foreach collection="list" item="item" separator=",">
        (#{item}, 18)
    </foreach>
</insert>
```

## 缓存机制

Mybatis 存在一级缓存和二级缓存,一级缓存仅对一个会话中的数据进行缓存(一级缓存强制启用,无法关闭,只能做调整),也就是每一个 SqlSession 都有一个对应的缓存,而二级缓存作用于整个 Mapper。

对于重复同样的操作,它不会再操作一次数据库,而是直接返回缓存的内容,但 DML 操作会清空当前 Session 的缓存。

使用二级缓存(事务性的),需要在 `<mapper>` 里打 `<cache>`,有以下属性:

- `eviction` — 清理策略:
  - `LRU` — 最近最少使用:移除最长时间不被使用的对象。
  - `FIFO` — 先进先出:按对象进入缓存的顺序来移除它们。
  - `SOFT` — 软引用:基于垃圾回收器状态和软引用规则移除对象。
  - `WEAK` — 弱引用:更积极地基于垃圾收集器状态和弱引用规则移除对象。
- `flushInterval` — 缓存刷新时间
- `size` — 最大缓存数量
- `readOnly` — 只读,设置为真的话相应的对象必须实现序列化接口

## 注解开发

首先注解使用的接口要在 `<mappers>` 里面声明。如果使用了 Spring,可以只配置 `@MapperScan`。

Mybatis 提供了丰富的注解来开发,如 `@Select`,SQL 语句可直接写里面,返回类型不用写,可通过反射获取,比如:

```java
@Select("select * from user")
List<User> selectAllUser();

@Insert("insert into user (name, age) values (#{name}, #{age})")
int insertUser(User user); // 对于自增主键要回写,还可以打 @Options(useGeneratedKeys=true, keyColumn="id", keyProperty="id")
```

可以使用 `@Results` 和 `@One` 类似 XML 配置规定返回对象的字段设置,`@One` 就是关联查询,里面填 select 等字段指定方法名。还有 `@ConstructorArgs`:

```java
@Results({
    @Result(column = "id", property = "id"),
    @Result(column = "uid", property = "user", one = @One(select = "selectUserById"))
})
```

……