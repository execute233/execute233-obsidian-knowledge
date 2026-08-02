---
title: LangGraph
tags: [Python, LangGraph, LLM, 状态图]
aliases: [langgraph]
---

# LangGraph

LangGraph 是 langchain 的图状态化扩展,详见 [[langchain]]。

先不引入 LLM,来看最简单的来理解:

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    text: str
    normalized_text: str
    length: int


def normalize_text(state: State):
    """清理用户输入。"""
    normalized = state["text"].strip().lower()
    return {"normalized_text": normalized}


def calculate_length(state: State):
    """计算清理后文本长度。"""
    return {"length": len(state["normalized_text"])}


builder = StateGraph(State)

builder.add_node("normalize_text", normalize_text)
builder.add_node("calculate_length", calculate_length)

builder.add_edge(START, "normalize_text")
builder.add_edge("normalize_text", "calculate_length")
builder.add_edge("calculate_length", END)

graph = builder.compile()

result = graph.invoke({
    "text": " Hello LangGraph! ",
    "normalized_text": "",
    "length": 0,
})

print(result)
```