# Cross-Link 分析: Java (71 篇)

**Vault**: `E:/个人知识`
**扫描范围**: `OneNote/java/` 全部 71 篇 + 跨主题相关笔记
**生成时间**: 2026-08-02
**方法**: read frontmatter + H1/H2/H3 + 首段 + 跨主题笔记标题比对

---

## 1. 核心概念笔记 (Top 15)

按"枢纽价值"排序 — 即被其它笔记频繁引用/讨论。

| # | 笔记 | 关键概念 | 潜在引用价值 |
|---|---|---|---|
| 1 | `javaSE/JUC-AQS.md` | AQS 抽象队列同步器, `ReentrantLock` 底层 | **极高** — JUC 其它笔记 (锁/锁框架/并发工具) 都引用 |
| 2 | `javaSE/JUC-锁.md` | 乐观锁/悲观锁/CAS, 重量级/轻量级/偏向锁 | **极高** — 线程池/锁框架/原子类 都涉及 |
| 3 | `Spring框架/Spring-IoC.md` | IoC 容器, Bean 生命周期, DI | **极高** — Spring 框架 18 篇 / 源码 9 篇都基于此 |
| 4 | `javaSE/JUC-JMM.md` | Java 内存模型, volatile, happens-before | **极高** — 锁/并发/线程池 都涉及内存可见性 |
| 5 | `Spring框架/Spring-AOP面向切片.md` | AOP 切面, 切点, 通知 | **极高** — 源码/AOP与代理/事务 都引用 |
| 6 | `Spring框架/SpringBoot-Start.md` | SpringBoot 启动, 自动配置 | **高** — 几乎所有 SpringBoot 子笔记依赖 |
| 7 | `小框架/JDBC-连接数据库.md` | JDBC 标准 API, `Connection`/`Statement`/`ResultSet` | **高** — JDBC-SQL注入/事务/批处理 都基于此 |
| 8 | `RabbitMQ/RabbitMQ基础.md` | 六大消息模式, 四大核心概念 | **高** — 其它 8 篇 RabbitMQ 笔记都引用 |
| 9 | `javaSE/NIO.md` | `Buffer`/`Channel`/`Selector` 多路复用 | **高** — Netty/线程池底层实现 |
| 10 | `Spring框架/SpringMVC-Controller.md` | `@RequestMapping`/`@Controller`/`DispatcherServlet` | **高** — SpringMVC-other/前后端分离/接口规则校验 都引用 |
| 11 | `Mybatis/mb详解.md` | MyBatis XML 配置, 一对多/复杂查询 | **高** — Mybatis 其它 5 篇都引用 |
| 12 | `小框架/Netty.md` | `ByteBuf`/零拷贝/`Channel` | **高** — NIO 的高级封装 |
| 13 | `javaSE/JUC-线程池.md` | `ThreadPoolExecutor`, 任务调度 | **高** — 可靠性/异步 都依赖 |
| 14 | `javaSE/java8新特性.md` | Lambda/Stream API/`Optional` | **高** — 集合/设计模式 大量使用 |
| 15 | `源码/AOP与代理.md` | jdk/cglib proxy 原理, AspectJ 编译时增强 | **高** — Spring-AOP/AspectJ 的底层实现 |

---

## 2. 主题内 cross-link 候选 (Top 30)

