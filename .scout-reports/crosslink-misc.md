# Cross-Link 分析: kotlin + unity + docker + computer + build_tools + AI + windows

**Vault**: `E:/个人知识`  
**分析范围**: 39 个新导入笔记  
**生成时间**: 2026-08-02  
**目的**: 不修改文件,仅识别 cross-link 候选

## 评估方法

1. 列出每个主题下所有笔记的 frontmatter + H1 + 标题结构
2. LLM 语义判断"枢纽价值"和链接关系
3. 输出结构化报告供后续人工/批处理添加 wikilink

---

## kotlin (11 笔记)

### 1. 核心概念 (Top 5 枢纽笔记)

| 笔记 | 枢纽价值 | 原因 |
|---|---|---|
| **类与对象** | ★★★★★ | kotlin 一切 OOP 概念的根,被 `封装,继承和多态`、`函数`、`泛型`、`特殊类型` 全部引用 |
| **基础语法** | ★★★★ | 变量/条件/循环,被 `函数`、`类与对象`、`常用方法` 引用 |
| **封装,继承和多态** | ★★★★ | OOP 三大特性 + 扩展函数/高阶函数(apply/let/run/also),几乎被所有高级笔记引用 |
| **集合** | ★★★ | List/Set/Map,与 `数组`、`泛型` 紧耦合 |
| **函数** | ★★★ | 函数类型/lambda/内联,被 `集合`、`数组`、`特殊类型` 引用 |

### 2. 主题内 cross-link 候选 (Top 10)

| 源 | 目标 | 关系 | 优先级 |
|---|---|---|---|
| `基础/基础语法.md` | `程序设计中级/封装,继承和多态.md` | "与 java 一样"→具体对比 | 高 |
| `基础/基础语法.md` | `程序设计中级/类与对象.md` | var/val 是类的属性基础 | 高 |
| `基础/基础语法.md` | `程序设计中级/函数.md` | fun 关键字 | 高 |
| `程序设计中级/封装,继承和多态.md` | `程序设计中级/类与对象.md` | 三大特性基于类与对象 | 高 |
| `程序设计中级/类与对象.md` | `程序设计高级/特殊类型.md` | 数据类/单例类都是类的特殊形式 | 高 |
| `程序设计中级/类与对象.md` | `程序设计高级/泛型.md` | 泛型类 `Score<T>` | 中 |
| `程序设计高级/集合.md` | `程序设计高级/泛型.md` | 集合默认泛型 | 高 |
| `程序设计高级/集合.md` | `程序设计高级/数组.md` | 数组 ↔ 集合互转 | 高 |
| `程序设计中级/函数.md` | `程序设计高级/特殊类型.md` | 函数类型 vs 函数式接口 | 中 |
| `程序设计高级/数组.md` | `程序设计中级/类与对象.md` | Array 是泛型类 | 中 |

### 3. 跨主题 link (跨向 java)

| 源 | 目标 | 关系 |
|---|---|---|
| `程序设计中级/封装,继承和多态.md` | `java/javaSE/...java8新特性.md` | lambda、apply/let/run/also 与 java stream 类似 |
| `程序设计中级/封装,继承和多态.md` | `java/javaSE/Hello World.md` | "与 java 一样" |
| `程序设计中级/类与对象.md` | `java/设计模式/创建类型.md` | 设计模式基于 OOP |
| `程序设计高级/集合.md` | `java/javaSE/...java8新特性.md` | Stream API、lambda |
| `程序设计高级/泛型.md` | `java/小框架/...` (JUC-泛型类) | 协变/逆变与 java 通配符 |

---

## unity (8 笔记)

### 1. 核心概念 (Top 3)

| 笔记 | 枢纽价值 | 原因 |
|---|---|---|
| **初步认识** | ★★★★★ | 生命周期方法(Awake/Update/LateUpdate)被 `transform控制父子`、`按键监听`、`场景`、`触摸`、`游戏时间` 引用 |
| **游戏物体的获取** | ★★★★ | gameObject/transform 引用基础,被 `transform控制父子`、`场景` 引用 |
| **transform控制父子** | ★★★ | transform 是核心组件,被 `游戏物体的获取`、`场景`、`触摸` 引用 |

