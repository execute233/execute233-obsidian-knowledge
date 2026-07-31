# Task: 删除 6 个空顶层子目录

**Worker:** 64deeb2f worker 0
**Commit:** `18a8658` (--allow-empty)
**Date:** 2026-07-31

## 删除清单

| 目录 | 状态 |
|---|---|
| `OneNote/computer/密码学/` | ✓ 物理删除 |
| `OneNote/computer/操作系统/` | ✓ 物理删除 |
| `OneNote/computer/汇编原理/` | ✓ 物理删除 |
| `OneNote/computer/组成原理/` | ✓ 物理删除 |
| `OneNote/java/JVM/` | ✓ 物理删除 |
| `OneNote/unity/各种组件/` | ✓ 物理删除 |

全部 6 个目录都是彻底空(`ls -la` 只返回 `.` 和 `..`),
**没有** `_assets/` 子目录,也没有任何 `.md` 文件。
按决策规则全部走"git rm -r 整个目录"分支 → 因为 git 本来就不
跟踪空目录,所以实际用 `rmdir` 物理删除,commit 用 `--allow-empty`。

## 影响

```
OneNote/computer/   从 7 子目录 → 3 (底层 / 网络安全 / 计算机网络)
OneNote/java/       从 8 子目录 → 7 (去掉 JVM)
OneNote/unity/      从 2 子目录 → 1 (只留 脚本开发)
```

## 验证

```bash
$ ls OneNote/computer/
底层  网络安全  计算机网络

$ ls OneNote/java/
Mybatis  RabbitMQ  Spring框架  javaSE  小框架  源码  设计模式

$ ls OneNote/unity/
脚本开发

$ for d in OneNote/computer/密码学 OneNote/computer/操作系统 \
          OneNote/computer/汇编原理 OneNote/computer/组成原理 \
          OneNote/java/JVM OneNote/unity/各种组件; do
    [ -d "$d" ] && echo "EXISTS: $d"
  done
# (empty)
```

## 范围限制

- 工作树里另有 5 个 unity 文件被 Obsidian 自动修改、`*.py` 3 个
  未追踪脚本、多份 `.pi-subagents/artifacts/64deeb2f_*` 元数据文件。
  这些都不是本任务职责,**未触碰**。
- 没有触动任何图片、笔记或 frontmatter。