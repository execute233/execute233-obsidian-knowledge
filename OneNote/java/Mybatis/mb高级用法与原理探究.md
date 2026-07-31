# mb高级用法与原理探究

1. 类型处理器

从数据库的数据类型到java的一些数据类型，mybatis都自定义好了，而对于我们自定义的类型，需要自定义Handler，可以这样定义
```python
@MappedJdbcTypes(JdbcType.VARCHAR) // 要打上注解，声明接受什么数据库的类型
class MyTypeHandler extends BaseTypeHandler<MyType> {} // 继承，设置自定义处理器，泛型是要处理的java类型
```
要重写以下方法：
// 将非空的Java类型参数转换为JDBC类型并设置到PreparedStatement中
void setNonNullParameter(PreparedStatement ps, int i, Student parameter, JdbcType jdbcType)
// 根据列名从ResultSet中获取值并转换为Java类型
Student getNullableResult(ResultSet rs, String columnName)
// 根据列索引从ResultSet中获取值并转换为Java类型
Student getNullableResult(ResultSet rs, int columnIndex)
// 从CallableStatement（存储过程）中根据列索引获取值并转换为Java类型
Student getNullableResult(CallableStatement cs, int columnIndex)
然后应用Handler：
XML：
<configuration>里打<typeHandlers>打<typeHandler>
注解:
@Result里配置typeHandler属性