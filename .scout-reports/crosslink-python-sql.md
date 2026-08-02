# Cross-Link 分析: Python + SQL

**分析日期**: 2026-08-02
**范围**: 50 个笔记 (python 25 + SQL 25)
**工作目录**: `/mnt/e/个人知识`
**约束**: 只分析,不改文件

## 概览

| 指标 | Python | SQL |
|---|---|---|
| 总笔记 | 25 | 25 |
| 主题分类 | 5 (conda/基础/基础n件/常用内置模块/常用第三方模块/机器学习) | 5 (MySQL/PostgreSQL/Redis/SQL语句/NoSQL) |
| 当前 wikilinks (出) | 0 | 0 |
| 估算 cross-link 价值 | 高 (机器学习有 9 篇 + 6 个数据科学库) | 高 (Redis 主从/哨兵/事务互引;SQL 语句被 MySQL/NoSQL/PG 引用) |

---

# Python

## 1. 核心概念笔记 (Top 15)

按"枢纽价值"排序 — 概念被多少其它笔记引用/讨论。

| 排名 | 笔记 | 关键概念 | 引用价值 |
|---|---|---|---|
| 1 | `python/机器学习/概述.md` | AI/ML/DL 三大概念、算法分类、模型评估 | 机器学习所有 8 篇算法笔记均需引用作为入门 |
| 2 | `python/机器学习/数学概念.md` | 标量/向量/矩阵/张量、偏导、矩阵运算 | 线性回归/逻辑回归/集成学习/决策树 全部依赖 |
| 3 | `python/基础n件/numpy.md` | ndarray、数组运算、广播 | pandas/matplotlib/机器学习 全部数据科学笔记基础 |
| 4 | `python/基础n件/pandas.md` | DataFrame/Series、数据分析 | matplotlib 可视化/sklearn 训练数据/机器学习 9 篇全部基于 |
| 5 | `python/基础n件/matplotlib.md` | plt.plot/figure/可视化 | 机器学习 4 篇(线性回归/聚类/集成/逻辑回归)含可视化代码 |
| 6 | `python/机器学习/决策树.md` | ID3/C4.5/CART、信息熵、剪枝 | 集成学习(随机森林)基于决策树 |
| 7 | `python/机器学习/集成学习.md` | Bagging/Boosting、随机森林、XGBoost | 决策树/概述 两端引用 |
| 8 | `python/机器学习/线性回归.md` | 正规方程/梯度下降/sklearn API | 数学概念(矩阵)/numpy(矩阵运算) |
| 9 | `python/机器学习/逻辑回归.md` | sigmoid/极大似然估计/分类 | 数学概念(sigmoid 是初等函数)/线性回归(同属回归族) |
| 10 | `python/基础/基础.md` | 命名约定、序列、内置类型 | 类/字符串/内置函数/常用内置模块 全部依赖 |
| 11 | `python/基础/类.md` | 类属性/继承/运算符重载/特殊方法 | 基础/常用第三方模块(requests 类继承)/常用内置模块(os 类) |
| 12 | `python/常用第三方模块/langchain.md` | LLM/ChatOpenAI/Prompt 模板 | LangGraph 基于 langchain 抽象;概述/AI 概念引申 |
| 13 | `python/常用第三方模块/LangGraph.md` | StateGraph、状态机 | langchain 的图状态化封装 |
| 14 | `python/常用第三方模块/requests.md` | HTTP 请求/响应 | 计算机网络 HTTP协议 协议层对应;内置函数/类 的应用 |
| 15 | `python/机器学习/朴素贝叶斯.md` | 贝叶斯公式、文本分类、概率 | 概述(分类算法)/数学概念(概率基础) |

## 2. 主题内 cross-link (Top 30)

