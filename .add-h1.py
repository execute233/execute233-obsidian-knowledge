#!/usr/bin/env python3
"""
为 OneNote/ 下所有 .md 笔记补 H1(基于文件名)。

策略:
  - 跳过已有真实 H1(第一个非空非代码块行是 # XXX)
  - 跳过空笔记
  - 跳过 _assets/ 下的文件
  - 跳过 copilot 目录(对话记录类)
  - H1 插在 frontmatter 之后,内容之前
  - 保留原 LF、行尾空白处理
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

H1_RE = re.compile(r"^#\s+(.+)$")


def has_real_h1(content: str) -> bool:
    """首个非空、非代码块行是 # XXX"""
    lines = content.split("\n")
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        m = H1_RE.match(stripped)
        if m and 0 < len(m.group(1).strip()) < 80:
            return True
        return False
    return False


def split_frontmatter(content: str) -> tuple[str, str]:
    """把 (frontmatter, rest) 分开。Content 必须以 --- 开头。"""
    if not content.startswith("---"):
        return "", content
    lines = content.split("\n")
    if lines[0] != "---":
        return "", content
    for i in range(1, len(lines)):
        if lines[i] == "---":
            fm = "\n".join(lines[:i + 1])
            rest = "\n".join(lines[i + 1:])
            return fm, rest
    return "", content


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    added = 0
    skipped = 0
    fail = 0
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 读取失败: {e}")
            fail += 1
            continue

        if not content.strip():
            skipped += 1
            continue
        if has_real_h1(content):
            skipped += 1
            continue

        title = p.stem
        h1 = f"# {title}"

        # 切 frontmatter
        fm, rest = split_frontmatter(content)
        # 移除 rest 开头空行
        rest_lstripped = rest.lstrip("\n")
        if fm:
            new_content = f"{fm}\n\n{h1}\n{rest_lstripped}"
        else:
            new_content = f"{h1}\n\n{rest_lstripped}"

        if len(samples) < 6:
            samples.append((p, content[:60].replace("\n", "⏎"),
                            new_content[:80].replace("\n", "⏎")))
        try:
            p.write_text(new_content, encoding="utf-8")
            added += 1
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")
            fail += 1

    print(f"\n=== H1 标题补齐完成 ===")
    print(f"  已添加 H1  : {added}")
    print(f"  跳过       : {skipped} (已有 H1 / 空)")
    print(f"  失败       : {fail}")
    print()
    if samples:
        print(f"=== 改写样本 (前 6) ===")
        for p, before, after in samples:
            print(f"  {p.relative_to(ROOT)}")
            print(f"    原文: {before!r}")
            print(f"    新文: {after!r}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
