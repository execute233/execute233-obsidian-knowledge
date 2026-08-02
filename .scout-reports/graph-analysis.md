# Obsidian 关系图谱分析

**Vault 路径**: `E:/个人知识`  
**扫描范围**: `OneNote/` 下所有 `.md` 笔记  
**生成时间**: 2026-08-02

## 概览

| 指标 | 数量 |
|---|---|
| 总笔记数 | **217** |
| 有 frontmatter 的笔记 | 216 (99.5%) |
| 有 tags 的笔记 | 216 (99.5%) |
| 唯一 tag 数 | **200** |
| 总 wikilinks (`[[...]]`) | 61 |
| 图片 wikilinks (`![[...]]`) | 61 |
| 笔记间 wikilinks | **0** |
| &nbsp;&nbsp;├─ 解析成功 (目标存在) | 0 |
| &nbsp;&nbsp;└─ 断裂 wikilinks | 0 |
| 双向链接对 (A↔B) | 0 |
| 孤立笔记 (0 入链 0 出链) | **217** |

## 关键发现

### 1. 笔记间几乎没有交叉引用

全 vault 仅有 **0 条笔记间 wikilink** (相对于 217 篇笔记),平均每篇 **0.000 条**。说明这是一个**纯文档堆叠结构**,没有真正发挥 Obsidian 的图谱能力。

### 2. 100% 笔记孤立

**217 / 217 = 100.0%** 的笔记没有任何 wikilink 关联(包括入链和出链)。这是典型的 OneNote 导入 vault 的特征 — 原 OneNote 笔记之间没有链接,只有层级目录结构。

### 3. 双向链接为零

没有任何 A↔B 形式的互链,因为 A→B 的单边都不存在。

### 4. tags 体系已基本建立

**216 / 217 = 99.5%** 笔记有 tags,共 **200** 个唯一 tag。可作为图谱构建的替代信号。

## 枢纽笔记 (按 wikilink 入链排名)

> 由于笔记间 wikilink 极少,**无入链排名**。改按 tag 共现网络给出'虚拟枢纽'参考。

### Tag 共现 Top 15 (同时出现在同一笔记中)

| Tag A | Tag B | 共现次数 |
|---|---|---|
| `Spring框架` | `java` | 18 |
| `java` | `javaSE` | 12 |
| `java` | `小框架` | 12 |
| `RabbitMQ` | `java` | 10 |
| `java` | `源码` | 9 |
| `Shell脚本` | `liunx` | 9 |
| `MySQL` | `SQL` | 9 |
| `Redis` | `SQL` | 8 |
| `unity` | `脚本开发` | 8 |
| `c` | `标准库` | 6 |
| `Mybatis` | `java` | 6 |
| `linux命令` | `liunx` | 5 |
| `SQL` | `SQL语句` | 5 |
| `computer` | `计算机网络` | 4 |
| `java` | `设计模式` | 4 |

## 高频 Tags (Top 20)

| Tag | 笔记数 |
|---|---|
| `java` | 71 |
| `SQL` | 25 |
| `c` | 21 |
| `go` | 18 |
| `Spring框架` | 18 |
| `liunx` | 18 |
| `javaSE` | 12 |
| `小框架` | 12 |
| `kotlin` | 11 |
| `RabbitMQ` | 10 |
| `源码` | 9 |
| `Shell脚本` | 9 |
| `机器学习` | 9 |
| `MySQL` | 9 |
| `Python` | 8 |
| `Redis` | 8 |
| `unity` | 8 |
| `脚本开发` | 8 |
| `docker` | 7 |
| `基础` | 7 |

## 主题集群统计

| 主题 | 笔记数 | 出链数 | 接收链接 | 跨主题链接 |
|---|---|---|---|---|
| java | 71 | 0 | 0 | 0 |
| python | 25 | 0 | 0 | 0 |
| SQL | 25 | 0 | 0 | 0 |
| c | 21 | 0 | 0 | 0 |
| go | 18 | 0 | 0 | 0 |
| liunx | 18 | 0 | 0 | 0 |
| kotlin | 11 | 0 | 0 | 0 |
| unity | 8 | 0 | 0 | 0 |
| docker | 7 | 0 | 0 | 0 |
| computer | 6 | 0 | 0 | 0 |
| build_tools | 5 | 0 | 0 | 0 |
| AI | 1 | 0 | 0 | 0 |
| windows | 1 | 0 | 0 | 0 |