### 2. 主题内 cross-link 候选 (Top 10)

| 源 | 目标 | 关系 | 优先级 |
|---|---|---|---|
| `transform控制父子.md` | `初步认识.md` | transform 在 Update 中调用 | 高 |
| `transform控制父子.md` | `游戏物体的获取.md` | 获取 transform 组件 | 高 |
| `游戏物体的获取.md` | `transform控制父子.md` | transform 子物体操作 | 高 |
| `按键监听.md` | `初步认识.md` | Update 内监听 | 高 |
| `触摸.md` | `按键监听.md` | 同为输入,触摸为多点 | 高 |
| `场景.md` | `初步认识.md` | Start/Update 中调用 | 高 |
| `游戏时间.md` | `初步认识.md` | Update 中使用 Time.deltaTime | 高 |
| `场景.md` | `transform控制父子.md` | 场景切换时父物体失效 | 中 |
| `文件-程序管理.md` | `场景.md` | persistentDataPath 跨场景保存 | 低 |
| `触摸.md` | `transform控制父子.md` | 触摸后移动 transform | 中 |

### 3. 跨主题 link

| 源 | 目标 | 关系 |
|---|---|---|
| `transform控制父子.md` | `c/基本/基础知识.md` | Unity 用 C#,类型系统与 C 类似 |
| `游戏物体的获取.md` | `c/基本/基础知识.md` | struct/class 类型 |
| `脚本开发/*` | `c/数据结构/...` | 容器数据结构 |

---

## docker (7 笔记)

### 1. 核心概念 (Top 3)

| 笔记 | 枢纽价值 | 原因 |
|---|---|---|
| **容器与镜像** | ★★★★★ | 核心概念,被 `单机容器编排`、`存储管理`、`网络管理`、`资源管理` 全部引用 |
| **网络管理** | ★★★★ | 端口映射、bridge 网络 |
| **单机容器编排** | ★★★ | docker-compose V2 配置入口 |

### 2. 主题内 cross-link 候选 (Top 7)

| 源 | 目标 | 关系 | 优先级 |
|---|---|---|---|
| `docker/单机容器编排.md` | `docker-compose/安装与配置.md` | docker-compose V2 入口 | 高 |
| `docker-compose/安装与配置.md` | `docker/单机容器编排.md` | V1 vs V2 对比 | 高 |
| `docker/存储管理.md` | `docker/容器与镜像.md` | 卷基于容器层 | 高 |
| `docker/网络管理.md` | `docker/容器与镜像.md` | 容器间网络 | 高 |
| `docker/资源管理.md` | `docker/容器与镜像.md` | 容器 CPU/内存限制 | 中 |
| `docker/配置与运行.md` | `docker/单机容器编排.md` | 启动配置 | 中 |
| `docker/单机容器编排.md` | `docker/容器与镜像.md` | build 镜像 | 高 |

### 3. 跨主题 link

| 源 | 目标 | 关系 |
|---|---|---|
| `docker/配置与运行.md` | `liunx/linux命令/系统操作相关.md` | systemctl 命令 |
| `docker/配置与运行.md` | `liunx/linux命令/...sudo用户权限` | sudo vim 操作 |
| `docker/单机容器编排.md` | `liunx/linux命令/...apt包管理` | apt install |
| `docker/网络管理.md` | `computer/计算机网络/TCP连接.md` | 端口映射基于 TCP |
| `docker/网络管理.md` | `computer/计算机网络/网络和通信协议.md` | OSI 7 层模型 |
| `docker/容器与镜像.md` | `liunx/基础知识/文件系统.md` | bootfs/rootfs 文件系统 |

---

## computer (6 笔记)

### 1. 核心概念 (Top 3)

