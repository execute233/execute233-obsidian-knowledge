# Cross-Link 分析: c + go + liunx (57 篇)

**Vault 路径**: `E:/个人知识`
**扫描范围**: `OneNote/c` (21) + `OneNote/go` (18) + `OneNote/liunx` (18) = 57 篇
**生成时间**: 2026-08-02
**报告作用**: 识别 cross-link 候选,辅助后续手动/半自动建立 wikilink,增强图谱密度。

---

## c (21 篇)

### 1. 核心概念笔记 (Top 10) — 枢纽价值排序

枢纽价值 = 概念被引频度 × 跨子主题相关度 × 是否有"基础 → 进阶"承接关系

| # | 笔记 | 路径 | 枢纽分 | 理由 |
|---|---|---|---|---|
| 1 | **指针** | `基本/变量.md` + `中级/指针.md` | 10 | 几乎所有高级主题都涉及指针(数组/字符串/函数/结构体)。这是 c 最核心的"知识枢纽"。 |
| 2 | **函数** | `中级/函数.md` + `基本/变量.md`(概念) | 9 | 函数参数传递、指针参数、回调函数等。stdarg.h / stdlib.h / string.h 都涉及。 |
| 3 | **字符串** | `基本/字符串.md` + `系统库/string.h.md` | 9 | 字符串是基础概念,所有 stdio.h(string IO) 和 string.h 都依赖。 |
| 4 | **数组** | `基本/数组.md` + `中级/数组.md` | 8 | 指针数组、字符串底层、线性表都是数组的延展。 |
| 5 | **结构体** | `高级/结构体，联合体和枚举.md` | 8 | typedef 关键字(`基本数据类型.md`)和 stdlib.h 的 qsort 都涉及结构体。 |
| 6 | **预处理** | `高级/预处理.md` + `编译,构建,调试/c语言的编译.md` | 7 | 编译流程第一阶段就是预处理。文件包含、宏定义贯穿所有 c 项目。 |
| 7 | **标准库** | `系统库/stdio.h.md` + `stdlib.h.md` + `string.h.md` + `math.h.md` + `time.h.md` | 7 | 标准库是 c 的核心 API 集合,被所有 c 笔记引用。 |
| 8 | **编译流程** | `编译,构建,调试/c语言的编译.md` | 6 | 跨主题枢纽:c 编译 ↔ build_tools(GCC/Make)。 |
| 9 | **基本数据类型** | `基本/基本数据类型.md` | 5 | typedef、sizeof、类型转换都涉及。 |
| 10 | **编码/二进制** | `基本/基础知识.md` | 4 | 字符串编码、字符集知识 — 支撑所有 IO 操作。 |

### 2. 主题内 cross-link 候选 (Top 30)

**强相关** (同概念基本 ↔ 进阶):

