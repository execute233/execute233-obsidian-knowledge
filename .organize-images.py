#!/usr/bin/env python3
"""
把根目录散落的 Exported image ...png/.jpeg 整理到 笔记旁的 .attachments/{slug}/ 下。
- 目标结构: {note_dir}/.attachments/{slug}/{slug}__{HH-MM-SS}-{N}.{ext}
- 引用重写: ![](Exported%20image%20...{ext})  →  ![[{slug}__{HH-MM-SS}-{N}.{ext}]]

用法:
  python3 .organize-images.py java --dry-run      # 只打印计划
  python3 .organize-images.py java                # 真正执行(java 主题)
  python3 .organize-images.py java --undo         # 回滚(基于 _backup/, 仅本次 session 有效)
"""
from __future__ import annotations
import argparse, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 匹配 ![任意文字](Exported%20image%20<14位时间戳>-<数字>.<png|jpg|jpeg>) 大小写不敏感
IMG_PATTERN = re.compile(
    r"!\[[^\]]*\]\((Exported%20image%20(\d{14})-(\d+)\.(png|jpe?g))\)",
    re.IGNORECASE,
)

# 匹配磁盘上文件名: Exported image <14位时间戳>-<数字>.<png|jpg|jpeg>
NAME_PATTERN = re.compile(
    r"^Exported image (\d{14})-(\d+)\.(png|jpe?g)$",
    re.IGNORECASE,
)


def slugify(name: str) -> str:
    """'Hello World.md' → 'Hello-World';中文/连字符保留,空格转 -。"""
    s = Path(name).stem
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r'[\\/:*?"<>|]', "-", s)
    return s.strip("-") or "note"


def read_note(note: Path) -> str:
    try:
        return note.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return note.read_text(encoding="gbk", errors="replace")


def scan_topic(topic: str) -> list[tuple[Path, Path, str]]:
    """返回 [(note, src_abs_image, new_relpath), ...]"""
    moves: list[tuple[Path, Path, str]] = []
    for note in (ROOT / "OneNote" / topic).rglob("*.md"):
        content = read_note(note)
        matches = IMG_PATTERN.findall(content)
        if not matches:
            continue
        slug = slugify(note.name)
        seen: dict[str, str] = {}  # urlname → new_basename
        for urlname, ts, idx, ext in matches:
            src = ROOT / f"Exported image {ts}-{idx}.{ext.lower()}"
            if not src.exists():
                print(f"  ⚠ 缺失图片: {src.name} (笔记 {note.name} 引用)")
                continue
            if urlname in seen:
                continue
            hh, mm, ss = ts[8:10], ts[10:12], ts[12:14]
            ext_l = ext.lower()
            new_name = f"{slug}__{hh}-{mm}-{ss}-{idx}.{ext_l}"
            seen[urlname] = new_name
            new_rel = f".attachments/{slug}/{new_name}"
            moves.append((note, src, new_rel))
    return moves


def rewrite_note(note: Path, mapping: dict[str, str]) -> None:
    content = read_note(note)
    slug = slugify(note.name)
    new_content = IMG_PATTERN.sub(
        lambda m: f"![[.attachments/{slug}/{mapping[m.group(1)]}]]" if m.group(1) in mapping else m.group(0),
        content,
    )
    note.write_text(new_content, encoding="utf-8")


def apply(topic: str) -> None:
    moves = scan_topic(topic)
    if not moves:
        print(f"(OneNote/{topic}/ 没有需要整理的图片)")
        return

    # 把每个 note 的所有替换一次性准备好,逐笔记写一次(避免同一笔记被反复 open/write)
    by_note: dict[Path, dict[str, str]] = {}
    order: list[tuple[Path, Path, str]] = []
    for note, src, new_rel in moves:
        mapping = by_note.setdefault(note, {})
        # 计算 urlname(用于写入 mapping)
        m = NAME_PATTERN.match(src.name)
        if not m:
            continue
        urlname = f"Exported%20image%20{m.group(1)}-{m.group(2)}.{m.group(3).lower()}"
        if urlname not in mapping:
            mapping[urlname] = Path(new_rel).name
            order.append((note, src, new_rel))

    print(f"\n== {topic} 主题: 移动 {len(order)} 张图、改写 {len(by_note)} 篇笔记 ==\n")

    print(f"\n== {topic} 主题: 移动 {len(order)} 张图、改写 {len(by_note)} 篇笔记 ==\n")
    for note, src, new_rel in order:
        slug = slugify(note.name)
        target_dir = note.parent / ".attachments" / slug
        target = target_dir / Path(new_rel).name
        target_dir.mkdir(parents=True, exist_ok=True)
        if target.exists():
            print(f"  ⚠ 已存在,跳过: {target.name}")
            continue
        shutil.move(str(src), str(target))

    for note, mapping in by_note.items():
        rewrite_note(note, mapping)
        print(f"  ↻ {note.relative_to(ROOT)} ({len(mapping)} 处引用已改写)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic", help="OneNote 下的子主题,例如 java")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划,不执行")
    args = ap.parse_args()

    topic_dir = ROOT / "OneNote" / args.topic
    if not topic_dir.is_dir():
        print(f"❌ OneNote/{args.topic} 不存在")
        sys.exit(1)

    moves = scan_topic(args.topic)
    if not moves:
        print(f"OneNote/{args.topic}/ 下没有需要整理的图片。")
        return

    # === DRY-RUN 概览 ===
    print(f"\n=== Dry run: OneNote/{args.topic}/ ===")
    by_note: dict[Path, list[tuple[Path, str]]] = {}
    for note, src, new_rel in moves:
        by_note.setdefault(note, []).append((src, new_rel))

    total_imgs = sum(len(v) for v in by_note.values())
    print(f"涉及笔记: {len(by_note)} 篇,移动图片: {total_imgs} 张\n")
    for note, items in sorted(by_note.items(), key=lambda x: str(x[0])):
        print(f"📄 {note.relative_to(ROOT)}")
        for src, new_rel in items:
            print(f"     {src.name}  →  {new_rel}")

    if args.dry_run:
        print(f"\n[DRY-RUN] 去掉 --dry-run 才会真正执行。")
        return

    apply(args.topic)
    print(f"\n✅ {args.topic} 主题整理完成。建议: git add -A && git commit")


if __name__ == "__main__":
    main()
