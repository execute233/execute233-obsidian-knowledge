---
title: curl 网络传输
tags: [liunx, 第三方命令]
aliases: [curl 网络传输]
---

# curl 网络传输

curl 基于 HTTP 协议,详见 [[computer/计算机网络/HTTP协议]];常用命令速查见 [[liunx/linux命令/快速命令]]。

curl(Client URL)是一个强大的命令行工具,用于在 Linux/Unix 系统中传输数据。它支持多种协议,包括 HTTP、HTTPS、FTP、SFTP 等,是开发者和系统管理员日常工作中不可或缺的工具。

基本语法结构：

```bash
curl [options] [URL...]
```

`-O` 最常用，下载到文件。

## 请求头相关参数选项

```text
-H "name: value"   # 或 --header "name: value"  添加一个 http 请求头
-H "name"          # 或 --header "name"          删除一个 http 请求头
-A "string"        # 或 --user-agent "string"    设置请求头 User-Agent
-e <URL>           # 或 --referer <URL>          告诉 http 服务器从哪个页面进入到这个页面，相当于 -H "Referer: <URL>"
```

## 响应头相关参数选项

```text
-I  或 --head            输出页面的 http 头（HTTP）或文件大小和最后修改时间（FTP/FILE）
-i  或 --include         输出 HTTP 头和返回内容
-D <file>                # 或 --dump-header <file>  转储 http 响应头到指定文件
```

## cookie

```text
-b data                 # 或 --cookie data             发送 cookie，data 格式是 "key1=value1;key2=value2;.."
-c filename             # 或 --cookie-jar              将服务器返回的 cookies 保存到指定文件，指定为 - 则是控制台
-j                      # 或 --junk-session-cookies    丢弃所有的 "session cookie"
```

## 代理

### 设置代理

未指定端口默认 8080，protocol 默认是 `http_proxy`，其他值可以是 `https_proxy`、`socks4`、`socks4a`、`socks5`：

```text
-x [protocol://[user:pwd@]host[:port]
--proxy [protocol://[user:pwd@]host[:port]]
```

例如 `-x "http_proxy://aiezu:123@aiezu.com:80"`。

```text
-p  或 --proxytunnel     将 -x 参数的代理作为通道的方式去代理非 HTTP 协议，如 ftp
```

### 使用不同类型的 socket 代理（注意会覆盖 -x 参数）

```text
--socks4  <host[:port]>
--socks4a <host[:port]>
--socks5  <host[:port]>
```

### HTTP 代理认证方式

```text
--proxy-anyauth
--proxy-basic
--proxy-digest
--proxy-negotiate
--proxy-ntlm
```

### 设置代理的用户名和密码

```text
-U <user:password>
--proxy-user <user:password>
```

## 数据传输

### 将 -d/--data/--data-binary 设置的数据附加在 URL 上以 GET 方式请求

```text
-G  或 --get
```

### 使用 HTTP POST 方式发送 key/value 对数据

相当于表单属性 `method="POST"; enctype="application/x-www-form-urlencoded"`：

```text
-d @file
-d "string"
--data "string"
--data-ascii "string"
--data-binary "string"
--data-urlencode "string"
```

### 使用 HTTP POST 发送多类型数据

相当于表单属性 `method="POST"; enctype="multipart/form-data"`：

```text
-F name=@file
-F name=<file
-F name=content
--form name=content
--form-string <key=value>     # 类似于 --form，但是 @ < 无特殊含义
```

### 通过 PUT 方式将文件传输到远程网址

如果参数使用 `-` 会使用 stdin 读入文件内容：

```text
-T file
--upload-file file
```