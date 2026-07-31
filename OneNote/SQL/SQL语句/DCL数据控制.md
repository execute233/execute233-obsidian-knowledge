1. 创建用户
2. 用户授权

可以通过CREATE USER来创建用户。  
CREATE USER 用户名[@限制IP] [IDENTIFIED BY 密码]；  
％表示匹配所有的IP地址。
 
我们可以通过使用GRANT来为一个数据库用户进行授权：  
GRANT ALL|权限1，权限2…（列1，列2…) ON 数据库. TO 用户 [WITH GRANT OPTION]  
还可以用REVOKE收回权限  
REVOKE 权限1，权限2…(列1，…) ON 数据库.表 FROM 用户