## 跨主题链接矩阵

| 源 → 目标 | AI | SQL | build_tools | c | computer | docker | go | java | kotlin | liunx | python | unity | windows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AI | · | · | · | · | · | · | · | · | · | · | · | · | · |
| SQL | · | · | · | · | · | · | · | · | · | · | · | · | · |
| build_tools | · | · | · | · | · | · | · | · | · | · | · | · | · |
| c | · | · | · | · | · | · | · | · | · | · | · | · | · |
| computer | · | · | · | · | · | · | · | · | · | · | · | · | · |
| docker | · | · | · | · | · | · | · | · | · | · | · | · | · |
| go | · | · | · | · | · | · | · | · | · | · | · | · | · |
| java | · | · | · | · | · | · | · | · | · | · | · | · | · |
| kotlin | · | · | · | · | · | · | · | · | · | · | · | · | · |
| liunx | · | · | · | · | · | · | · | · | · | · | · | · | · |
| python | · | · | · | · | · | · | · | · | · | · | · | · | · |
| unity | · | · | · | · | · | · | · | · | · | · | · | · | · |
| windows | · | · | · | · | · | · | · | · | · | · | · | · | · |

**注**:本 vault 跨主题链接为 0,所有 wikilink (零星几条) 都在同一主题内。

## 断裂 Wikilinks

没有真正断裂的笔记 wikilink(所有非图片 wikilink 都能解析)。

## 孤立笔记 (无 wikilink 关联)

共 **217** 篇 (按主题分组):

### java (71 篇)

- `AOP与代理`
- `AspectJ`
- `Aware与Scope`
- `BeanFactory后处理器`
- `Bean及其后处理器`
- `ControllerAdvice之@InitBinder`
- `Hello World`
- `JDBC-SQL注入`
- `JDBC-事务操作`
- `JDBC-批处理`
- `JDBC-连接数据库`
- `JPA介绍`
- `JUC-AQS`
- `JUC-JMM`
- `JUC-原子类`
- `JUC-并发容器`
- `JUC-并发工具`
- `JUC-线程池`
- `JUC-锁`
- `JUC-锁框架`
- `MP`
- `MP-接口`
- `MP-条件构造器`
- `Mapping与Handler`
- `NIO`
- `Netty`
- `Publish Confirm`
- `Publish-Subscribe`
- `RabbitMQ基础`
- `Routing`
- `Spring-AOP面向切片`
- `Spring-IoC`
- `Spring-SpEL`
- `Spring-Start`
- `Spring-数据库框架整合`
- `Spring-高级特性`
- `SpringBoot-JPA`
- `SpringBoot-Log`
- `SpringBoot-Start`
- `SpringBoot-前后端分离`
- `SpringBoot-多环境配置`
- `SpringBoot-接口规则校验`
- `SpringBoot整合`
- `SpringCache`
- `SpringMVC-Controller`
- `SpringMVC-other`
- `SpringMVC-配置`
- `SpringSecurity-授权`
- `SpringSecurity-认证`
- `SpringSecurity-配置`
- `Spring整合Swagger或Knife4j`
- `Topic`
- `Work Queues`
- `java18~24新特性`
- `java8新特性`
- `java9~17新特性`
- `langchain4j`
- `logging-介绍`
- `logging-配置`
- `lombok`
- `mb使用`
- `mb详解`
- `mb高级用法与原理探究`
- `创建类型`
- `参数解析器`
- `可靠性`
- `对象绑定与类型转换`
- `延迟消息`
- `结构型`
- `行为型`
- `设计原则`

### c (28 篇)

- `c语言的编译`
- `emoji`
- `math.h`
- `stdarg.h`
- `stdio.h`
- `stdlib.h`
- `string.h`
- `time.h`
- `函数`
- `函数`
- `函数`
- `函数`
- `变量`
- `变量`
- `基本数据类型`
- `基础知识`
- `基础知识`
- `字符串`
- `指针`
- `数组`
- `数组`
- `树 森林 二叉树`
- `流程控制`
- `流程控制`
- `线性表`
- `结构体，联合体和枚举`
- `预处理`
- `高级树 其它树`

