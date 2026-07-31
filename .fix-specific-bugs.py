#!/usr/bin/env python3
"""
修复 4 个具体的格式 bug:
  1. DQL数据查询.md L1: 代码块标签 xml → sql
  2. DML数据操作.md L1: 编号 1. 插入数据 3. 修改数据 → 1.\n 2.\n 3.\n
  3. Git/使用.md L45: 半截 ** 闭合
  4. 任意 .md: 合并连续 **** → 单空格
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def fix_dql_label(content: str) -> tuple[str, int]:
    """Bug 1: DQL数据查询.md L1 标签 xml → sql (开头第一个 ```xml 段是 SQL)"""
    if not content.startswith("# DQL数据查询") and "DQL数据查询" not in content[:50]:
        return content, 0
    # 找到第一个 ```xml 改成 ```sql
    new_content, n = re.subn(r'^(```)xml(\n)', r'\1sql\2', content, count=1, flags=re.MULTILINE)
    return new_content, n

def fix_dml_numbering(content: str) -> tuple[str, int]:
    """Bug 2: DML数据操作.md L1 编号错乱"""
    if "DML数据操作" not in content[:50]:
        return content, 0
    # 匹配 `1. 插入数据 3. 修改数据` 开头
    pattern = r'^(\s*)1\. (插入数据)\s+3\. (修改数据)(\s*\n\s*)4\. (删除数据)'
    new_content, n = re.subn(
        pattern,
        r'\g<1>1. \g<2>\g<4>2. \g<3>\g<4>3. \g<5>',
        content, count=1, flags=re.MULTILINE
    )
    return new_content, n

def fix_unclosed_emphasis(content: str) -> tuple[str, int]:
    """Bug 3: Git/使用.md L45 半截 ** 闭合"""
    # 匹配 `**强制让分支指向另一个提交` (强调开启但没闭合)
    pattern = r'\*\*强制让分支指向另一个提交(\s*\n)'
    new_content, n = re.subn(
        pattern,
        r'**强制让分支指向另一个提交**\g<1>',
        content, count=1
    )
    return new_content, n

def fix_merged_emphasis(content: str) -> tuple[str, int]:
    """Bug 4: 合并连续 **** 成单空格"""
    # 4+ 个连续 *  → 单空格
    new_content, n = re.subn(r'\*{4,}', ' ', content)
    return new_content, n


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_bugs = {
        "dql_label": 0,
        "dml_numbering": 0,
        "unclosed_emphasis": 0,
        "merged_emphasis_files": 0,
        "merged_emphasis_count": 0,
    }
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception:
            continue

        original = content
        file_changed = False

        # Bug 1
        content, n1 = fix_dql_label(content)
        if n1:
            total_bugs["dql_label"] += n1
            file_changed = True

        # Bug 2
        content, n2 = fix_dml_numbering(content)
        if n2:
            total_bugs["dml_numbering"] += n2
            file_changed = True

        # Bug 3
        content, n3 = fix_unclosed_emphasis(content)
        if n3:
            total_bugs["unclosed_emphasis"] += n3
            file_changed = True

        # Bug 4
        content, n4 = fix_merged_emphasis(content)
        if n4:
            total_bugs["merged_emphasis_files"] += 1
            total_bugs["merged_emphasis_count"] += n4
            file_changed = True

        if file_changed:
            try:
                p.write_text(content, encoding="utf-8")
                if len(samples) < 8:
                    samples.append((p, original[:100].replace("\n", "⏎"),
                                    content[:100].replace("\n", "⏎")))
            except Exception as e:
                print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")

    print(f"\n=== 4 个 bug 修复完成 ===")
    print(f"  Bug 1 (DQL label xml→sql)             : {total_bugs['dql_label']}")
    print(f"  Bug 2 (DML 编号 1→3→4 修正为 1→2→3)  : {total_bugs['dml_numbering']}")
    print(f"  Bug 3 (Git/使用.md L45 半截 ** 闭合) : {total_bugs['unclosed_emphasis']}")
    print(f"  Bug 4 (合并 **** 成空格)             : {total_bugs['merged_emphasis_files']} 文件, {total_bugs['merged_emphasis_count']} 处")
    print()
    if samples:
        print(f"=== 抽样 (前 8) ===")
        for p, before, after in samples:
            print(f"  {p.relative_to(ROOT)}")
            print(f"    原文: {before!r}")
            print(f"    新文: {after!r}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
