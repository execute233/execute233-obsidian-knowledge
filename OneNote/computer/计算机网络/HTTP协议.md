---
title: HTTP协议
tags: [computer, 计算机网络]
aliases: [HTTP协议]
---

# HTTP协议

HTTP 是 [[computer/计算机网络/网络和通信协议|网络和通信协议]] 中定义的应用层（第 7 层）协议，HTTP/1.x 基于 [[computer/计算机网络/TCP连接|TCP连接]]，HTTP/3 基于改进版 UDP（QUIC）。

HTTP 请求头部包含请求行、请求头部、空行和请求数据四个部分组成。

1. 请求行：首先就是请求方法（GET、POST、OPTION 等），请求方法代表对服务器资源的不同操作，比如 GET 请求用于向服务器获取特定资源，POST 请求用于向服务器提交数据，用于创建新资源或处理数据等。接着是请求的资源 URI，比如我们要访问某个页面下的子页面或是其他内容时，可以通过不同的 URI 地址来指定。紧跟着的 HTTP/1.1 就是当前使用的 HTTP 版本，目前大部分网站采用的是 HTTP/1.1 版本，不同的 HTTP 版本有着一些差异。
2. 请求头：请求头中包含了客户端以及请求的很多信息，由一系列键值对组成，使用英文冒号进行分割，不同的键代表着不同的含义。

比如 Accept-Language 表示客户端支持的语言类型，Host 表示请求的主机名字（也就是网站地址）、User-Agent 包含了当前浏览器的一些信息。

3. 空行：仅用于分割请求头和请求体。
4. 请求体：一些请求可能会包含一些要发送给服务端的数据，一般都通过请求体进行携带。比如我们网站登录请求，就需要发送给服务端我们的用户名和密码，此时就需要通过请求体携带，并且此时我们选择的请求方法也有一定的要求，一般提交数据都是使用 POST 请求而不是 GET，GET 虽然也可以携带请求体，但并不规范，甚至有些浏览器直接不支持。

## HTTP 响应头部

HTTP 响应头部包含状态行、响应头、空行和响应体：

1. 状态行：和 HTTP 请求差不多，首先是服务端响应的 HTTP 版本，与请求中的相匹配，而状态码代表服务端处理本次请求的结果，一般正常响应就是 200。
2. 响应头：和请求头一样，包含诸多键值对，同时响应头中也有各种响应标头表示不同的含义。
3. 空行：仅用于分割响应头和响应体。
4. 响应体：就是我们上面看到的响应内容了，一般就是页面内容或是我们后面会认识到的 JSON 数据。

## HTTP 版本

- **HTTP/0.9**：发布于 1991 年，这个版本只支持 GET 请求，且无状态，无头部信息，仅用于传输纯文本文件，功能非常有限，无法满足一些复杂需求。
- **HTTP/1.0**：发布于 1996 年，相比最初的版本增加了多种 HTTP 方法（如 POST 和 HEAD）以及引入了 HTTP 头部，允许传输元数据，支持 MIME 类型，可以传输多种文件类型，缺点是默认每个连接只能为单个请求服务，请求完成后就会关闭连接，效率低，只能手动设置 Connection: keep-alive 请求头来实现连接复用。
- **HTTP/1.1**：最终发布于 1999 年，在上一代的基础上进行了扩展和优化，引入了管线化、分块传输编码等特性，同时为了优化一次请求的利用效率，默认支持了持久连接，同一个 TCP 连接可复用以处理多个请求和响应，无需额外设置 Connection: keep-alive 请求头。虽然这个版本提升了一些性能，但由于在同一时间内只能处理一个请求，万一刚好有一个请求卡住了后面全部跟着卡，仍存在队头阻塞问题。
- **HTTP/2**：发布于 2015 年，这个版本支持多路复用，即一个 TCP 连接现在可以并发处理多个请求和响应，解决了 HTTP/1.1 中的队头阻塞问题，此外，HTTP/2 还引入了头部压缩，提升传输效率、二进制分帧层，提升解析效率，以及允许服务器主动向客户端推送资源。现在比较主流的网站基本都已经支持 HTTP/2 协议访问了。
- **HTTP/3**：发布于 2022 年，采用 QUIC 协议，QUIC 协议是一种基于 UDP 协议的新型传输层协议，在这个版本之前，HTTP 请求一律采用的是 TCP 协议进行交互，免不了三次握手和四次挥手带来的时间开销，而 HTTP/3 基于 UDP 改进版 QUIC 协议，提供低延迟的连接建立和重传机制，完全解决了队头阻塞问题，提升了网络传输效率且内置加密，更加安全，是目前的主要发展方向。

