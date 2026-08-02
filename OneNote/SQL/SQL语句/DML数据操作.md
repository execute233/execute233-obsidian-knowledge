---
title: DML 数据操作
tags: [SQL, SQL语句]
aliases: [DML数据操作]
---

# DML数据操作

## 插入数据

通过使用 `INSERT INTO` 语句来向数据库中插入一条数据(一条记录):

```sql
INSERT INTO 表名 VALUES (值1, 值2, 值3);
```

如果插入的数据与列一一对应,那么可以省略列名;如果希望向指定列上插入数据,就需要给出列名:

```sql
INSERT INTO 表名(列名1, 列名2) VALUES (值1, 值2);
```

也可以一次性向数据库中插入多条数据:

```sql
INSERT INTO 表名(列名1, 列名2) VALUES (值1, 值2), (值1, 值2), (值1, 值2);
```

## 修改数据

我们可以通过 `UPDATE` 语句来更新表中的数据:

```sql
UPDATE 表名 SET 列名 = 值… WHERE 条件;
```

## 删除数据

```sql
DELETE FROM 表名 WHERE 条件;
```