---
title: lombok
tags: [java, 小框架]
aliases: [lombok]
---

# lombok

## 类属性相关
## 构造方法相关
## 打印对象
## 比较对象
## @Data注解
## @Value注解
## 建造者模式
## 锁处理

自动生成Getter方法，修饰字段或类
@Getter（[accessLevel=AccessLevel.PUBLIC， onMethod=[]， lazy=false]）
accessLevel - 枚举，指生成的getter方法的访问级别
onMethod - 生成的getter的注解
lazy - 字段是否懒初始化
自动生成Getter方法，修饰字段或类
@Setter（[accessLevel=AccessLevel.PUBLIC， onMethod=[]， onParam=[]]）
accessLevel - 枚举，指生成的setter方法的访问级别
onMethod - 生成的setter的注解
onParam - 传入参数的注解

要注意，如果直接写了Getter和Setter，注解该字段的注解是不会生效的
自动生成包含所有字段的构造方法
@AllArgsConstructor（[staticName=""， onConstructor=[]， access=[]]）
staticName - 生成静态构造方法名，使用静态构造会封闭构造方法
onConstructor - 构造方法修饰注解
access - 访问权限
生成无参构造
@NoArgConstructor（[staticName=""， onConstructor=[]， access=[]， force = false]）
force - 强制使用无参构造，final字段会被赋值为默认值
其他参数与上面用法相同
生成包含final的字段的构造方法
@RequiredArgsConstructor
用于修饰类，为对象生成toString（）方法
@ToString（[includeFieldName=true， callSuper=false， doNotUseGetters=false， onlyExplicitIyIncIuded=false]）
includeFieldName - 是否包含字段名字
callSuper - 调用父类的toString拼接
doNotUseGetters - 不使用Getter获取字段
onlyExplicitIyIncIuded - 白名单，只为字段或get（）添加了@ToString.Included的生成ToString
自动生成类的比较方法与hashCode
@EqualsAndHashCode（callSuper=false， doNotUseGetters=false， cacheStrategy=EqualsAndHashCode.CacheStrategy.NEVER）
cacheStrategy - hashCode缓存
等价于有以下注解
```python
@Getter
@Setter
@RequiredArgsConstructor
@ToString
@EqualsAndHashCode
```
等价于有以下注解
```python
@Getter
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
@AllArgsConstructor
@ToString
@EqualsAndHashCode
```
生成建造者模式的类
@Builder
直接在方法里生成同步代码块
@Synchronized（锁名称）
不写锁名称就是这个对象拿着锁