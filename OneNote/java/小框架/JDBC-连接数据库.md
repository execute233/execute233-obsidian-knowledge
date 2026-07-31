1. 从maven导入一般是
2. 查看依赖是否导入成功
3. 创建一个数据库的链接，从DriverManager中获取
4. 不清楚的SQL操作情况下

```xml
\<dependency\>
    \<groupId\>com.mysql\</groupId\>
    \<artifactId\>mysql-connector-j\</artifactId\>
    \<version\>9.4.0\</version\>
\</dependency\>
// Drivernager是管理数据驱动的工具类，我们可以通过它来查看当前已经引入的驱动列表
DriverManagerdrivers().forEach(System.out::println);
Connection con = DriverManager.getConnection("连接URL", "用户名", "密码"); // 一般用try-with-resource包围
// 连接URL一般是这样 jdbc:mysql://localhost:3306/study
Statement statement = con.createStatement() // 获取Statement对象，这也一般用try-with-resource包围
// 使用executeQuery来执行一个查询SQL语句
ResultSet set = statement.executeQuery("select * from user");//选择user表全部内容
// 这个ResultSet是个迭代器，类似于游标，一般这样遍历如
while(set.next()) {
System.out.println(set.getXXX("name"));
}
// 注意执行下一个execute语句获得ResultSet对象后，之前的ResultSet对象会被关闭,无法使用
// 也可以执行添加 修改 删除操作，返回的是修改的行数
statement.executeUpdate("xxx");
直接使用
boolean statement.execute("xxx")； // 如果得到ResultSet对象，则返回true，更新计数或无结果则为false
// 在这之后可使用statement.getResultSet()主动获取
```