---
title: java8新特性
tags: [java, javaSE]
aliases: [java8新特性]
---

# java8新特性

## Lambda 表达式

### 函数式接口

使用 `@FunctionalInterface` 来创建自定义函数式接口。

## Stream API

```java
// 使用 stream 的方式,可让同样的逻辑变得更简洁直观
```

## 对列表分组

在终端操作使用 `Collectors.partitioningBy(...)`,按照某一条件分组。

### 统计功能

通过最后 `summaryStatistics()` 获取 `IntSummaryStatistics` 对象。

### 按对象的某个字段分组计算

```java
// 以包含 Person(String name, int age, String city) 的 List 对象为例
// 按城市分组
Map<String, List<Person>> byCity = people.stream().collect(Collectors.groupingBy(Person::getCity));
// 按城市分组并统计年龄
Map<String, Double> avgAgeByCity = people.stream().collect(Collectors.groupingBy(
        Person::getCity,
        Collectors.averagingInt(Person::getAge)
));
// 按城市分组并收集姓名
Map<String, List<String>> nameByCity = people.stream().collect(Collectors.groupingBy(
        Person::getCity,
        Collectors.mapping(Person::getName, Collectors.toList())
));
```

## Optional:优雅地处理可能为空的值

在以前,通常创建匿名内部类来调用其中的方法:

```java
// 给按钮添加事件
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        // ...
    }
});

// 使用线程
Thread t = new Thread(new Runnable() {
    @Override
    public void run() {
        // ...
    }
});
```

在这之后,可以使用 lambda 简化:

```java
// lambda
button.addActionListener(e -> /* ... */);
Thread t = new Thread(() -> /* ... */);
```

也有方法引用,只调用一个存在的静态方法且参数最多一个时:

```java
// names 为 List 对象
names.forEach(System.out::println);
```

java8 提供了很多函数式接口来简化操作:

```java
// Predicate<T> 用于条件判断
Predicate<Integer> isEven = n -> n % 2 == 0;

// Function<T, R> 用于数据转换,支持函数组合
Function<String, Integer> stringLength = String::length;

// Consumer 和 Supplier 用于消费和提供数据
Consumer<String> printer = System.out::println;
Supplier<String> randomId = () -> UUID.randomUUID().toString();

// BinaryOperator 用于二元操作,如数学运算
BinaryOperator<Integer> max = Integer::max;
```

stream 在开发中的实际应用:

```java
List<String> result = words.stream()
        .filter(word -> word.length() > 5)   // 过滤长度大于 5 的单词
        .map(String::toUpperCase)            // 转换为大写
        .sorted()                            // 排序
        .collect(Collectors.toList());       // 收集结果
```

中间操作:

- `filter()`:过滤元素。
- `map()`:转换元素。
- `sorted()`:排序。
- `distinct()`:去重。
- `limit()`:限制数量。
- `skip()`:跳过元素。

终端操作(触发实际的数据处理):

- `collect()`:收集到集合。
- `forEach()`:遍历每个元素。
- `count()`:统计数量。
- `findFirst()`:查找第一个。
- `anyMatch()`:是否有匹配的。
- `reduce()`:归约操作。

## Optional 创建对象

```java
Optional.of(T)            // 不可能为空
Optional.ofNullable(T)    // 可能为空
Optional.empty()          // 空
```

## Optional 使用对象

```java
opt.isPresent()             // 检查是否有值
opt.ifPresent(Consumer c)   // 如果对象存在则消费
opt.orElse(T)               // 设置默认值
opt.orElseGet(Supplier s)   // 获取的默认值
opt.orElseThrow(...)        // 空值时抛出异常
```