#!/usr/bin/env python3
"""
更精细的"行级"代码包裹器:
  - 逐行判断"代码"还是"文本"
  - 连续 2+ 代码行形成 run
  - 每个 run 包成 fenced code block
  - 单行代码不动

启发式:
  强匹配 (是代码): 行首匹配 shell/python/c#/java/kotlin/sql/yaml/xml/regex
  弱匹配 (是代码): 含 4+ 代码符号 (去掉 * 和 _,以免把 **xxx** 误判)
  中文比例 > 50% → 不是

避免:
  - **xxx** 强调伪标题(被 sym_count 误判)
  - 1. **xxx** 编号列表伪标题
  - 列表项 (- xxx) 在纯叙述段落中
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 删掉 * 和 _ (emphasis 标记太常见)
CODE_SYMS = set('=()[]{}<>;|\\&!@#$%^+-/`"\'')

# 强匹配: pattern → 语言
STRONG_PATTERNS = [
    # shell prompts
    (r'^\s*[$>]\s', "bash"),
    # 常见 shell 命令
    (r'^\s*(git|docker|docker-compose|apt|apt-get|curl|wget|cd|ls|cat|echo|printf|sudo|systemctl|service|chmod|chown|mv|cp|rm|mkdir|rmdir|touch|vim|vi|nano|grep|egrep|find|awk|sed|ps|kill|killall|tar|zip|unzip|gzip|gunzip|ssh|scp|rsync|psql|mysql|redis-cli|ping|netstat|ifconfig|ip|route|export|source|alias|unalias|env|which|file|less|more|head|tail|wc|sort|uniq|diff|patch|xargs|tee|nohup|eval|exec|exit|umask|chgrp|ln|readlink|basename|dirname|realpath|stat|passwd|su|login|reboot|shutdown|halt|sync|mount|umount|swapon|swapoff|blkid|lsblk|crontab|at|journalctl|loginctl|conda|pip|python|node|java|javac|make|cmake|gcc|iwr|mvn|npm|gradle|kotlinc|keytool|bash|sh|zsh|fish)\b', "bash"),
    # Python
    (r'^\s*(def|class|import|from|print|if|elif|else|for|while|try|except|with|as|return|yield|raise|pass|break|continue|lambda|global|nonlocal|assert|@)\b', "python"),
    # Java 优先 (System.out, Thread, package, String[], Spring annotations)
    (r'^\s*(public\s+(static\s+)?(class|void|int|long|String|boolean|@interface|abstract|final)|@Override|@Autowired|@RestController|@Component|@Service|@Repository|@Configuration|@Bean|@RequestMapping|@PostMapping|@GetMapping|@Post\s*Mapping|@PathVariable|@RequestParam|@RequestBody|@Transactional|@Value|@Lazy|@Scope|@Resource|@ResponseBody|@RestController)\b', "java"),
    (r'^\s*(System\.(out|err|in)\.|Thread\.\w|Thread\s+\w|new\s+Thread|String\[\]|String\s+\w|@SuppressWarnings|@SafeVarargs)\b', "java"),
    (r'^\s*(import\s+java\.|package\s+[\w.]+;)', "java"),
    # C# / Kotlin / JS / TS (去掉公有 Java 关键字)
    (r'^\s*(void|class|public|private|protected|static|return|if|else|for|while|switch|case|break|continue|new|this|super|abstract|final|interface|extends|implements|import|package|const|let|var|function|using|namespace|enum|struct|typedef|sizeof|typeof|instanceof|do|try|catch|finally|throw|throws|fun|val|object|companion|when|is|sealed|data|open|override|internal|out|@)\b', "csharp"),
    # SQL
    (r'^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE|select|insert|update|delete|create|alter|drop|set|values|from|where|order|group|having|join|union|with|as|on|desc|asc|limit|offset|begin|commit|rollback|use|show|describe|desc|explain|like|in|not|and|or|null|is|default|primary|foreign|key|references|index|unique|check|constraint)\b', "sql"),
    # XML/HTML
    (r'^\s*<[\w!?/]', "xml"),
    # Dockerfile
    (r'^\s*(FROM|RUN|CMD|COPY|ADD|ENTRYPOINT|ENV|EXPOSE|WORKDIR|USER|VOLUME|ARG|LABEL|STOPSIGNAL|HEALTHCHECK|SHELL|ONBUILD)\b', "dockerfile"),
    # YAML: starts with `key:` (有或无 value)
    (r'^\s*[\w][\w-]*:', "yaml"),
    # C/C++: 指针解引用赋值 / 明显 C 语法
    (r'^\s*\*\w+\s*=', "cpp"),
    (r'^\s*(int|char|long|float|double|void|bool|auto|const|static|extern|sizeof|typedef|struct|enum|union|unsigned|signed|short)\s+\w+[\s*]', "cpp"),
    # JSON: starts with { or [ or "]"
    (r'^\s*[\{\[]|"\s*:\s*[\d"]', "json"),
    # shell/python/yaml comments
    (r'^\s*#[^!]', "bash"),
]


def chinese_ratio(s: str) -> float:
    if not s:
        return 0.0
    chinese = sum(1 for c in s if '\u4e00' <= c <= '\u9fff')
    return chinese / len(s)


def is_code_line(line: str) -> bool:
    """行是否像代码。"""
    s = line.strip()
    if not s:
        return False
    # 排除 markdown 表格
    if s.startswith('|'):
        return False
    # 排除 wikilink 图片
    if s.startswith('![['):
        return False
    # 排除 markdown 链接行 [text](url)
    if re.match(r'^\s*\[.+\]\(.+\)', s):
        return False
    # 优先级 0: 注释行 (肩 # 或 ##) → 跳中文检查
    if re.match(r'^\s*#+\s', s):
        for pat, _ in STRONG_PATTERNS:
            if re.search(pat, line):
                return True
        # 没见过 # 却不匹配?默认当成代码
        return True
    # 中文比例 > 50% → 不是
    if chinese_ratio(s) > 0.5:
        return False
    # 强匹配
    for pat, _ in STRONG_PATTERNS:
        if re.search(pat, line):
            return True
    # 弱匹配: >= 4 个代码符号
    sym_count = sum(1 for c in s if c in CODE_SYMS)
    return sym_count >= 4


def guess_lang(run_lines: list[str]) -> str:
    """投票决定语言。"""
    from collections import Counter
    langs = []
    for line in run_lines:
        if not is_code_line(line):
            continue
        for pat, lang in STRONG_PATTERNS:
            if re.search(pat, line):
                langs.append(lang)
                break
    if not langs:
        return "text"
    return Counter(langs).most_common(1)[0][0]


def wrap_code_runs(content: str) -> tuple[str, int]:
    """包连续代码行为 fenced block。"""
    parts = re.split(r'(```.*?\n```)', content, flags=re.DOTALL)
    new_parts = []
    n_wrapped = 0
    for part in parts:
        if part.startswith('```') and part.endswith('```'):
            new_parts.append(part)
            continue
        lines = part.split('\n')
        new_lines = []
        run = []
        for line in lines:
            if is_code_line(line):
                run.append(line)
            else:
                if len(run) >= 2:
                    lang = guess_lang(run)
                    new_lines.append(f'```{lang}')
                    new_lines.extend(run)
                    new_lines.append('```')
                    n_wrapped += 1
                elif len(run) == 1:
                    new_lines.append(run[0])
                run = []
                new_lines.append(line)
        # 处理文件末尾 run
        if len(run) >= 2:
            lang = guess_lang(run)
            new_lines.append(f'```{lang}')
            new_lines.extend(run)
            new_lines.append('```')
            n_wrapped += 1
        elif len(run) == 1:
            new_lines.append(run[0])
        new_parts.append('\n'.join(new_lines))
    return ''.join(new_parts), n_wrapped


def is_unity_file(rel_path: str) -> bool:
    """判定是否为 Unity 笔记（绝大多数是纯 C# 代码）。"""
    return rel_path.startswith('OneNote/unity/')


