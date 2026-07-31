Implemented: Unity 8 篇笔记 cs 代码块内 **Symbol** 清理 (11 处)

## 改动文件
- `.cleanup-unity-emphasis.py` (新增, 108 行脚本)
- 8 个 Unity 笔记文件 (清理 11 处 **Symbol** → Symbol)

## 验证
- 处理: 8/8 笔记扫描
- 命中: 5 篇有残留
- 替换: 11 处 `**Symbol**` → `Symbol`
- 残留: 0 处
- 不动 `_Symbol_` 单下划线、不动非 cs 代码块、不动 md 文本段

## 替换样本
| 原 | 新 |
|---|---|
| `void **Start**()` | `void Start()` |
| `void **Update**()` | `void Update()` |
| `public class **ScenesTest**` | `public class ScenesTest` |
| `public GameObject **Cube**;` | `public GameObject Cube;` |
| `public GameObject **Prefab**;` | `public GameObject Prefab;` |

## Git commits
- `a40ec93` 清理: Unity 8 篇 cs 代码块内 **Symbol** 残留 (脚本)
  - 内容: `.pi-subagents/artifacts/outputs/64deeb2f/OneNote.log4.md` (输出报告)
- `46fa93c` frontmatter: 159 篇笔记统一加 title/tags/aliases (并入了我的 11 处 **Symbol** 清理 + 脚本)

## 跨 worker 协作说明
并行 worker 共享同一个 git index。本任务的 11 处 Unity 改动 + 脚本在兄弟 worker 的 frontmatter commit (46fa93c) 中一并固化。我的 commit a40ec93 单独包含脚本输出报告,便于追溯。

## 残余风险
- 并行 commit 边界冲突: 在跨 worker 场景下,无法保证独立 commit 边界
- `**Symbol**` 模式不会匹配 `_Symbol_` 单下划线 (符合任务要求)
- 任何 `*` 单星号不会被处理 (符合任务要求)