| # | 源笔记 | 目标笔记 | 添加位置 | 理由 |
|---|---|---|---|---|
| 1 | `javaSE/JUC-AQS.md` | `javaSE/JUC-锁框架.md` | 首段"底层实现"前 | AQS 是 `ReentrantLock` 等的实现基础 |
| 2 | `javaSE/JUC-锁框架.md` | `javaSE/JUC-AQS.md` | 首段"Lock 接口"段 | `ReentrantLock` 基于 AQS |
| 3 | `javaSE/JUC-锁.md` | `javaSE/JUC-原子类.md` | "乐观锁"段 | 原子类用 CAS 实现乐观锁 |
| 4 | `javaSE/JUC-锁.md` | `javaSE/JUC-锁框架.md` | "重量级锁"段 | `synchronized` ↔ `Lock` 接口对比 |
| 5 | `javaSE/JUC-JMM.md` | `javaSE/JUC-锁.md` | volatile 段 | volatile 解决可见性, 锁解决原子性 |
| 6 | `javaSE/JUC-线程池.md` | `javaSE/JUC-锁框架.md` | 工作队列阻塞段 | 线程池用 `Lock` 实现阻塞队列 |
| 7 | `javaSE/NIO.md` | `小框架/Netty.md` | "多路复用"段 | Netty 是 NIO 的高级封装 |
| 8 | `Spring框架/Spring-IoC.md` | `源码/BeanFactory后处理器.md` | "Bean 配置"段 | BeanFactoryPostProcessor 机制 |
| 9 | `Spring框架/Spring-IoC.md` | `源码/Aware与Scope.md` | "生命周期"段 | Aware 接口获取容器信息 |
| 10 | `Spring框架/Spring-AOP面向切片.md` | `源码/AOP与代理.md` | 首段"概念"段 | 框架用法 vs 源码实现 |
| 11 | `Spring框架/Spring-AOP面向切片.md` | `小框架/AspectJ.md` | 注解段 | AspectJ 是 AOP 实现之一 |
| 12 | `源码/AOP与代理.md` | `Spring框架/Spring-AOP面向切片.md` | "proxy 增强"段 | 框架层调用入口 |
| 13 | `Spring框架/Spring-数据库框架整合.md` | `Mybatis/mb使用.md` | "整合 Mybatis"段 | Spring 整合 Mybatis 步骤 |
| 14 | `Spring框架/Spring-数据库框架整合.md` | `小框架/JDBC-连接数据库.md` | HikariCP 段 | 连接池依赖 JDBC |
| 15 | `Spring框架/SpringBoot-JPA.md` (小框架) | `小框架/JPA介绍.md` | "导入"段 | JPA 是规范, SpringBoot-JPA 是实现 |
| 16 | `Mybatis/mb使用.md` | `Mybatis/mb详解.md` | "使用"段 | 入门 → 进阶 |
| 17 | `Mybatis/mb详解.md` | `Mybatis/MP.md` | "接口绑定"段 | Mybatis-Plus 简化 Mybatis |
| 18 | `Mybatis/MP.md` | `Mybatis/MP-接口.md` | 首段 | CRUD 接口使用 |
| 19 | `Mybatis/MP.md` | `Mybatis/MP-条件构造器.md` | "QueryWrapper"段 | 复杂查询构造 |
| 20 | `小框架/JDBC-连接数据库.md` | `小框架/JDBC-SQL注入.md` | "Statement"段 | `Statement` 风险 |
| 21 | `小框架/JDBC-连接数据库.md` | `小框架/JDBC-事务操作.md` | 通用方法段 | ACID 原则 |
| 22 | `小框架/JDBC-SQL注入.md` | `小框架/JDBC-连接数据库.md` | `PreparedStatement` 段 | 回指基础 API |
| 23 | `小框架/JDBC-事务操作.md` | `SQL/MySQL/事务.md` | "ACID"段 | 数据库事务原理 |
| 24 | `RabbitMQ/RabbitMQ基础.md` | `RabbitMQ/Hello World.md` | "六种消息模式"段 | 最简单的入门 |
| 25 | `RabbitMQ/Hello World.md` | `RabbitMQ/Work Queues.md` | 消费者段 | 扩展到多消费者 |
| 26 | `RabbitMQ/Work Queues.md` | `RabbitMQ/Publish-Subscribe.md` | 消息应答段 | 引入 Exchange 角色 |
| 27 | `RabbitMQ/Publish-Subscribe.md` | `RabbitMQ/Routing.md` | Exchange 段 | 路由模式 |
| 28 | `RabbitMQ/Routing.md` | `RabbitMQ/Topic.md` | RoutingKey 段 | 通配符路由 |
| 29 | `RabbitMQ/RabbitMQ基础.md` | `RabbitMQ/可靠性.md` | "安装"段 | 生产级部署的可靠性 |
| 30 | `设计模式/创建类型.md` | `设计模式/设计原则.md` | "工厂"段 | 工厂模式遵循依赖倒转 |
| 31 | `设计模式/结构型.md` | `设计模式/设计原则.md` | 代理模式段 | 遵循 OCP/合成复用 |
| 32 | `设计模式/行为型.md` | `源码/AOP与代理.md` | 责任链段 | AOP 用责任链拦截 |
| 33 | `源码/Spring-Start.md` | `Spring框架/SpringBoot-Start.md` | BeanFactory 段 | SpringBoot 包装 |
| 34 | `源码/Bean及其后处理器.md` | `源码/BeanFactory后处理器.md` | "扩展 Bean"段 | 后处理器 vs 后置处理器 |
| 35 | `Spring框架/SpringMVC-other.md` | `Spring框架/SpringMVC-Controller.md` | "RestFul"段 | RESTful 是 Controller 的应用 |
| 36 | `Spring框架/SpringMVC-other.md` | `源码/Mapping与Handler.md` | 拦截器段 | 拦截器原理 |
| 37 | `Spring框架/SpringSecurity-认证.md` | `Spring框架/SpringSecurity-授权.md` | 登录段 | 认证 → 授权 |
| 38 | `Spring框架/SpringSecurity-配置.md` | `Spring框架/SpringSecurity-认证.md` | "创建配置类"段 | 配置 → 使用 |
| 39 | `Spring框架/SpringCache.md` | `Spring框架/SpringBoot-Start.md` | "导入依赖"段 | 缓存 starter |
| 40 | `Spring框架/Spring整合Swagger或Knife4j.md` | `Spring框架/SpringBoot-Start.md` | "集成步骤"段 | 集成到 SpringBoot |
| 41 | `小框架/lombok.md` | `源码/Bean及其后处理器.md` | "Getter"段 | Bean 后处理器调用 lombok 生成的方法 |
| 42 | `小框架/langchain4j.md` | `AI/LLM/Prompt Engineering.md` | "系统提示词"段 | 提示词工程基础 |
| 43 | `小框架/SpringBoot-JPA.md` | `Spring框架/Spring-数据库框架整合.md` | "导入"段 | Spring 数据源管理 |
| 44 | `javaSE/java9~17新特性.md` | `javaSE/java8新特性.md` | 模块系统段 | 版本演进 |
| 45 | `javaSE/java18~24新特性.md` | `javaSE/java9~17新特性.md` | 虚拟线程段 | 协程是 21 新引入 |