def wrap_unity_file(content: str) -> tuple[str, int]:
    """Unity 笔记: 整篇包成 cs fence。
    例外: 如果文件已有 fence 或文件以 Ruby 强调/H2 以上其他内容开头,不包。"""
    if '```' in content:
        return content, 0
    # 跳过 H1 标题
    lines = content.split('\n')
    if not lines:
        return content, 0
    # 移除 H1 行
    body_lines = []
    h1 = None
    for line in lines:
        if line.startswith('#') and not h1:
            h1 = line
            continue
        body_lines.append(line)
    body = '\n'.join(body_lines).strip()
    if not body:
        return content, 0
    # 检查是否是 C# 代码（明显标记）
    cs_markers = sum(1 for pat in [r'\busing\s+UnityEngine\b', r'\bMonoBehaviour\b',
                                    r'\bDebug\.\w', r'\bInput\.\w', r'\bGameObject\b',
                                    r'\bTransform\b', r'\bRigidbody\b', r'\bVector[23]\b',
                                    r'\bOnTrigger\w*\(', r'\bOnCollision\w*\(', r'\bStart\(\)\b',
                                    r'\bUpdate\(\)\b', r'\bAwake\(\)\b'] if re.search(pat, body))
    if cs_markers < 2:
        return content, 0
    # 跳去尾部 blank lines
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()
    # 拼接
    new_body = '\n'.join(body_lines)
    new_content = (h1 + '\n\n' if h1 else '') + '```cs\n' + new_body + '\n```'
    return new_content, 1


def main() -> int:
    md_files = list((ROOT / "OneNote").rglob("*.md"))
    targets = [p for p in md_files if "_assets" not in p.parts]

    total_files = 0
    total_wrapped = 0
    samples = []

    for p in targets:
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = p.read_text(encoding="gbk", errors="replace")
        except Exception:
            continue

        rel = str(p.relative_to(ROOT))
        n_wrapped = 0
        # Unity 特殊处理
        if is_unity_file(rel):
            new_content, n_u = wrap_unity_file(content)
            n_wrapped += n_u
        else:
            new_content = content
        # 一般代码包裹
        new_content, n_run = wrap_code_runs(new_content)
        n_wrapped += n_run

        if n_wrapped == 0:
            continue
        try:
            p.write_text(new_content, encoding="utf-8")
            total_files += 1
            total_wrapped += n_wrapped
            if len(samples) < 8:
                # 找一段新的围栏作为样本
                m = re.search(r'```(\w*)\n(.*?)\n```', new_content, re.DOTALL)
                if m:
                    snip = m.group(0)[:200]
                    samples.append((p, snip))
        except Exception as e:
            print(f"  ! {p.relative_to(ROOT)} 写入失败: {e}")

    print(f"\n=== 代码段包裹完成 ===")
    print(f"  受影响笔记: {total_files}")
    print(f"  包裹代码段  : {total_wrapped}")
    print()
    if samples:
        print(f"=== 抽样 (前 8) ===")
        for p, snip in samples:
            print(f"  {p.relative_to(ROOT)}")
            for line in snip.split('\n'):
                print(f"    {line[:80]}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
