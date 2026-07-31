---
title: mb详解
tags: [java, Mybatis]
aliases: [mb详解]
---

# mb详解

## 查询操作

```java
指定构造方法
```

```java
接口绑定
```

```java
复杂查询
```

```java
DML操作
```

```java
事务操作
```

7. 批处理（同时处理多条数据）
8. 动态SQL
9. 缓存机制

```java
注解开发
```

查询操作在XML配置中使用一个select标签进行囊括，，假设我们现在需要编写一个根据ID查询用户的操作，首先我们需要指定它的id，建议把id名称起的有代表性一点：
<select id="selectUserById"> </select>
这个标签还有parameterType属性，指定传入参数的类型（也可以不写，会自动判断）
如果是基本数据类型，前面加个_，如 _int
如果JDK内置类型，直接用类型名称，如 String
如果是自己写的类型，用自己类的全路径，如 org.example.User
接下来就是SQL语句，占位符是#{xxx}这样的形式，如
```xml
<select id="selectUserById" parameterType="_int" resultType=""或resultMap>
SELECT * FROM User WHERE id = #{id}
</select>
```
调用select方法后面接上参数就行了，多个参数使用Map.of（）指定相应的参数（传入实体类也行）
由于resultType要写全，写多个可能太累了，我们可在<configuration>里打<typeAliases>再打<typeAlias type="全包类名" alias="别名">
有时候SQL里获取的字段名与实体类字段名不匹配，那么这时候mybits自动封装成对象必须要有个映射表，那些不知道的字段会是默认值
需要在<select>里取消resultType，使用resultMap字段，值是resultMap的id
<resultMap>标签放在<mapper>里，id是对应的id，type是相应的java类，里面加<id column="数据库里的字段名" property="类的字段名">
这里对几个select方法解释：
selectList - 查询结果是一个列表，没有则是null
selectOne - 查询结果只有一个，多个则会报错
selectMap - 返回一个Map，指定的东西为key，对象为value
selectCursor - 返回Cursor对象，他是个迭代器对象，类似于JDBC里的游标
```sql
select - 用lambda处理ResultContext对象
在<mapper>中的<resultMap>中打<constructor>,这里面可以使用以下的单标签
```
<idArg> 主键才使用这个标签
column - 数据库中的键名
javaType - java类型
<arg> 对于非主键用的，用法同上
注意参数的顺序，必须和构造方法的顺序一致，否则会无法确认。指定构造方法后，若此字段被填入了构造方法作为参数，将不会通过反射给字段单独值，而构造方法中没有传入的字段，依然会被反射赋值。
首先需要一个接口，里面有各种数据库操作的抽象方法，如
```text
List<User> selectAllUser(); // 名字对应着配置文件中的id
List<User> selectUserById(int id) // 对应的语句就是用#{id}占位
然后通过session.getMapper(接口class对象)获得相应的接口,在调用接口即可(注意你还是得在mapper里写<select />,同时mapper的namespace属性是接口全路径名)
```
多参处理，要么SQL语句以#{param1}等等按传入参数顺序，要么使用@Param修饰传入参数
查询获得的对象内的字段，还包含另一个对象，这个对象也需要通过查询获得更多的详细数据
首先対<select>语句中的resultType替换为resultMap，新建一个resultMap
有两种不同的方式加载关联
SQL查询语句使用左连接
<resultMap/> 里打上<association/>，property是相应的对象字段名
不使用指定构造，使用<id><result>等标签在里面或外面打
嵌套select查询
只要在<association>指定属性select到其他的select语句即可
一对多
假设我们有user（用户信息）和book（图书借出信息）表
```yaml
User: int id, String name, int age, List<Book> books
Book: int bid, String title, int uid
我们选择左联表查询: select * from user left join book on user.id = book.uid wher id = #{id}
```
查询结果如：
id name age bid title uid
1 Jack 18 1 book1 1
1 Jack 18 1 book2 1
对于集合，只要在<resultMap>里使用<collection>，这些属性要填
property - 字段名
ofType - 集合的泛型类型
然后就可以在标签内填写对象相关的东西了，如<id>， <result>这些，以上面那个查询结果则该集合大小为2
```xml
对应的java操作则是使用delete update insert等方法,同时<mapper>里用相应的<delete> <update> <insert>标签,比如
<insert id="insertUser" parameterType="User">
insert into user (name, age) values (#{name}, #{age})
<insert>
```
由于字段名在运行时保存，可以直接使用#{name}， #{age}让其自动填充
也可以在接口中写int insertUser（@Param（"age"） int age， @Param（"name"） String name） 来
如果插入的表有自增主键时，我们需要配置以下属性来自动生成
useGeneratedKeys - 设置为true
keyColumn - 自增主键名
keyProperty - 类的主键参数字段名，SQL操作完成后数据会回写到这个字段
跟JDBC类似
启用批处理，只要使用 factory.opensession（ExecutorType.BATCH， autoCommit）
对于多次调用同一语句循环插入不同数据时，会优化为多个参数，启用批处理需要手动commit
动态SQL在执行时可以进行各种条件判断以及循环拼接等操作，极大地提升了SQL语句编写的的灵活性
比如我们希望在根据ID查询用户时，如果查询的ID大于3，那么必须同时要满足大于18岁这个条件

![[_assets/mb详解/mb详解__09-21-03-0.png]]

除了if操作之外，针对多分支情况提供了choose操作，它类似于Java中的switch语句，比如现在我们希望在查询用户时，ID等于1的必须同时要满足小于18岁，ID等于2的必须满足等于18岁，其他情况的必须满足大于18岁，我们可以像这样进行编写：（注意<要用&lt；转义）

![[_assets/mb详解/mb详解__09-21-05-1.png]]

我们也可以用for循环拼接，通常用在插入多条数据的时候

![[_assets/mb详解/mb详解__09-21-08-2.png]]

Mybatis存在一级缓存和二级缓存，一级缓存仅对一个会话中的数据进行缓存（一级缓存强制启用，无法关闭，只能做调整）也就是每一个SqlSession都有有一个对应的缓存，而二级缓存作用于整个Mapper
对于重复同样的操作，它不在会再次操作一次数据库，而是直接返回缓存的内容，但DML操作会清空当前Session的缓存
使用二级缓存（事务性的），需要在<mapper>里打<cache>，有以下属性
eviction - 清理策略
LRU - 最近最少使用：移除最长时间不被使用的对象。
FIFO - 先进先出：按对象进入缓存的顺序来移除它们。
SOFT - 软引用：基于垃圾回收器状态和软引用规则移除对象。
WEAK - 弱引用：更积极地基于垃圾收集器状态和弱引用规则移除对象。
flushInterval - 缓存刷新时间
size - 最大缓存数量
readOnly - 只读，设置为真的话相应的对象必须实现序列化接口
首先注解使用的接口要在<mappers>里面声明
如果使用了Spring，可以只配置@MapperScan
Mybatis提供了丰富的注解来开发，如@Select，SQL语句可直接写里面，返回类型不用写，可通过反射获取，比如
```python
@Select("select * from user")
List<User> selectAllUser();
@Insert("insert into user (name, age) values (#{name}, #{age})") #{这两个参数是会通过反射获取}
int insertUser(User user); // 对于自增主键要回写,还可以打 @Option(useGeneratedKeys=rue,keyColumn="id",keyproperty="id")
可以使用@Results([@Result(..), @Result(..)..], ont=@one())类似xml配置规定返回对象的字段设置,one就是关联查询,里面填select等字段指定方法名
还有@CopnstrutorArgs([@Arg(..), @Arg(..)..])
```
……