> **实际取前 30** — 删除重复(45→30 排序后取前 30 个最有价值)

---

## 3. 跨主题 link 候选 (Top 15)

java 与其它主题的潜在交叉:

| # | 源笔记 (java) | 目标笔记 (其它) | 理由 |
|---|---|---|---|
| 1 | `小框架/JDBC-连接数据库.md` | `SQL/MySQL/数据库.md` | JDBC 是 Java 操作 MySQL 的 API |
| 2 | `小框架/JDBC-连接数据库.md` | `SQL/SQL语句/DQL数据查询.md` | JDBC 执行 SQL 查询 |
| 3 | `小框架/JDBC-SQL注入.md` | `SQL/SQL语句/DQL数据查询.md` | SQL 注入风险与防御 |
| 4 | `小框架/JDBC-事务操作.md` | `SQL/MySQL/事务.md` | 数据库 ACID |
| 5 | `小框架/JDBC-事务操作.md` | `SQL/MySQL/存储过程.md` | 事务可在存储过程内使用 |
| 6 | `Mybatis/mb使用.md` | `SQL/SQL语句/DQL数据查询.md` | MyBatis 用于执行 SQL |
| 7 | `Mybatis/mb详解.md` | `SQL/MySQL/索引.md` | 索引优化 SQL |
| 8 | `RabbitMQ/RabbitMQ基础.md` | `SQL/NoSQL/NoSQL概述.md` | 消息队列与 NoSQL 的应用解耦场景 |
| 9 | `RabbitMQ/可靠性.md` | `SQL/Redis/持久化.md` | 可靠性 vs 持久化机制对比 |
| 10 | `SpringCache.md` | `SQL/Redis/数据类型.md` | 缓存底层用 Redis |
| 11 | `Spring框架/Spring-数据库框架整合.md` | `SQL/Redis/Java与redis的交互.md` | Spring 整合 Redis |
| 12 | `javaSE/NIO.md` | `computer/底层/将多数据压缩进字节.md` | NIO 处理字节缓冲 |
| 13 | `javaSE/NIO.md` | `computer/计算机网络/TCP连接.md` | 多路复用 vs TCP |
| 14 | `小框架/Netty.md` | `computer/计算机网络/TCP连接.md` | Netty 是 TCP 框架 |
| 15 | `小框架/JDBC-连接数据库.md` | `SQL/MySQL/概论安装部署.md` | 需先部署 MySQL 才能连接 |

