# java 目录 markdown 格式审计

## 概况
- 文件总数: 73 (全部 `.md`,无子目录外散落)
- 影响笔记数: 71 / 73 (绝大多数文件仍存在结构性偏离)
- 子目录 (实际有内容): javaSE (12) / Spring框架 (19) / Mybatis (6) / RabbitMQ (11) / 小框架 (12) / 源码 (11) / 设计模式 (4)
- 空目录: **JVM/** (占位空,无任何文件)
- 已完成清理回顾: 行尾空格✅ / 反斜杠转义✅ / 代码块语言标签✅ / 空 Untitled✅ / 图片 wikilink 化✅ — 本次审计以 73 篇仍属于"通过"维度,不再单独报告
- 字节/规模: JVM 空目录,2 个 0 字节空文件,3 个 < 200 字节近空文件
- 工作目录实际根: `E:/个人知识/OneNote/java/`(Win 路径) ≡ `/mnt/e/个人知识/OneNote/java/`(WSL 路径)

## 偏离清单 (按严重程度排)

### 高优 (可读性问题 — 已知的硬伤)

- **缺失 H1/标题层级**: 71 / 73 篇文章 **完全没有使用任何 `# / ## / ###` 标题语法**,只是把"标题"伪装成三种形式之一:
  - **伪 H1 风格 A — 数字列表开头**:15 篇,以 `1. **xxx**` 作为"全文标题",再用 2./3./4.… 充当二级章节
  - **伪 H1 风格 B — 加粗行开头**:12 篇,以 `**xxx**` 作为分段/章节标题,但所有标题都是同一视觉权重(都是 2 级粗体),无法在目录/大纲里显示层级
  - **图片开头** :9 篇(RabbitMQ/Hello World.md 等),首行即 `![[image.png]]`,文档无标题
  - **正文流(纯散文)**:35 篇,完全没有章节结构,只有粗体短语散落文中作"小标题",TOC 完全失效
  - 例外:`Spring框架/Spring-高级特性.md`(仅 1 个 H1)、`Spring框架/SpringCache.md`(4 个 H1 但同一层级,后接乱序的 `## `)
  - 影响: 73 篇几乎无法在 Obsidian/VSCode 的"大纲视图"折叠;无法生成目录;无法被 `[!info]` Dataview 等插件解析

  详情分组:
  - **以 `1. **X**` 数字列表冒充标题(15)**:
    - `javaSE/java8新特性.md`、`javaSE/java9~17新特性.md`、`javaSE/java18~24新特性.md`
    - `Mybatis/mb使用.md`、`Mybatis/mb详解.md`、`Mybatis/mb高级用法与原理探究.md`
    - `Spring框架/Spring-IoC.md`、`Spring框架/SpringMVC-Controller.md`、`Spring框架/Spring-数据库框架整合.md`
    - `小框架/JDBC-连接数据库.md`、`小框架/lombok.md`
    - `设计模式/创建类型.md`、`设计模式/结构型.md`、`设计模式/行为型.md`、`设计模式/设计原则.md`
  - **以加粗 `**X**` 行冒充标题(12)**:
    - `javaSE/JUC-JMM.md`、`JUC-锁.md`、`JUC-线程池.md`、`JUC-并发工具.md`
    - `RabbitMQ/RabbitMQ基础.md`、`Work Queues.md`、`可靠性.md`
    - `Spring框架/SpringBoot-Start.md`、`SpringBoot-前后端分离.md`、`SpringMVC-other.md`、`SpringMVC-配置.md`、`SpringSecurity-认证.md`
  - **以图片/代码块开端(13)**:`RabbitMQ/Hello World.md`、`Publish Confirm.md`、`Publish-Subscribe.md`、`Routing.md`、`Topic.md`、`SpringBoot-Log.md`、`小框架/JDBC-事务操作.md`、`JPA介绍.md`、`logging-介绍.md`、`小框架/AspectJ.md`、`Mybatis/MP-接口.md`、`MP-条件构造器.md`、`MP.md` 等共 35 篇正文流文件均从无结构直接进入正文

- **空文件 / 几乎空文件(5 篇)**: 这些不是格式问题,但属于结构异常,影响目录完整性
  - `Spring框架/SpringSecurity-原理.md` — **0 字节**,显然是占位
  - `源码/SpringMVC-Start.md` — **0 字节**,显然是占位
  - `小框架/logging-配置.md` — 14 字节,只有一行 `log4j to slf4j`(无标题、无段落结构)
  - `小框架/logging-介绍.md` — 58 字节,只有一行 `![[image.png]]`(纯图)
  - `小框架/JPA介绍.md` — 97 字节,两行 `![[image.png]]`(纯图)
  - 另外 `JVM/` 子目录是空的(0 个文件) — 是否保留待定

- **表格表头为空 (3 篇,GFM 风格错)**: 表格使用 `|   |   |   |` 作为表头,接 `|---|---|---|` 分隔,再把原本应该写表头的内容放到第一行
  - `Spring框架/SpringBoot-接口规则校验.md`(规则注解对照表)
  - `Spring框架/SpringCache.md`(缓存注解对照表)
  - `小框架/SpringBoot-JPA.md`(JPA 方法名拼接表)
  - 详见各文件第 4-6 行附近;数据列对齐但标题为空,Obsidian 渲染出"空表头丑表"

### 中优 (风格/可读性问题)

- **相邻加粗 `**X****Y**` 粘接错位**: 35 处,涉及 14 篇文件,典型渲染结果是 `**A** **B**`(中间多一空格或断成两段,而非预期的 `**A B**`)
  - `RabbitMQ/RabbitMQ基础.md`(7 处,如 `**Broker****：**`)、`javaSE/java9~17新特性.md`(6 处,如 `**改进的****try-with-resources**`)、`Spring框架/SpringBoot-前后端分离.md`(4)、`Spring框架/SpringMVC-Controller.md`(4)、`javaSE/JUC-JMM.md`(3)、`小框架/Netty.md`(3)
  - 全部 14 篇:
    - `RabbitMQ/RabbitMQ基础.md`、`RabbitMQ/可靠性.md`
    - `Spring框架/Spring-数据库框架整合.md`、`Spring框架/SpringBoot-前后端分离.md`、`Spring框架/SpringMVC-Controller.md`、`Spring框架/SpringMVC-配置.md`
    - `javaSE/java8新特性.md`、`javaSE/java9~17新特性.md`、`javaSE/JUC-AQS.md`、`javaSE/JUC-JMM.md`、`javaSE/JUC-锁.md`、`javaSE/JUC-锁框架.md`、`javaSE/NIO.md`
    - `小框架/Netty.md`
  - 共同特征:**两个粗体紧挨**(`**XXXX****YYYY**`),中间无空格,源自 OneNote 复制粘贴时把"中文 + 英文/英数"分隔成了两个粗体段。**可自动修复**:把 `\*\*([^*]+?)\*\*\s*\*\*([^*]+?)\*\*` 折叠成 `\*\*$1$2\*\*`(需保留中间的空格)

- **手写编号列表跳号 / 重号 (4 篇明显)**:
  - `javaSE/java8新特性.md`:出现的编号 = `{1, 3, 5, 6}`(缺 2、4)
  - `javaSE/java9~17新特性.md`:出现的编号 = `{1, 2, 10, 4, 5, 6, 7, 8, 9}`(4 后面冒出 10)
  - `Spring框架/SpringMVC-Controller.md`:`{1, 4, 5}`
  - `设计模式/设计原则.md`:`{1, 3, 5, 6, 7, 8}`(缺 2,跳到 3 后又 5;6 之后还正常)
  - 其它(例如 `Spring-IoC.md`、`mb使用.md`)用 `1.` + 缩进子项 `    1.` `    2.` `    3.` 形式尚属标准有序列表
  - **可自动修复**(谨慎,需保留"编号 = 顺序"语义而非"编号 = 显式值",更安全是改用 `1.` 自动编号)

- **XML/DOCTYPE 上下文里的 markdown 链接语法(4 篇)**:`[http://...](http://...)` 这种 markdown 链接被错误地用在了 `<!DOCTYPE mapper PUBLIC "..." "[url](url)">`、`xsi:schemaLocation="[url](url)"` 这些 XML 字符串字面值里;markdown 渲染器会把它们当成真链接,而 XML 解析器把它当成坏 DOCTYPE,双错。
  - `Mybatis/mb使用.md` L13、L33
  - `Spring框架/Spring-IoC.md` L17
  - `Spring框架/SpringMVC-配置.md` L23、L32
  - **可自动修复**(同时也要 escape `>` 为 `&gt;` 在 XML 里)

- **加粗孤悬/错位(1 处)**:
  - `javaSE/java8新特性.md` L91 出现裸行 `**))**`(前面是 `Collectors.toList()\n))` 在某 lambda 收尾后的代码片段里漏掉了分号 + 多了一组 markdown bold)
  - 这是内容错(代码残缺)+ 格式错(孤 `**`)的混合体

### 低优 (风格一致性)

- **中英文标点混用 — 普遍但需取舍**:绝大部分文件的中文叙述里夹杂大量 **英文逗号 `.` `,`**、`英文冒号 `:`、`英文括号 `(` 而非 `， 。 ： （`)。粗略分布(仅前 50 个量级较大的文件):
  - **几乎纯英文标点的**: `源码/AOP与代理.md`(en=135/cn=0 句号、en_paren=172)、`源码/对象绑定与类型转换.md`、`源码/Mapping与Handler.md`、`源码/参数解析器.md`、`源码/BeanFactory后处理器.md`、`源码/Bean及其后处理器.md`、`源码/Spring-Start.md`
  - **中英混用的(占多数)**: `javaSE/JUC-AQS.md`(cn=169 逗 vs en=29)、`JUC-锁.md`、`JUC-锁框架.md`、`Netty.md`
  - **几乎纯中文的**:`设计模式/*.md`、`Mybatis/MP-接口.md`、`Mybatis/MP-条件构造器.md`、`Spring框架/SpringSecurity-授权.md`
  - 同一文件内经常一句话 cn 标点、下一句 en 标点(尤其 `RabbitMQ/RabbitMQ基础.md` 一类问答体)
  - 这个改动波及面广且 **会改变文本语义**(例如 URL 里的 `:` 不应改成 `：`,代码块里的全角符号会破坏编译),所以**不建议自动全局替换**;建议针对少数篇(例如 `设计模式/*`)挑选做"中文段落只换中文标点"的小局部补丁

- **`__bold__` 与 `**bold**` 混用(2-3 个例外)**:`源码/AOP与代理.md` L224/L226 大量使用 `__AspectJMethodBeforeAdvice__`(下方注释里本来要的是加粗),`源码/Spring-Start.md` L76/L77/L79 同上,但同篇其它行又用 `**xxx**`。其余个别 `_#_`、`_重试间隔_` 这种 `_text_` 当斜体用,见 `RabbitMQ/可靠性.md`、`RabbitMQ/Publish Confirm.md`,看起来是有意用斜体注释,**不算偏离**

- **Javadoc 片段里的 `_*_` 注释首字符"星号"被当斜体/加粗触发**:`源码/AOP与代理.md` L224 出现 `_/**_`(Javadoc 注释外加斜体外层),`源码/Spring-Start.md` L76/L77/L79 同样。这些都是原 markdown 输入 _与_ Java 注释标记混用,渲染上会带斜体样式。**风格不一致,但不会报错**

## 自动修复可行性

### 完全可自动(纯正则 + 文件级)
- ✅ **相邻加粗 `**X****Y**`**:正则 `\*\*([^*]+?)\*\*\s*\*\*([^*]+?)\*\*` → `\*\*$1$2\*\*`,35 处/14 篇
- ✅ **空 H1 / 表头填充**:针对 3 个空表头表格,把 `|   |   |` 提升为从下一行取表头内容(需谨慎,因为下一行就是数据);这两个修法都涉及"猜标题",最好做"半自动":先报告,再人工填
- ✅ **手写数字列表去跳号**:对 `设计原则.md` 等 4 篇,把所有 `^\d+\. ` 替换成 `1. ` 让渲染器自动编号(纯机械替换,语义保留)
- ✅ **空文件/近空文件**:2 篇 0 字节可直接删除(需人确认);3 篇 < 200B 的可视情况合并或删除
- ✅ **`JVM/` 空目录**:可删除

### 需人工判断(半自动)
- ⚠️ **把 `**X**` 升级为 `## X`、把数字列表升级为 `## X`**:这是结构重写,需要先确定:
  1. 当前"标题"是否真的是章节(而不是被加粗的术语) — 必须人眼看
  2. 哪些 "伪 H1" 提升为 H1,哪些降为 H2 — 需要原笔记意图
- ⚠️ **空表头表格填充表头**:基本上得靠术语常识补;例如 "验证注解 / 验证的数据类型 / 说明"、"方法名 / 拼接 / SQL"
- ⚠️ **数字列表跳号**:上面 4 篇基本可以 100% 改成自动编号,但要确认作者本来不是要"跳号表达权重"
- ⚠️ **`xsi:schemaLocation` 等里的 markdown 链接**:转回纯 URL,但要保留 `<...>` XML 上下文里的空格

### 不可自动(必须人工)
- ❌ **OCR-style 中文乱字符**:`Spring框架/SpringBoot-前后端分离.md` L93 的 "亻吏用" 应改 "使用"、`Spring框架/SpringMVC-配置.md` L7 的 "圭寸装" 应改 "封装"、`设计模式/创建类型.md` L20 同样 "亻吏用"。还要看上下文("办法"、"事"、"权威")这些手感可疑的字。本批 3 例可肉眼识别,但全表 73 篇是否还有更多需抽查。
- ❌ **代码片段里的词法错误**:`Spring框架/SpringSecurity-认证.md` 中 `JdbcUserDetaiIsManager`(应是 `JdbcUserDetailsManager`)等 l/I 混淆;`Mybatis/MP-接口.md` 中 `MybatisPIus`(应是 `MybatisPlus`)等。这些是 OCR 而非 markdown 风格问题
- ❌ **中英文标点混用**:可局部自动,但需要保证不破坏 URL、代码、不在引号/书名号里换。建议"一次性"只针对设计模式/`Mybatis/MP*` 这种短篇做,且做完整文件复核
- ❌ **加粗 `_X_`/`__X__` 风格混用**:有的是有意为之("`_#_`" 表示某控制符旁注),不能批量改

## 推荐处理顺序

按 ROI(改动小、收益大、风险低)排序:

1. **先清理"硬伤"**(几乎无损、风险 = 0):
   1.1 删除 `Spring框架/SpringSecurity-原理.md`、`源码/SpringMVC-Start.md` 两个 0 字节文件(确认无引用后)
   1.2 删除或合并 `小框架/logging-配置.md`(14B)、`logging-介绍.md`(58B)、`JPA介绍.md`(97B)
   1.3 删除空目录 `JVM/`

2. **正则批量改相邻加粗**(35 处全自动):
   - 脚本: `re.sub(r'\*\*([^*]+?)\*\*\s*\*\*([^*]+?)\*\*', r'**\1\2**', text)`
   - 影响 14 篇,先 dry-run 检验渲染

3. **修 4 处 DOCTYPE/xsi 里的 `[url](url)`** → 还原为 `url`:
   - 涉及 3 篇(Mybatis/mb使用、Spring-IoC、SpringMVC-配置)
   - 别忘了在 markdown 里把 `<` 转 `&lt;`(避免被认作标签)

4. **修 3 篇空表头表格**:
   - `SpringBoot-接口规则校验.md`(写"验证注解 / 验证的数据类型 / 说明")
   - `SpringCache.md`(写"注解 / 用途 / 说明")
   - `小框架/SpringBoot-JPA.md`(写"属性 / 拼接方法名称示例 / 执行语句")
   - 半自动:人写表头,脚本只填位置

5. **修 4 篇手写数字列表跳号**:
   - 全部 `^[0-9]+\. ` 全替换为 `1. ` 让 markdown 自动编号(保留原顺序)
   - 或者保留手写但补齐缺失编号

6. **结构重写(最大工作量)**:把 71 篇的伪标题升格为真实 `# / ##` 层级
   - 优先级:先做 `设计模式/*.md`(4 篇短)、`Mybatis/MP*.md`(3 篇短)
   - 每个文件先识别"作者想要 H1 还是 H2",然后用脚本把 `**X**` → `## X`、把有序列表 `1.`/`2.`/`3.` → `## X`(`2.` → `### X`)
   - 此步必须有人参与,因为 71 篇没有同样的模式,机械做会丢层级语义

7. **OCR/中文修正**:
   - 全文 grep: `亻|圭|圭寸|问问|贼` 等明显错误字符 — 找到全部 3 处,人工订正
   - 全文 grep:`[A-Za-z]I[A-Za-z]` 高频位置(MPIus、Sercurity、JdbcUserDetails),人工订正

8. **中英文标点**: 这是最后一步,要在前面结构已稳定后做。每篇人工/半自动,避免对代码段、URL 误伤

## 文件清单(L1 注释用)
- 全 73 篇扫描结果(按目录分组):
  - **javaSE (12)**:`java18~24新特性.md`、`java8新特性.md`、`java9~17新特性.md`、`JUC-AQS.md`、`JUC-JMM.md`、`JUC-原子类.md`、`JUC-并发容器.md`、`JUC-并发工具.md`、`JUC-线程池.md`、`JUC-锁.md`、`JUC-锁框架.md`、`NIO.md`
  - **Spring框架 (19)**:`Spring-AOP面向切片.md`、`Spring-IoC.md`、`Spring-SpEL.md`、`Spring-数据库框架整合.md`、`Spring-高级特性.md`、`SpringBoot-Log.md`、`SpringBoot-Start.md`、`SpringBoot-前后端分离.md`、`SpringBoot-多环境配置.md`、`SpringBoot-接口规则校验.md`、`SpringCache.md`、`SpringMVC-Controller.md`、`SpringMVC-other.md`、`SpringMVC-配置.md`、`SpringSecurity-原理.md`(0B)、`SpringSecurity-授权.md`、`SpringSecurity-认证.md`、`SpringSecurity-配置.md`、`Spring整合Swagger或Knife4j.md`
  - **Mybatis (6)**:`mb使用.md`、`mb详解.md`、`mb高级用法与原理探究.md`、`MP-接口.md`、`MP-条件构造器.md`、`MP.md`
  - **RabbitMQ (11)**:`Hello World.md`、`Publish Confirm.md`、`Publish-Subscribe.md`、`RabbitMQ基础.md`、`Routing.md`、`SpringBoot整合.md`、`Topic.md`、`Work Queues.md`、`可靠性.md`、`延迟消息.md`
  - **小框架 (12)**:`AspectJ.md`、`JDBC-SQL注入.md`、`JDBC-事务操作.md`、`JDBC-批处理.md`、`JDBC-连接数据库.md`、`JPA介绍.md`、`Netty.md`、`SpringBoot-JPA.md`、`langchain4j.md`、`logging-介绍.md`、`logging-配置.md`、`lombok.md`
  - **源码 (11)**:`AOP与代理.md`、`Aware与Scope.md`、`BeanFactory后处理器.md`、`Bean及其后处理器.md`、`ControllerAdvice之@InitBinder.md`、`Mapping与Handler.md`、`Spring-Start.md`、`SpringMVC-Start.md`(0B)、`参数解析器.md`、`对象绑定与类型转换.md`
  - **设计模式 (4)**:`创建类型.md`、`结构型.md`、`行为型.md`、`设计原则.md`

## 备注
- 全部扫描均使用只读工具(`grep` / `find` / `read` / 自写 `python3` 脚本)。**本次审计未对任何文件做修改**。
- "结构正常"的判定标准: 至少 1 个 `# H1`,且章节使用 `## / ###`。本次仅 1 篇(`Spring框架/Spring-高级特性.md` 1 个 H1)勉强达标,`SpringCache.md` 4 个 H1 但未嵌套。也就是真正"标题层级合格" = 0.0 / 73。