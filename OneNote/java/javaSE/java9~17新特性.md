# java9~17新特性

1. **模块系统**
2. **集合工厂方法**

现在可用List.of(), Set.of(), Map.of() 创建不可变集合

4. **改进的 try-with-resources**
5. **var 关键字**
6. **HTTP 客户端 API**
7. **增强的 switch**
8. **Records**
9. **instanceof 模式匹配，可以在匹配类型时声明变量**
10. **Sealed 密封类**

使用module-info.java定义模块便捷，明确哪些包对外开放，哪些依赖是必须的
module user.management {
// 只导出service包，dao包对外不可见
exports com.company.user.service;
// 依赖其他模块
requires java.base;
requires database.connection;
}
为集合类添加了便捷地工厂方法，创建不可变集合
// 之前的不可变集合创建方式
List<String> oldList = new ArrayList<>();
xxx
List<String> immutableList = Collections.unmodifiableList(oldList);
// 或者使用Google Guava
List<String> guavaList = ImmutableList.of(xxx);
可在括号中直接使用变量（或多个），无需再次赋值，如
```python
BufferedReader reader1 = Files.newBufferedReader(Paths.get(file1));
BufferedReader reader2 = Files.newBufferedReader(Paths.get(file2));
try (reader1; reader2) {
```
xxx
}
支持局部变量的类型推断，让代码变得简洁
var list = new ArrayList<String>();
java11将HTTP客户端API正式化，支持HTTP/2和WebSocket
// 创建HTTP客户端
HttpClient client = HttpClient.newBuilder()
.connectTimeout(Duration.ofSeconds(10))
.followRedirects(HttpClient.Redirect.NORMAL)
.build();
// 构建GET请求
HttpRequest getRequest = HttpRequest.newBuilder()
```text
.uri(URI.create("https://xxxx.cn/"))
.header("Accept", "application/json")
.header("User-Agent", "Java-HttpClient")
.timeout(Duration.ofSeconds(10))
```
.GET()
.build();
// 构建POST请求
HttpRequest postRequest = HttpRequest.newBuilder()
```text
.uri(URI.create("https://xxxx.cn/"))
.header("Content-Type", "application/json")
.POST(HttpRequest.BodyPublishers.ofString(jsonData))
```
.build();
// 同步发送请求
HttpResponse<String> response = client.send(getRequest, HttpResponse.BodyHandlers.ofString());
xxxxx
// 异步发送请求
client.sendAsync(getRequest, HttpResponse.BodyHandlers.ofString)
.thenApply(Httpresponse::body)
.thenAccept(System.out::println);
// 自定义响应处理
HttpRespnse<String> customResponse = client.send(getRequest,
responeInfo - {
xxx
return xxx;
}
);
// WebSocket支持
WebSocket webSocket = HttpClient.newHttpClient()
.newWebSocketBuilder()
.buildAsync(URI.create(xxx), new WebSocket() {
xxxx
})
.join();
可以多个匹配，也可以作为结果赋值，如
// 简洁写法
```csharp
String dayType = switch (day) {
case MONDAY, TUESDAT, WEDNESDAY, THURSDAY, FRIDAY -> "work day";
case SATURDAY, SUNDAY -> "rest day";
default -> "unkown";
```
}
// 支持复杂逻辑的yield关键字
```cpp
int score = switch (grade) {
case 'A' -> {
```
xxx
yield 90;
}
```csharp
case 'B' -> 80;
default -> 0;
```
}
创建数据包装更简单,自动生成toString和HashCode等方法，直接属性()来调用属性
```python
public record Person(String name, int age, String email)
if (obj instanceof String str) {
return str.length();
```
}
让类的继承变得更可控与安全
// 只允许某几个类继承
public sealed class Shape
permits Circle, Rectangle, Triangle {
// 只允许这三个类继承
}
// 但是，被允许继承的子类必须闲着一种继承策略
// final - 到我为止，sealed - 指定谁能控制我， non-sealed - 开放继承