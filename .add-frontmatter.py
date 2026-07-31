#!/usr/bin/env python3
"""
为 OneNote/ 下所有 .md 笔记批量加 frontmatter。

Schema:
---
title: {filename 去 .md}
tags: [{dir1}, {dir2}]
aliases: [{filename 去 .md}]
---

规则:
  1. 跳过已有 frontmatter (--- 开头)
  2. 跳过 _assets/
  3. 跳过空文件 (0 字节)
  4. 不修改正文
  5. 写时再次检查 (避免被并发 worker 抢改)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def parse_path(rel: Path) -> tuple[str, list[str]]:
    """返回 (title, [tags])"""
    title = rel.stem
    parts = rel.parts  # ('OneNote', 'java', 'javaSE', 'NIO.md')
    tags = []
    if len(parts) >= 3:
        tags.append(parts[1])
        tags.append(parts[2])
    elif len(parts) >= 2:
        tags.append(parts[1])
    return title, tags


def make_frontmatter(rel: Path) -> str:
    title, tags = parse_path(rel)
    title_yaml = f"title: {title}"
    tags_yaml = "tags: [" + ", ".join(tags) + "]"
    aliases_yaml = f"aliases: [{title}]"
    return f"---\n{title_yaml}\n{tags_yaml}\n{aliases_yaml}\n---\n\n"


def has_frontmatter(content: str) -> bool:
    return content.lstrip("\n").startswith("---")


def process(p: Path, dry_run: bool = False) -> tuple[bool, str]:
    """返回 (是否改了, 备注)"""
    try:
        content = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = p.read_text(encoding="gbk", errors="replace")

    if not content.strip():
        return False, "空文件,跳过"

    if has_frontmatter(content):
        return False, "已有 frontmatter,跳过"

    fm = make_frontmatter(p.relative_to(ROOT))
    new_content = fm + content

    if not dry_run:
        # 写时再读一次,防止并发 worker 已经动了文件
        try:
            content2 = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content2 = p.read_text(encoding="gbk", errors="replace")
        if has_frontmatter(content2):
            return False, "并发 worker 已加 frontmatter,跳过"
        if content2.strip() != content.strip():
            # 并发 worker 改了正文,我们的 frontmatter 仍然 prepend 到当前最新内容
            new_content = fm + content2
        p.write_text(new_content, encoding="utf-8")
    return True, f"已加 frontmatter (tags={[t for t in parse_path(p.relative_to(ROOT))[1]]})"


def main() -> int:
    dry_run_arg = "--apply" not in sys.argv
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    samples = []
    changed = 0
    skipped_empty = 0
    skipped_has_fm = 0
    skipped_concurrent = 0

    for p in sorted(targets):
        c, note = process(p, dry_run=dry_run_arg)
        if c:
            changed += 1
            if len(samples) < 5:
                samples.append((p, note))
        else:
            if "空文件" in note:
                skipped_empty += 1
            elif "并发" in note:
                skipped_concurrent += 1
            else:
                skipped_has_fm += 1

    print(f"=== Frontmatter 批量加 ===")
    print(f"  待处理笔记总数    : {len(targets)}")
    print(f"  已加 frontmatter  : {changed}")
    print(f"  跳过(空文件)      : {skipped_empty}")
    print(f"  跳过(已有 fm)     : {skipped_has_fm}")
    print(f"  跳过(并发已加)    : {skipped_concurrent}")
    if dry_run_arg:
        print(f"\n  >>> dry-run 模式 (不带 --apply 不写文件)")
        print(f"  >>> 加 --apply 才修改\n")
    if samples:
        print(f"=== 样本 (前 5 个) ===")
        for p, note in samples:
            print(f"  {p.relative_to(ROOT)}")
            print(f"    {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())