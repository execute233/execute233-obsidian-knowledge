对于复杂查询，可以构造QueryWrapper用于复杂查询：  
QueryWrapper\<User\> wrapper = Wrapper; // 复杂查询使用此完成  
wrapper.select("id", "username") // 可自定义哪些字段  
.ge("id", 2) // 选择判断id大于等于1的所有数据  
.orderByDesc("id"); // 按照id降序排列  
mapper.selectList(wrapper); // Mapper同样支持使用QueryWrapper查询  
等价于下面的SQL语句  
select id, username from user where id \>= 2 order by id desc  
有很多方法可以使用，如：
 
有时候会遇到批处理的情况，比如快速删除多个指定用户：
 
也可以快速进行分页操作，不过需要提前配置：