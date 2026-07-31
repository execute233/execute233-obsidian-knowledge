#!/usr/bin/env python3
"""
轮 2 标题重构第二遍:把单独成段的 1. xxx 也转成 ## h2
启发式:
  - 文件首 H1 之后
  - 单条孤立 `1. xxx`(后面是空行/文本/代码块,不是 2. xxx)
  - 标题文本 ≤ 60 字符
  - 文本内容像"标题"(含中文,或单行短)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def transform_file(p):
    try:
        content = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = p.read_text(encoding="gbk", errors="replace")
    except Exception:
        return None, 0

    lines = content.split("\n")
    in_fence = False
    in_frontmatter = False
    h1_seen = False
    new_lines = []
    n = 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        # 处理 frontmatter
        if not h1_seen and not in_frontmatter and ln == "---":
            in_frontmatter = True
            new_lines.append(ln)
            i += 1
            continue
        if in_frontmatter:
            if ln == "---":
                in_frontmatter = False
            new_lines.append(ln)
            i += 1
            continue
        # code block toggle
        if not in_fence and ln.startswith("```"):
            in_fence = True
            new_lines.append(ln)
            i += 1
            continue
        if in_fence:
            if ln.startswith("```"):
                in_fence = False
            new_lines.append(ln)
            i += 1
            continue
        # 找 H1
        if not h1_seen:
            if re.match(r"^#\s+", ln):
                h1_seen = True
            new_lines.append(ln)
            i += 1
            continue
        # H1 之后:看是否是单条 1. xxx 孤立编号
        m = re.match(r"^(\s*)1\.\s+(.+)$", ln)
        if m:
            indent = m.group(1)
            text = m.group(2).strip()
            # 长度 < 60
            if len(text) > 60:
                new_lines.append(ln)
                i += 1
                continue
            # 跳过空行
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            next_line = lines[j] if j < len(lines) else ""
            # 下一行不是 2. xxx (即不是连续编号列表)
            if not re.match(r"^\s*2\.\s+", next_line):
                # 单独成段,转成 ## h2
                # 移除前后 `**` 强调(如果整个内容被 `**` 包裹)
                title = re.sub(r"^\*\*|\*\*$", "", text)
                new_lines.append(f"{indent}## {title}")
                n += 1
                i += 1
                continue
        new_lines.append(ln)
        i += 1

    new_content = "\n".join(new_lines)
    if new_content != content:
        return new_content, n
    return None, 0


def main():
    md_files = [p for p in (ROOT / "OneNote").rglob("*.md") if "_assets" not in p.parts]
    total = 0
    n_total = 0
    for p in md_files:
        new_content, n = transform_file(p)
        if new_content:
            p.write_text(new_content, encoding="utf-8")
            total += 1
            n_total += n
    print(f"=== 轮 2 第二遍标题重构 ===")
    print(f"  处理笔记: {total}")
    print(f"  单条孤立 1. xxx → ## h2: {n_total}")


if __name__ == "__main__":
    main()
