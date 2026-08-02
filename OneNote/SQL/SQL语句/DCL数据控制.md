---
title: DCL 数据控制
tags: [SQL, SQL语句]
aliases: [DCL数据控制]
---

# DCL数据控制

> 用户授权与权限管理建立在 [[SQL语句/DDL数据定义|DDL数据定义]] 创建的库表之上;MySQL 用户概念对应 Linux 用户,详见 [[liunx/linux命令/用户 用户组 权限|用户 用户组 权限]]。

## 创建用户

可以通过 `CREATE USER` 来创建用户:

```sql
CREATE USER 用户名 [@限制IP] [IDENTIFIED BY 密码];
```

`%` 表示匹配所有的 IP 地址。

## 用户授权

我们可以通过使用 `GRANT` 来为一个数据库用户进行授权:

```sql
GRANT ALL|权限1, 权限2…(列1, 列2…) ON 数据库.* TO 用户 [WITH GRANT OPTION];
```

还可以用 `REVOKE` 收回权限:

```sql
REVOKE 权限1, 权限2…(列1, …) ON 数据库.表 FROM 用户;
```
