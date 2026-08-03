---
title: 第 3 课：Reducer 与 MessagesState
tags: [Python, LangGraph, MessagesState]
aliases: [Reducer, add_messages]
---

# 第 3 课：Reducer 与 MessagesState

## 3.1 为什么需要 Reducer

普通 State 字段默认采用覆盖更新：

```text
旧值 + 新值 -> 新值
```

如果消息字段没有 Reducer：

```python
class ChatState(TypedDict):
    messages: list
```

节点返回新消息时：

```python
return {
    "messages": [AIMessage(content="你好")]
}
```

旧的用户消息会被覆盖。

Reducer 决定新旧值如何合并：

```text
reducer(old_value, new_value) -> merged_value
```

## 3.2 Annotated

```python
from typing import Annotated

messages: Annotated[list, reducer]
```

可以读作：

> `messages` 是列表；更新时使用 `reducer` 合并。

`Annotated` 本身不会执行函数，是 LangGraph 读取其中的元数据并应用 Reducer。

## 3.3 add_messages

```python
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class ChatState(TypedDict):
    messages: Annotated[
        list[AnyMessage],
        add_messages,
    ]
```

`add_messages` 的主要行为：

- 追加新的消息；
- 新消息和旧消息 ID 相同时，更新原消息；
- 把支持的字典消息转换成 LangChain 消息对象。

节点通常只返回新增消息：

```python
return {
    "messages": [response]
}
```

不要再次返回完整历史：

```python
# 不推荐：Reducer 会再次合并这些历史
return {
    "messages": [
        *state["messages"],
        response,
    ]
}
```

## 3.4 MessagesState

由于消息 State 非常常见，LangGraph 已提供：

```python
from langgraph.graph import MessagesState
```

它本质上包含：

```python
messages: Annotated[list[AnyMessage], add_messages]
```

最小示例：

```python
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, MessagesState, StateGraph


def reply(state: MessagesState):
    last_message = state["messages"][-1]

    return {
        "messages": [
            AIMessage(
                content=f"收到：{last_message.content}"
            )
        ]
    }


builder = StateGraph(MessagesState)
builder.add_node("reply", reply)
builder.add_edge(START, "reply")
builder.add_edge("reply", END)

graph = builder.compile()

result = graph.invoke({
    "messages": [
        {
            "role": "user",
            "content": "你好",
        }
    ]
})
```

最终消息历史：

```text
HumanMessage("你好")
AIMessage("收到：你好")
```

## 3.5 常见消息类型

| 类型 | 用途 |
|---|---|
| `SystemMessage` | 系统指令 |
| `HumanMessage` | 用户消息 |
| `AIMessage` | 模型回答或工具调用请求 |
| `ToolMessage` | 工具执行结果 |

工具 Agent 的典型消息链：

```text
HumanMessage
AIMessage(tool_calls)
ToolMessage
AIMessage(final answer)
```

## 3.6 扩展 MessagesState

```python
from typing_extensions import NotRequired
from langgraph.graph import MessagesState


class TravelState(MessagesState):
    user_id: str
    destination: NotRequired[str]
    budget: NotRequired[int]
```

`messages` 使用 `add_messages`，其他字段默认覆盖。

## 3.7 MessagesState 不等于多轮记忆

`MessagesState` 只定义消息如何合并。

它不会自动让两次独立的 `invoke()` 共享历史。跨调用记忆需要：

```text
Checkpointer + thread_id
```

---

---

[[02-Conditional-Edge条件分支|上一课]] · [[04-接入真实LLM节点|下一课]]