### SQL (24 篇)

- `DCL数据控制`
- `DDL数据定义`
- `DML数据操作`
- `DQL数据查询`
- `Java与redis的交互`
- `NoSQL概述`
- `主从复制`
- `事务`
- `事务和锁`
- `哨兵模式`
- `基本操作`
- `存储过程`
- `持久化`
- `数据库`
- `数据库安全管理`
- `数据类型`
- `数据类型`
- `有用的SQL`
- `概论安装部署`
- `管理`
- `索引`
- `视图`
- `触发器`
- `配置`

### python (24 篇)

- `KNN`
- `LangGraph`
- `langchain`
- `matplotlib`
- `matplotlib速查与讲义`
- `numpy`
- `os`
- `pandas`
- `requests`
- `内置函数`
- `决策树`
- `包管理`
- `字符串相关`
- `常见问题`
- `数学概念`
- `朴素贝叶斯`
- `概述`
- `环境管理`
- `管理conda`
- `类`
- `线性回归`
- `聚类算法`
- `逻辑回归`
- `集成学习`

### go (21 篇)

- `Go Modules`
- `bind绑定器`
- `中级`
- `单元测试`
- `基础`
- `基础`
- `库-flag`
- `库-fmt`
- `库-http`
- `库-log`
- `库-net-http`
- `库-strconv`
- `库-time`
- `文件操作`
- `文件操作`
- `泛型`
- `泛型`
- `环境搭建`
- `请求`
- `路由`
- `迭代器和iter包`

### liunx (14 篇)

- `curl 网络传输`
- `echo`
- `printf`
- `screen`
- `ssh`
- `前言`
- `快速命令`
- `文件包含`
- `文件系统`
- `用户 用户组 权限`
- `系统操作相关`
- `软件安装`
- `输入-输出重定向`
- `运算符`

### unity (8 篇)

- `transform控制父子`
- `初步认识`
- `场景`
- `按键监听`
- `文件-程序管理`
- `游戏时间`
- `游戏物体的获取`
- `触摸`

### docker (7 篇)

- `单机容器编排`
- `存储管理`
- `安装与配置`
- `容器与镜像`
- `网络管理`
- `资源管理`
- `配置与运行`

### kotlin (7 篇)

- `基础语法`
- `封装，继承和多态`
- `常用方法`
- `数学运算`
- `特殊类型`
- `类与对象`
- `集合`

### computer (6 篇)

- `HTTP协议`
- `TCP连接`
- `UDP协议`
- `将多数据压缩进字节`
- `网络和通信协议`
- `网络安全攻击`

### build_tools (5 篇)

- `使用`
- `依赖管理`
- `安装 配置 初始化`
- `快捷键操作`
- `操作`

### AI (1 篇)

- `Prompt Engineering`

### windows (1 篇)

- `WSL`

## 建议

### 立即可行

1. **保持现状**:本 vault 是文档堆叠结构(OneNote 导入风格),Obsidian 图谱视图只会显示零星几条边,价值有限。

2. **启用 Dataview**:用 tags 而非 wikilink 构建 Dataview 查询 — 现有 200 个 tag 已足够支撑。

### 中期优化

3. **批量添加 wikilink**:对核心概念(如 `NIO` `JUC` `AOP` `lambda` `切片` `Bean`)在相关笔记间手动建立链接,可显著提升图谱密度。

4. **MOC (Map of Content) 笔记**:为每个主题创建一个目录笔记,集中列出子笔记并用 wikilink 串联 — 这是图谱可视化效果最明显的改造方式。

### 长期

5. **Tag 体系治理**:200 个 tag 数量适中,但需检查是否有同义 tag(如 `java` 和 `Java`)、过时 tag(`untagged` `test` 等)。

6. **链接建议插件**:安装 Obsidian 插件 [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections) 或 [Related Notes](https://github.com/marcusjzw/obsidian-related-notes) 可基于内容相似度自动建议 wikilink。
