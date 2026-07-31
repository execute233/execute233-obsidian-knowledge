导入  
mybatis-plus-spring-boot3/4-starter  
快速使用  
依然是实体类，可以直接映射到数据库中的表  
@Data  
@TableName("user")  
public class User {  
@TableId(type = IdType._AUTO_)  
int id;  
@TableField("username")  
String name;  
@TableField("password")  
String password;  
}  
然后是mapper  
@Mapper  
public interface UserMapper extends BaseMapper\<User\> {  
// 使用方式与JPA极为相似，也一样预设了大量的方法  
}