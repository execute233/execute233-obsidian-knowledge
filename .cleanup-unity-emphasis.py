#!/usr/bin/env python3
"""
清理 Unity 8 篇笔记 cs 代码块内的 **Symbol** 残留。

规则:
  1. 只在 cs fenced code block 内替换 (不区分大小写: cs, CS, C#)
  2. 模式: **Xxx**  (Xxx 以字母或下划线开头,后跟 word char)
  3. 替换为 单字符名 Xxx
  4. 不动 _Symbol_ (单下划线)
  5. 不动 *单星号*
  6. 不动代码块外
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNITY_DIR = ROOT / "OneNote" / "unity"

# 匹配 **Xxx** —— Xxx 必须以字母或下划线开头,后跟 \w*
PATTERN = re.compile(r"\*\*([A-Za-z_]\w*)\*\*")

# 匹配 cs 围栏 (open),以行首 ```cs 开头 (忽略大小写)
CS_OPEN = re.compile(r"^```(cs|csharp|c#)\s*$", re.IGNORECASE)
# 匹配任意围栏的 close
FENCE_RE = re.compile(r"^```")


def clean_file(path: Path) -> tuple[str, int]:
    """清理单个文件,返回 (新内容, 替换数)。"""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    in_cs = False
    new_lines = []
    total = 0
    for line in lines:
        # 围栏来回切换
        if FENCE_RE.match(line):
            if CS_OPEN.match(line):
                in_cs = True
            else:
                # 围栏关闭
                if in_cs:
                    in_cs = False
            new_lines.append(line)
            continue
        if in_cs:
            new_line, n = PATTERN.subn(r"\1", line)
            total += n
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines), total


def main() -> int:
    if not UNITY_DIR.exists():
        print(f"! 目录不存在: {UNITY_DIR}")
        return 1
    md_files = list(UNITY_DIR.rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_files = 0
    total_replacements = 0
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 读取失败: {e}")
            continue

        new_content, n = clean_file(p)
        if n > 0:
            try:
                p.write_text(new_content, encoding="utf-8")
                total_files += 1
                total_replacements += n
                rel = p.relative_to(ROOT)
                # 找 before/after 样本
                old_lines = content.split("\n")
                new_lines = new_content.split("\n")
                for i, (o, x) in enumerate(zip(old_lines, new_lines)):
                    if o != x and "**" in o:
                        samples.append((rel, i + 1, o.strip(), x.strip()))
                        if len(samples) >= 8:
                            break
            except Exception as e:
                print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")

    print(f"\n=== Unity **Symbol** 清理完成 ===")
    print(f"  受影响笔记 : {total_files}")
    print(f"  移除 ** 数   : {total_replacements}")
    print()
    if samples:
        print(f"=== 改写样本 (前 8) ===")
        for rel, lineno, before, after in samples:
            print(f"  {rel}:L{lineno}")
            print(f"    原文: {before[:80]}")
            print(f"    新文: {after[:80]}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