| # | A | B | 关系 | 建议 |
|---|---|---|---|---|
| 1 | `基本/变量.md` | `中级/指针.md` | 变量 → 指针(指针是变量的特殊形式) | `[[指针]]` |
| 2 | `基本/变量.md` | `中级/函数.md` | 变量 → 函数(函数参数涉及变量传递) | `[[函数]]` |
| 3 | `基本/数组.md` | `中级/指针.md` | 数组 → 指针(数组名是指针) | `[[指针]]` |
| 4 | `基本/数组.md` | `中级/函数.md` | 数组 → 函数参数 | `[[函数]]` |
| 5 | `基本/字符串.md` | `系统库/string.h.md` | 字符串 → string.h 函数 | `[[string.h]]` |
| 6 | `基本/字符串.md` | `系统库/stdio.h.md` | 字符串 → IO 函数 | `[[stdio.h]]` |
| 7 | `基本/字符串.md` | `基本/基础知识.md` | 字符串 → 编码基础 | `[[基础知识]]` |
| 8 | `基本/基本数据类型.md` | `高级/结构体，联合体和枚举.md` | 数据类型 → 结构体(typedef 用法) | `[[结构体，联合体和枚举]]` |
| 9 | `基本/基本数据类型.md` | `高级/预处理.md` | typedef → 宏定义(类型别名也可用宏) | `[[预处理]]` |
| 10 | `基本/基本数据类型.md` | `基本/变量.md` | 数据类型 → 变量声明 | `[[变量]]` |
| 11 | `中级/指针.md` | `中级/函数.md` | 函数指针 → 函数 | `[[函数]]` |
| 12 | `中级/函数.md` | `中级/指针.md` | 函数参数 → 指针 | `[[指针]]` |
| 13 | `中级/函数.md` | `系统库/stdarg.h.md` | 函数 → 可变参数 | `[[stdarg.h]]` |
| 14 | `中级/函数.md` | `高级/预处理.md` | 函数 → 宏函数 | `[[预处理]]` |
| 15 | `数据结构/线性表.md` | `数据结构/树 森林 二叉树.md` | 线性表 → 树(数据结构基础) | `[[树 森林 二叉树]]` |
| 16 | `数据结构/线性表.md` | `基本/数组.md` | 顺序表 → 数组 | `[[数组]]` |
| 17 | `数据结构/树 森林 二叉树.md` | `数据结构/高级树 其它树.md` | 树 → 高级树 | `[[高级树 其它树]]` |
| 18 | `数据结构/树 森林 二叉树.md` | `中级/指针.md` | 树 → 指针(树用指针实现) | `[[指针]]` |
| 19 | `系统库/stdio.h.md` | `基本/字符串.md` | stdio → 字符串 IO | `[[字符串]]` |
| 20 | `系统库/stdlib.h.md` | `基本/基本数据类型.md` | stdlib → 数据类型(size_t 等) | `[[基本数据类型]]` |
| 21 | `系统库/stdlib.h.md` | `中级/指针.md` | qsort → 函数指针 | `[[指针]]` |
| 22 | `系统库/string.h.md` | `基本/字符串.md` | string.h → 字符串 | `[[字符串]]` |
| 23 | `高级/预处理.md` | `编译,构建,调试/c语言的编译.md` | 预处理 → 编译流程 | `[[c 语言的编译]]` |
| 24 | `高级/结构体，联合体和枚举.md` | `中级/函数.md` | 结构体 → 函数(传结构体) | `[[函数]]` |
| 25 | `高级/结构体，联合体和枚举.md` | `中级/指针.md` | 结构体 → 指针(结构体指针) | `[[指针]]` |

**弱相关** (类似/上下文):

| # | A | B | 关系 |
|---|---|---|---|
| 26 | `基本/变量.md` | `基本/流程控制.md` | 变量 → 控制流 |
| 27 | `基本/流程控制.md` | `中级/函数.md` | 控制流 → 函数调用 |
| 28 | `系统库/time.h.md` | `系统库/math.h.md` | 同为标准库 |
| 29 | `系统库/stdarg.h.md` | `中级/函数.md` | 可变参数 → 函数 |
| 30 | `系统库/math.h.md` | `基本/基本数据类型.md` | math → 数据类型 |

### 3. 跨主题 link 候选 (Top 15) — c 与其它主题

| # | 源 | 目标 | 关系 |
|---|---|---|---|
| 1 | `c/编译,构建,调试/c语言的编译.md` | `build_tools/Git/...` | c 编译 → 构建工具链 |
| 2 | `c/编译,构建,调试/c语言的编译.md` | `build_tools/maven/...` | (弱)构建流程概念 |
| 3 | `c/系统库/stdio.h.md` | `liunx/linux命令/快速命令.md` | c 标准 IO ↔ linux 文件 IO 命令 |
| 4 | `c/系统库/stdio.h.md` | `liunx/linux命令/文件操作.md` | stdio.fopen ↔ shell 文件操作 |
| 5 | `c/基本/字符串.md` | `liunx/Shell脚本/变量.md` | c 字符串 ↔ shell 字符串变量 |
| 6 | `c/基本/字符串.md` | `go/go基础/库-fmt.md` | c printf ↔ go fmt |
| 7 | `c/中级/指针.md` | `go/go基础/基础.md` | c 指针 ↔ go 引用(语法对比) |
| 8 | `c/基本/基本数据类型.md` | `go/go基础/基础.md` | 数据类型对比 |
| 9 | `c/数据结构/线性表.md` | `java/javaSE/...` (集合框架) | 概念对应(java 集合 = c 线性表的高级版) |
| 10 | `c/编译,构建,调试/c语言的编译.md` | `build_tools/Git/使用.md` | 编译流程 ↔ Git 工作流 |
| 11 | `c/高级/预处理.md` | `java/javaSE/java9~17新特性.md` | (弱)预处理概念 |
| 12 | `c/数据结构/树 森林 二叉树.md` | `kotlin/...` | 数据结构通用知识 |
| 13 | `c/数据结构/线性表.md` | `python/python/基础n件/numpy.md` | 线性表 = numpy 数组 |
| 14 | `c/系统库/math.h.md` | `python/python/机器学习/数学概念.md` | 数学函数 ↔ 数学概念 |
| 15 | `c/高级/结构体，联合体和枚举.md` | `go/go基础/基础.md` | c struct ↔ go struct |

