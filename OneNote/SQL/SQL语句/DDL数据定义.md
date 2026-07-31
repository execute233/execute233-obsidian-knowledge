1. 数据库操作
2. 数据表操作

查询所有数据库  
SHOW DATABASES;  
查询当前数据库  
SELECT DATABASE;  
创建数据库  
CREATE DATABASE [IF NOT EXISTS] db_name [[DEFAULT] CHARSET charset_name] [[DEFAULT] COLLATE collation_name];  
修改数据库  
CREATE DATABASE [IF NOT EXISTS] db_name [[DEFAULT] CHARSET charset_name] [[DEFAULT] COLLATE collation_name];  
删除数据库  
DROP DATABASE [IF EXISTS] db_name;  
使用数据库  
USE db_name;  
查询当前数据库所有表  
SHOWTABLES;  
查询表结构  
DESCRIBE/DESC 表名;  
查洵指定表的建表语句  
SHOW CREATETABLE 表名;  
创建表  
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] table (列名 数据类型[列级约束条件]，  
column_name1 type [DEFAULT] [AUTO_INCREMENT] [COMMENT ' '] [{\<列约束\>}] ,  
…  
) [table_option] [select_statement];
 
列级约束：  
默认值 DEFAULT  
主键 PRIMARY KEY  
外键 FOREIGN KEY (column) REFERENCES other_table other_column  
唯一 UNIQUE  
检查 CHECK（MySQL不支持）  
非空／空值 NOT NULL/NULL  
表级约束有四种：主键、外键、唯一、检查
 
比如  
CREATE TABLE goods (  
id int comment '编号',  
name varchar(32) comment '商品名'  
);  
其中COMMENT是备注  
添加字段  
ALTER TABLE table ADD column_name… type [AFTER other_column] [COMMENT] [约束]；  
修改数据类型  
ALTER TABLE table MODIFY column_name new_type;  
修改字段名和字段类型  
ALTER TABLE table CHANGE old_column new_column type [COMMENT] [约束]；  
修改类型和排序  
ALTER TABLE table MODIFY column type [FIRST | AFTER other_column]  
删除字段  
ALTE RTABLE table DROP column；  
修改表名  
ALTER TABLE table RENAME TO new_table；  
修改表的存储引擎  
ALTER TABLE table ENGINE=engine_name;  
删除表字段  
ALTER TABLE table DROP column[, DROP other_column]；  
删除字段完整性约束  
ALTER TABLE table DROP CONSTRAINT \<约束名\>；  
删除主键只需  
ALTER TABLE table DROP PRIMARY KEY;  
删除NOT NULL字段需  
ALTER TABLE table CHANGE column type NULL;  
删除表  
DROP TABLE [IF EXISTS] table;  
删除指定表，并重新创建该表  
TRUNCATE TABLE table；