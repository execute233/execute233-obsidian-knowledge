#!/usr/bin/env python3
"""
清掉所有 .md 文件的行尾空格(trailing whitespace)。
- 只针对 行内有内容后再接空格的行;全空白行作为空行保留
- 排除 _assets/ 内的任何文件
- 写回原文件(保留 LF,不变 CRLF)
- 不修改 _DIAG-* 诊断笔记
- 报告改动统计
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_DIR_NAMES = {"_assets"}
SKIP_FILE_NAMES = set()  # 暂不跳任何

def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md")) + list((ROOT / "copilot").rglob("*.md"))
    targets = [p for p in md_files if not any(part in SKIP_DIR_NAMES for part in p.parts)]

    total_files_changed = 0
    total_lines_stripped = 0
    total_chars_removed = 0
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")

        # 必须以 LF 结尾才规范;不存在 CRLF,所以原样即可
        new_lines = []
        file_changes = 0
        file_chars = 0
        for line in content.splitlines():
            stripped = line.rstrip()
            if len(stripped) != len(line):
                file_changes += 1
                file_chars += len(line) - len(stripped)
                if len(samples) < 8:
                    samples.append((p.relative_to(ROOT), line[:60]))
            new_lines.append(stripped)
        new_content = "\n".join(new_lines)
        if content.endswith("\n"):
            new_content += "\n"

        if file_changes:
            p.write_text(new_content, encoding="utf-8")
            total_files_changed += 1
            total_lines_stripped += file_changes
            total_chars_removed += file_chars

    print(f"\n=== 行尾空格清理完成 ===")
    print(f"  受影响笔记: {total_files_changed} / {len(targets)} 篇")
    print(f"  清理行数  : {total_lines_stripped} 行")
    print(f"  移除字节  : {total_chars_removed} 个空格")
    if samples:
        print(f"\n=== 改写样本 (前 8 行) ===")
        for path, line in samples:
            print(f"  {path}")
            print(f"    原文: {line!r}")
            print(f"    新文: {line.rstrip()!r}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
