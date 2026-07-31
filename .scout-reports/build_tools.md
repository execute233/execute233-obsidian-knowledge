# build_tools 目录 markdown 格式审计

## 概况
- 文件总数: 5
- 影响笔记数: 5/5（按硬性语法或结构可读性问题计；Frontmatter 缺失另作目录级规范备注）
- 子目录: Git / IDEA / maven
- 总行数: 120（`Git/使用.md` 92、`Git/安装 配置 初始化.md` 14、`IDEA/快捷键操作.md` 4、`maven/依赖管理.md` 6、`maven/操作.md` 4）
- 审计口径: 只读取源笔记；未改动 `OneNote/build_tools/`。图片目标做了本地存在性核验。

## 偏离清单
### 高优
- **标题层级整体缺失**: 5 个文件均没有真实 ATX 标题（`#` 至 `######`）或 setext 标题，因此没有可导航的 H1→H2→H3 层级，也没有可判定的跳级。
  - `OneNote/build_tools/Git/使用.md` L1-L92、`OneNote/build_tools/Git/安装 配置 初始化.md` L1-L14：文件名之外正文没有标题，主题名和小节名都是普通段落。
  - `OneNote/build_tools/IDEA/快捷键操作.md` L1-L4：直接以表格开始，没有文档标题。
  - `OneNote/build_tools/maven/依赖管理.md` L1 的 `1. 依赖作用域` 是孤立有序列表项，不是标题；`maven/操作.md` L1-L4 只有图片、没有标题或说明。
  - 后果是 Obsidian 大纲/目录无法识别章节；仅机械给每个文件补 H1 不能恢复内部小节边界，需人工确认。
- **Git 命令未围栏，导致语义内容被 Markdown 解析**: `OneNote/build_tools/Git/使用.md` L1-L92 与 `OneNote/build_tools/Git/安装 配置 初始化.md` L1-L14 均没有任何 fenced code block；命令、说明和 shell 注释全部作为普通段落混排。示例：`Git/使用.md` L2、L27、L56-L57、L70，安装笔记 L1-L4、L6-L12。裸命令不仅不可复制为完整代码段，也直接触发下面的 HTML/链接问题。
- **裸角括号占位符残留为 HTML-like 标签**: `OneNote/build_tools/Git/使用.md` 共 29 个 `<...>` 占位符、分布于 18 行（L2、L4、L6、L8、L23、L27、L29、L35、L39、L41、L48、L50、L56-L57、L75、L77、L87、L89-L91）；其中 27 个是 `<name>`、`<branch-name>`、`<tag>` 等符合 HTML 标签形状的 ASCII 名称。Markdown 渲染器可能将其作为原始 HTML 标签，造成占位符不显示/改变 DOM，而 `<本地分支>`、`<冲突文件>` 也缺少代码语境。应将命令放入 `bash` 代码块，正文示例改用行内代码或安全转义。
- **命令中的 Markdown 外链破坏可复制性**: `OneNote/build_tools/Git/安装 配置 初始化.md` L3-L4 把 shell 参数写成 `"[http://127.0.0.1:8080](http://127.0.0.1:8080)"`。语法上是平衡的链接、目标也与显示文本相同，但它位于命令参数中；从源码复制会带走 Markdown 标记，不能作为原始 proxy URL 使用。应在 fenced `bash` 中保留裸 URL（是否保留可点击链接需人工决定）。
- **未闭合强调标记**: `OneNote/build_tools/Git/使用.md` L45 为 `**强制让分支指向另一个提交`，只有开头 `**`、没有闭合标记；当前不会形成有效粗体，且很可能是误把小节标题写成了半截强调。应在确定语义后改为标题或成对强调。