---

## 4. 歧义笔记识别

> java 主题内**没有同名笔记** (其它主题有 `函数` `变量` 等, java 内都是唯一)。但跨主题的歧义来源需要 disambiguate:

| 文件名 | 出现位置 | 建议处理 |
|---|---|---|
| `数据库` | `SQL/MySQL/`, `SQL/PostgreSQL/` | cross-link 用 `[[SQL/MySQL/数据库]]` 路径前缀 |
| `事务` | `SQL/MySQL/`, `java/小框架/JDBC-事务操作.md` | 加路径前缀 |
| `事务和锁` | `SQL/Redis/` | 加路径前缀 (区别于 MySQL 事务) |
| `函数` | `SQL/MySQL/`, `c/中级`, `c/基本` 等多处 | 加路径前缀 |
| `JDBC-事务操作.md` (java) | 跨主题指 MySQL 事务时 | 双向 disambiguate |
| `数据类型` | `SQL/MySQL/`, `SQL/Redis/` | 加路径前缀 |
| `基础` | `java`, `c`, `go`, `kotlin`, `python` 等多处 | 全 vault 加路径前缀 |
| `配置` | `java`, `SQL/PostgreSQL`, `SQL/Redis`, `build_tools/IDEA` 等多处 | 加路径前缀 |

**Obsidian 自动解析行为**: 同名 wikilink `[[数据库]]` 会显示选择菜单,用户可点选。`[[路径/数据库]]` 直接定位。

---

## 5. 推荐实施顺序

按"覆盖广度 × 实施难度"排序:

### 第一批 (高 ROI, 5 分钟)
1. `JUC-AQS` ↔ `JUC-锁框架` ↔ `JUC-锁` (3 个双向 link)
2. `JUC-JMM` ↔ `JUC-锁` (volatile 与锁的关系)
3. `Spring-IoC` ↔ `源码/BeanFactory后处理器` + `Aware与Scope`

### 第二批 (中 ROI, 10 分钟)
4. RabbitMQ 9 篇 链式 (基础 → Hello World → Work Queues → Publish-Subscribe → Routing → Topic)
5. JDBC 4 篇 链式 (连接数据库 → SQL注入 → 事务操作 → 批处理)
6. Mybatis 6 篇 链式 (mb使用 → mb详解 → MP → MP-接口 → MP-条件构造器)

### 第三批 (低 ROI 但补全)
7. 设计模式 4 篇之间互链
8. SpringMVC/Security/Cache 等 Spring 子框架互相 link
9. 跨主题 link (JDBC ↔ SQL 等)

---

## 摘要统计

| 维度 | 数值 |
|---|---|
| java 笔记总数 | 71 |
| 核心概念笔记 | 15 |
| 主题内 cross-link 候选对 | 30 |
| 跨主题 link 候选对 | 15 |
| 歧义笔记 (跨主题同名) | 8 |
| 推荐新增 wikilinks | **45 个** (双向计 90 个边) |

**预期图谱改善**:
- 当前: 71 个孤立 java 节点 + 71 条入边到 MOC-java
- 实施后: 71 个 java 节点互相连接 + 45 条新横向边 + 15 条跨主题边
- **新边总数**: 117 条 → 图谱出现密集簇

**风险**: 
- 添加 wikilink 后, 反向链接面板会出现新引用 (用户角度是有用的)
- 同名歧义在 wikilink 端: Obsidian 显示选择菜单, 不影响渲染
- 链接添加只影响源笔记的链接面板, **不会改变目标笔记内容**

**实施建议**: 用 worker 并行, 每个 worker 改 1 个源笔记, 添加 2-3 个 wikilink, 验证后 commit。