| # | 源 | 目标 | 添加位置 | 理由 |
|---|---|---|---|---|
| 1 | `机器学习/线性回归.md` | `机器学习/数学概念.md` | "数学基础"一节首部 | 矩阵/向量运算的数学前置知识 |
| 2 | `机器学习/逻辑回归.md` | `机器学习/数学概念.md` | "数学基础"首部 | sigmoid 函数的数学定义 |
| 3 | `机器学习/逻辑回归.md` | `机器学习/线性回归.md` | 简介处 | 同属回归族,逻辑回归是分类版的线性回归 |
| 4 | `机器学习/决策树.md` | `机器学习/概述.md` | 简介处 | 决策树是监督学习基本算法 |
| 5 | `机器学习/决策树.md` | `机器学习/集成学习.md` | "随机森林"段首 | 集成学习中随机森林基于决策树 |
| 6 | `机器学习/集成学习.md` | `机器学习/决策树.md` | "随机森林"段 | 引用决策树作为基学习器 |
| 7 | `机器学习/集成学习.md` | `机器学习/概述.md` | 简介处 | 集成学习是机器学习的一种思想 |
| 8 | `机器学习/聚类算法.md` | `机器学习/概述.md` | "K-Means"段 | 聚类属于无监督学习 |
| 9 | `机器学习/朴素贝叶斯.md` | `机器学习/概述.md` | 简介处 | 朴素贝叶斯是监督学习分类算法 |
| 10 | `机器学习/KNN.md` | `机器学习/概述.md` | 简介处 | KNN 是监督学习 |
| 11 | `基础n件/numpy.md` | `基础n件/pandas.md` | "ndarray"段末 | pandas 基于 numpy 数组 |
| 12 | `基础n件/pandas.md` | `基础n件/numpy.md` | 简介/数据结构段 | DataFrame 底层用 ndarray |
| 13 | `基础n件/matplotlib.md` | `基础n件/pandas.md` | "可视化"相关段 | pandas plot() 基于 matplotlib |
| 14 | `基础n件/matplotlib.md` | `基础n件/matplotlib速查与讲义.md` | 顶部或简介 | 同主题速查/讲义互引 |
| 15 | `基础n件/matplotlib速查与讲义.md` | `基础n件/matplotlib.md` | "讲义"段首 | 详细版与速查版互引 |
| 16 | `基础n件/常见问题.md` | `基础n件/matplotlib.md` | "matplotlib 中文显示乱码" | 解决 matplotlib 中文问题 |
| 17 | `基础/类.md` | `基础/基础.md` | "类"段首 | 类属于 Python 基础语法 |
| 18 | `基础/字符串相关.md` | `基础/内置函数.md` | "相关方法"段 | 字符串方法是内置 str 类型方法 |
| 19 | `基础/内置函数.md` | `基础/基础.md` | 顶部 | 内置函数是基础语法组成 |
| 20 | `基础/内置函数.md` | `基础/字符串相关.md` | 涉及 print 的部分 | print 是内置函数,字符串是 print 的常见对象 |
| 21 | `常用内置模块/os.md` | `基础/基础.md` | 顶部 | os 模块基于基础语法 |
| 22 | `常用第三方模块/LangGraph.md` | `常用第三方模块/langchain.md` | 顶部 | LangGraph 是 langchain 的图状态化扩展 |
| 23 | `常用第三方模块/langchain.md` | `机器学习/概述.md` | "概述"段 | langchain 是 LLM 应用框架,属于 AI 范畴 |
| 24 | `常用第三方模块/requests.md` | `基础/内置函数.md` | 涉及 input 的部分 | requests 是 HTTP 层的"内置函数"等价物 |
| 25 | `conda/管理conda.md` | `conda/包管理.md` | "包管理"段 | 管理 conda 后包管理 |
| 26 | `conda/包管理.md` | `conda/环境管理.md` | 顶部 | 包管理与环境管理是 conda 两大功能 |
| 27 | `conda/环境管理.md` | `conda/管理conda.md` | 顶部 | conda 基础→环境管理 |
| 28 | `机器学习/线性回归.md` | `基础n件/numpy.md` | "代码示例"段 | sklearn 训练数据需用 numpy 数组 |
| 29 | `机器学习/聚类算法.md` | `基础n件/numpy.md` | "代码示例"段 | make_blobs 生成 numpy 数组 |
| 30 | `机器学习/集成学习.md` | `基础n件/pandas.md` | "随机森林示例"段 | pd.read_csv / pd.DataFrame |

