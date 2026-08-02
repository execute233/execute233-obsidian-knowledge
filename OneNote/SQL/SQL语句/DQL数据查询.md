---
title: DQL 数据查询
tags: [SQL, SQL语句]
aliases: [DQL数据查询]
---

# DQL数据查询

## 单表查询

```sql
SELECT [ALL|DISTINCT] <column> [AS name] [{, <column2> [AS name2]}]
FROM table|view [AS name]
[WHERE …]
[GROUP BY column [HAVING …]]
[ORDER BY column [ASC|DESC]]
[LIMIT count];
```

### 基础查询

```sql
-- 指定某一列数据
SELECT 列名[, 列名] FROM 表名;

-- 以别名显示此列
SELECT 列名 别名 FROM 表名;

-- 查询所有的列数据
SELECT * FROM 表名;

-- 只查询不重复的值
SELECT DISTINCT 列名 FROM 表名;
```

### WHERE 条件

|类型|说明|
|---|---|
|比较运算符|`=`、`>`、`<`、`>=`、`<=`|
|是否在集合中|`IN`、`NOT IN`|
|字符模糊匹配|`LIKE`、`NOT LIKE`|

可以有的通配符:

|通配符|说明|
|---|---|
|`%`|0 个或多个字符|
|`_`|一个字符|
|`[]`|某个范围内的字符|
|`[^]`|不在某个范围内的字符|

多重条件连接查询:`AND`、`OR`、`NOT`。

也可以将结果排序,优先按照要求的列开始排序:

```sql
ORDER BY 列名1 ASC|DESC [, 列名2 ASC|DESC]
```

## 聚焦函数

聚集函数一般用作统计,包括:

|函数|说明|
|---|---|
|`count([distinct] *)`|统计所有的行数(distinct 表示去重再统计,下同)|
|`count([distinct] 列名)`|统计某列的值总和|
|`sum([distinct] 列名)`|求一列的和(注意必须是数字型的)|
|`avg([distinct] 列名)`|求一列的平均值(注意必须是数字类型)|
|`max([distinct] 列名)`|求一列的最大值|
|`min([distinct] 列名)`|求一列的最小值|

一般聚集函数是这样使用的:

```sql
SELECT count(distinct 列名) FROM 表名 WHERE 条件;
```

## 分组和分页查询

通过使用 `GROUP BY` 来对查询结果进行分组,它需要结合聚合函数一起使用:

```sql
SELECT sum(*) FROM 表名 WHERE 条件 GROUP BY 列名;
```

我们还可以添加 `HAVING` 来限制分组条件:

```sql
SELECT sum(*) FROM 表名 WHERE 条件 GROUP BY 列名 HAVING 约束条件;
```

我们可以通过 `LIMIT` 来限制查询数量,只取前 n 个结果:

```sql
SELECT * FROM 表名 LIMIT 数量;
```

也可以进行分页:

```sql
SELECT * FROM 表名 LIMIT 起始位置, 数量;
```

## 多表查询

多表查询是同时查询两个或两个以上的表,得到两张表的笛卡尔积,多表查询会通过连接转换为单表查询:

```sql
SELECT * FROM 表1 [name1] [how_join] 表2 [name2] ON 条件;
```

注意:如果两个表中都带有此属性,需要添加表名前缀来指明是哪一个表的数据。

## 自身连接查询

自身连接,就是将表本身和表进行笛卡尔积计算,得到结果,但是由于表名相同,因此要先起一个别名:

```sql
SELECT * FROM 表名 别名1, 表名 别名2;
```

其实自身连接查询和前面的是一样的,只是连接对象变成自己和自己了。

## 外连接查询

外连接就是专门用于联合查询情景的,比如现在有一个存储所有用户的表,还有一张用户详细信息的表,我希望将这两张表结合起来查看完整的数据,我们就可以通过使用外连接来进行,外连接有三种方式:

- **内连接**:返回两个表满足条件的交集部分。
- **左连接**:不仅会返回两个表满足条件的交集部分,也会返回左边表中的全部数据,而在右表中缺失的数据会使用 `NULL` 来代替。
- **右连接**:方式与左连接相似。

```sql
SELECT * FROM 表1 INNER JOIN 表2 ON 条件;
SELECT * FROM 左表 LEFT JOIN 右表 ON 条件;
SELECT * FROM 左表 RIGHT JOIN 右表 ON 条件;
```

## 嵌套查询

可以根据另一个 SQL 语句的查询结果作为条件输入:

```sql
SELECT * FROM 表 WHERE 键 = (SELECT 键 FROM 表);
```

这里的条件判断必须返回一个查询结果,若返回多个查询结果可用:

```sql
SELECT * FROM 表 WHERE 键 IN (SELECT 键 FROM 表);
```

使用 `UNION` 来对两个表查询的结果去重,比如对用户表和商家表的城市全部提取出来,并去重:

```sql
SELECT city FROM customers UNION SELECT city FROM suppliers;
```