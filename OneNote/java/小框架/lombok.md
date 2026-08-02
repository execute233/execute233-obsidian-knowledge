---
title: lombok
tags: [java, 小框架]
aliases: [lombok]
---

# lombok

lombok 通过注解在编译期自动生成样板代码,注解的语法与元注解机制可参考 [[java8新特性]],在 Spring 项目中的集成使用见 [[SpringBoot-Start]]。

## 类属性相关

自动生成 Getter 方法,修饰字段或类:

```java
@Getter(accessLevel = AccessLevel.PUBLIC, onMethod = {}, lazy = false)
```

- `accessLevel` — 枚举,指生成的 getter 方法的访问级别
- `onMethod` — 生成的 getter 的注解
- `lazy` — 字段是否懒初始化

自动生成 Setter 方法,修饰字段或类:

```java
@Setter(accessLevel = AccessLevel.PUBLIC, onMethod = {}, onParam = {})
```

- `accessLevel` — 枚举,指生成的 setter 方法的访问级别
- `onMethod` — 生成的 setter 的注解
- `onParam` — 传入参数的注解

要注意,如果直接写了 Getter 和 Setter,注解该字段的注解是不会生效的。

## 构造方法相关

自动生成包含所有字段的构造方法:

```java
@AllArgsConstructor(staticName = "", onConstructor = {}, access = AccessLevel.PUBLIC)
```

- `staticName` — 生成静态构造方法名,使用静态构造会封闭构造方法
- `onConstructor` — 构造方法修饰注解
- `access` — 访问权限

生成无参构造:

```java
@NoArgsConstructor(staticName = "", onConstructor = {}, access = AccessLevel.PUBLIC, force = false)
```

- `force` — 强制使用无参构造,final 字段会被赋值为默认值

生成包含 final 字段的构造方法:

```java
@RequiredArgsConstructor
```

## 打印对象

用于修饰类,为对象生成 `toString()` 方法:

```java
@ToString(includeFieldName = true, callSuper = false,
          doNotUseGetters = false, onlyExplicitlyIncluded = false)
```

- `includeFieldName` — 是否包含字段名字
- `callSuper` — 调用父类的 toString 拼接
- `doNotUseGetters` — 不使用 Getter 获取字段
- `onlyExplicitlyIncluded` — 白名单,只为字段或 get() 添加了 `@ToString.Included` 的生成 ToString

## 比较对象

自动生成类的比较方法与 hashCode:

```java
@EqualsAndHashCode(callSuper = false, doNotUseGetters = false,
                   cacheStrategy = EqualsAndHashCode.CacheStrategy.NEVER)
```

- `cacheStrategy` — hashCode 缓存

## @Data 注解

等价于有以下注解:

```java
@Getter
@Setter
@RequiredArgsConstructor
@ToString
@EqualsAndHashCode
```

## @Value 注解

等价于有以下注解:

```java
@Getter
@FieldDefaults(makeFinal = true, level = AccessLevel.PRIVATE)
@AllArgsConstructor
@ToString
@EqualsAndHashCode
```

## 建造者模式

生成建造者模式的类:

```java
@Builder
```

## 锁处理

直接在方法里生成同步代码块:

```java
@Synchronized("锁名称")
```

不写锁名称就是这个对象拿着锁。