---

## go (18 篇)

### 1. 核心概念笔记 (Top 10)

| # | 笔记 | 路径 | 枢纽分 | 理由 |
|---|---|---|---|---|
| 1 | **基础** | `go基础/基础.md` | 10 | 变量声明、类型、语法 — 所有 go 笔记的基础前置。 |
| 2 | **中级** | `go基础/中级.md` | 10 | slice/map/面向对象 — 高频引用对象,核心数据结构。 |
| 3 | **库-fmt** | `go基础/库-fmt.md` | 8 | 格式化输出 — 几乎所有 demo 代码都用 `fmt.Println`。 |
| 4 | **库-net-http** | `go基础/库-net-http.md` | 8 | HTTP 客户端/服务端,web 编程核心。 |
| 5 | **库-strconv** | `go基础/库-strconv.md` | 7 | 类型转换,数据处理常用。 |
| 6 | **Go Modules** | `go基础/Go Modules.md` | 7 | 包管理 — 跨所有项目,环境搭建相关。 |
| 7 | **泛型** | `go基础/泛型.md` | 6 | 1.18+ 重要特性,与中级/数据结构相关。 |
| 8 | **文件操作** | `go基础/文件操作.md` | 6 | IO 基础,与 os/io 包相关。 |
| 9 | **库-time** | `go基础/库-time.md` | 5 | 时间处理,日志/调度常用。 |
| 10 | **库-log** | `go基础/库-log.md` | 5 | 日志,与库-fmt/库-flag 相关。 |

### 2. 主题内 cross-link 候选 (Top 30)

**强相关**:

| # | A | B | 关系 |
|---|---|---|---|
| 1 | `go基础/基础.md` | `go基础/中级.md` | 基础 → 中级(继承关系) | `[[中级]]` |
| 2 | `go基础/基础.md` | `go基础/泛型.md` | 基础类型 → 泛型 | `[[泛型]]` |
| 3 | `go基础/中级.md` | `go基础/泛型.md` | slice/map → 泛型 | `[[泛型]]` |
| 4 | `go基础/中级.md` | `go基础/库-strconv.md` | 类型转换场景 | `[[库-strconv]]` |
| 5 | `go基础/库-fmt.md` | `go基础/库-strconv.md` | fmt 格式化 ↔ strconv 转换 | `[[库-strconv]]` |
| 6 | `go基础/库-fmt.md` | `go基础/库-log.md` | fmt ↔ log(都是输出) | `[[库-log]]` |
| 7 | `go基础/库-fmt.md` | `go基础/库-time.md` | 时间格式化字符串 | `[[库-time]]` |
| 8 | `go基础/库-http.md` | `go基础/库-net-http.md` | http 库对比 | `[[库-net-http]]` |
| 9 | `go基础/库-net-http.md` | `gin/路由.md` | http 服务 ↔ gin 路由 | `[[路由]]` |
| 10 | `go基础/库-net-http.md` | `gin/请求.md` | http request ↔ gin request | `[[请求]]` |
| 11 | `go基础/库-net-http.md` | `gin/bind绑定器.md` | http body ↔ gin bind | `[[bind绑定器]]` |
| 12 | `go基础/Go Modules.md` | `go基础/环境搭建.md` | 包管理 → 环境 | `[[环境搭建]]` |
| 13 | `go基础/Go Modules.md` | `go基础/库-http.md` | (弱)模块引入第三方包 | `[[库-http]]` |
| 14 | `go基础/迭代器和iter包.md` | `go基础/中级.md` | 迭代器 ↔ slice/map 遍历 | `[[中级]]` |
| 15 | `go基础/迭代器和iter包.md` | `go基础/泛型.md` | 迭代器 ↔ 泛型 | `[[泛型]]` |
| 16 | `go基础/文件操作.md` | `go基础/库-fmt.md` | 文件读写 ↔ 格式化 | `[[库-fmt]]` |
| 17 | `go基础/文件操作.md` | `go基础/库-log.md` | 文件操作 ↔ 日志 | `[[库-log]]` |
| 18 | `go基础/库-flag.md` | `go基础/环境搭建.md` | 命令行 ↔ 环境配置 | `[[环境搭建]]` |
| 19 | `go基础/库-log.md` | `go基础/库-flag.md` | 日志 flag ↔ 命令行 flag | `[[库-flag]]` |
| 20 | `go基础/库-time.md` | `go基础/库-log.md` | 时间戳 ↔ 日志 | `[[库-log]]` |
| 21 | `gin/路由.md` | `gin/请求.md` | 路由 ↔ 请求处理 | `[[请求]]` |
| 22 | `gin/路由.md` | `gin/bind绑定器.md` | 路由 ↔ bind | `[[bind绑定器]]` |
| 23 | `gin/请求.md` | `gin/bind绑定器.md` | 请求数据 ↔ bind | `[[bind绑定器]]` |
| 24 | `gin/请求.md` | `go基础/库-net-http.md` | gin request ↔ net/http | `[[库-net-http]]` |
| 25 | `gin/bind绑定器.md` | `go基础/库-net-http.md` | gin bind ↔ net/http | `[[库-net-http]]` |