| 笔记 | 枢纽价值 | 原因 |
|---|---|---|
| **网络和通信协议** | ★★★★★ | OSI 7 层框架,被 `TCP连接`、`UDP协议`、`HTTP协议`、`网络安全攻击` 引用 |
| **TCP连接** | ★★★★ | 三次握手/四次挥手基础 |
| **HTTP协议** | ★★★ | 应用层协议,被 `网络安全攻击` 引用(CSRF) |

### 2. 主题内 cross-link 候选 (Top 5)

| 源 | 目标 | 关系 | 优先级 |
|---|---|---|---|
| `计算机网络/TCP连接.md` | `计算机网络/网络和通信协议.md` | TCP 是传输层(OSI 第 4 层) | 高 |
| `计算机网络/UDP协议.md` | `计算机网络/网络和通信协议.md` | UDP 是传输层 | 高 |
| `计算机网络/HTTP协议.md` | `计算机网络/网络和通信协议.md` | HTTP 是应用层 | 高 |
| `计算机网络/HTTP协议.md` | `计算机网络/TCP连接.md` | HTTP/1.1 基于 TCP, HTTP/3 基于 UDP | 高 |
| `网络安全/网络安全攻击.md` | `计算机网络/HTTP协议.md` | CSRF 通过 HTTP cookie 攻击 | 中 |
| `底层/将多数据压缩进字节.md` | `c/基本/...位运算` | uint8_t 操作基于 C | 中 |

### 3. 跨主题 link

| 源 | 目标 | 关系 |
|---|---|---|
| `计算机网络/HTTP协议.md` | `go/go基础/库-http.md` | Go http 库实现 HTTP 协议 |
| `计算机网络/HTTP协议.md` | `java/...NIO.md` | Java NIO 实现非阻塞 HTTP |
| `计算机网络/TCP连接.md` | `java/javaSE/NIO.md` | Java NIO 封装 TCP |
| `计算机网络/UDP协议.md` | `java/小框架/Netty.md` | Netty 同时支持 TCP/UDP |
| `计算机网络/网络和通信协议.md` | `liunx/基础知识/文件系统.md` | TCP/IP 与 Linux 内核网络栈 |

---

## build_tools (5 笔记)

### 1. 核心概念 (Top 2)

