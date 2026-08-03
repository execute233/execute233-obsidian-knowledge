---
title: 第 7 课：Streaming 流式输出
tags: [Python, LangGraph, Streaming]
aliases: [流式输出, SSE]
---

# 第 7 课：Streaming 流式输出

## 7.1 两套流式 API 的定位

LangGraph 1.2 中：

- `stream()` / `astream()` + `stream_mode`：直接消费运行时事件，适合精细控制；
- `stream_events(..., version="v3")`：新项目更推荐的事件投影 API，可分别消费消息、状态和子图事件。

本节主要保留课程中使用的 `stream_mode + version="v2"`，因为结构直观，便于理解底层事件。

## 7.2 常用 Stream Mode

| 模式 | 内容 |
|---|---|
| `updates` | 每个节点产生的局部 State 更新 |
| `values` | 每一步后的完整 State |
| `messages` | LLM Token 和元数据 |
| `custom` | 节点主动发送的业务事件 |
| `checkpoints` | Checkpoint 事件，需要 Checkpointer |
| `tasks` | 节点任务开始、结束、错误，需要 Checkpointer |
| `debug` | 更完整的调试信息 |

## 7.3 v2 统一格式

```python
{
    "type": "updates",
    "ns": (),
    "data": {...},
}
```

其中：

- `type`：事件类型；
- `ns`：子图命名空间；
- `data`：实际数据。

## 7.4 节点更新流

```python
for part in graph.stream(
    inputs,
    stream_mode="updates",
    version="v2",
):
    if part["type"] != "updates":
        continue

    for node_name, update in part["data"].items():
        print(node_name, update)
```

## 7.5 完整状态流

```python
for part in graph.stream(
    inputs,
    stream_mode="values",
    version="v2",
):
    if part["type"] == "values":
        print(part["data"])
```

`values` 会重复传输越来越大的完整 State，更适合调试，不适合长期直接推给前端。

## 7.6 Token 流

```python
for part in graph.stream(
    inputs,
    stream_mode="messages",
    version="v2",
):
    if part["type"] != "messages":
        continue

    message_chunk, metadata = part["data"]

    if message_chunk.content:
        print(
            message_chunk.content,
            end="",
            flush=True,
        )
```

即使节点内部使用 `model.invoke()`，LangGraph 也可以捕获模型流式事件。

## 7.7 按节点过滤 Token

```python
if (
    metadata.get("langgraph_node") == "agent"
    and message_chunk.content
):
    print(message_chunk.content, end="")
```

多个 LLM 节点存在时，应根据节点名或模型标签过滤。

## 7.8 同时订阅多种模式

```python
for part in graph.stream(
    inputs,
    stream_mode=[
        "messages",
        "updates",
        "custom",
    ],
    version="v2",
):
    if part["type"] == "messages":
        ...
    elif part["type"] == "updates":
        ...
    elif part["type"] == "custom":
        ...
```

推荐职责：

```text
messages -> 最终回答文字
updates  -> 节点和工具状态
custom   -> 业务进度
```

不要同时把 `messages` Token 和 `updates` 中的完整 AIMessage 都追加到前端，否则最终回答会重复。

## 7.9 自定义进度事件

```python
from langgraph.config import get_stream_writer


def plan_route(state):
    writer = get_stream_writer()

    writer({
        "type": "progress",
        "stage": "search_poi",
        "progress": 20,
        "message": "正在搜索候选景点",
    })

    # 执行业务逻辑

    writer({
        "type": "progress",
        "stage": "complete",
        "progress": 100,
        "message": "路线规划完成",
    })

    return {"result": "..."}
```

接收：

```python
for part in graph.stream(
    inputs,
    stream_mode="custom",
    version="v2",
):
    if part["type"] == "custom":
        print(part["data"])
```

## 7.10 异步流

```python
async for part in graph.astream(
    inputs,
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",
):
    ...
```

FastAPI、SSE 和 WebSocket 服务优先使用 `astream()`。

## 7.11 推荐前端事件协议

不要让前端直接依赖 LangGraph 内部对象，后端应转换为稳定业务事件：

```json
{"type":"token","content":"你好"}
```

```json
{
  "type":"tool_call",
  "name":"search_poi",
  "args":{"city":"广州"}
}
```

```json
{
  "type":"progress",
  "stage":"route_optimization",
  "progress":60
}
```

```json
{"type":"done"}
```

## 7.12 FastAPI SSE 骨架

```python
import json
from collections.abc import AsyncIterator
from fastapi.responses import StreamingResponse


async def generate_sse(message: str) -> AsyncIterator[str]:
    async for part in graph.astream(
        {
            "messages": [
                {"role": "user", "content": message}
            ]
        },
        stream_mode=["messages", "updates"],
        version="v2",
    ):
        if part["type"] == "messages":
            chunk, metadata = part["data"]

            if chunk.content:
                payload = {
                    "type": "token",
                    "content": chunk.content,
                }

                yield (
                    "data: "
                    + json.dumps(payload, ensure_ascii=False)
                    + "\n\n"
                )

    yield 'data: {"type":"done"}\n\n'


@app.post("/chat/stream")
async def chat_stream(body: ChatRequest):
    return StreamingResponse(
        generate_sse(body.message),
        media_type="text/event-stream",
    )
```

---

---

[[06-Checkpointer与多轮记忆|上一课]] · [[08-interrupt与人工审批|下一课]]