## 3. 跨主题 link (Top 15)

| # | 源 (python/SQL) | 目标 (其它) | 添加位置 | 理由 |
|---|---|---|---|---|
| 1 | `python/常用第三方模块/requests.md` | `OneNote/computer/计算机网络/HTTP协议.md` | "Quickly Start" 段 | requests 是 Python 的 HTTP 客户端 |
| 2 | `python/常用第三方模块/requests.md` | `OneNote/computer/计算机网络/网络和通信协议.md` | "协议"段 | HTTP 是应用层协议 |
| 3 | `python/基础n件/matplotlib.md` | `OneNote/python/常用第三方模块/requests.md` | (反向,非优先) | 数据来源常是 requests |
| 4 | `python/conda/管理conda.md` | `OneNote/liunx/linux命令/软件安装.md` | "Linux 安装"段 | conda 也是软件安装方式之一 |
| 5 | `python/conda/包管理.md` | `OneNote/liunx/linux命令/软件安装.md` | "包安装"段 | apt/pip/conda 包管理对比 |
| 6 | `python/conda/环境管理.md` | `OneNote/liunx/linux命令/系统操作相关.md` | "环境变量"段 | 虚拟环境涉及 PATH |
| 7 | `python/基础n件/numpy.md` | `OneNote/c/系统库/math.h.md` | 简介 | numpy 实现 C 数学库的超集 |
| 8 | `python/常用第三方模块/LangGraph.md` | `OneNote/AI/LLM/Prompt Engineering.md` | 顶部 | LLM 应用框架 |
| 9 | `python/常用第三方模块/langchain.md` | `OneNote/AI/LLM/Prompt Engineering.md` | "概述"段 | langchain 与 Prompt Engineering 直接相关 |
| 10 | `python/机器学习/概述.md` | `OneNote/AI/LLM/Prompt Engineering.md` | "人工智能"段 | AI 概念引申到 LLM |
| 11 | `python/基础/类.md` | `OneNote/kotlin/基础/基础语法.md` | "运算符重载"段 | 类/运算符重载跨语言对比 |
| 12 | `python/基础/基础.md` | `OneNote/go/go基础/基础.md` | "命名约定"段 | Python/Go 命名规范对比 |
| 13 | `python/常用内置模块/os.md` | `OneNote/liunx/linux命令/文件操作.md` | "文件/路径"段 | os.path 基于 Linux 文件系统 |
| 14 | `python/常用内置模块/os.md` | `OneNote/liunx/Shell脚本/变量.md` | (反向) | shell 变量 → 环境变量 → os.environ |
| 15 | `python/常用第三方模块/requests.md` | `OneNote/computer/计算机网络/TCP连接.md` | "连接"段 | HTTP 基于 TCP |

---

# SQL

## 1. 核心概念笔记 (Top 15)

按"枢纽价值"排序。

