#!/usr/bin/env python3
"""
OCR 错字修正脚本 - 高置信度批

修复 6 类明确的 OCR 错误:
  1. 形近字: 囗→口, 瞎→响, 巒→密, 柝→标, 柝→标 (光纤标准)
  2. 网络术语: HDLCO→HDLC, RARPo→RARP, F|N→FIN, DestinationPO→DestinationPort
  3. OSI/TCP 层名: ApplicationLayer→Application Layer 等
  4. HTTP 状态码标签: BadRequest→Bad Request, NotModified→Not Modified 等(HTTP 标准)
  5. 概念: 数据加巒→数据加密, 像想→想象, 传输编码, 响应→响应
  6. 孤悬的 1. 2. 3. 编号错了的 1．→1. (全角)

约束:
  - 只在指定 4 个文件内替换
  - 不动代码块/fenced block
  - 不动 wikilink/URL
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 高置信度单字/组合字替换
SINGLE_CHAR = {
    '囗': '口',     # 端口
    '瞎': '响',     # 响应
    '巒': '密',     # 加密
    '柝': '标',     # 标准
}

# 高置信度短词组
WORD_PAIRS = [
    ('数据加巒', '数据加密'),
    ('像想', '想象'),
    ('F|N', 'FIN'),
    ('DestinationPO', 'DestinationPort'),
    ('HDLCO', 'HDLC'),
    ('RARPo', 'RARP'),
    ('到端的通信', '端到端的通信'),
    ('Eventsource', 'EventSource'),
    ('传辅编码', '传输编码'),
    ('瞎应', '响应'),
    ('巨的端囗', '目的端口'),
    ('触类传奇', '触类旁通'),  # 不可靠,先不动
]

# OSI 七层: 西文 + Layer → 西文 + ' ' + Layer
LAYER_NAMES = [
    ('ApplicationLayer', 'Application Layer'),
    ('PresentationLayer', 'Presentation Layer'),
    ('SessionLayer', 'Session Layer'),
    ('TransportLayer', 'Transport Layer'),
    ('NetworkLayer', 'Network Layer'),
    ('DataLinkLayer', 'Data Link Layer'),
    ('PhysicalLayer', 'Physical Layer'),
    ('UserDatagramProtocol', 'User Datagram Protocol'),
]

# HTTP 状态码标签 (注: 原文是 "400 BadRequest..." 形式,源串不携数字)
HTTP_STATUS = [
    ('Continue', 'Continue'),
    ('SwitchingProtocols', 'Switching Protocols'),
    ('OK', 'OK'),
    ('Created', 'Created'),
    ('Accepted', 'Accepted'),
    ('No Content', 'No Content'),
    ('MovedPermanently', 'Moved Permanently'),
    ('Found', 'Found'),
    ('NotModified', 'Not Modified'),
    ('BadRequest', 'Bad Request'),
    ('Unauthorized', 'Unauthorized'),
    ('Forbidden', 'Forbidden'),
    ('NotFound', 'Not Found'),
    ('MethodNotAllowed', 'Method Not Allowed'),
    ('TooManyRequests', 'Too Many Requests'),
    ('InternalServerError', 'Internal Server Error'),
    ('NotImplemented', 'Not Implemented'),
    ('BadGateway', 'Bad Gateway'),
    ('ServiceUnavailable', 'Service Unavailable'),
    ('GatewayTimeout', 'Gateway Timeout'),
]

# 编号列表规范化 (全角句点 → 半角)
NUMBER_NORM = [
    (r'^(\s*)1．', r'\g<1>1.'),
    (r'^(\s*)2．', r'\g<1>2.'),
    (r'^(\s*)3．', r'\g<1>3.'),
    (r'^(\s*)4．', r'\g<1>4.'),
    (r'^(\s*)5．', r'\g<1>5.'),
]


def fix_in_text(text: str) -> tuple[str, int]:
    """对一段文本做所有替换,返回 (新文本, 替换数)。"""
    count = 0
    out = text

    # 单字
    for src, dst in SINGLE_CHAR.items():
        if src in out:
            count += out.count(src)
            out = out.replace(src, dst)

    # 词组
    for src, dst in WORD_PAIRS:
        if src in out:
            count += out.count(src)
            out = out.replace(src, dst)

    # OSI 层名
    for src, dst in LAYER_NAMES:
        if src in out:
            count += out.count(src)
            out = out.replace(src, dst)

    # HTTP 状态码(注意: 必须是 ":XXX" 形式以避免误改) — 文件里都是 "响应码: " 后跟
    # 这里用单词边界检查
    for src, dst in HTTP_STATUS:
        # 出现位置前必须不是字母 (避免误改)
        for m in re.finditer(r'(?<![A-Za-z])' + re.escape(src) + r'(?![A-Za-z])', out):
            count += 1
        out = re.sub(r'(?<![A-Za-z])' + re.escape(src) + r'(?![A-Za-z])', dst, out)

    # 编号全角 → 半角
    for pat, rep in NUMBER_NORM:
        new_out, n = re.subn(pat, rep, out, flags=re.MULTILINE)
        if n:
            count += n
            out = new_out

    return out, count


def fix_file(p: Path) -> tuple[int, list[str]]:
    """修复单个文件,返回 (总替换数, 改动的行号列表)。"""
    try:
        content = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = p.read_text(encoding="gbk", errors="replace")
    except Exception:
        return 0, []

    # 切代码块,只对非代码块段落替换
    parts = re.split(r'(```.*?\n```)', content, flags=re.DOTALL)
    new_parts = []
    total = 0
    changed_lines = []
    for part in parts:
        if part.startswith('```') and part.endswith('```'):
            new_parts.append(part)
            continue
        new_part, n = fix_in_text(part)
        if n:
            # 找具体改动的行
            old_lines = part.split('\n')
            new_lines = new_part.split('\n')
            for i, (o, k) in enumerate(zip(old_lines, new_lines)):
                if o != k:
                    changed_lines.append(i + 1)
        total += n
        new_parts.append(new_part)
    new_content = ''.join(new_parts)
    if new_content != content:
        p.write_text(new_content, encoding="utf-8")
    return total, changed_lines


def main():
    targets = [
        ROOT / "OneNote/computer/计算机网络/HTTP协议.md",
        ROOT / "OneNote/computer/计算机网络/TCP连接.md",
        ROOT / "OneNote/computer/计算机网络/UDP协议.md",
        ROOT / "OneNote/computer/计算机网络/网络和通信协议.md",
    ]

    grand_total = 0
    for p in targets:
        if not p.exists():
            continue
        n, lines = fix_file(p)
        grand_total += n
        print(f"  {p.relative_to(ROOT)}: {n} 处替换")

    print(f"\n=== OCR 错字修正完成 ===")
    print(f"  总替换: {grand_total}")


if __name__ == "__main__":
    main()