### 中优
- **列表风格/章节语义不一致**: `OneNote/build_tools/Git/使用.md` 与 `Git/安装 配置 初始化.md` 的命令目录完全没有 `-`/`*`/`+` 或连续有序列表标记，说明行与命令行只是连续裸段落；`OneNote/build_tools/maven/依赖管理.md` 只有 L1 一个 `1.` 项，后面没有 `2.` 或同级项。这既不是一致的列表，也不是明确的标题结构。应按人工确认的章节边界改为 H2/H3、列表或代码块，不能机械把每行都加项目符号。
- **GFM 表头为空**: `OneNote/build_tools/IDEA/快捷键操作.md` L1-L4 是列数一致、分隔行有效的 4 列表格，但 L1 四个表头单元格全部为空。渲染虽可成功，阅读器大纲/无障碍/复制后语义都不明确；应补充类似“快捷键 / 功能 / 快捷键 / 功能”的表头，具体命名需人工确认。
- **中英文标点混用（仅自然语言）**: 2 个文件、4 行明确 prose 有半角标点：`OneNote/build_tools/Git/使用.md` L1 `使用(可使用通配符)`、L68 `提交,也可以...数字,`、L73 `变基: 让记录更好看？`，以及 `OneNote/build_tools/Git/安装 配置 初始化.md` L8 `token鉴权(作为密码输入)`。建议分别统一为全角括号、逗号、冒号；命令中的引号、斜杠、`->`、`#` 不应套用中文标点替换。
- **文档末尾缺少换行符**: `OneNote/build_tools/Git/使用.md`、`Git/安装 配置 初始化.md`、`IDEA/快捷键操作.md`、`maven/操作.md` 4 个文件的最后字节不是 LF；`maven/依赖管理.md` L6 后有 LF。不会改变渲染结果，但会造成 POSIX 文本工具和后续 diff 的收尾不一致，可安全补齐。
- **截图笔记缺少语义锚点（需确认）**: `OneNote/build_tools/maven/操作.md` L1-L4 是纯图片序列，`maven/依赖管理.md` L2、L4、L6 也几乎只有图片。图片语法本身没有发现断链，但没有标题、图注或步骤说明，脱离 Obsidian 预览后难以理解；是否补说明属于内容判断，不应自动生成。
- **Frontmatter 目录级缺省（规范待决，不计作单篇损坏）**: 5 个文件均没有 YAML/TOML frontmatter。仓库 `OneNote` 其余 Markdown 也未发现统一 frontmatter，且当前 linter 的插入规则关闭，因此不存在字段格式不一致。若项目决定启用元数据，应先确定 `title/tags/aliases` schema，再批量补；目前不建议把“缺失”当作自动修复项。

### 检查通过/不计偏离
- `maven/依赖管理.md` 的 5 个图片 wikilink（L2、L4、L6）和 `maven/操作.md` 的 4 个图片 wikilink（L1-L4）均能解析到本地存在的目标；未发现混用 `![](path)` 或断裂图片引用。
- 未发现实际的 `<details>`、`<br>`、`<summary>`、HTML 注释、`[TOC]`、任务框、乱码替换字符或其它明显特殊控件残留。
- 未发现未标语言的 fenced block；本目录的主要问题是命令根本未围栏，而不是已存在代码块缺语言标签。

## 自动修复可行性
- 完全可自动: 2 类（为明确缺失的文件末尾补 LF；仅对上述已确认自然语言行做保守的全/半角标点规范化）
- 需人工判断: 6 类（建立 H1/H2/H3 章节骨架；识别命令/说明边界并加 `bash` 围栏；处理 `<...>` 占位符；把命令中的 Markdown 链接还原为裸 URL；决定孤立 `1.` 与未闭合 `**` 的真实语义；补表头、图注及 Frontmatter 字段）
- 不可自动: 0 类（没有技术上绝对不可修复的格式项，但结构和内容语义不能无人审阅批量改写）

