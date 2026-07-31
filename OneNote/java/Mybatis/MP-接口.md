---
title: MP-接口
tags: [java, Mybatis]
aliases: [MP-接口]
---

# MP-接口

虽然使用MybatisPIus提供的BaseMapper已经很方便了，但是我们的业务中，实际上很多时候也是一样的工作，都是去简单调用底层的Mapper做一个很简单的事情，那么能不能干脆把Service也给弄个模版？MybatisPlus为我们提供了很方便的CRUD接囗，直接实现了各种业务中会用到的增删改查操作。
只需要继承即可：
```python
@Service
public interface UserService extends IService<User> {
```
// 除了继承模版，也可以把它当成普通Service添加自己需要的方法
}
还要编写对应的实现类：
```python
@Service // 需要继承ServiceImpl才能实现默认的CRUD方法
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
```

}