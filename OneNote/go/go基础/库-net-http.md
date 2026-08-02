---
title: 库-net-http
tags: [go, net-http, http客户端, http服务端]
aliases: []
---

# 库-net-http

## HTTP 客户端

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-41-0.png)

使用完 response 后必须关闭回复的主体。

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-43-1.png)

带参数的 GET 请求示例:

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-45-2.png)

POST 请求示例:

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-46-3.png)

## 自定义 Client

如果要管理客户端的头域、重定向策略等等,可以用 `http.Client`。

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-48-4.png)

## 自定义 Transport

自定义管理代理、TLS 配置、keep-alive、压缩和其他设置。

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-52-5.png)

## 服务端

可以直接用包的 `Handle` 来处理,这用的是默认的 `DefaultServeMux`。

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-54-6.png)

自定义服务端:

![Exported image](_assets/%E5%BA%93-net-http/%E5%BA%93-net-http__13-01-56-7.png)
