---
title: java9~17新特性
tags: [java, javaSE]
aliases: [java9~17新特性]
---

# java9~17新特性

## 1. 模块系统

使用 `module-info.java` 定义模块便捷,明确哪些包对外开放,哪些依赖是必须的:

```java
module user.management {
    // 只导出 service 包,dao 包对外不可见
    exports com.company.user.service;
    // 依赖其他模块
    requires java.base;
    requires database.connection;
}
```

## 2. 集合工厂方法

现在可用 `List.of()`、`Set.of()`、`Map.of()` 创建不可变集合。

```java
// 之前的不可变集合创建方式
List<String> oldList = new ArrayList<>();
// ...
List<String> immutableList = Collections.unmodifiableList(oldList);
// 或者使用 Google Guava
List<String> guavaList = ImmutableList.of(/* ... */);
```

## 3. 改进的 try-with-resources

可在括号中直接使用变量(或多个),无需再次赋值:

```java
BufferedReader reader1 = Files.newBufferedReader(Paths.get(file1));
BufferedReader reader2 = Files.newBufferedReader(Paths.get(file2));
try (reader1; reader2) {
    // ...
}
```

## 4. var 关键字

支持局部变量的类型推断,让代码变得简洁:

```java
var list = new ArrayList<String>();
```

## 5. HTTP 客户端 API

Java 11 将 HTTP 客户端 API 正式化,支持 HTTP/2 和 WebSocket:

```java
// 创建 HTTP 客户端
HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .followRedirects(HttpClient.Redirect.NORMAL)
        .build();

// 构建 GET 请求
HttpRequest getRequest = HttpRequest.newBuilder()
        .uri(URI.create("https://xxxx.cn/"))
        .header("Accept", "application/json")
        .header("User-Agent", "Java-HttpClient")
        .timeout(Duration.ofSeconds(10))
        .GET()
        .build();

// 构建 POST 请求
HttpRequest postRequest = HttpRequest.newBuilder()
        .uri(URI.create("https://xxxx.cn/"))
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(jsonData))
        .build();

// 同步发送请求
HttpResponse<String> response = client.send(getRequest, HttpResponse.BodyHandlers.ofString());
// ...

// 异步发送请求
client.sendAsync(getRequest, HttpResponse.BodyHandlers.ofString())
        .thenApply(HttpResponse::body)
        .thenAccept(System.out::println);

// 自定义响应处理
HttpResponse<String> customResponse = client.send(getRequest,
        responseInfo -> {
            // ...
            return /* ... */;
        });

// WebSocket 支持
WebSocket webSocket = HttpClient.newHttpClient()
        .newWebSocketBuilder()
        .buildAsync(URI.create(/* ... */), new WebSocket() {
            // ...
        })
        .join();
```

## 6. 增强的 switch

可以多个匹配,也可以作为结果赋值:

```java
// 简洁写法
String dayType = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "work day";
    case SATURDAY, SUNDAY -> "rest day";
    default -> "unknown";
};

// 支持复杂逻辑的 yield 关键字
int score = switch (grade) {
    case 'A' -> {
        // ...
        yield 90;
    }
    case 'B' -> 80;
    default -> 0;
};
```

## 7. Records

创建数据包装更简单,自动生成 `toString` 和 `hashCode` 等方法,直接属性()来调用属性:

```java
public record Person(String name, int age, String email) { }
```

## 8. instanceof 模式匹配

可以在匹配类型时声明变量:

```java
if (obj instanceof String str) {
    return str.length();
}
```

## 9. Sealed 密封类

让类的继承变得更可控与安全:

```java
// 只允许某几个类继承
public sealed class Shape
    permits Circle, Rectangle, Triangle {
    // 只允许这三个类继承
}

// 被允许继承的子类必须选用一种继承策略
// final - 到我为止,sealed - 指定谁能控制我,non-sealed - 开放继承
```

## 10. 其他常用改进

- **文本块**(Java 13/15):使用 `"""` 三引号定义多行字符串。
- **空指针友好提示**(Java 14):`NullPointerException` 会精确指出哪个变量为 null。
- **ZGC / Shenandoah**(Java 11+):低延迟垃圾收集器。