| 排名 | 笔记 | 关键概念 | 引用价值 |
|---|---|---|---|
| 1 | `SQL/MySQL/事务.md` | ACID、隔离级别、InnoDB | Redis 事务和锁/MySQL 索引/MySQL 函数 全部依赖 |
| 2 | `SQL/MySQL/索引.md` | CREATE INDEX/EXPLAIN/B+Tree | MySQL 函数(查询)/视图/触发器/事务 性能优化基础 |
| 3 | `SQL/MySQL/数据类型.md` | 数字/字符串/日期/枚举 | MySQL 函数/MySQL 管理/MySQL 视图/PostgreSQL 数据库 全部依赖 |
| 4 | `SQL/MySQL/函数.md` | 聚集/字符串/日期/控制流函数 | DQL 数据查询/有用的 SQL/MySQL 视图 全部引用 |
| 5 | `SQL/SQL语句/DQL数据查询.md` | SELECT/where/group/order/limit | MySQL 函数/MySQL 索引/MySQL 视图/PostgreSQL/有用的 SQL 全部基础 |
| 6 | `SQL/SQL语句/DDL数据定义.md` | CREATE/ALTER/DROP 数据库与表 | MySQL/PostgreSQL 库表操作基础 |
| 7 | `SQL/SQL语句/DML数据操作.md` | INSERT/UPDATE/DELETE | MySQL 触发器/DQL 数据源/MySQL 函数(统计) |
| 8 | `SQL/SQL语句/DCL数据控制.md` | 用户/授权/GRANT/REVOKE | MySQL 数据库安全管理 直接对应 |
| 9 | `SQL/Redis/数据类型.md` | Hash/List/Set/SortedSet | Redis 基本操作(基于类型)/Redis 持久化(序列化) |
| 10 | `SQL/Redis/基本操作.md` | set/get/hset/lpush 五大类型操作 | Redis 数据类型(具体实现)/Java与redis的交互/事务和锁 |
| 11 | `SQL/Redis/主从复制.md` | Master/Slave/replicaof | Redis 哨兵模式(基于主从)/Redis 持久化(主从同步) |
| 12 | `SQL/Redis/哨兵模式.md` | sentinel monitor/选举规则 | Redis 主从复制(故障转移基于主从) |
| 13 | `SQL/Redis/持久化.md` | RDB/AOF/save/bgsave | Redis 主从复制(初次同步快照)/Redis 基本操作(数据丢失) |
| 14 | `SQL/Redis/事务和锁.md` | multi/exec/watch 乐观锁 | MySQL 事务(对比悲观锁)/Redis 基本操作 |
| 15 | `SQL/NoSQL/NoSQL概述.md` | 键值/列存/文档/图形 4 类 | Redis(键值)归类/PostgreSQL(关系型)对比 |

## 2. 主题内 cross-link (Top 30)

