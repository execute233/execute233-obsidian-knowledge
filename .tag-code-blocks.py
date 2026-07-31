#!/usr/bin/env python3
"""
逐块给无语言标签的代码块打标签。
策略(优先级从高到低):
  1. 内容启发式(看到关键字直接定)
  2. 文件夹默认(启发式不命中时按路径降级)
  3. 留空(极短文本碎片且无模式)
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

OPEN_RE = re.compile(r"^```(\w*)$")

# === 内容启发式(按优先级顺序)===
HEURISTICS = [
    ("xml",       r"</?\w+[^>]*>|<\?xml\s|<!DOCTYPE\s|<project\s|<dependency>|<plugin\s|<groupId>|<artifactId>|<configuration>|<properties>|<settings>"),
    ("sql",       r"^\s*(SELECT|INSERT\s+INTO|UPDATE\s+\w+|DELETE\s+FROM|CREATE\s+(TABLE|INDEX|VIEW|PROCEDURE)|ALTER\s+|DROP\s+)\b", re.MULTILINE),
    ("json",      r'^\s*[\{\[][\s\S]*[\}\]]\s*$'),
    ("yaml",      r"^\s*\w+:\s*$|^\s*-\s+\w+:", re.MULTILINE),
    ("java",      r"\bimport\s+[\w.]+\s*;|@Override|@Autowired|@RestController|System\.out\.print|\bpublic\s+class\s+|\bprivate\s+(?:static\s+)?\w+\s+\w+\s*[(=;]|protected\s+\w+\s+\w+\s*[(=;]|\bnew\s+\w+\s*\("),
    ("python",    r"^\s*def\s+\w+\s*\(|^\s*from\s+\w+\s+import\s+|^\s*print\s*\(|^\s*if\s+__name__|^\s*self\.", re.MULTILINE),
    ("kotlin",    r"\bfun\s+\w+\s*\(|\bval\s+\w+\s*[=:]|\bvar\s+\w+\s*[=:]|\bcompanion\s+object|\bobject\s+\w+\s*[:\{]|@Composable"),
    ("javascript",r"^\s*function\s+\w+|^\s*const\s+\w+\s*=|^\s*let\s+\w+\s*=|^\s*var\s+\w+\s*=|^\s*import\s+\w+\s+from\s", re.MULTILINE),
    ("cpp",       r"#include\s+<\w+>|\bstd::|\bint\s+main\s*\(|printf\s*\("),
    ("csharp",    r"\busing\s+System|namespace\s+\w+|class\s+\w+\s*:\s+\w+|: MonoBehaviour|\bUnityEngine\."),
    ("bash",      r"^\s*\$\s+|^\s*docker\s+|^\s*git\s+|^#\!/bin/|^\s*mvn\s+|^curl\s+|^npm\s+|^\s*apt\s+|^pip\s+install|conda\s+", re.MULTILINE),
    ("properties",r"^\s*[\w.]+\s*=\s*\w+\s*$", re.MULTILINE),
    ("http",      r"^(GET|POST|PUT|DELETE|PATCH|HEAD)\s+/|HTTP/\d\.\d", re.MULTILINE),
    ("dockerfile",r"^FROM\s+\w+|^RUN\s+|^CMD\s+\[|^WORKDIR\s+", re.MULTILINE),
]

# === 文件夹默认 ===
def folder_default(rel_path: Path) -> str:
    parts = rel_path.parts
    if not parts:
        return ""
    if len(parts) >= 2:
        top = parts[1]
    else:
        top = parts[0]
    sub = parts[2] if len(parts) >= 3 else ""

    table = {
        "java": "java",
        "kotlin": "kotlin",
        "python": "python",
        "SQL": {
            "MySQL": "sql", "SQL语句": "sql", "PostgreSQL": "sql",
            "Redis": "bash",  # redis 主要命令示例
            "NoSQL": "json",
        },
        "build_tools": {"maven": "xml", "IDEA": "bash", "Git": "bash"},
        "docker": "bash",
        "liunx": "bash",
        "computer": {
            "底层": "cpp",
            "汇编原理": "asm",
            "计算机网络": "bash",
            "操作系统": "bash",
            "网络安全": "bash",
            "密码学": "bash",
            "组成原理": "asm",
        },
        "unity": "csharp",
        "windows": "powershell",
    }

    if top in table:
        v = table[top]
        if isinstance(v, dict):
            return v.get(sub, "")
        return v
    return ""


def guess_lang(content: str, rel: Path) -> tuple[str, str]:
    """返回 (lang, reason)。reason 描述为什么这么标。"""
    body = content.strip()
    # 启发式尝试
    for pat in HEURISTICS:
        lang = pat[0]
        regex = pat[1]
        if re.search(regex, body, re.IGNORECASE if lang in ("json",) else 0):
            return (lang, f"启发式命中:{lang}")
    # 文件夹默认
    fd = folder_default(rel)
    if fd:
        return (fd, f"文件夹默认:{fd}")
    return ("", "未匹配")


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_files = 0
    total_blocks = 0
    total_tagged = 0
    total_skipped = 0
    decisions = []  # (file, line, before, after, reason)

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")

        lines = content.split("\n")
        new_lines = []
        i = 0
        file_changed = False
        while i < len(lines):
            ln = lines[i]
            m = OPEN_RE.match(ln)
            if m and not m.group(1):
                # 无语言的开 fence — 找下一个 ``` 闭合
                body_start = i + 1
                j = body_start
                while j < len(lines) and lines[j] != "```":
                    j += 1
                body_lines = lines[body_start:j] if j < len(lines) else lines[body_start:]
                body = "\n".join(body_lines)
                rel = p.relative_to(ROOT)
                lang, reason = guess_lang(body, rel)
                new_ln = f"```{lang}" if lang else ln  # 没命中就保留原文
                if lang:
                    total_tagged += 1
                    decisions.append((rel, i, ln, new_ln, reason))
                else:
                    total_skipped += 1
                    decisions.append((rel, i, ln, ln, "无法识别"))
                new_lines.append(new_ln)
                # 写 body 与 close
                new_lines.extend(body_lines)
                if j < len(lines):
                    new_lines.append("```")
                i = j + 1 if j < len(lines) else len(lines)
                file_changed = True
                total_blocks += 1
            else:
                new_lines.append(ln)
                i += 1

        if file_changed:
            p.write_text("\n".join(new_lines), encoding="utf-8")
            total_files += 1

    print(f"\n=== 代码块标签补全完成 ===")
    print(f"  受影响笔记: {total_files}")
    print(f"  处理代码块: {total_blocks}")
    print(f"  已打标签  : {total_tagged}")
    print(f"  留空      : {total_skipped}")
    print()
    # 按 reason 聚合
    from collections import Counter
    reasons = Counter(reason for _, _, _, _, reason in decisions)
    print(f"=== 决策分布 ===")
    for reason, ct in reasons.most_common():
        print(f"  {reason:30s}: {ct:4d}")
    print()

    # 抽样显示
    print(f"=== 抽样(每个 reason 各 2 条) ===")
    seen = set()
    for rel, idx, before, after, reason in decisions:
        if reason in seen: continue
        if not after.endswith("```"): continue
        seen.add(reason)
        print(f"  {rel}  L{idx+1}")
        print(f"    {before}  →  {after}")
        print(f"    ({reason})")
        if len(seen) >= 12: break
    return 0


if __name__ == "__main__":
    sys.exit(main())