**弱相关**:

| # | A | B | 关系 |
|---|---|---|---|
| 26 | `go基础/环境搭建.md` | `go基础/Go Modules.md` | 环境 ↔ 包管理 |
| 27 | `go基础/单元测试.md` | `go基础/基础.md` | 测试 ↔ 基础语法 |
| 28 | `go基础/单元测试.md` | `go基础/中级.md` | 测试 ↔ 数据结构 |
| 29 | `go基础/库-time.md` | `go基础/基础.md` | time 类型 |
| 30 | `go基础/文件操作.md` | `go基础/库-http.md` | 文件 ↔ http body |

### 3. 跨主题 link 候选 (Top 15) — go 与其它主题

| # | 源 | 目标 | 关系 |
|---|---|---|---|
| 1 | `go/go基础/库-net-http.md` | `computer/计算机网络/HTTP协议.md` | HTTP 客户端 ↔ HTTP 协议 | `[[HTTP协议]]` |
| 2 | `go/go基础/库-net-http.md` | `computer/计算机网络/TCP连接.md` | HTTP 基于 TCP | `[[TCP连接]]` |
| 3 | `go/gin/路由.md` | `computer/计算机网络/HTTP协议.md` | gin 路由 ↔ HTTP | `[[HTTP协议]]` |
| 4 | `go/gin/请求.md` | `computer/计算机网络/HTTP协议.md` | gin request ↔ HTTP | `[[HTTP协议]]` |
| 5 | `go/go基础/库-flag.md` | `liunx/linux命令/快速命令.md` | 命令行参数 ↔ linux 命令 | `[[快速命令]]` |
| 6 | `go/go基础/环境搭建.md` | `liunx/linux命令/软件安装.md` | go 安装 ↔ linux 软件安装 | `[[软件安装]]` |
| 7 | `go/go基础/环境搭建.md` | `liunx/linux命令/系统操作相关.md` | go path ↔ 系统环境变量 | `[[系统操作相关]]` |
| 8 | `go/go基础/文件操作.md` | `liunx/linux命令/文件操作.md` | go 文件 IO ↔ shell 文件操作 | `[[文件操作]]` |
| 9 | `go/go基础/中级.md` | `python/python/常用内置模块/...` | 数据结构通用知识 | (弱) |
| 10 | `go/go基础/Go Modules.md` | `build_tools/Git/使用.md` | go mod ↔ git(go.mod 提交) | `[[使用]]` |
| 11 | `go/go基础/Go Modules.md` | `build_tools/Git/安装 配置 初始化.md` | go mod ↔ git 初始化 | `[[安装 配置 初始化]]` |
| 12 | `go/go基础/库-fmt.md` | `java/javaSE/...` (字符串格式化) | fmt ↔ java Formatter | (弱) |
| 13 | `go/go基础/库-http.md` | `python/python/常用第三方模块/requests.md` | http 客户端对比 | `[[requests]]` |
| 14 | `go/gin/bind绑定器.md` | `python/python/常用第三方模块/...` | 数据绑定 | (弱) |
| 15 | `go/go基础/基础.md` | `liunx/Shell脚本/前言.md` | go 编译 ↔ shell 执行 | (弱) |