| # | 源 | 目标 | 添加位置 | 理由 |
|---|---|---|---|---|
| 1 | `MySQL/事务.md` | `MySQL/索引.md` | "事务示例"段 | 事务查询性能依赖索引 |
| 2 | `MySQL/索引.md` | `MySQL/事务.md` | "EXPLAIN" 段 | 索引是事务一致性的实现手段 |
| 3 | `MySQL/索引.md` | `MySQL/数据类型.md` | "数据类型选择" | 索引与字段类型密切相关 |
| 4 | `MySQL/视图.md` | `MySQL/函数.md` | "不能更新的视图" | 字段来自集函数 |
| 5 | `MySQL/视图.md` | `MySQL/触发器.md` | "不能更新的视图"段 | 视图/触发器互引 |
| 6 | `MySQL/触发器.md` | `MySQL/视图.md` | (反向) | 触发器可监听视图 |
| 7 | `MySQL/函数.md` | `SQL语句/DQL数据查询.md` | "聚集函数"段 | 聚集函数用在 SELECT |
| 8 | `MySQL/函数.md` | `MySQL/数据类型.md` | "数据类型转换" | 字符串函数/日期函数依赖类型 |
| 9 | `MySQL/存储过程.md` | `SQL语句/DDL数据定义.md` | "创建存储过程"段 | 存储过程需建表 |
| 10 | `MySQL/存储过程.md` | `SQL语句/DML数据操作.md` | 段中 | 存储过程含 INSERT/UPDATE |
| 11 | `MySQL/数据库安全管理.md` | `SQL语句/DCL数据控制.md` | "用户管理"段 | CREATE USER 对应 DCL |
| 12 | `MySQL/数据库安全管理.md` | `MySQL/管理.md` | "权限管理" | 与字符集/校对并列管理项 |
| 13 | `MySQL/管理.md` | `MySQL/数据库安全管理.md` | (反向) | 字符集与安全管理都是 DBA 工作 |
| 14 | `MySQL/管理.md` | `MySQL/数据类型.md` | 字符集段 | 数据类型与字符集/校对规则紧密相关 |
| 15 | `PostgreSQL/数据库.md` | `PostgreSQL/配置.md` | "基本建库" | 建库涉及字符集配置 |
| 16 | `PostgreSQL/数据库.md` | `MySQL/数据类型.md` | "基本建库"段 | 数据类型概念相通 |
| 17 | `PostgreSQL/配置.md` | `liunx/linux命令/系统操作相关.md` | "Linux 安装" | Linux 下配置服务 |
| 18 | `Redis/基本操作.md` | `Redis/数据类型.md` | 顶部 | 基本操作基于数据类型 |
| 19 | `Redis/数据类型.md` | `Redis/基本操作.md` | (反向) | 数据类型给出命令细节 |
| 20 | `Redis/数据类型.md` | `Redis/持久化.md` | 顶部 | 持久化基于不同类型的存储结构 |
| 21 | `Redis/主从复制.md` | `Redis/持久化.md` | "数据同步"段 | 从节点首次同步基于 RDB 快照 |
| 22 | `Redis/主从复制.md` | `Redis/哨兵模式.md` | 顶部 | 哨兵是主从的故障转移升级 |
| 23 | `Redis/哨兵模式.md` | `Redis/主从复制.md` | 顶部 | 哨兵基于一主一从 |
| 24 | `Redis/哨兵模式.md` | `Redis/持久化.md` | (间接) | 选举过程涉及数据完整性 |
| 25 | `Redis/事务和锁.md` | `MySQL/事务.md` | 顶部 | Redis 事务与 MySQL 事务对比 |
| 26 | `Redis/事务和锁.md` | `Redis/基本操作.md` | "watch"段 | watch 对基本操作的影响 |
| 27 | `Redis/概论安装部署.md` | `liunx/linux命令/软件安装.md` | "安装"段 | apt install redis-server |
| 28 | `Redis/Java与redis的交互.md` | `Redis/基本操作.md` | "jedis.set"等 | Java 调用 Redis 命令 |
| 29 | `Redis/Java与redis的交互.md` | `Redis/数据类型.md` | "jedis.hset" | Jedis 方法与 Redis 类型对应 |
| 30 | `NoSQL/NoSQL概述.md` | `Redis/概论安装部署.md` | "键值存储" | Redis 是键值存储代表 |
| 31 | `NoSQL/NoSQL概述.md` | `PostgreSQL/数据库.md` | "对比" | SQL 关系型 vs NoSQL |
| 32 | `SQL语句/有用的SQL.md` | `SQL语句/DQL数据查询.md` | "统计某列数量" | 用到 GROUP BY |
| 33 | `SQL语句/有用的SQL.md` | `MySQL/函数.md` | "count" | count 函数用法 |

## 3. 跨主题 link (Top 15)

