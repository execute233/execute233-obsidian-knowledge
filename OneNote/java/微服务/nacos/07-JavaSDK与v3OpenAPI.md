---
title: Java SDK 与 v3 OpenAPI
tags: [java, nacos, SDK, OpenAPI]
aliases: [Nacos JavaSDK, Nacos v3接口]
---

# Java SDK 与 v3 OpenAPI

Java SDK 负责运行时长连接和恢复，v3 HTTP API 适合明确资源的读取、调试以及管理自动化。

## 接口选择

| 接口 | 面向对象 | 典型行为 |
| --- | --- | --- |
| Client SDK | 业务应用 | 注册、订阅、读取、监听 |
| <code>/nacos/v3/client/...</code> | HTTP 运行时客户端 | 查询配置；注册、注销、查询实例 |
| <code>/nacos/v3/admin/...</code> | 管理 / 发布工具 | 发布配置、资源管理、运维诊断 |
| <code>/v3/console/...</code> | Console UI | 管理页面交互，使用 Console 端口 |
| Maintainer SDK | Java 管理工具 | 以管理 SDK 执行运维操作 |

普通应用优先使用 SDK，管理脚本使用 Admin API。不要用 Console API 做长期的通用业务依赖。

## SDK 连接参数

在 [[04-SpringCloud服务注册与调用|本课程 Maven 工程]] 中，Discovery / Config starter 已传递引入 Nacos Client；以下示例继续使用 BOM 管理的 <code>3.1.1</code>。

```java
Properties p = new Properties();
p.setProperty(PropertyKeyConst.SERVER_ADDR, "<NACOS_SERVER_ADDR>");
p.setProperty(PropertyKeyConst.NAMESPACE, "public");
p.setProperty(PropertyKeyConst.USERNAME, "<NACOS_USERNAME>");
p.setProperty(PropertyKeyConst.PASSWORD, "<NACOS_PASSWORD>");
```

以上是方法内片段，需导入 <code>java.util.Properties</code> 和 <code>com.alibaba.nacos.api.PropertyKeyConst</code>。把尖括号占位符替换为自己的地址与凭据；实际项目用配置或密钥管理注入，不把明文写进代码库。

## 查询和订阅服务

```java
NamingService naming = NacosFactory.createNamingService(p);
EventListener namingListener = event -> {
    if (event instanceof NamingEvent e) {
        System.out.println("实例数量：" + e.getInstances().size());
    }
};
try {
    naming.subscribe("service-product", "DEFAULT_GROUP", namingListener);
    Instance instance = naming.selectOneHealthyInstance(
            "service-product", "DEFAULT_GROUP");
    System.out.println(instance.getIp() + ":" + instance.getPort());
    Thread.sleep(60_000); // 学习时保留进程，观察实例变更
} finally {
    naming.unsubscribe("service-product", "DEFAULT_GROUP", namingListener);
    naming.shutDown();
}
```


<code>selectOneHealthyInstance</code> 执行 SDK 的实例选择；没有可用实例时处理异常，不能假设始终返回地址。长期应用复用 SDK 对象，不为每个业务请求重建连接。

## 配置读取与监听

```java
ConfigService config = NacosFactory.createConfigService(p);
Listener configListener = new Listener() {
    @Override
    public Executor getExecutor() { return null; }

    @Override
    public void receiveConfigInfo(String content) {
        System.out.println("配置变更，是否存在：" + (content != null));
    }
};
try {
    String current = config.getConfigAndSignListener(
            "service-product.yml", "DEFAULT_GROUP", 5000, configListener);
    System.out.println("初次查询是否存在：" + (current != null));
    Thread.sleep(60_000);
} finally {
    config.removeListener("service-product.yml", "DEFAULT_GROUP", configListener);
    config.shutDown();
}
```


<code>getConfigAndSignListener</code> 把初始查询与监听登记组合起来，优于在业务代码中随意先读再监听。它也不是跨服务的原子配置事务。

## 终端登录

在有目标资源权限的账号下，先取访问 Token：

```bash
nacosApi='http://<NACOS_HOST>:8848/nacos' # 替换为自己的 Server HTTP 入口
curl -sS -X POST "$nacosApi/v3/auth/user/login" \
    -d 'username=<NACOS_USERNAME>' -d 'password=<NACOS_PASSWORD>'
```

默认 Nacos 鉴权插件的登录响应直接包含 <code>accessToken</code> 和 <code>tokenTtl</code>。Token 到期重新登录；不要把 Token 或完整登录响应输出到共享日志。后续命令把 <code>&lt;NACOS_ACCESS_TOKEN&gt;</code> 换成这里返回的 Token。

## 发布与读取配置

发布是管理操作，需要写权限。下面使用独立学习资源，避免覆盖商品服务的 YAML：

```bash
curl -sS -X POST "$nacosApi/v3/admin/cs/config" \
    -H 'accessToken: <NACOS_ACCESS_TOKEN>' \
    -d 'namespaceId=public' -d 'groupName=DEFAULT_GROUP' \
    -d 'dataId=quickstart.txt' -d 'content=Hello Nacos 3.2.4' -d 'type=text'

curl -sS "$nacosApi/v3/client/cs/config?namespaceId=public&groupName=DEFAULT_GROUP&dataId=quickstart.txt" \
    -H 'accessToken: <NACOS_ACCESS_TOKEN>'
```

| 事项 | 注意点 |
| --- | --- |
| 参数名 | v3 示例使用 <code>groupName</code>、<code>namespaceId</code>，按当前接口定义填写 |
| 返回体 | 普通 v3 HTTP API 为 <code>code / message / data</code>；业务成功是 <code>code=0</code> |
| HTTP 状态 | 状态成功仍应检查业务 <code>code</code>；参数、鉴权或资源状态错误可能直接返回非 2xx |
| URL 编码 | 变量包含空格、中文或特殊字符时，对查询参数逐项编码 |
| 监听 | 一次 Client HTTP 查询不提供 SDK 的持续监听 |

## HTTP 服务查询

在商品应用已启动后查询：

```bash
curl -sS "$nacosApi/v3/client/ns/instance/list?namespaceId=public&groupName=DEFAULT_GROUP&serviceName=service-product" \
    -H 'accessToken: <NACOS_ACCESS_TOKEN>'
```

手工 POST 注册的临时实例仍需续约，不能用于替代正常 SDK 生命周期。诊断全量服务、客户端或订阅者时，使用 Admin API / Maintainer SDK。

详见 [[03-服务模型与实例生命周期|实例生命周期]]、[[05-配置中心与动态刷新|Spring 刷新]]、[[官方资料索引|SDK 与 API 文档]]。