## 推荐处理顺序
1. 先为 5 篇建立文件标题和人工确认的小节骨架；优先把 `Git/使用.md` L45、`maven/依赖管理.md` L1 的伪标题转成明确 H2/H3。
2. 将 Git 命令/说明按主题分组并围栏为 `bash`；这一步会同时隔离 `<...>`，避免其被当作 HTML。
3. 在代码语境确定后修复安装笔记 L3-L4 的 Markdown 化 URL，并处理 Git/使用 L2-L91 的剩余占位符显示问题；再单独修复 L45 的强调标记。
4. 给 IDEA 表格补语义表头，统一列表表达；为 Maven 截图笔记补最小标题/图注（若内容方确认需要）。
5. 最后对自然语言做中英文标点规范化、补齐 4 个文件的末尾 LF，并按知识库政策决定是否引入 Frontmatter。

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "已逐行审计 5 个源文件，并在高/中优清单中给出具体路径、行号、数量与影响说明；例如 Git/使用.md L45 的未闭合强调、L2-L91 的 29 个角括号占位符，以及 IDEA/快捷键操作.md L1-L4 的空表头。"
    }
  ],
  "changedFiles": [
    "E:/个人知识/.pi-subagents/artifacts/progress/f6ea5cfd/progress.md",
    "E:/个人知识/.pi-subagents/artifacts/outputs/f6ea5cfd/.scout-reports/build_tools.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "find OneNote/build_tools -type f -name '*.md'",
      "result": "passed",
      "summary": "确认源 Markdown 文件总数为 5，子目录为 Git、IDEA、maven。"
    },
    {
      "command": "nl -ba/read/grep 与 Python3 只读正则扫描 OneNote/build_tools/**/*.md",
      "result": "passed",
      "summary": "完成标题、Frontmatter、列表、强调、表格、链接、HTML-like 标签、图片、标点、特殊残留和行尾检查。"
    },
    {
      "command": "Python3 Markdown 渲染探针与本地图片目标存在性检查",
      "result": "passed",
      "summary": "验证裸 <name> 会进入 HTML-like 语境、命令 URL 会渲染为链接；9/9 图片目标存在。"
    },
    {
      "command": "git diff --check -- OneNote/build_tools && git status --short -- OneNote/build_tools",
      "result": "passed",
      "summary": "源目录无 diff、无 staged 或 unstaged 修改。"
    }
  ],
  "validationOutput": [
    "5 个文件共 120 行；0 个真实标题、0 个 YAML/TOML frontmatter、0 个 fenced code block。",
    "检测到 1 个未闭合粗体标记、1 个空表头 GFM 表格、2 个命令内 Markdown 外链、29 个角括号占位符，以及 4 个缺少末尾 LF 的文件。",
    "9 个图片 wikilink 均解析到本地存在文件；源笔记未被修改。"
  ],
  "residualRisks": [
    "Obsidian 与 CommonMark 对未知 HTML-like 标签的呈现细节可能不同，但未围栏的 <name>/<tag> 仍存在语义丢失风险。",
    "标题层级、命令与说明的分组、表头名称、截图图注及 Frontmatter 字段都需要内容方判断；自动改写可能改变原始笔记意图。",
    "外链只做了 Markdown 形态和命令语境检查，未进行网络可达性测试。"
  ],
  "noStagedFiles": true,
  "diffSummary": "未修改 OneNote/build_tools 下任何源笔记；仅写入本审计报告和进度产物。",
  "reviewFindings": [
    "high: OneNote/build_tools/Git/使用.md:2-91 - 29 个裸角括号占位符，其中 27 个符合 HTML 标签形状，可能被渲染器误解析。",
    "high: OneNote/build_tools/Git/安装 配置 初始化.md:3-4 - shell proxy 命令包含 Markdown 化 URL，源码不可直接复制执行。",
    "high: OneNote/build_tools/Git/使用.md:45 - `**` 强调标记未闭合。",
    "high: OneNote/build_tools/Git/使用.md:1-92 等 5 篇 - 没有真实标题层级，正文无法形成可导航大纲。",
    "medium: OneNote/build_tools/IDEA/快捷键操作.md:1-4 - GFM 表格表头四格均为空。",
    "medium: OneNote/build_tools/maven/依赖管理.md:1 - 孤立的单条有序列表项承担疑似章节标题。",
    "medium: OneNote/build_tools/Git/使用.md:1,68,73 与 Git/安装 配置 初始化.md:8 - 自然语言半角括号/逗号/冒号混用。"
  ],
  "manualNotes": "按用户约束只读源目录；已完成清理项不列为偏离。Frontmatter 缺失被标为目录级规范待决，而非单篇损坏。"
}
```