| # | 源 (SQL) | 目标 (其它) | 添加位置 | 理由 |
|---|---|---|---|---|
| 1 | `SQL/Redis/Java与redis的交互.md` | `OneNote/java/小框架/`(langchain4j/jdbc 类似) | "Jedis" 段 | Java 与外部系统交互的同类 |
| 2 | `SQL/Redis/概论安装部署.md` | `OneNote/liunx/linux命令/系统操作相关.md` | "systemctl" 段 | Redis 服务启停 |
| 3 | `SQL/Redis/持久化.md` | `OneNote/liunx/linux命令/文件操作.md` | "dump.rdb 路径" | RDB 文件位置 |
| 4 | `SQL/MySQL/数据类型.md` | `OneNote/java/基础/类.md` | (反向非优先) | Java 数据类型对 SQL 类型的映射 |
| 5 | `SQL/MySQL/事务.md` | `OneNote/java/javaSE/JUC-并发工具.md` | "事务并发"段 | 数据库并发与 Java 并发对照 |
| 6 | `SQL/MySQL/索引.md` | `OneNote/java/javaSE/`(集合/HashMap 类似结构) | "EXPLAIN" 段 | 索引与 HashMap 都是 O(1) 查找 |
| 7 | `SQL/MySQL/管理.md` | `OneNote/liunx/linux命令/系统操作相关.md` | "配置文件"段 | MySQL my.cnf 配置 |
| 8 | `SQL/MySQL/数据库安全管理.md` | `OneNote/liunx/linux命令/用户 用户组 权限.md` | "用户授权"段 | MySQL 用户 vs Linux 用户/权限 |
| 9 | `SQL/PostgreSQL/配置.md` | `OneNote/liunx/linux命令/系统操作相关.md` | "systemctl" 段 | PostgreSQL 服务管理 |
| 10 | `SQL/SQL语句/DQL数据查询.md` | `OneNote/python/基础n件/pandas.md` | "group by"段 | SQL → pandas groupby 对应 |
| 11 | `SQL/SQL语句/DQL数据查询.md` | `OneNote/python/机器学习/概述.md` | 数据查询 | ML 训练数据来源是 SQL 查询 |
| 12 | `SQL/NoSQL/NoSQL概述.md` | `OneNote/computer/底层/将多数据压缩进字节.md` | "文档型"段 | 数据存储压缩 |
| 13 | `SQL/Redis/基本操作.md` | `OneNote/java/javaSE/JUC-锁.md` | "setnx"段 | Redis 分布式锁与 Java 锁对比 |
| 14 | `SQL/MySQL/数据库安全管理.md` | `OneNote/build_tools/maven/依赖管理.md` | (非优先) | 间接关联 |
| 15 | `SQL/MySQL/事务.md` | `OneNote/computer/计算机网络/TCP连接.md` | "分布式事务"段 | 事务概念在分布式系统中的应用 |

---

# 4. 歧义笔记识别

跨多个目录的同名笔记,wikilink `[[xxx]]` 会触发 Obsidian 歧义提示。

| 笔记名 | 出现位置 (次数) | 建议处理 |
|---|---|---|
| `数据类型` | `MySQL/数据类型.md`, `Redis/数据类型.md` (2) | 用 `[[MySQL/数据类型]]` / `[[Redis/数据类型]]` 加路径 |
| `数据库` | `PostgreSQL/数据库.md` (1) — 当前唯一,但 vault 内还有其它"数据库"相关概念 | 当前唯一,但建议加路径前缀防歧义 |
| `事务` | `MySQL/事务.md`, `Redis/事务和锁.md` (无别名冲突) | 当前 OK;若加 `事务和锁.md` 别名需小心 |
| `事务和锁` | `Redis/事务和锁.md` (1) — 当前唯一 | OK |
| `函数` | `MySQL/函数.md`, `kotlin/程序设计中级/函数.md`, `liunx/Shell脚本/函数.md` (3) | 严重歧义,加路径前缀 |
| `基础` | `python/基础/基础.md`, `go/go基础/基础.md`, `kotlin/基础/基础语法.md` (3) | 加路径前缀 |
| `基础知识` | `c/基本/基础知识.md`, `kotlin/基础/基础知识.md` (2) | 加路径前缀 |
| `变量` | `c/基本/变量.md`, `liunx/Shell脚本/变量.md` (2) | 加路径前缀 |
| `数组` | `c/基本/数组.md`, `kotlin/程序设计高级/数组.md` (2) | 加路径前缀 |
| `流程控制` | `c/基本/流程控制.md`, `liunx/Shell脚本/流程控制.md` (2) | 加路径前缀 |
| `字符串` / `字符串相关` | `c/基本/字符串.md`, `python/基础/字符串相关.md` (2) | 加路径前缀 |
| `文件操作` | `go/go基础/文件操作.md`, `liunx/linux命令/文件操作.md` (2) | 加路径前缀 |
| `泛型` | `go/go基础/泛型.md`, `kotlin/程序设计高级/泛型.md` (2) | 加路径前缀 |
| `常用方法` | `kotlin/库/常用方法.md` (1) — 当前唯一 | OK |
| `配置` | `PostgreSQL/配置.md`, `Redis/概论安装部署.md`(配置外网访问) (1 + 1 段内) | 加路径前缀 |

