#!/usr/bin/env python3
"""
把 .attachments/ 改名为 _assets/(避开点号开头的潜在索引问题),
并同步改写所有 ![[.attachments/...]] 形式的 wikilink。
"""
from __future__ import annotations
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    one_dir = ROOT / "OneNote"
    # 1) 找到所有 .attachments/ 目录
    dot_dirs = [d for d in one_dir.rglob(".attachments") if d.is_dir()]
    print(f"找到 {len(dot_dirs)} 个 .attachments/ 目录:")
    for d in dot_dirs:
        print(f"  {d.relative_to(ROOT)}")
    print()

    # 2) 重命名: .attachments  →  _assets
    rename_count = 0
    for d in dot_dirs:
        new = d.with_name("_assets")
        if new.exists():
            print(f"  ⚠ 目标已存在,跳过: {new.relative_to(ROOT)}")
            continue
        d.rename(new)
        rename_count += 1
        print(f"  ✔ mv {d.relative_to(ROOT)}  →  {new.relative_to(ROOT)}")
    print(f"\n目录重命名完成: {rename_count} 个。\n")

    # 3) 改写笔记里的 wikilink (把 .attachments/ 替换成 _assets/)
    wikilink_re = re.compile(r"!\[\[\.attachments/([^\]]+)\]\]")
    note_count = 0
    edit_count = 0
    # 找所有被 git 跟踪 / 在 vault 内 的 .md
    for note in one_dir.rglob("*.md"):
        if ".attachments" in note.parts or "_assets" in note.parts:
            continue
        try:
            content = note.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = note.read_text(encoding="gbk", errors="replace")
        new_content, n = wikilink_re.subn(r"![[_assets/\1]]", content)
        if n:
            note.write_text(new_content, encoding="utf-8")
            note_count += 1
            edit_count += n
    print(f"笔记 wikilink 改写: {edit_count} 处,影响 {note_count} 篇。")

    # 4) 同时改 .fix-wikilinks.py 里硬编码的 .attachments/, 保持脚本可用
    fix_script = ROOT / ".fix-wikilinks.py"
    if fix_script.exists():
        txt = fix_script.read_text(encoding="utf-8")
        new_txt = txt.replace(".attachments", "_assets")
        if new_txt != txt:
            fix_script.write_text(new_txt, encoding="utf-8")
            print(f"  ↻ .fix-wikilinks.py 也已同步")
    # 5) 同步 .organize-images.py(给未来批次)
    org_script = ROOT / ".organize-images.py"
    if org_script.exists():
        txt = org_script.read_text(encoding="utf-8")
        new_txt = txt.replace(".attachments", "_assets")
        if new_txt != txt:
            org_script.write_text(new_txt, encoding="utf-8")
            print(f"  ↻ .organize-images.py 也已同步")

if __name__ == "__main__":
    main()