| 笔记 | 枢纽价值 | 原因 |
|---|---|---|
| **Git/安装 配置 初始化.md** | ★★★★ | 环境配置入口 |
| **maven/操作.md` | ★★★ | 生命周期命令基础 |

### 2. 主题内 cross-link 候选 (Top 5)

| 源 | 目标 | 关系 | 优先级 |
|---|---|---|---|
| `Git/使用.md` | `Git/安装 配置 初始化.md` | 使用前需安装配置 | 高 |
| `maven/操作.md` | `maven/依赖管理.md` | install 操作引入依赖 | 高 |
| `maven/依赖管理.md` | `maven/操作.md` | pom.xml 配置 → mvn 命令 | 高 |
| `IDEA/快捷键操作.md` | `Git/使用.md` | IDEA 内 Git 操作 | 中 |
| `IDEA/快捷键操作.md` | `maven/操作.md` | IDEA 右上角 Maven 板块 | 高 |

### 3. 跨主题 link

| 源 | 目标 | 关系 |
|---|---|---|
| `maven/操作.md` | `java/...Spring-Start.md` | SpringBoot 用 maven 构建 |
| `maven/依赖管理.md` | `java/Spring框架/...spring-boot` | SpringBoot 依赖 |
| `Git/使用.md` | `liunx/Shell脚本/...` | Git 内部用 shell |

---

## AI + windows (1+1 笔记)

主题笔记太少,无法主题内 link。

**AI/LLM/Prompt Engineering.md** 跨主题候选:
- → `computer/计算机网络/HTTP协议.md` (HTTP/SSE 流式传输 → LLM 回复流)
- → `computer/网络安全/网络安全攻击.md` (Prompt Injection 是 AI 时代新型攻击)

**windows/WSL.md** 跨主题候选:
- → `liunx/linux命令/系统操作相关.md` (WSL 中用 Linux 命令)
- → `liunx/基础知识/文件系统.md` (ext4 文件系统挂载)

---

## 4. 歧义笔记识别

### 同名歧义 (跨主题)

| 名称 | 出现位置 | 解决方案 |
|---|---|---|
| `基础知识` | kotlin/基础/, SQL/NoSQL/, 其他 | Obsidian 文件名重复 → 会弹歧义选择 |
| `基础` | (未在新批次) | 历史已存在 |
| `函数` | kotlin/程序设计中级/, 其他 (C/Python/Java) | 历史歧义 |
| `数组` | kotlin/程序设计高级/, c/基本/, python/基础/ | 历史歧义 |
| `类与对象` | kotlin/程序设计中级/, python/基础/ | 历史歧义 |
| `封装,继承和多态` | kotlin/程序设计中级/ | 仅 1 处 |
| `网络管理` | docker/docker/, docker/docker-compose/ | 同主题但子目录不同 |
| `安装与配置` | docker/docker-compose/, 其他 (Git/maven/...) | 历史歧义 |
| `使用` | Git/使用, build_tools/使用, 其他 (SQL/Redis) | 历史歧义 |
| `操作` | maven/操作, maven/依赖管理/操作, 其他 | 历史歧义 |
| `依赖管理` | maven/依赖管理 | 仅 1 处 (新批次) |
| `快捷键操作` | IDEA/快捷键操作 | 仅 1 处 (新批次) |

### 新增跨主题歧义 (会引发 Obsidian ambiguous 选择)

- **`网络管理`**: docker/docker/网络管理.md vs docker/docker-compose/(隐含) → 后者不存在,OK
- **`安装与配置`**: docker/docker-compose/安装与配置.md vs 历史 build_tools/Git/安装 配置 初始化.md → 会歧义
- **`使用`**: build_tools/Git/使用.md vs 历史 SQL/Redis/基本操作.md → 会歧义
- **`操作`**: build_tools/maven/操作.md vs SQL/Redis/操作.md → 会歧义

### 解决建议

后续添加 wikilink 时使用**完整路径**:
```markdown
[[docker-compose/安装与配置]]   而非 [[安装与配置]]
[[Git/使用]]                    而非 [[使用]]
```

---

## 实施建议 (供后续批次使用)

### 优先级排序

**P0 (核心枢纽,价值最高)**:
1. `计算机网络/网络和通信协议.md` 接收 5 条入链
2. `docker/docker/容器与镜像.md` 接收 5 条入链
3. `unity/脚本开发/初步认识.md` 接收 5 条入链
4. `kotlin/程序设计中级/类与对象.md` 接收 4 条入链
5. `docker-compose/安装与配置.md` 接收 1 条但补强 `单机容器编排`

**P1 (主题内密度提升)**:
- kotlin: 10 条
- docker: 7 条
- unity: 10 条
- computer: 5 条
- build_tools: 5 条

**P2 (跨主题,建立知识网)**:
- kotlin ↔ java: 5 条
- docker ↔ liunx/computer: 6 条
- computer ↔ go/java: 4 条
- build_tools ↔ java: 2 条
- AI/windows 各 2 条

### 总链接预测

| 主题 | 主题内新增 | 跨主题新增 |
|---|---|---|
| kotlin | 10 | 5 |
| unity | 10 | 2 |
| docker | 7 | 6 |
| computer | 5 | 4 |
| build_tools | 5 | 2 |
| AI + windows | 0 | 4 |
| **合计** | **37** | **23** |

总计可新增 ~60 条 cross-link,加上现有 217 条 MOC wikilinks → 约 **277 条 wikilinks**。

---

## 后续步骤

**选项 A**: 立即派 4-5 worker 并行实施 cross-link (P0+P1)
- 预期: 37 条主题内链接
- 风险: 同名歧义必须用完整路径

**选项 B**: 手动去歧义 + 派 worker
- 先把 4 个歧义笔记改名/加路径前缀
- 再派 worker 实施链接
- 预期更干净

**选项 C**: 暂缓,等用户看到 Obsidian 图谱效果后再决定