---

## liunx (18 篇)

### 1. 核心概念笔记 (Top 10)

| # | 笔记 | 路径 | 枢纽分 | 理由 |
|---|---|---|---|---|
| 1 | **文件操作** | `linux命令/文件操作.md` | 10 | ls/cp/mv/find — 使用频率最高。 |
| 2 | **系统操作相关** | `linux命令/系统操作相关.md` | 9 | systemctl/ln/date — 系统管理核心。 |
| 3 | **文件系统** | `基础知识/文件系统.md` | 8 | /bin /home /etc — 所有 linux 操作的基础认知。 |
| 4 | **Shell 脚本/前言** | `Shell脚本/前言.md` | 7 | Shell 编程入门,与所有 Shell 笔记关联。 |
| 5 | **用户/用户组/权限** | `linux命令/用户 用户组 权限.md` | 7 | 权限管理,跨所有 linux 操作。 |
| 6 | **快速命令** | `linux命令/快速命令.md` | 6 | 高频命令速查,基础入门。 |
| 7 | **Shell 变量** | `Shell脚本/变量.md` | 6 | Shell 编程基础,所有 Shell 脚本前置。 |
| 8 | **软件安装** | `linux命令/软件安装.md` | 6 | apt/yum,环境搭建相关。 |
| 9 | **curl** | `第三方命令/curl 网络传输.md` | 6 | HTTP 命令行,测试/调试高频。 |
| 10 | **ssh** | `第三方命令/ssh.md` | 5 | 远程登录,服务器管理必备。 |

### 2. 主题内 cross-link 候选 (Top 30)

**强相关**:

