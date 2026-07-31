# windows 目录 markdown 格式审计

## 概况
- 文件总数: 1
- 影响笔记数: 1
- 子目录: `可选功能/`
- 检查文件: `OneNote/windows/可选功能/WSL.md`

## 偏离清单
### 高优
- **结构/标题层级**：全文没有任何 ATX 标题（`#`–`######`）。第 3 行的 `**安装**` 以强调语法充当标题；第 6、10、14、16、18、20、22、24、27、29、31、33、35 行也都是未标记的章节/命令说明，无法形成可导航的层级结构。建议至少增加一个 H1，并将安装、常用命令、磁盘挂载等分组为一致的 H2/H3。
- **代码与列表结构**：第 4、15、17、19、21、23、25、28、32、34 行是独立 shell 命令，却全部是普通段落；第 7–9、11–13、36–41 行是选项列表，却没有 `-`/`*`/`+` 列表标记。代码和选项在渲染后会与说明文字混在一起，属于结构性偏离。应将命令放入 `sh` 代码块（或统一行内代码），选项改成统一无序列表。
- **特殊残留/内容结构异常**：第 39 行末尾出现 `blkid <BlockDevice>blkid <dev/sdb1>`，两个示例命令直接拼接，疑似缺少句号、分隔符或换行；需人工确认原意后拆分。

### 中优
- **HTML 残留风险/占位符未代码化**：第 5、17、28、34、36、39、40、41 行含 `<Distribution Name>`、`<User Name>`、`<DistributionName>`、`<DiskPath>`、`<Disk>`、`<Filesystem>` 等尖括号参数。部分形式可能被 Markdown 解析器当作 HTML 标签，且当前并未统一包裹为代码；应统一置于反引号或代码块中，并保持占位符命名一致（例如 `DistributionName` 与 `Distribution Name` 的差异需人工确认）。
- **Frontmatter**：文件开头没有 YAML frontmatter。若 OneNote 笔记规范要求元数据（如 `title`、`source`、`tags`），这是缺失项；字段内容不能凭格式检查自动推断，需人工决定。若该目录明确不要求 frontmatter，可降为无偏离。
- **强调风格**：仅第 3 行使用 `**安装**`，其实际意图是章节标题而非强调。建议改为标题，不要用粗体模拟标题。
- **中文/英文标点与间距**：第 2 行以英文小写 `more see` 开头，且链接后使用 `| Microsoft Learn` 的英文竖线作为分隔；第 5、7、39 行中英文命令与中文之间缺少统一的空格/标点（如 `--install <Distribution Name>来`、`--online来`）；第 11–12 行混用英文双引号与中文括号。建议统一中文叙述标点，并将命令全部代码化后再调整间距。
- **链接**：第 2 行有 1 个标准 Markdown 链接，URL 形式正常；但链接所在整行不是完整句子（`more see` 语序/大小写异常），建议人工润色链接前后的引导文字。未发现裸 URL 或图片链接。

### 低优/未发现
- **表格**：未发现表格语法；当前内容看不出需要表格化，暂无偏离。
- **图片引用**：未发现图片引用。
- **HTML 标签**：未发现明确的 `<div>`、`<br>`、`<img>` 等 HTML 标签；上述尖括号占位符构成 HTML 解析风险。
- **行尾空格、反斜杠转义、代码块语言标签、空 Untitled**：按任务说明不重复报告；本文件也未发现可新增的相关问题。

## 自动修复可行性
- 完全可自动: 3 类（把独立命令统一包裹为 `sh` 代码块、把明确的选项行加统一列表标记、将尖括号参数包裹反引号）
- 需人工判断: 4 类（标题分组与层级、frontmatter 字段、`blkid` 拼接断句、中文/英文措辞和标点）
- 不可自动: 0 类（不存在必须依赖外部资料才能完成的格式项；但自动修改仍需人工复核语义）

## 推荐处理顺序
1. 先人工核对第 39 行 `blkid` 拼接及所有命令/占位符的原始语义，避免格式化时改变命令。
2. 建立 H1/H2/H3 标题层级，将第 3、6、10、14、16、18、20、22、24、27、29、31、33、35 行重构为章节或小节标题。
3. 将独立命令改为带 `sh` 语言标签的代码块，并将第 7–9、11–13、36–41 行改为统一无序列表。
4. 统一参数占位符的代码样式和命名，处理第 2、5、7、11、12、39 行的中英文标点、空格与措辞。
5. 根据目录规范决定是否补充 frontmatter，最后用 Markdown 渲染器复查链接、HTML 解析和层级导航。

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "已只读检查 OneNote/windows 下唯一文件 OneNote/windows/可选功能/WSL.md，并在偏离清单中给出具体行号、路径及高/中优严重度。"
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "find E:/个人知识/OneNote/windows -name '*.md'",
      "result": "passed",
      "summary": "确认目录下仅有 1 个 Markdown 文件。"
    },
    {
      "command": "read E:/个人知识/OneNote/windows/可选功能/WSL.md",
      "result": "passed",
      "summary": "读取并审计文件内容；未修改源文件。"
    },
    {
      "command": "grep markdown patterns in E:/个人知识/OneNote/windows",
      "result": "passed",
      "summary": "核查标题、列表、表格、强调、链接及尖括号残留。"
    }
  ],
  "validationOutput": [
    "文件总数 1，影响笔记数 1；源目录未执行任何写入操作。"
  ],
  "residualRisks": [
    "第 39 行 blkid 示例拼接的正确断句无法仅凭格式推断。",
    "frontmatter 是否为目录强制规范未知。",
    "尖括号占位符在不同 Markdown 渲染器中的 HTML 解析行为可能不同。"
  ],
  "noStagedFiles": true,
  "diffSummary": "只读审计，无源文件改动。",
  "reviewFindings": [
    "高优: OneNote/windows/可选功能/WSL.md:3-41 - 缺少标题层级、代码块和列表结构。",
    "高优: OneNote/windows/可选功能/WSL.md:39 - blkid 示例命令直接拼接。",
    "中优: OneNote/windows/可选功能/WSL.md:5,17,28,34,36,39-41 - 尖括号参数未代码化，存在 HTML 解析风险。",
    "中优: OneNote/windows/可选功能/WSL.md:1-41 - 未发现 frontmatter（是否偏离取决于目录规范）。"
  ],
  "manualNotes": "已按要求排除已完成清理项；报告文件本身写入指定 artifacts 输出路径，未修改任何 OneNote 源文件。"
}
```