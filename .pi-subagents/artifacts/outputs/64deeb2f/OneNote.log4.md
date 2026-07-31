# Unity **Symbol** 清理 — 实施报告

## 任务
清理 Unity 8 篇笔记 cs 代码块内的 `**Symbol**` 残留(11 处)。

## 实施
- 写脚本: `.cleanup-unity-emphasis.py`
- 启发式: **`[A-Za-z_]\w*`** → 移除包围的 `**`
- 边界: 仅在 `cs` (不区分大小写) fenced code block 内替换
- 跳过: `_Symbol_` 单下划线、单 `*` 单星号

## 结果
- **处理笔记数**: 8 篇 (5 篇实际有残留)
- **被替换的 `**` 数**: 11
- **残留 `**Symbol**`**: 0

## 清理样例
| 原 | 新 |
|---|---|
| `void **Start**()` | `void Start()` |
| `void **Update**()` | `void Update()` |
| `public class **ScenesTest**` | `public class ScenesTest` |
| `public GameObject **Cube**;` | `public GameObject Cube;` |
| `public GameObject **Prefab**;` | `public GameObject Prefab;` |

## 不动的样例(确认脚本不会过度)
- `Debug._Log_(transform.position)` — 单下划线保留
- `void Start(){` — 已经在前一波清理过

## 后续 commit 状态
我的 11 处 **Symbol** 清理**已经与 46fa93c (frontmatter commit) 合并提交**:
- HEAD~1: 仍含 `void **Start**()` 2 处
- HEAD: 0 处残留

脚本本身 (`.cleanup-unity-emphasis.py`) 已 tracked。

## 任务边界
✅ 仅动了 Unity 8 篇 cs 内 **Symbol**
✅ 不动 `_Symbol_` 单下划线
✅ 不动 md 文本段
✅ 不动非 cs 代码块
✅ 不动 `*` 单星号

## 风险
- 极低: 这是纯字符串级替换,无外部依赖
- 没有副作用: 11 处全部成功,0 残留
- commit 边界: 与 frontmatter 合并 commit,无法分离(并行 worker 抢用工作树)
