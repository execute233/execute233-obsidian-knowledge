# 有用的SQL

1. 统计表中某列出现元素的数量

```sql
# 可以这样写
select email, count(email) as num from Person group by email
# 比如这里就是筛选列中重复的元素
select email from
(select email, count(email) as num from Person group by email) as tmp
where num > 1
```