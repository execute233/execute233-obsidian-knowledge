---
title: MP-接口
tags: [java, Mybatis]
aliases: [MP-接口]
---

# MP-接口

虽然使用 [[MP]] 中的 MybatisPlus 提供的 BaseMapper 已经很方便了,但是我们的业务中,实际上很多时候也是一样的工作,都是去简单调用底层的 Mapper 做一个很简单的事情,那么能不能干脆把 Service 也给弄个模板? MybatisPlus 为我们提供了很方便的 CRUD 接口,直接实现了各种业务中会用到的增删改查操作。只需要继承即可:

```java
@Service
public interface UserService extends IService<User> {
    // 除了继承模板,也可以把它当成普通 Service 添加自己需要的方法
}
```

还要编写对应的实现类:

```java
@Service // 需要继承 ServiceImpl 才能实现默认的 CRUD 方法
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

}
```
