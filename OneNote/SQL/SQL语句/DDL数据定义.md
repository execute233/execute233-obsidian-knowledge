---
title: DDL 数据定义
tags: [SQL, SQL语句]
aliases: [DDL数据定义]
---

# DDL 数据定义

## 数据库操作

```sql
-- 查询所有数据库
SHOW DATABASES;

-- 查询当前数据库
SELECT DATABASE();

-- 创建数据库
CREATE DATABASE [IF NOT EXISTS] db_name [[DEFAULT] CHARSET charset_name] [[DEFAULT] COLLATE collation_name];

-- 修改数据库
ALTER DATABASE db_name [[DEFAULT] CHARSET charset_name] [[DEFAULT] COLLATE collation_name];

-- 删除数据库
DROP DATABASE [IF EXISTS] db_name;

-- 使用数据库
USE db_name;
```

## 数据表操作

```sql
-- 查询当前数据库所有表
SHOW TABLES;

-- 查询表结构
DESCRIBE 表名;
-- 或
DESC 表名;

-- 查询指定表的建表语句
SHOW CREATE TABLE 表名;
```

### 创建表

```sql
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] table (
    列名 数据类型 [列级约束条件],
    column_name1 type [DEFAULT] [AUTO_INCREMENT] [COMMENT ' '] [{<列约束>}],
    -- ...
) [table_option] [select_statement];
```

**列级约束**:

|约束|说明|
|---|---|
|`DEFAULT`|默认值|
|`PRIMARY KEY`|主键|
|`FOREIGN KEY (column) REFERENCES other_table(other_column)`|外键|
|`UNIQUE`|唯一|
|`CHECK ( ... )`|检查(MySQL 不支持)|
|`NOT NULL` / `NULL`|非空 / 空值|

表级约束有四种:主键、外键、唯一、检查。

例如:

```sql
CREATE TABLE goods (
    id   int         COMMENT '编号',
    name varchar(32) COMMENT '商品名'
);
```

其中 `COMMENT` 是备注。

### 修改字段

```sql
-- 添加字段
ALTER TABLE table ADD column_name… type [AFTER other_column] [COMMENT] [约束];

-- 修改数据类型
ALTER TABLE table MODIFY column_name new_type;

-- 修改字段名和字段类型
ALTER TABLE table CHANGE old_column new_column type [COMMENT] [约束];

-- 修改类型和排序
ALTER TABLE table MODIFY column type [FIRST | AFTER other_column];
```

### 删除字段

```sql
-- 删除字段
ALTER TABLE table DROP column;

-- 删除字段完整性约束
ALTER TABLE table DROP CONSTRAINT <约束名>;

-- 删除主键
ALTER TABLE table DROP PRIMARY KEY;

-- 删除 NOT NULL 字段
ALTER TABLE table CHANGE column type NULL;
```

### 修改表

```sql
-- 修改表名
ALTER TABLE table RENAME TO new_table;

-- 修改表的存储引擎
ALTER TABLE table ENGINE = engine_name;
```

### 删除表

```sql
-- 删除表
DROP TABLE [IF EXISTS] table;

-- 删除指定表,并重新创建该表
TRUNCATE TABLE table;
```