## 常见的 HTTP 响应码

### 1xx：信息响应

这类响应结果不是很常见。

- `100 Continue`：服务器已接收请求头，客户端应继续发送请求主体。
- `101 Switching Protocols`：服务器同意切换协议。

### 2xx：成功

这类状态码基本都是请求成功。

- `200 OK`：请求成功，服务器已返回请求的数据。
- `201 Created`：请求已成功，并且服务器创建了新的资源。
- `202 Accepted`：服务器已接受请求，但尚未处理。
- `204 No Content`：请求成功但无返回内容。

### 3xx：重定向

这类状态码一般是用于告诉浏览器请求的站点已经被移动到其他地址了，需要更换到新的地址。

- `301 Moved Permanently`：请求的资源已被永久移动到新 URL。
- `302 Found`：请求的资源临时被移动到新 URL。
- `304 Not Modified`：资源未被修改，可以使用缓存的版本。

### 4xx：客户端错误

这类状态码在我们后续学习中会经常碰到，基本都是由于浏览器发送的请求缺少携带了什么数据或是请求有问题之类的。

- `400 Bad Request`：服务器无法理解请求的格式。
- `401 Unauthorized`：请求需要用户认证。
- `403 Forbidden`：服务器拒绝请求。
- `404 Not Found`：服务器找不到请求的资源。
- `405 Method Not Allowed`：请求方法被禁用。
- `429 Too Many Requests`：客户端在给定的时间内发送了太多请求。

### 5xx：服务器错误

这类状态码也会在我们后续学习中经常碰到，基本都是由于服务端出现错误导致的。

- `500 Internal Server Error`：服务器内部错误。
- `501 Not Implemented`：服务器不支持请求的功能。
- `502 Bad Gateway`：网关或代理服务器收到无效响应。
- `503 Service Unavailable`：服务器暂时无法处理请求（超负载或维护）。
- `504 Gateway Timeout`：网关或代理服务器未及时收到上游服务器的响应。

## SSE 流式传输

### 交互过程

- 客户端通过普通 HTTP 请求连接服务器。
- 服务器返回一个特殊的响应类型，也就是事件流。
- 这个 HTTP 连接不会马上结束。
- 服务器可以在这个连接里不断写入事件数据。
- 浏览器通过 `EventSource` 持续接收这些消息。

客户端发送 HTTP 请求后，服务端的响应头如下：

```http
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

### 消息格式

| 字段 | 含义 |
| --- | --- |
| data | 消息内容，也就是具体的数据 |
| event | 事件类型，可自定义事件类型 |
| id | 消息 ID，用于断线重连后续传 |
| retry | 重连间隔，单位毫秒 |

服务器开始持续推送 LLM 产生的回复，注意每一条消息后面都有一个空行：

```text
event: message
data: {"delta":"SSE "}

event: message
data: {"delta":"是一种"}

event: message
data: {"delta":"基于 HTTP "}

event: message
data: {"delta":"的服务器"}

event: message
data: {"delta":"推送技术。"}

event: done
data: [DONE]
```

### 如何标识传输结束？

SSE 协议只规定了消息格式，没有规定结束时必须发送某个标识码。常见的做法有以下几种：

**方式 1**：发送结束后，连接自动断开。

**方式 2**：发送自定义结束事件。

```text
event: message
data: {"delta":"最后一段内容"}

event: done
data: {}
```

**方式 3**：发送自定义结束消息。

```text
event: done
data: [DONE]
```

**方式 4**：发送业务状态字段。

```text
event: chat
data: {"delta":"最后一段内容","finished":false}

event: chat
data: {"delta":"","finished":true}
```

### Fast API 示例

```python
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="对话Agent")

# 输入消息数据模型
class ChatRequest(BaseModel):
    message: str

# 声明路由，并且指定返回内容为 EventSource
@app.post("/api/chat/stream", response_class=EventSourceResponse)
async def chat_stream(req: ChatRequest):  # 定义一个协程函数。输入数据参数，pydantic 会自动转换
    async for ev in LLM.astream(req.message):
        if ev.get("type") == "_done":  # 自定义结束消息
            return
        else:
            yield ServerSentEvent(data=ev)  # 迭代器返回 SSE 内容


if __name__ == "__main__":
    # 启动服务
    uvicorn.run("app:app", host="0.0.0.0", port=8080)
```