## 跨主题歧义重灾区

1. **`函数`** (3 个目录): `MySQL/函数`, `kotlin/函数`, `Shell/函数` — 加路径前缀必做
2. **`基础` / `基础知识`** (3 个): `python/基础`, `go/go基础`, `kotlin/基础` — 加路径前缀必做
3. **`数据类型`** (2 个): `MySQL/数据类型`, `Redis/数据类型` — 加路径前缀必做

## 建议: 路径前缀策略

```markdown
# 当前 MOC 里 (不带路径)
[[JUC-AQS]]

# 改进 (带路径,避免歧义)
[[java/javaSE/JUC-AQS]]

# 适用场景
- 同名笔记存在 → 加路径
- 唯一笔记 → 可省略路径(MOC 当前用纯文件名)
```

注: 大多数笔记名唯一,只有 ~15 个需要路径前缀。MOC 中当前使用的纯文件名已覆盖大部分场景,只在涉及歧义笔记时才需要路径。

---

# 5. 实施优先级建议

| 优先级 | 工作量 | 内容 |
|---|---|---|
| P0 (推荐先做) | 10 分钟 | 修复 MOC 中歧义笔记的 wikilink (15 处) |
| P1 | 30 分钟 | 机器学习 9 篇互引(决策树↔集成学习↔概述↔数学概念) |
| P1 | 30 分钟 | 基础n件 互引(numpy↔pandas↔matplotlib↔常见问题) |
| P2 | 20 分钟 | Redis 4 篇互引(主从↔哨兵↔持久化↔事务↔基本操作↔数据类型) |
| P2 | 20 分钟 | MySQL 8 篇互引(事务↔索引↔数据类型↔函数↔视图↔触发器) |
| P3 | 15 分钟 | SQL 语句 5 篇互引(DQL/DDL/DML/DCL↔有用 SQL) |
| P3 | 15 分钟 | python 基础 4 篇互引(基础↔类↔字符串↔内置函数) |
| P3 | 15 分钟 | conda 3 篇互引(管理 conda↔包管理↔环境管理) |
| P4 | 30 分钟 | langchain↔LangGraph↔AI Prompt Engineering 跨主题链 |
| P4 | 30 分钟 | requests↔HTTP协议/TCP连接 跨主题链 |
| P4 | 30 分钟 | SQL ↔ pandas 跨主题链 (DQL↔pandas groupby) |

**总预估**: 4-5 小时分散实施 / 1.5 小时集中实施。

---

# 6. 关键观察

1. **机器学习是 Python 主题的核心枢纽**: 9 篇笔记互引密度最高,跨引到 numpy/pandas/matplotlib,价值大。
2. **Redis 主题高度耦合**: 主从/哨兵/持久化/事务/基本操作/数据类型 6 篇内部链接丰富,适合优先做。
3. **MySQL 主题分散**: 9 篇笔记覆盖事务/索引/数据类型/函数/视图/触发器/存储过程/管理/数据库安全管理,核心是事务+索引+数据类型 三件套。
4. **SQL 语句是基础**: DQL/DDL/DML/DCL 四篇是 MySQL/PostgreSQL 通用基础。
5. **跨主题价值**: python↔SQL 在 pandas↔DQL 有强对应;python↔AI 在 langchain/LangGraph/Prompt Engineering;python↔liunx 在 conda/requests。
6. **现有 MOC 是 wikilink 起点**: 13 个 MOC 已建立,跨主题链接可直接连到 MOC(主题级 hub-and-spoke),也可深入到笔记级。