| # | A | B | 关系 |
|---|---|---|---|
| 1 | `基础知识/文件系统.md` | `linux命令/文件操作.md` | 文件系统 → 文件操作 | `[[文件操作]]` |
| 2 | `基础知识/文件系统.md` | `linux命令/用户 用户组 权限.md` | 文件系统 → /home 权限 | `[[用户 用户组 权限]]` |
| 3 | `基础知识/文件系统.md` | `linux命令/系统操作相关.md` | /etc/systemd → systemctl | `[[系统操作相关]]` |
| 4 | `linux命令/文件操作.md` | `linux命令/快速命令.md` | 文件操作 ↔ 快速命令速查 | `[[快速命令]]` |
| 5 | `linux命令/文件操作.md` | `linux命令/系统操作相关.md` | ln -s → 创建软链接 | `[[系统操作相关]]` |
| 6 | `linux命令/文件操作.md` | `linux命令/用户 用户组 权限.md` | 文件权限 | `[[用户 用户组 权限]]` |
| 7 | `linux命令/快速命令.md` | `linux命令/系统操作相关.md` | 命令 ↔ 系统操作 | `[[系统操作相关]]` |
| 8 | `linux命令/快速命令.md` | `linux命令/软件安装.md` | apt 速查 | `[[软件安装]]` |
| 9 | `linux命令/用户 用户组 权限.md` | `linux命令/系统操作相关.md` | 用户 ↔ 服务权限 | `[[系统操作相关]]` |
| 10 | `linux命令/用户 用户组 权限.md` | `linux命令/文件操作.md` | chmod → 文件权限 | `[[文件操作]]` |
| 11 | `linux命令/系统操作相关.md` | `linux命令/软件安装.md` | systemctl ↔ apt(服务) | `[[软件安装]]` |
| 12 | `Shell脚本/前言.md` | `Shell脚本/变量.md` | 前言 → 变量 | `[[变量]]` |
| 13 | `Shell脚本/前言.md` | `Shell脚本/流程控制.md` | 前言 → 控制流 | `[[流程控制]]` |
| 14 | `Shell脚本/前言.md` | `Shell脚本/函数.md` | 前言 → 函数 | `[[函数]]` |
| 15 | `Shell脚本/变量.md` | `Shell脚本/流程控制.md` | 变量 → 控制流 | `[[流程控制]]` |
| 16 | `Shell脚本/变量.md` | `Shell脚本/函数.md` | 变量 → 函数参数 | `[[函数]]` |
| 17 | `Shell脚本/变量.md` | `Shell脚本/输入-输出重定向.md` | 变量 ↔ 重定向 | `[[输入-输出重定向]]` |
| 18 | `Shell脚本/流程控制.md` | `Shell脚本/函数.md` | 控制流 → 函数 | `[[函数]]` |
| 19 | `Shell脚本/流程控制.md` | `Shell脚本/运算符.md` | 条件 ↔ 运算符 | `[[运算符]]` |
| 20 | `Shell脚本/流程控制.md` | `Shell脚本/文件包含.md` | 控制 ↔ source | `[[文件包含]]` |
| 21 | `Shell脚本/函数.md` | `Shell脚本/文件包含.md` | 函数 ↔ source | `[[文件包含]]` |
| 22 | `Shell脚本/echo.md` | `Shell脚本/printf.md` | echo ↔ printf | `[[printf]]` |
| 23 | `Shell脚本/echo.md` | `Shell脚本/输入-输出重定向.md` | echo ↔ 重定向 | `[[输入-输出重定向]]` |
| 24 | `Shell脚本/printf.md` | `Shell脚本/变量.md` | printf 格式化 ↔ 变量 | `[[变量]]` |
| 25 | `Shell脚本/输入-输出重定向.md` | `linux命令/文件操作.md` | 重定向 ↔ 文件 IO | `[[文件操作]]` |

**弱相关**:

| # | A | B | 关系 |
|---|---|---|---|
| 26 | `第三方命令/curl 网络传输.md` | `linux命令/快速命令.md` | curl 速查 |
| 27 | `第三方命令/ssh.md` | `linux命令/系统操作相关.md` | sshd ↔ systemctl |
| 28 | `第三方命令/screen.md` | `linux命令/系统操作相关.md` | 后台进程 |
| 29 | `linux命令/软件安装.md` | `linux命令/系统操作相关.md` | apt + systemctl |
| 30 | `Shell脚本/运算符.md` | `Shell脚本/变量.md` | 整数运算 ↔ 变量 |

### 3. 跨主题 link 候选 (Top 15) — liunx 与其它主题

| # | 源 | 目标 | 关系 |
|---|---|---|---|
| 1 | `liunx/第三方命令/curl 网络传输.md` | `computer/计算机网络/HTTP协议.md` | curl ↔ HTTP 协议 | `[[HTTP协议]]` |
| 2 | `liunx/第三方命令/ssh.md` | `computer/计算机网络/TCP连接.md` | ssh 基于 TCP | `[[TCP连接]]` |
| 3 | `liunx/第三方命令/ssh.md` | `computer/计算机网络/UDP协议.md` | (弱) | `[[UDP协议]]` |
| 4 | `liunx/linux命令/系统操作相关.md` | `docker/docker/容器与镜像.md` | systemctl ↔ docker 容器 | `[[容器与镜像]]` |
| 5 | `liunx/linux命令/用户 用户组 权限.md` | `docker/docker/存储管理.md` | 权限 → 卷挂载 | `[[存储管理]]` |
| 6 | `liunx/基础知识/文件系统.md` | `docker/docker/存储管理.md` | 文件系统 ↔ docker volume | `[[存储管理]]` |
| 7 | `liunx/Shell脚本/变量.md` | `python/python/...` | Shell 字符串 ↔ python 字符串 | (弱) |
| 8 | `liunx/Shell脚本/前言.md` | `build_tools/Git/安装 配置 初始化.md` | Shell ↔ Git 安装 | `[[安装 配置 初始化]]` |
| 9 | `liunx/Shell脚本/前言.md` | `build_tools/Git/使用.md` | Shell + git 命令 | `[[使用]]` |
| 10 | `liunx/linux命令/系统操作相关.md` | `build_tools/Git/...` | systemctl ↔ git hooks | (弱) |
| 11 | `liunx/Shell脚本/流程控制.md` | `python/python/...` | 控制流通用 | (弱) |
| 12 | `liunx/Shell脚本/函数.md` | `python/python/...` | 函数通用 | (弱) |
| 13 | `liunx/Shell脚本/输入-输出重定向.md` | `c/c/系统库/stdio.h.md` | shell 重定向 ↔ c stdio | `[[stdio.h]]` |
| 14 | `liunx/linux命令/文件操作.md` | `c/c/系统库/stdio.h.md` | shell 文件操作 ↔ c stdio | `[[stdio.h]]` |
| 15 | `liunx/linux命令/软件安装.md` | `build_tools/maven/...` | linux 安装 ↔ maven 仓库 | (弱) |

