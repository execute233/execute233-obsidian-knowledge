---
title: 有用的 SQL
tags: [SQL, SQL语句]
aliases: [有用的SQL]
---

# 有用的SQL

## 统计表中某列出现元素的数量

```sql
-- 可以这样写
SELECT email, count(email) AS num FROM Person GROUP BY email;

-- 比如这里就是筛选列中重复的元素
SELECT email FROM
    (SELECT email, count(email) AS num FROM Person GROUP BY email) AS tmp
WHERE num > 1;
```