#!/usr/bin/env python3
"""
把 OneNote/ 下 **文件首 H1 之后** 的连续 N. xxx 编号列表转成 ## N. xxx 标题。

启发式:
  1. 找 H1 行 (首个代码块外 ^# )
  2. 从 H1+1 开始,找连续 N. xxx 段 (跳过空行、跳过代码块)
  3. 段长度 ≥ 2 行
  4. 段内每行内容.len() ≤ 60 字符 ("1. xxx" 中 xxx 部分)
  5. 段后接空行或非编号行(非嵌套)
  6. 段内每行号可以是 1, 2, 3... 也可以跳号 (1, 3, 5)

动作:
  - 1. xxx   →  ## xxx
  - 2. xxx   →  ## xxx  (残缺或跳号也保持同级 ##)
  - 数字部分去掉

输出:
  - 打印每个文件的处理决策
  - 写文件
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NUM_RE = re.compile(r'^(\d+)\.\s+(.+)$')
H1_RE = re.compile(r'^#\s+\S')


def find_h1(lines: list[str]) -> int | None:
    """在第一个代码块外的 H1 行索引, 否则 None"""
    in_fence = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence: continue
        if H1_RE.match(line):
            return i
    return None


def find_num_run(lines: list[str], start: int) -> tuple[int, int] | None:
    """从 start 开始,找连续 N. xxx 段。返回 (run_start, run_end) 索引, 段长 < 2 返回 None。"""
    in_fence = False
    run_start = None
    run_end = None
    for i in range(start, len(lines)):
        line = lines[i]
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence: continue
        m = NUM_RE.match(line)
        if m:
            if run_start is None:
                run_start = i
            run_end = i
        else:
            if run_start is not None and line.strip() == '':
                continue
            # 撞到非编号非空行, 段结束
            if run_start is not None:
                break
    if run_start is None:
        return None
    if run_end - run_start < 1:  # 段长 < 2
        return None
    return (run_start, run_end)


def is_segment_transformable(lines: list[str], start: int, end: int) -> bool:
    """段内每行内容(数字后部分) ≤ 60 字符才算 '章节大纲', 否则保持原状 (避免误伤真列表步骤)"""
    for i in range(start, end + 1):
        m = NUM_RE.match(lines[i])
        if not m:
            return False
        content = m.group(2).strip()
        if len(content) > 60:
            return False
    return True


def restate(num_lines: list[str]) -> list[str]:
    """1. xxx → ## xxx"""
    out = []
    for line in num_lines:
        m = NUM_RE.match(line)
        if m:
            content = m.group(2).strip()
            out.append(f"## {content}")
        else:
            out.append(line)
    return out


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_files = 0
    total_lines = 0
    samples = []
    skipped = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception:
            continue

        lines = content.split("\n")
        h1_idx = find_h1(lines)
        if h1_idx is None:
            continue

        run = find_num_run(lines, h1_idx + 1)
        if run is None:
            continue
        run_start, run_end = run

        if not is_segment_transformable(lines, run_start, run_end):
            skipped.append((p, lines[run_start:run_end + 1]))
            continue

        # 转换
        original_block = lines[run_start:run_end + 1]
        transformed = restate(original_block)
        new_lines = lines[:run_start] + transformed + lines[run_end + 1:]
        new_content = "\n".join(new_lines)

        # 写
        try:
            p.write_text(new_content, encoding="utf-8")
            total_files += 1
            total_lines += len(original_block)
            if len(samples) < 8:
                samples.append((p, original_block[:3], transformed[:3]))
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")

    print(f"\n=== 编号列表转 ## 标题 ===")
    print(f"  处理笔记数: {total_files}")
    print(f"  转换为 ## 的行数: {total_lines}")
    print(f"  跳过 (含长内容真列表): {len(skipped)}")
    print()
    if samples:
        print("=== 抽样 (前 8) ===")
        for p, o, t in samples:
            print(f"  {p.relative_to(ROOT)}")
            for line in o:
                print(f"    原: {line}")
            for line in t:
                print(f"    新: {line}")
            print()
    if skipped:
        print("=== 跳过的笔记 (含长内容, 保留) ===")
        for p, o in skipped:
            print(f"  {p.relative_to(ROOT)}")
            for line in o[:3]:
                print(f"    {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
