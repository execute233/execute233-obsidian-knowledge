# java 目录 markdown 格式审计

## 概况
- 文件总数: 73
- 影响笔记数: 73
- 子目录: javaSE / Spring框架 / Mybatis / RabbitMQ / 小框架 / 源码 / 设计模式

## 偏离清单 (按严重程度排)
### 高优 (可读性问题)
- **标题结构缺失/误判**: 73 个文件 / 76 处。71 篇没有 `# H1`；其余 2 篇也没有真正的文档标题，而是正文中的 `#` 被 Markdown 误判为 H1。`SpringCache.md` 有 4 个伪 H1；`Spring-高级特性.md` 有 1 个伪 H1。全目录未发现真实 H2–H6，因此没有可判定的 H1→H3 跳级，但整体缺乏可导航的标题层级。
  - 示例: OneNote/java/javaSE/JUC-AQS.md L1（正文直接开始，无标题）
  - 示例: OneNote/java/Spring框架/SpringCache.md L18-L24（YAML 注释被误渲染成 4 个 H1）
  - 示例: OneNote/java/Spring框架/Spring-高级特性.md L35（cron 字段说明 `# - ...` 被误渲染成 H1）
- **代码/配置未围栏导致误渲染**: 13 个文件 / 94 处独占 XML/HTML 标签行未放入代码块，渲染器会将其当作 HTML，示例代码可能隐藏或改变页面结构；这不是 `<details>/<br>/<summary>` 一类装饰 HTML，而是未围栏的 XML/Maven/Spring 配置。另有大量 YAML/Java/SQL 同样作为普通正文出现，应按代码段边界人工判断。
  - 示例: OneNote/java/Mybatis/mb使用.md L14-L26（`<configuration>` 配置被当作 HTML）
  - 示例: OneNote/java/Spring框架/SpringCache.md L2-L5（Maven `<dependency>` 裸标签）
  - 示例: OneNote/java/Spring框架/Spring-AOP面向切片.md L23-L33（Spring XML 裸标签）
- **下划线被误解析为强调**: 25 个文件 / 151 处。代码标识符被 `_..._` 包围，例如 `_AUTO_`、`System._out_`、`IO._println_`，正文显示会丢失下划线并出现斜体；部分迁移文本还形成碎片化强调。
  - 示例: OneNote/java/Mybatis/MP.md L8
  - 示例: OneNote/java/RabbitMQ/Hello World.md L37-L39
  - 示例: OneNote/java/RabbitMQ/Publish Confirm.md L7-L22
- **疑似错误的强调转换**: 4 个文件 / 7 处明确 `__...__` 加粗，与全库主流 `**...**` 不一致，且多数嵌在 `_..._` 片段中导致渲染边界混乱。
  - 示例: OneNote/java/RabbitMQ/Publish Confirm.md L7
  - 示例: OneNote/java/RabbitMQ/可靠性.md L58
  - 示例: OneNote/java/源码/AOP与代理.md L224-L226
- **代码中的链接被 Markdown 化**: 3 个文件 / 5 处。XML/DTD/schemaLocation 属性值内出现 `[url](url)`，复制代码后不是合法 XML。
  - 示例: OneNote/java/Mybatis/mb使用.md L13、L33
  - 示例: OneNote/java/Spring框架/Spring-IoC.md L17
  - 示例: OneNote/java/Spring框架/SpringMVC-配置.md L23、L32

### 中优 (风格问题)
- **Frontmatter 全部缺失**: 73 个文件 / 73 处，均无 YAML frontmatter；因此不存在字段不一致，而是目录级统一缺省。若知识库规范不要求元数据，可视为一致而不处理。
  - 示例: OneNote/java/Mybatis/MP-接口.md L1
  - 示例: OneNote/java/设计模式/设计原则.md L1
- **有序列表编号不连续/显式编号**: 19 个文件 / 99 个列表项使用具体数字，扫描到 18 篇含非 `1.` 编号。部分编号承担章节结构，却没有标题；也存在跳号，自动统一为 `1.` 可能掩盖内容结构。
  - 示例: OneNote/java/javaSE/java8新特性.md L1-L28（1、3、…、6）
  - 示例: OneNote/java/Mybatis/mb使用.md L1-L6（顶层与嵌套编号）
