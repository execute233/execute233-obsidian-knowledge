# SpringBoot-JPA

导入
spring-boot-starter-data-jpa(默认使用hibernate)
快速上手
我们可以通过注解的形式，在属性上添加数据库映射关系，比如：
@Data
@Entity // 表示这个类是一个实体类
@Table(name = "user") // 对应数据库中表的名称
public class Account {
@GeneratedValue(strategy = GenerationType._IDENTITY_) // 生成策略，这里为自增
@Column(name = "id") // 对应表中id这一列
@Id // 主键
int id;
@Column(name = "username") // 表中的username这一列
String username;
@Column(name = "password")
String password;
}
可以在配置文件中设置表定义：
spring.jpa.hibernate.ddl-auto:
none - 不进行任何操作
create - 每次运行时删除所有表，并重新创建
create-drop - 每次运行时删除所有表，然后再创建，但程序结束时会再次删除所有表
update - 会检查表结构，不匹配就会修改
validate - 检查表结构是否匹配，不匹配则跑异常
可以这样管理表（已自动注册为Bean）：
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {}
就可以自动装配调用此Bean的方法了
方法名称拼接自定义SQL
我们可以在这样的接口里写上有规则的名称，这样的有规则名称会自动转为SQL语句，比如有以下这些方式

|   |   |   |
|---|---|---|
|属性|拼接方法名称示例|执行语句|
|Distinct|findDistinctByLastnameAndFirstname|select distinct… where x.lastname = ?1 and x.firstname = ?2|
|And|findByLastnameAndFirstname|… where x.lastname = ?1 and x.firstname = ?2|
|Or|findByLastnameOrFirstname|… where x.lastname = ?1 or x.firstname = ?2|
|Is, Equals|findByFirstname, findByFirstnameIs, findByFirstnameEquals|… where x.firstname = ?1|
|Between|findByStartDateBetween|… where x.startDte between ?1 and ?2|
|LessThan|findByAgeLessThan|… where x.age < ?1|
|LessThanEauals|…|… where x.age <= ?1|
|GreatThan|findByageGreaterThan|… where x.age > ?1|
|GreatThanEqual|…|… where x.age >= ?1|
|After|findByStartDateAfter|… where x.startDate > ?1|
|Before|…|…|
|IsNull, Null|findByage(Is)Null|… where x.age is null|
|IsNotNull, NotNull|…|…|
|Like|findByFirstnameLike|… whre x.firstname like ?1|
|NotLike|…|…|
|StartingWith|finByFirstnameStartingWith|… where x.firstname like ?1 (参数与附加%绑定)|
|EndingWith|…|…|

关联查询
我们知道，在JPA中，每张表实际上就是一个实体类的映射，而表之间的关联关系，也可以看作对象之间的依赖关系，比如用户表中包含了用户详细信息的ID字段作为外键，那么实际上就是用户表实体中包括了用户详细信息实体对象：
@Data
@Entity
@Table(name = "user_detail")
public class UserDetail {
@Id
@GeneratedValue(strategy = GenerationType._IDENTITY_)
@Column(name = "id")
int id;
@Column(name = "email")
String email;
@Column(name = "phone")
String phone;
}
我们可以在User类里直接写UserDetail的属性，声明@JoinColumn(name = 存储外键的名称)，同时可以@OneToOne等指明两张表的关系，比如：
@JoinColumn(name = "id") // 外键列，关联到UserDetail表的id
@OneToOne // 一对一关联
UserDetail detail;
如果想要像User对象已有的USerDetail一样，已有User可以执行插入两张表的数据，我们需要设置级联关联操作
@OneToONe有个属性cascade,指定其属性：
ALL - 所有操作都进行关联操作
PERSIST - 插入操作才进行关联操作
REMOVE - 删除操作才进行关联操作
MERGE - 修改操作才进行关联操作
JPQL自定义SQL

使用JPA我们也可以像Mybatis那样，直接编写SQL语句，不过它是JPQL语言，与原生SQL语句很类似，但是它是面向对象的，当然我们也可以写原生SQL语句。
比如我们要更新用户表中指定ID用户的密码：
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
@Transactional // DML需要事务环境，可以不在这声明，但调用必须在事务环境下
@Modifying // 表示DML操作
@Query("==update User set password = ?1 where id = ?2==") // 这里操作的是一个实体类对应的表，参数使用?代表，后面接第n个参数
int updatePasswordById(String password, Integer id);
}
现在使用原生SQL语句：
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
@Transactional // DML需要事务环境，可以不在这声明，但调用必须在事务环境下
@Modifying // 表示DML操作
// 使用原生SQL，和Mybatis一样
@Query(value = "==update User set password = :pwd where id = :id==", nativeQuery = true)
int updatePasswordById(@Param("pws") String password, // 可以使用@Param指定名称
@Param("id") Integer id);
}