---
title: 第 6 课：Checkpointer 与多轮会话记忆
tags: [Python, LangGraph, Checkpointer]
aliases: [thread_id, 短期记忆]
---

# 第 6 课：Checkpointer 与多轮会话记忆

## 6.1 三个概念

```text
MessagesState
    决定消息如何合并

Checkpointer
    决定 State 是否跨调用保存

thread_id
    决定保存和恢复哪一段线程
```

## 6.2 InMemorySaver 示例

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)
```

配置会话 ID：

```python
config = {
    "configurable": {
        "thread_id": "conversation-001"
    }
}
```

第一轮：

```python
graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "我的名字叫小明。",
            }
        ]
    },
    config=config,
)
```

第二轮只提交新消息：

```python
result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "我叫什么名字？",
            }
        ]
    },
    config=config,
)

print(result["messages"][-1].content)
```

同一个 `thread_id` 会恢复原 State，再合并本轮的新消息。

## 6.3 不要重复提交完整历史

启用 Checkpointer 后，每轮只提交新增消息：

```python
{
    "messages": [
        {"role": "user", "content": "本轮问题"}
    ]
}
```

不要再次提交：

```python
{
    "messages": [
        *previous_result["messages"],
        {"role": "user", "content": "本轮问题"},
    ]
}
```

否则可能造成重复消息和 Token 浪费。

## 6.4 不同 thread_id 相互隔离

```python
alice_config = {
    "configurable": {
        "thread_id": "alice-session"
    }
}

bob_config = {
    "configurable": {
        "thread_id": "bob-session"
    }
}
```

Alice 的历史不会自动进入 Bob 的 State。

## 6.5 查看当前 State

```python
snapshot = graph.get_state(config)

print(snapshot.values)
print(snapshot.next)
print(snapshot.metadata)
```

查看历史：

```python
for snapshot in graph.get_state_history(config):
    print(snapshot.values)
```

## 6.6 Checkpointer 与 Store

| 对比项 | Checkpointer | Store |
|---|---|---|
| 保存内容 | Graph 状态快照 | 应用自定义数据 |
| 范围 | 单个 thread | 跨 thread |
| 记忆类型 | 短期会话记忆 | 长期用户记忆 |
| 适合 | 对话历史、中断恢复、容错 | 用户偏好、事实、共享知识 |
| 定位方式 | `thread_id` | namespace 与 key |

```

## 6.7 thread_id 设计

推荐：

```text
thread_id = conversation_id
```

不要直接固定为：

```text
thread_id = user_id
```

一个用户可能同时拥有多段独立会话。

`thread_id` 应：

- 稳定；
- 唯一；
- 长度受控；
- 不能作为权限凭证。

业务层仍需校验当前用户是否拥有对应会话。

## 6.7 InMemorySaver 的局限

- 进程重启后丢失；
- 多实例不共享；
- 不适合暂停数小时或数天的审批；
- 状态会持续占用内存。

生产环境通常使用 PostgreSQL 等持久化 Checkpointer。

---

---

[[05-Tool-Calling与ReAct循环|上一课]] · [[07-Streaming流式输出|下一课]]