- **无序列表符号混用**: 19 个文件 / 126 项；总体以 `-` 为主（124 项），2 篇各出现一个 `*`，未发现 `+`。同文件混用发生于 2 篇。
  - 示例: OneNote/java/javaSE/JUC-AQS.md L268-L321（`-` 与 `*` 混用）
  - 示例: OneNote/java/Spring框架/Spring-高级特性.md L29-L35（`*` 实为字段说明/伪列表，需先围栏或转表格）
- **中文/英文标点混用**: 38 个文件 / 至少 71 处“中文邻接半角逗号、冒号、分号、感叹号”等；代码行与技术符号会造成误报，应仅修正文句。
  - 示例: OneNote/java/javaSE/java9~17新特性.md L94（中文句中半角逗号）
  - 示例: OneNote/java/Mybatis/mb详解.md L75（中文句中半角冒号）
  - 示例: OneNote/java/javaSE/JUC-JMM.md L67（三个半角 `!`）
- **加粗风格局部异常**: 27 个文件 / 122 处采用 `**...**`，这是主流风格；但存在相邻加粗块和孤立标记，影响可读性。
  - 示例: OneNote/java/javaSE/java8新特性.md L1（`**Lambda****表达式**`）
  - 示例: OneNote/java/javaSE/java8新特性.md L91（`**))**`）
- **表格样式基本有效但表头为空**: 3 个文件 / 3 张 GFM 表格，分隔行和列数一致，未检出结构损坏；三张表的表头单元格全部为空，语义与可访问性较弱。
  - 示例: OneNote/java/Spring框架/SpringBoot-接口规则校验.md L6-L7
  - 示例: OneNote/java/Spring框架/SpringCache.md L28-L29
  - 示例: OneNote/java/小框架/SpringBoot-JPA.md L32-L33
- **链接体系不完整**: 除上述 5 个被嵌入代码的外链外，未发现普通正文内部 `[[...]]` 链接，也未发现可确认的损坏括号链接；目录内笔记之间没有显式导航链接。这可能是内容策略而非格式错误。

### 低优 (一致性/残留检查)
- **图片格式已统一**: 35 个文件 / 94 张图片均为 `![[...]]`，未发现 `![](path)` 混用；符合已完成清理项，不建议再改。
  - 示例: OneNote/java/javaSE/JUC-AQS.md L8
- **特殊残留未发现**: 0 个文件 / 0 处 `[TOC]`、任务框 `[ ]`、`<details>`、`<summary>`、`<br>`、明显 emoji 乱码（`�`/常见 mojibake）或未渲染控件。
- **结构稀疏**: 多数文档由连续短句、代码和列表构成而没有标题分区；这是 71 篇缺 H1、全目录无 H2–H6 的延伸问题。不能仅靠文件名机械补全所有章节边界。

## 自动修复可行性
- 完全可自动: 4 类（为每篇补文件名 H1；统一明确的 `__粗体__` 为 `**粗体**`；统一真实无序列表符号；仅对明确中文正文做保守标点规范化）
- 需人工判断: 7 类（识别并围栏 XML/YAML/Java/SQL；修复 `_..._` 中代码与真实斜体；将伪 H1 还原为代码/说明；重建 H2–H6；判断有序编号语义；补表头；决定内部链接与 frontmatter 字段）
- 不可自动: 0 类（没有技术上绝对不可修复项，但结构与语义类不应无审阅批量执行）

## 推荐处理顺序
1. 先为 73 篇建立真实文档 H1，并修正 `SpringCache.md`、`Spring-高级特性.md` 的 5 个伪 H1。
2. 人工识别代码/配置边界并加围栏，优先处理 13 篇含裸 XML 标签的文档；这一步也会消除大量强调、HTML与标点误报。
3. 在代码围栏完善后，修复 25 篇 151 处下划线强调和 4 篇 7 处双下划线强调残留。
4. 修复 3 篇 XML 中的 5 个 Markdown 化 URL，确保示例可复制。
5. 再规范列表、补 H2–H6 章节结构和表头；有序编号先核对语义，避免机械重排。
6. 最后按仓库规范决定是否批量加入 frontmatter、内部导航链接，并只对自然语言执行中英文标点统一。