# DML数据操作

1. 插入数据 3. 修改数据
4. 删除数据

通过使用INSTERT INTO语句来向数据库中插入一条数据（一条记录）
INSERT INTO 表名 VALUES(值1，值2，值3）
如果插入的数据与列一一对应，那么可以省略列名，但是如果希望向指定列上插入数据，就需要给出列名
INSERT INTO表名（列名1，列名2) VALUES (值1，值2);
我们也可以一次性向数据库中插入多条数据．
INSERT INTO 表名（列名1，列名2）VALUES (值1，值2）,（值1，值2），（值1，值2)

我们可以通过UPDATE语句来更新表中的数据
UPDATE 表名 SET 列名=值… WHERE 条件
DELETE FROM 表名 WHERE 条件