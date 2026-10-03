---
title: Windows 单机部署与鉴权
tags: [java, nacos, Windows, 部署]
aliases: [Nacos Windows安装, Nacos单机部署]
---

# Windows 单机部署与鉴权

Windows 单机部署用于在本机学习服务注册和配置管理，默认使用内置 Derby 存储。

> [!abstract]
> 本课重点：下载 3.2.4 发行包；配置 JDK 和鉴权；启动、验证与停止服务。

## 准备环境

以下命令在 **PowerShell 7** 中执行。先安装 64 位 JDK 17，将 <code>&lt;JDK_DIR&gt;</code> 替换为自己的安装目录，再设置当前会话：

```powershell
$env:JAVA_HOME = '<JDK_DIR>'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
java -version
& "$env:JAVA_HOME\bin\jps.exe" -l
```

检查 <code>8080</code>、<code>8848</code>、<code>9848</code> 等端口是否被占用：

```powershell
Get-NetTCPConnection -State Listen |
    Where-Object LocalPort -In 8080, 8848, 9848, 9849, 7848 |
    Select-Object LocalAddress, LocalPort, OwningProcess
```

## 下载与解压

```powershell
$nacosVersion = '3.2.4'
$toolsDir = '<TOOLS_DIR>' # 替换为自己的工具目录
$nacosZip = Join-Path $toolsDir "nacos-server-$nacosVersion.zip"
New-Item -ItemType Directory -Path $toolsDir -Force
Invoke-WebRequest -Uri "https://github.com/alibaba/nacos/releases/download/$nacosVersion/nacos-server-$nacosVersion.zip" -OutFile $nacosZip
$extractDir = Join-Path $toolsDir "nacos-$nacosVersion"
Expand-Archive -LiteralPath $nacosZip -DestinationPath $extractDir
$nacosDir = Join-Path $extractDir 'nacos'
```

以 [3.2.4 官方发布页](https://github.com/alibaba/nacos/releases/tag/3.2.4)的 Assets 为准；下载的是发行包，不是 GitHub 自动生成的 Source code 包。解压后应有 <code>bin</code>、<code>conf</code>、<code>target</code> 等目录。

## 配置端口与鉴权

编辑 <code>$nacosDir\conf\application.properties</code> 中的**既有配置项**，避免在文件末尾重复添加同名项：

```properties
nacos.server.main.port=8848
nacos.server.contextPath=/nacos
nacos.console.port=8080
nacos.console.contextPath=
nacos.core.auth.system.type=nacos
nacos.core.auth.enabled=true
nacos.core.auth.admin.enabled=true
nacos.core.auth.console.enabled=true
```

| 配置项 | 3.2.4 发行包默认值 | 含义 |
| --- | --- | --- |
| <code>nacos.core.auth.enabled</code> | <code>false</code> | Client HTTP / SDK / gRPC 访问鉴权；本课主动开启 |
| <code>nacos.core.auth.admin.enabled</code> | <code>true</code> | 管理接口鉴权 |
| <code>nacos.core.auth.console.enabled</code> | <code>true</code> | 控制台鉴权 |

另外填写三个空值：

```properties
nacos.core.auth.plugin.nacos.token.secret.key=<NACOS_TOKEN_SECRET_BASE64>
nacos.core.auth.server.identity.key=<NACOS_IDENTITY_KEY>
nacos.core.auth.server.identity.value=<NACOS_IDENTITY_VALUE>
```

使用 PowerShell 在本机生成值，然后填进上述配置；尖括号内容是占位说明，不能原样保留：

```powershell
[Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
# 上面结果用作 token.secret.key
'<NACOS_IDENTITY_KEY>' # 自行填写内部身份key
# 上面结果用作 server.identity.key
[Guid]::NewGuid().ToString('N')
# 上面结果用作 server.identity.value
```

Token 密钥是签名材料，**不是登录密码或 accessToken**。后续集群所有节点必须使用相同的 Token 密钥和内部身份配置。

> [!warning]
> 官网部分页面对客户端鉴权默认值的描述不一致。本课默认值以 3.2.4 标签下的发行配置为准，并显式开启三类鉴权。真实密钥、密码、Token 保存在私有配置或环境变量中，不写进公开文章、示例代码或日志。

## 启动与初始化

```powershell
& "$nacosDir\bin\startup.cmd" -m standalone
```

<code>startup.cmd</code> 在当前终端前台运行，验证操作放到另一个 PowerShell 窗口。若三个鉴权配置仍为空，脚本会提示输入；提前填好可以避免交互修改配置。

打开 <code>http://&lt;NACOS_HOST&gt;:8080</code>，首次设置管理员 <code>nacos</code> 的密码，再登录。新增学习用业务账号，为所需命名空间分配角色与权限；业务应用使用该账号。这里的主机地址由读者填写，端口是默认值。

| 端口 | 默认用途 | 本机学习关注点 |
| --- | --- | --- |
| <code>8080</code> | Console | 浏览器管理页面 |
| <code>8848</code> | Server 主端口 | SDK 的 <code>server-addr</code> 和 HTTP API |
| <code>9848</code> | SDK gRPC，主端口 + 1000 | Java 应用必须可达 |
| <code>9849</code> | Server 间 gRPC，主端口 + 1001 | 集群节点间可达 |
| <code>7848</code> | JRaft，主端口 - 1000 | 集群节点间可达 |

默认合并部署同时启动 Server 与 Console；独立控制台部署是另一种拓扑。Server 地址中填写 <code>&lt;NACOS_HOST&gt;:8848</code>，不填写控制台地址或 <code>/nacos</code> 页面路径。

## 验证启动

```powershell
Test-NetConnection -ComputerName '<NACOS_HOST>' -Port 8848
Test-NetConnection -ComputerName '<NACOS_HOST>' -Port 9848
Get-Content -LiteralPath "$nacosDir\logs\nacos.log" -Tail 50 -Wait
```

以终端启动成功信息和控制台可登录为第一步验证，再完成 [[04-SpringCloud服务注册与调用|服务调用]] 和 [[05-配置中心与动态刷新|配置刷新]] 的闭环。端口打开仅证明进程监听，不能证明权限和业务功能正确。

## 停止与数据目录

仅运行一个 Nacos 进程时，可以在另一个终端执行：

```powershell
& "$nacosDir\bin\shutdown.cmd"
```

> [!warning]
> 3.2.4 的 Windows 关闭脚本会查找并强制结束带 <code>nacos.nacos</code> 标记的 Java 进程，可能停止本机多个 Nacos 实例。三进程练习不能把它当作“只停止当前目录”的命令。

| 目录 | 用途 |
| --- | --- |
| <code>conf</code> | 应用配置、集群地址、数据库初始化 SQL |
| <code>data</code> | 内置数据库及协议持久化数据等 |
| <code>logs</code> | 服务端日志 |
| <code>target</code> | 发行包运行 JAR |

单机内置 Derby 不需要安装 MySQL；切换到外置 MySQL 时要初始化对应版本的 SQL，并明确迁移原数据，修改连接配置不会自动搬运 Derby 数据。

详见 [[08-集群部署与外置数据库|集群与数据库]]、[[10-运维监控与故障排查|监控与排错]]、[[01-PowerShell入门与核心思维|PowerShell 入门]]。
