![[JDBC-事务操作__09-24-43-0.png]]

JDBC默认的事务处理行为是自动提交，所以执行一个SQL语句就会被直接提交（相当于没有启动事务）  
首先关闭自动提交  
connection.setAutoCommit(false)  
然后执行SQL操作，但这些操作不会立马更新  
xxx  
最后提交，前面的操作就会更新  
connection.commit()