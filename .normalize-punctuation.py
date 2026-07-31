#!/usr/bin/env python3
"""
规范化中英文标点。
- 代码段 (fenced code + 行内 code) → 半角
- 中文文本段 → 全角
- wikilink / 链接 / 邮箱 / frontmatter → 跳过
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 代码段内: 全角 → 半角 映射 (在 fenced/inline code 中)
CODE_HALF = {
    '，': ',', '：': ':', '；': ';',
    '（': '(', '）': ')',
    '？': '?', '！': '!',
    '。': '.',   # 句号 → 句点 (代码)
    '、': ',',
    '"': '"', '"': '"',
    ''': "'", ''': "'",
}

# 文本段内: 半角 → 全角 映射
TEXT_FULL = {
    ',': '，', ':': '：', ';': '；',
    '(': '（', ')': '）',
    '?': '？', '!': '！',
    # 句号 . 保留为半角(在中文中句号是 .,不是 。)— 实际上中文写作用 。
    # 但要避免把 0.5 这种小数点也转了,所以不做 . →
}


def protect_regions(content: str) -> tuple[str, list[tuple[int, int, str]]]:
    """把代码块、行内代码、wikilink、md link、URL 等保护起来,返回占位符。
    返回 (protected_content, [(start, end, placeholder)])
    """
    placeholders = []

    # fenced code block
    def fence_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00FENCE_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'```.*?\n```', fence_repl, content, flags=re.DOTALL)

    # wikilink ![[...]]
    def wikilink_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00WIKI_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'!\[\[[^\]]*\]\]', wikilink_repl, content)

    # markdown link [text](url)
    def mdlink_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00MDLINK_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'\[[^\]]*\]\([^)]*\)', mdlink_repl, content)

    # plain wikilink [[...]] (no embed)
    def wiki_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00WIKI2_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'\[\[[^\]]*\]\]', wiki_repl, content)

    # inline code `xxx`
    def inline_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00INLINE_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'`[^`\n]+`', inline_repl, content)

    # URL
    def url_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00URL_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'https?://[^\s)\]]+', url_repl, content)

    # email
    def email_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00EMAIL_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', email_repl, content)

    # frontmatter 块
    def fm_repl(m):
        body = m.group(0)
        s = m.start()
        ph = f"\x00FM_{len(placeholders)}\x00"
        placeholders.append((s, s + len(body), body))
        return ph
    content = re.sub(r'^---\n.*?\n---\n', fm_repl, content, count=1, flags=re.DOTALL | re.MULTILINE)

    return content, placeholders


def transform_half_to_full(text: str) -> tuple[str, int]:
    """文本段: 半角 → 全角 (中文语境)。计数."""
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


def transform_code_half(text: str) -> tuple[str, int]:
    """代码段: 全角 → 半角。计数。"""
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


def is_code_placeholder(ph: str) -> bool:
    return ph.startswith('\x00FENCE_') or ph.startswith('\x00INLINE_')


def process_file(content: str) -> tuple[str, int, int]:
    """处理一个文件,返回 (新内容, 全角化次数, 半角化次数)。"""
    protected, placeholders = protect_regions(content)

    # 按占位符排序,从前往后处理
    placeholders.sort(key=lambda x: x[0])

    # 替换占位符为可变标记:文本段 → 不变,代码段 → 半角化
    full_count = 0
    half_count = 0
    parts = []
    last = 0
    for start, end, body in placeholders:
        parts.append(protected[last:start])
        if is_code_placeholder(body):
            # code: 全角 → 半角
            new_body, n = transform_code_half(body)
            half_count += n
            parts.append(new_body)
        else:
            parts.append(body)
        last = end
    parts.append(protected[last:])

    new_protected = ''.join(parts)

    # 现在 new_protected 是"代码已半角化、文本段还在"
    # 对全部剩余文本做 半角 → 全角
    new_protected, n_full = transform_half_to_full(new_protected)
    full_count += n_full

    return new_protected, full_count, half_count


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