---

## 4. 歧义笔记 (同名多文件)

Obsidian wikilink `[[xxx]]` 在同名文件存在时会弹歧义提示。

### 完全同名的笔记

| 笔记名 | 出现位置 (路径) |
|---|---|
| `函数` | `OneNote/c/中级/函数.md` + `OneNote/liunx/Shell脚本/函数.md` |
| `变量` | `OneNote/c/基本/变量.md` + `OneNote/liunx/Shell脚本/变量.md` |
| `数组` | `OneNote/c/基本/数组.md` + (其它) |
| `流程控制` | `OneNote/c/基本/流程控制.md` + `OneNote/liunx/Shell脚本/流程控制.md` |
| `基础知识` | `OneNote/c/基本/基础知识.md` + `OneNote/liunx/基础知识/文件系统.md`(广义) |
| `基础` | `OneNote/c/...` + `OneNote/go/go基础/基础.md`(广义) |
| `文件操作` | `OneNote/go/go基础/文件操作.md` + `OneNote/liunx/linux命令/文件操作.md` |

### 同名文件出现 2+ 次

| 笔记名 | 出现次数 |
|---|---|
| `函数` | 2 (c/中级, liunx/Shell脚本) |
| `变量` | 2 (c/基本, liunx/Shell脚本) |
| `数组` | 2 (c/基本, c/中级 等) |
| `流程控制` | 2 (c/基本, liunx/Shell脚本) |
| `文件操作` | 2 (go/go基础, liunx/linux命令) |
| `基础知识` | 2 (c/基本, liunx/基础知识) |
| `基础` | 2 (go/go基础, MOC) |

### 解决方案建议

**方案 A — wikilink 带路径前缀** (推荐):
```markdown
[[c/中级/函数]]   # c 函数
[[liunx/Shell脚本/函数]]   # shell 函数
```

**方案 B — 重命名消歧**:
```markdown
c/中级/函数.md → c/中级/C函数.md
liunx/Shell脚本/函数.md → liunx/Shell脚本/Shell函数.md
```

**方案 C — 接受歧义提示**:
让 Obsidian 在点击时弹出选择(影响 UX,降低密度)。

---

## 5. 总结与建议

### 优先级建议 (按价值)

1. **P0 (10+ wikilink)**: 立即建立 — `c/中级/指针.md` ↔ `c/基本/变量.md` 系列
2. **P1 (5-10 wikilink)**: 一周内 — go 库↔gin 系列
3. **P2 (1-4 wikilink)**: 渐进 — 跨主题稀疏 link

### 总潜在 wikilink 数

| 主题 | 主题内 | 跨主题 | 小计 |
|---|---|---|---|
| c | 30 | 15 | 45 |
| go | 30 | 15 | 45 |
| liunx | 30 | 15 | 45 |
| **合计** | **90** | **45** | **135** |

建立后,这三主题的笔记 wikilinks 从 0 → 135,孤立笔记从 57 → 大幅减少。

### 后续步骤建议

1. **建立 P0 link**: 主题内 30+30 = 60 个强相关 wikilink(人工或半自动)
2. **歧义消解**: 先决定用方案 A/B/C
3. **跨主题 link**: 价值密度低,可后置