#!/usr/bin/env python3
"""
规范化中英文标点。
- 代码段 (fenced code + 行内 code) → 半角
- 中文文本段 → 全角
- wikilink / 链接 / 邮箱 / frontmatter → 跳过

修正记录:
  v1 (line-style position slicing) → 错位,wikilink/fence 嵌套会破
  v2 (dict-based 占位符查找)     → 修复嵌套问题
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 代码段内: 全角 → 半角 映射
CODE_HALF = {
    '，': ',', '：': ':', '；': ';',
    '（': '(', '）': ')',
    '？': '?', '！': '!',
    '。': '.',
    '、': ',',
    '"': '"', '"': '"',
    ''': "'", ''': "'",
}

# 文本段内: 半角 → 全角 映射
TEXT_FULL = {
    ',': '，', ':': '：', ';': '；',
    '(': '（', ')': '）',
    '?': '？', '!': '！',
}


def transform_code_half(text: str) -> tuple[str, int]:
    count = 0
    out = []
    for ch in text:
        new_ch = CODE_HALF.get(ch)
        if new_ch is not None:
            out.append(new_ch)
            count += 1
        else:
            out.append(ch)
    return ''.join(out), count


def transform_half_to_full(text: str) -> tuple[str, int]:
    count = 0
    out = []
    for ch in text:
        new_ch = TEXT_FULL.get(ch)
        if new_ch is not None:
            out.append(new_ch)
            count += 1
        else:
            out.append(ch)
    return ''.join(out), count


def protect_regions(content: str) -> tuple[str, dict[str, str]]:
    """把所有"应保留原貌"的区域占位符化。返回 (protected, {占位符: 原内容})"""
    placeholders: dict[str, str] = {}

    def fence_repl(m):
        key = f"\x00FENCE_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'```.*?\n```', fence_repl, content, flags=re.DOTALL)

    def wikilink_repl(m):
        key = f"\x00WIKI_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'!\[\[[^\]]*\]\]', wikilink_repl, protected)

    def mdlink_repl(m):
        key = f"\x00MDLINK_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'\[[^\]]*\]\([^)]*\)', mdlink_repl, protected)

    def wiki_repl(m):
        key = f"\x00WIKI2_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'\[\[[^\]]*\]\]', wiki_repl, protected)

    def inline_repl(m):
        key = f"\x00INLINE_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'`[^`\n]+`', inline_repl, protected)

    def url_repl(m):
        key = f"\x00URL_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'https?://[^\s)\]]+', url_repl, protected)

    def email_repl(m):
        key = f"\x00EMAIL_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', email_repl, protected)

    def fm_repl(m):
        key = f"\x00FM_{len(placeholders):04d}\x00"
        placeholders[key] = m.group(0)
        return key
    protected = re.sub(r'^---\n.*?\n---\n', fm_repl, protected, count=1, flags=re.DOTALL | re.MULTILINE)

    return protected, placeholders


def process_file(content: str) -> tuple[str, int, int]:
    protected, placeholders = protect_regions(content)

    full_count = 0
    half_count = 0

    # FENCE/INLINE 占位符里:做全→半
    new_placeholders = {}
    for key, body in placeholders.items():
        if key.startswith('\x00FENCE_') or key.startswith('\x00INLINE_'):
            new_body, n = transform_code_half(body)
            half_count += n
            new_placeholders[key] = new_body
        else:
            new_placeholders[key] = body

    # 全 protected 走 半→全 (占位符都是 ASCII,不会被错改)
    new_protected, n_full = transform_half_to_full(protected)
    full_count += n_full

    # 还原占位符
    final = new_protected
    for key, body in new_placeholders.items():
        final = final.replace(key, body)

    return final, full_count, half_count


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md")) + list((ROOT / "copilot").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_files = 0
    total_full = 0
    total_half = 0
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception:
            continue

        new_content, n_full, n_half = process_file(content)
        if n_full + n_half == 0:
            continue
        try:
            p.write_text(new_content, encoding="utf-8")
            total_files += 1
            total_full += n_full
            total_half += n_half
            if len(samples) < 8:
                samples.append((p, n_full, n_half))
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")

    print(f"\n=== 标点规范化完成 ===")
    print(f"  受影响笔记: {total_files}")
    print(f"  文本段 半→全: {total_full} 处")
    print(f"  代码段 全→半: {total_half} 处")
    print()
    if samples:
        print(f"=== 抽样 (前 8) ===")
        for p, f, h in samples:
            print(f"  {p.relative_to(ROOT)}  (半→全 {f}, 全→半 {h})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
