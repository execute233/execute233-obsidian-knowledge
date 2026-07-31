#!/usr/bin/env python3
"""
清掉 OneNote 迁移留下的反斜杠转义。
只针对 \\< 和 \\> (其它元字符扫描后无残留)。
严格:
  - 不在 fenced code block (``` ... ```) 内替换
  - 不在 inline code (`...`) 内替换
  - 不动 \\X (双反斜杠场景,避免破坏 escape-of-escape 语义)
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_DIRS = {"_assets"}

def fix_file(content: str) -> tuple[str, int]:
    in_fence = False
    in_inline = False
    out_chars = []
    count = 0
    i = 0
    N = len(content)
    while i < N:
        # fenced code block toggle
        if not in_inline and content[i:i+3] == "```":
            in_fence = not in_fence
            out_chars.append("```")
            i += 3
            continue
        # inline code toggle
        if not in_fence and content[i] == "`":
            in_inline = not in_inline
            out_chars.append("`")
            i += 1
            continue
        # inside code: pass through
        if in_fence or in_inline:
            out_chars.append(content[i])
            i += 1
            continue
        # \\< or \\> replacement (only if not preceded by \\)
        if (content[i] == "\\" and i + 1 < N and content[i+1] in "<>"
                and (i == 0 or content[i-1] != "\\")):
            out_chars.append(content[i+1])  # emit the < or >, drop the \
            count += 1
            i += 2
            continue
        out_chars.append(content[i])
        i += 1
    return "".join(out_chars), count


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md")) + list((ROOT / "copilot").rglob("*.md"))
    targets = [p for p in md_files if not any(part in SKIP_DIRS for part in p.parts)]

    total_files = 0
    total_changes = 0
    samples = []  # (file, before, after)

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        new_content, n = fix_file(content)
        if n:
            # 取一个 before/after 样本
            for j in range(len(content) - 1):
                if content[j] == "\\" and j + 1 < len(content) and content[j+1] in "<>" and (j == 0 or content[j-1] != "\\"):
                    s = max(0, j - 30)
                    e = min(len(content), j + 30)
                    samples.append((p.relative_to(ROOT), content[s:e].replace("\n","⏎"),
                                    new_content[s:e].replace("\n","⏎")))
                    break
            p.write_text(new_content, encoding="utf-8")
            total_files += 1
            total_changes += n

    print(f"\n=== 反斜杠转义清理完成 ===")
    print(f"  受影响笔记: {total_files}")
    print(f"  移除 \\   : {total_changes} 个")
    print()
    if samples:
        print(f"=== 改写样本 (前 8 条) ===")
        for fname, before, after in samples[:8]:
            print(f"  {fname}")
            print(f"    原文: ...{before}...")
            print(f"    新文: ...{after}...")
            print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
