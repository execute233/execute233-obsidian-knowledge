---
title: 第 9 课：Command 动态更新与跳转
tags: [Python, LangGraph, Command]
aliases: [动态路由, Command goto]
---

# 第 9 课：Command 动态更新与跳转

`Command` 可以在一个节点中同时：

```text
更新 State + 决定下一节点
```

## 9.1 基本写法

```python
from typing import Literal
from langgraph.types import Command


def classify(
    state: State,
) -> Command[
    Literal[
        "handle_simple",
        "handle_complex",
    ]
]:
    if len(state["request"]) <= 10:
        return Command(
            update={
                "category": "simple"
            },
            goto="handle_simple",
        )

    return Command(
        update={
            "category": "complex"
        },
        goto="handle_complex",
    )
```

## 9.2 update

```python
update={
    "category": "simple",
    "reason": "文本较短",
}
```

和普通节点返回字典一样，会按照对应字段的 Reducer 更新 State。

## 9.3 goto

```python
goto="handle_simple"
```

表示该节点完成后前往指定节点。

## 9.4 返回类型

```python
Command[
    Literal["handle_simple", "handle_complex"]
]
```

帮助 IDE、类型检查器和图可视化理解可能目标。

## 9.5 与 Conditional Edge 的选择

| 场景 | 推荐 |
|---|---|
| 只根据 State 选择下一节点 | Conditional Edge |
| 判断结果和路由职责需要分离 | Conditional Edge |
| 同一函数既更新 State 又决定跳转 | `Command` |
| 工具或子图需要动态交接 | `Command` |

## 9.6 不要混用普通出边和动态路由

如果一个节点返回：

```python
Command(goto="node_a")
```

同时又配置：

```python
builder.add_edge("current", "node_b")
```

`node_a` 和 `node_b` 都可能执行。

原则：

> 一个节点的出路优先只选择一种机制：普通 Edge、Conditional Edge 或 Command 动态路由。

## 9.7 Command 与 interrupt 组合

```python
def human_review(
    state: State,
) -> Command[
    Literal["execute", "cancel"]
]:
    response = interrupt({
        "question": "是否批准？"
    })

    if response["decision"] == "approve":
        return Command(
            update={"decision": "approve"},
            goto="execute",
        )

    return Command(
        update={"decision": "reject"},
        goto="cancel",
    )
```

## 9.8 形成循环

```python
return Command(
    update={
        "retry_count": retry_count + 1
    },
    goto="retry_node",
)
```

循环必须同时设置：

- 明确退出条件；
- 业务级次数字段；
- `recursion_limit`。

---

---

[[08-interrupt与人工审批|上一课]] · [[10-Send并行执行与Map-Reduce|下一课]]
