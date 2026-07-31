#!/usr/bin/env python3
"""
修补: 把已迁移笔记里的裸 wikilink  ![[name.png]!
改成显式相对路径  ![[_assets/{slug}/name.png]!
仅作用于指定主题的 .md 文件。
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# 抓 ![[ xxx __HH-MM-SS-N.{ext} ]]
WIKILINK_RE = re.compile(r"!\[\[([^\]]+)\]\]")
SLUG_RE = re.compile(r"^(.+)__\d{2}-\d{2}-\d{2}-\d+\.(png|jpe?g)$", re.IGNORECASE)

def slugify(name: str) -> str:
    s = Path(name).stem
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r'[\\/:*?"<>|]', "-", s)
    return s.strip("-") or "note"

def read_note(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="gbk", errors="replace")

def fix_note(note: Path) -> int:
    """返回该笔记修改了多少处。"""
    content = read_note(note)
    slug = slugify(note.name)
    attach_dir = note.parent / "_assets" / slug
    changed = 0
    new_lines = []
    # 按行处理以便更精确匹配(同时输出 diff 友好)
    # 但 wikilink 可能在行内也可能在行尾,直接 sub 也行
    def repl(m: re.Match) -> str:
        nonlocal changed
        inner = m.group(1).strip()
        # 已经是相对路径的(包含 / )不动
        if "/" in inner or "\\" in inner:
            return m.group(0)
        # 仅当文件名形如 {slug}__HH-MM-SS-N.{ext} 时改写
        mm = SLUG_RE.match(inner)
        if not mm:
            return m.group(0)
        # 二次验证: 目标文件必须真实存在(否则保持原样免得回归)
        target = attach_dir / inner
        if not target.exists():
            return m.group(0)
        changed += 1
        return f"![[_assets/{slug}/{inner}]]"
    new_content = WIKILINK_RE.sub(repl, content)
    if changed:
        note.write_text(new_content, encoding="utf-8")
    return changed

def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "java"
    topic_dir = ROOT / "OneNote" / topic
    if not topic_dir.is_dir():
        print(f"❌ OneNote/{topic} 不存在")
        sys.exit(1)
    notes = list(topic_dir.rglob("*.md"))
    # 排除 _assets 内(以防扫描目录本身)
    notes = [n for n in notes if "_assets" not in n.parts]
    total_changed = 0
    affected_files = 0
    for note in notes:
        c = fix_note(note)
        if c:
            affected_files += 1
            total_changed += c
            print(f"  ↻ {note.relative_to(ROOT)}  ({c} 处)")
    print(f"\n✅ 完成。共改写 {total_changed} 处 wikilink,影响 {affected_files} 篇笔记。")
    print("   建议: 在 Obsidian 中稍等几秒让其重建索引,或重启 Obsidian 强制刷新。")

if __name__ == "__main__":
    main()
