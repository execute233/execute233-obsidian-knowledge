---
title: requests
tags: [Python, requests, HTTP, 网络]
aliases: [Requests]
---

# requests

requests 是 Python 的 HTTP 客户端,HTTP 协议细节见 [[HTTP协议]]。

## Quickly Start

### requests.各种类型的请求()

### response context

请求参数:

- `data` - 发送请求的数据(如果有)
- `params` - 拼接在 URL 的数据
- `headers` - 请求头信息
- `allow_redirects` - 允许重定向
- `stream` - 处理大响应时,逐块接收数据
- `json` - 上传 json 数据
- `timeout` - 超时时间
- `proxies` - 代理设置
- `verify` - SSL 设置

响应属性:

- `.text` - 文本数据,自动使用字符集
- `.encoding` - 字符集,可自己指定
- `.content` - 二进制数据(gzip, deflate 会自动解码)
- `.json()` - 将返回的数据转为 json
- `.raw` - 原始包数据
- `.status_code` - 响应状态码
- `.headers` - 响应头
- `.cookies` - 服务器返回的 cookies
- `.history` - 重定向历史记录

## 高级功能

### 持久化管理

```python
with requests.Session() as session:
    session.headers.update(xxxx)
    session.auth = ...
```