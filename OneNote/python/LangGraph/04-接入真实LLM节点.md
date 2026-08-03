---
title: 第 4 课：接入真实 LLM 节点
tags: [Python, LangGraph, LangChain, LLM]
aliases: [LLM Node, ChatOpenAI]
---

# 第 4 课：接入真实 LLM 节点

LLM 节点仍然只是普通节点，只是内部调用了模型。

## 4.1 环境变量

`.env`：

```dotenv
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://your-compatible-endpoint/v1
MODEL_NAME=your-model-name
```

直接使用某个官方提供商时，按其集成要求配置；OpenAI 兼容服务通常需要 `base_url`。

## 4.2 先单独测试模型

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model=os.environ["MODEL_NAME"],
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0,
)

response = model.invoke("你好")
print(type(response))
print(response.content)
```

`model.invoke()` 返回 `AIMessage`，不是普通字符串。

## 4.3 LLM Graph

```python
import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

load_dotenv()

model = ChatOpenAI(
    model=os.environ["MODEL_NAME"],
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0,
)


def call_model(state: MessagesState):
    response = model.invoke([
        SystemMessage(
            content=(
                "你是一个耐心、准确的编程学习助手。"
                "请使用清晰的中文回答。"
            )
        ),
        *state["messages"],
    ])

    return {
        "messages": [response]
    }


builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", END)

graph = builder.compile()
```

调用：

```python
result = graph.invoke({
    "messages": [
        {
            "role": "user",
            "content": "LangGraph 的节点是什么？",
        }
    ]
})

print(result["messages"][-1].content)
```

## 4.4 `*state["messages"]`

```python
[
    SystemMessage(content="系统提示"),
    *state["messages"],
]
```

表示把历史消息列表展开到新列表中。

等价于：

```python
messages = [SystemMessage(content="系统提示")]
messages.extend(state["messages"])
```

## 4.5 SystemMessage 是否进入 State

下面的系统提示只是临时加入模型输入：

```python
response = model.invoke([
    SystemMessage(content="你是助手"),
    *state["messages"],
])
```

节点只返回：

```python
{"messages": [response]}
```

所以系统提示不会被反复保存进 State。

## 4.6 常见错误

- 把 `AIMessage` 再包装成 `AIMessage(content=response)`；
- 节点直接返回 `response`，而不是 State 更新字典；
- 返回完整消息历史造成重复；
- 模型名称与兼容服务的别名不一致；
- 把内部异常详情直接返回给最终用户。

---

---

[[03-Reducer与MessagesState|上一课]] · [[05-Tool-Calling与ReAct循环|下一课]]
