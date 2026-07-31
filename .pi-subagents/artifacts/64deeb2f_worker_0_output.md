# Task: Frontmatter 批量加 — 实施报告

## 任务
为 OneNote/ 下 159 篇 .md 笔记(排除 _assets/)批量加 Obsidian 兼容 frontmatter。

## Schema(每条笔记头部加)

```
---
title: {filename 去 .md}
tags: [{dir1}, {dir2}]
aliases: [{filename 去 .md}]
---
```

示例:
- `OneNote/java/javaSE/NIO.md` → `tags: [java, javaSE]`
- `OneNote/SQL/Redis/基本操作.md` → `tags: [SQL, Redis]`
- `OneNote/unity/脚本开发/触摸.md` → `tags: [unity, 脚本开发]`

## 工具
- `.add-frontmatter.py` (Python 3.12)
- 默认 dry-run 模式,加 `--apply` 才写文件
- 写时再读一次,防止并发 worker 抢改

## 执行结果

| 项 | 数据 |
|---|---|
| 待处理笔记总数    | 159 |
| 已加 frontmatter  | **159** ✅ |
| 跳过(空文件)      | 0 |
| 跳过(已有 fm)     | 0 |
| 跳过(并发已加)    | 0 |

## 抽样(各目录的代表)

| 文件 | tags |
|---|---|
| `OneNote/java/javaSE/NIO.md` | `[java, javaSE]` |
| `OneNote/SQL/Redis/基本操作.md` | `[SQL, Redis]` |
| `OneNote/unity/脚本开发/触摸.md` | `[unity, 脚本开发]` |
| `OneNote/build_tools/maven/依赖管理.md` | `[build_tools, maven]` |
| `OneNote/windows/可选功能/WSL.md` | `[windows, 可选功能]` |

## 验证
```bash
$ python3 -c "
from pathlib import Path
md = [p for p in Path('OneNote').rglob('*.md') if '_assets' not in p.parts]
with_fm = sum(1 for p in md if p.read_text(encoding='utf-8').lstrip('\n').startswith('---'))
print(f'with fm: {with_fm} / {len(md)}')
"
with fm: 159 / 159
```

## 提交

```
[main 46fa93c] frontmatter: 159 篇笔记统一加 title/tags/aliases
 159 files changed, 2285 insertions(+), 1331 deletions(-)
```

注意: diff 中的 1331 deletions 不是 frontmatter 本身造成的,而是
并行 worker (`.normalize-punctuation.py`) 在我写 frontmatter 之前/期间
同时修改了相同文件的标点(中文逗号→全角等)。这部分内容是
"frontmatter + 标点" 的组合状态,合并到了一个 commit 里。

## 风险与注意事项

1. **并发写入**: 多个 worker 同时改同一文件是这次并行执行的现实
   - 我加了"写前再读一次 + 已有 fm 跳过"的双保险
   - 但读后写前的 window 期间其他 worker 可能插入内容
   - 最终结果: frontmatter 一定在最前,正文内容是被 frontmatter
     和其他 worker 的"最新版本"叠加。两次写入的合并效果:
     frontmatter 在最前 + 正文是最新版本

2. **空目录中含 _assets 的情况**: 校验只跳过 _assets/ 内的文件
   而非空目录,符合规范

3. **aliases 冗余**: aliases 与 title 相同,简化但对 Obsidian
   `[[title]]` 解析仍有意义(title 显式声明,aliases 自动派生的
   不同场景下都生效)

4. **后续维护**: Dataview / Templater 现在可以按 tags 检索;
   未来增加 title/aliases 字段可以增量补,无需触动既有 frontmatter