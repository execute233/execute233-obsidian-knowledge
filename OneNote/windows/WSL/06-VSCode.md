---

title: WSL2与VS Code
tags: [windows, linux, wsl, wsl2, vscode]
aliases: [WSL2 VS Code, VS Code WSL]
---

# WSL2 与 VS Code

> [!abstract]
> 推荐架构：
>
> **VS Code UI 运行在 Windows，项目、Toolchain、Terminal、Git、Debugger、部分 Extension 运行在 WSL 2。**

---

# 1. 推荐架构

不要在 WSL 里再安装一套 Linux GUI 版 VS Code。

推荐：

```text
Windows
│
├── VS Code
│   └── WSL Extension
│
└── WSL 2
    │
    ├── VS Code Server
    ├── Git
    ├── Java
    ├── Node.js
    ├── Python
    ├── Debugger
    └── ~/projects
```

VS Code 官方推荐在 **Windows 侧安装 VS Code**，WSL Extension 会自动在 WSL 中安装并管理 VS Code Server。

---

# 2. Client / Server 架构

WSL Extension 会把 VS Code 拆成两部分：

```text
Windows
│
└── VS Code Client
    │
    │ WSL Extension
    │
    ▼
WSL 2
└── VS Code Server
    │
    ├── File Operations
    ├── Extension Host
    ├── Terminal
    ├── Debugger
    ├── Git
    └── Language Server
```

Windows 主要负责：

* Editor UI
* Window
* Theme
* Keyboard Shortcut
* 本地 UI Extension

WSL 主要负责：

* 文件操作
* Git
* Terminal
* Language Server
* Debugger
* Build Tool
* Runtime
* Workspace Extension

这也是 WSL 开发体验比较自然的关键。

---

# 3. 安装

Windows 安装：

`Visual Studio Code`

然后安装扩展：

`WSL`

建议安装 VS Code 时启用 `Add to PATH`，这样 WSL Terminal 中可以直接使用：

```bash
code .
```

不需要在 Ubuntu 中再安装：

```text
apt install code
```

---

# 4. 推荐项目位置

延续 [[WSL2文件系统]] 的原则：

推荐：

`~/projects/my-app`

而不是：

`/mnt/c/Users/<user>/projects/my-app`

例如：

```bash
mkdir -p ~/projects
cd ~/projects

git clone git@github.com:example/backend.git
cd backend

code .
```

如果 Toolchain 主要运行在 Linux，就让项目也位于 Linux 文件系统。

---

# 5. `code .`

进入项目：

```bash
cd ~/projects/backend
code .
```

第一次使用时，VS Code 会自动准备 WSL 中需要的 Server 组件。

之后会打开一个新的 VS Code Window。

左下角应该显示类似：

`WSL: Ubuntu`

这表示当前窗口是：

`Remote WSL Window`

而不是普通 Windows Workspace。

---

# 6. 如何确认当前处于 WSL

最简单：

查看 VS Code 左下角：

`WSL: Ubuntu`

Terminal 中：

```bash
uname -a
```

或者：

```bash
echo $WSL_DISTRO_NAME
```

再检查：

```bash
pwd
```

正常项目可能是：

`/home/ema/projects/backend`

而不是：

`C:\...`

---

# 7. 从 VS Code 连接 WSL

除了：

```bash
code .
```

也可以使用 Command Palette：

`Ctrl + Shift + P`

执行：

`WSL: Connect to WSL`

或者指定 Distribution：

`WSL: Connect to WSL using Distro`

已经打开 Windows Folder 时，可以：

`WSL: Reopen Folder in WSL`

从 WSL Window 返回 Windows：

`WSL: Reopen in Windows`

---

# 8. 从 Windows CLI 直接打开 WSL 项目

例如：

```powershell
code --remote wsl+Ubuntu /home/ema/projects/backend
```

基本格式：

```powershell
code --remote wsl+<Distro> <LinuxPath>
```

对于自动化脚本或多 Distribution 环境比较实用。

---

# 9. Terminal 在哪里运行？

当 Workspace 已经通过 WSL 打开后：

`Terminal → New Terminal`

打开的是 WSL Terminal。

例如：

```bash
pwd
which git
which node
which python3
which java
```

这些都会在 WSL 中执行。

因此：

```text
VS Code UI
```

虽然还在 Windows，

但：

```text
Terminal
```

已经运行在 Linux。

---

# 10. Toolchain 应该安装在哪里？

既然项目在 WSL 中运行，那么 Runtime 和 Toolchain 也应该安装在 WSL。

例如：

## Java

```bash
java -version
which java
```

期望类似：

`/usr/bin/java`

或者 Linux SDK 管理器中的路径。

## Node.js

```bash
node --version
which node
```

期望：

`/usr/bin/node`

或：

`~/.nvm/...`

## Python

```bash
python3 --version
which python3
```

例如：

`/usr/bin/python3`

或者：

`~/projects/app/.venv/bin/python`

---

# 11. 不要混用 Windows Runtime

例如项目运行在 WSL，却发现：

```bash
which node
```

解析到了：

`/mnt/c/Program Files/nodejs/node.exe`

这通常不是想要的结果。

对于 WSL 项目，更合理的是：

```text
Linux Project
+
Linux Node
+
Linux Git
+
Linux Python
+
Linux Java
```

也就是让整个 Toolchain 位于同一环境。

必要时可以在 `/etc/wsl.conf` 中关闭 Windows PATH 自动注入：

```ini
[interop]
appendWindowsPath=false
```

详见：

[[WSL2配置]]

---

# 12. Extension 运行在哪里？

VS Code WSL 最容易误解的一点就是：

> Extension 不一定全部运行在 Windows。

大体分为两类。

## Local Extension

运行在 Windows VS Code Client。

典型：

* Theme
* UI Extension
* Keymap

## Workspace Extension

运行在 WSL 的 Extension Host。

典型：

* Java
* Python
* ESLint
* Language Server
* Debugger
* 与项目文件交互的 Extension

架构：

```text
Windows
│
├── Theme Extension
├── UI Extension
│
└── VS Code Client
        │
        ▼
WSL
├── Java Extension
├── Python Extension
├── ESLint
├── Debugger
└── VS Code Server
```

---

# 13. 为什么 Extension 要在 WSL 安装？

假设 TypeScript 项目位于：

`~/projects/frontend`

并使用 Linux：

`node`

如果 ESLint / TypeScript Extension 在 WSL 中运行，它看到的是：

```text
Linux File System
Linux Node
Linux PATH
Linux node_modules
Linux Environment
```

这避免了：

```text
Windows Extension
↓
操作 Linux Project
↓
Path / Binary / Runtime 边界
```

带来的很多问题。

---

# 14. 查看 Extension 安装位置

打开：

`Extensions`

WSL Window 中通常会看到不同区域：

`Local - Installed`

以及：

`WSL: Ubuntu`

VS Code 会根据 Extension 类型决定安装位置。

如果某个本地 Extension 实际需要运行在 WSL，通常会看到：

`Install in WSL`

---

# 15. Java 开发

假设：

```text
~/projects/spring-app
```

WSL 中：

```bash
java -version
./mvnw --version
```

VS Code 的 Java Extension 运行在 WSL 后，就会使用 Linux Java Toolchain。

典型结构：

```text
Windows
└── VS Code UI
        │
        ▼
WSL
├── Java Extension
├── JDT Language Server
├── JDK
├── Maven / Gradle
└── Spring Boot
```

因此不要出现：

```text
Windows JDK
+
Linux Maven
+
WSL Project
```

这种不必要的混合环境。

---

# 16. TypeScript / Node.js 开发

推荐：

```bash
cd ~/projects/frontend

node --version
npm --version
pnpm --version

code .
```

之后：

```bash
pnpm install
pnpm dev
```

`node_modules` 留在 Linux 文件系统。

如果使用：

`nvm`

也应该安装在 WSL。

---

# 17. Python 开发

项目：

```bash
cd ~/projects/api

python3 -m venv .venv
source .venv/bin/activate

code .
```

然后 VS Code Python Extension 选择：

`~/projects/api/.venv/bin/python`

而不是：

`C:\Python...`

检查：

```bash
which python
```

确保 VS Code Terminal 和项目 Runtime 使用同一个 Python。

---

# 18. Debugger

WSL Workspace 中按：

`F5`

Debugger 会在 WSL 环境中启动程序。

例如：

`.vscode/launch.json`

中的程序会在 Remote Host，也就是 WSL 中执行。

架构：

```text
VS Code UI
   │
   │ Debug Protocol
   ▼
WSL Debug Adapter
   │
   ▼
Linux Process
```

因此可以直接 Debug：

* Java
* Node.js
* Python
* Go
* C/C++

而应用实际运行在 Linux。

---

# 19. `.vscode`

Workspace 配置仍然可以放：

```text
.vscode/
├── settings.json
├── launch.json
├── tasks.json
└── extensions.json
```

这些配置属于项目。

例如：

```json
{
  "editor.formatOnSave": true
}
```

或者 Debug：

```json
{
  "version": "0.2.0",
  "configurations": []
}
```

是否运行在 WSL，由当前 VS Code Workspace 的 Remote Context 决定。

---

# 20. Settings 的层级

WSL 模式下至少要区分：

```text
Local User Settings
Remote WSL Settings
Workspace Settings
```

可以理解：

```text
Local Settings
      ↓
Remote WSL Settings
      ↓
Workspace Settings
```

其中 Remote Settings 只在 WSL Remote Window 中生效。

打开：

`Ctrl + Shift + P`

执行：

`Preferences: Open Remote Settings`

可以配置 WSL 专属设置。

---

# 21. 什么时候使用 Remote Settings？

例如你希望：

Windows 本地：

```text
terminal.integrated.defaultProfile.windows
```

使用 PowerShell。

但 WSL：

```text
Terminal
```

使用 Bash / Zsh。

又比如：

Windows 和 Linux：

* Runtime Path
* Formatter
* Environment
* Terminal
* Extension Behavior

需要不同配置时，可以使用 Remote Settings。

---

# 22. Git 在哪里运行？

WSL Workspace 中，VS Code Source Control 通常使用 WSL 中的 Git。

检查：

```bash
which git
```

推荐：

`/usr/bin/git`

配置：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

注意：

> Windows Git 与 WSL Git 是两套独立环境。

所以：

```text
Windows ~/.gitconfig
```

和：

```text
WSL ~/.gitconfig
```

不是天然同一份配置。

---

# 23. Git Repository 不建议 Windows / WSL 混用

如果 Repository 在：

`~/projects/backend`

就优先使用：

`WSL Git`

不要今天：

```bash
git commit
```

明天又用：

`git.exe`

从 Windows 操作同一个 Repository。

可能导致：

* Credential 差异
* Line Ending 差异
* Hooks 环境差异
* SSH Key 差异
* Toolchain 差异

一个 Repository 尽量绑定一个主要开发环境。

---

# 24. SSH

WSL 项目通常也直接使用 Linux SSH：

`~/.ssh`

例如：

```bash
ls -la ~/.ssh
```

Git：

```bash
git clone git@github.com:example/project.git
```

此时使用的是：

```text
WSL
└── ~/.ssh
```

不是 Windows：

```text
C:\Users\<user>\.ssh
```

SSH 与 Git 凭据会在：

[[WSL2与Git]]

进一步整理。

---

# 25. VS Code Server

WSL Extension 会自动维护：

`VS Code Server`

通常相关文件位于：

`~/.vscode-server`

例如：

```bash
ls ~/.vscode-server
```

一般不需要手工管理它。

它负责在 WSL 侧提供：

* Remote Extension Host
* File Access
* Terminal
* Debugging
* Language Features

---

# 26. 一个重要细节：Shell Startup Script

VS Code Server 启动时，不会按普通 Interactive Shell 的方式执行所有 Shell Startup Script。

也就是说不要默认认为：

`.bashrc`

或：

`.zshrc`

中的所有环境修改一定会成为 VS Code Server 自身的环境。

如果确实需要修改 VS Code Server 启动环境，可以使用：

`~/.vscode-server/server-env-setup`

例如：

```bash
#!/bin/sh

export MY_ENV=value
```

> [!warning]
> 这个脚本出错可能直接导致 VS Code Server 无法正常启动，因此只在确实需要时使用。

普通开发环境通常不需要配置。

---

# 27. PATH 排错

如果：

Terminal 中：

```bash
java -version
```

正常，

但 VS Code Extension 找不到 Java，

或者：

```bash
node --version
```

正常，

Language Server 却找不到 Node，

先检查：

```bash
which java
which node
which python3

echo $PATH
```

再确认 Extension 是否真的安装在：

`WSL: Ubuntu`

而不是只有 Windows Local 版本。

---

# 28. VS Code WSL 日志

遇到 Remote 问题：

`Ctrl + Shift + P`

执行：

`WSL: Show Log`

重点用于排查：

* VS Code Server 安装失败
* Extension 启动失败
* Proxy
* PATH
* Server Environment
* WSL Connection

---

# 29. Proxy / 网络问题

VS Code WSL 首次启动时需要下载 VS Code Server 相关组件。

如果公司网络、Proxy 或 VPN 环境导致安装失败，可以结合：

[[WSL2网络]]

检查：

```bash
curl -I https://code.visualstudio.com
```

以及：

```bash
env | grep -i proxy
```

还可以查看：

`WSL: Show Log`

确认失败阶段。

---

# 30. 不要直接用 Windows VS Code 打开 `\\wsl$` 项目

虽然 Windows 可以通过：

`\\wsl$\Ubuntu\home\...`

访问 Linux 文件，

但开发时更推荐：

```bash
cd ~/projects/app
code .
```

让 VS Code 明确进入 WSL Remote Context。

区别在于：

```text
Windows File Access
```

和：

```text
WSL Remote Development
```

不是同一个概念。

真正需要的是：

```text
VS Code Client
        ↓
WSL Extension
        ↓
VS Code Server
        ↓
Linux Toolchain
```

---

# 31. 推荐开发工作流

进入 WSL：

```powershell
wsl
```

进入项目：

```bash
cd ~/projects/backend
```

确认环境：

```bash
which git
which java
which node
which python3
```

打开：

```bash
code .
```

之后所有：

```text
Terminal
Git
Build
Test
Debug
Language Server
```

都尽量留在 WSL Context 中。

---

# 32. Java / TS / Python 的统一模型

无论项目使用什么语言，本质都一样：

```text
Windows
└── VS Code UI
        │
        ▼
WSL 2
├── Project
├── Runtime
├── Package Manager
├── Language Server
├── Debugger
├── Git
└── Terminal
```

Java：

```text
JDK + Maven/Gradle
```

TypeScript：

```text
Node + npm/pnpm
```

Python：

```text
Python + venv/uv
```

都应该尽量属于 WSL 环境。

---

# 33. WSL + Dev Containers

WSL 还可以继续叠加 Dev Containers：

```text
Windows
│
└── VS Code
    │
    ▼
WSL 2
│
├── Source Code
│
└── Docker
    │
    ▼
Dev Container
│
├── Runtime
├── Dependencies
└── Toolchain
```

也就是：

```text
Windows UI
↓
WSL
↓
Container
```

VS Code 官方支持：

`WSL: Open Folder`

之后：

`Dev Containers: Reopen in Container`

如果项目存在：

`Dockerfile`

或：

`compose.yaml`

也可以作为 Dev Container 的基础。

这部分之后可以单独学习：

`[[Dev Containers]]`

---

# 34. 常见错误

## VS Code 安装两份

不推荐：

```text
Windows VS Code
+
WSL Linux VS Code GUI
```

推荐只维护：

`Windows VS Code`

再通过 WSL Extension 连接 Linux。

---

## Runtime 只安装在 Windows

例如项目运行在 WSL，但：

```bash
which java
```

找不到 Java。

Windows 已经安装 JDK 并不能自动代表 WSL 安装了 JDK。

WSL 是独立 Linux 环境。

---

## Extension 只安装在 Local

例如 Python Extension：

Windows 已安装，

但 WSL Workspace 中没有安装 Remote 版本。

检查 Extensions 中：

`WSL: Ubuntu`

---

## Repository 放 `/mnt/c`

如果主要使用 Linux Toolchain，不推荐：

`/mnt/c/...`

推荐：

`~/projects/...`

详见：

[[WSL2文件系统]]

---

## Windows Git 与 Linux Git 混用

尽量保持：

```text
WSL Repository
→ WSL Git
```

---

## 把 `.bashrc` 当 VS Code Server 配置

VS Code Server 启动环境和 Interactive Shell 并不完全相同。

需要特殊 Server Environment 时使用：

`~/.vscode-server/server-env-setup`

---

# 35. 常用命令

打开当前项目：

```bash
code .
```

打开指定目录：

```bash
code ~/projects/backend
```

检查：

```bash
which code
```

查看 CLI：

```bash
code --help
```

Windows 指定 WSL：

```powershell
code --remote wsl+Ubuntu /home/ema/projects/backend
```

检查 Toolchain：

```bash
which git
which java
which node
which python3
```

检查环境：

```bash
env
```

检查 WSL：

```bash
echo $WSL_DISTRO_NAME
```

---

# 36. 推荐心智模型

不要理解成：

```text
VS Code
↓
编辑 Linux 文件
```

而应该理解成：

```text
Windows
│
└── VS Code Client
        │
        │ Remote Protocol
        ▼
WSL 2
│
└── VS Code Server
    │
    ├── Workspace
    ├── Extension Host
    ├── Git
    ├── Terminal
    ├── Debugger
    └── Language Toolchain
```

所以 VS Code 虽然“看起来运行在 Windows”，开发环境实际上已经进入 WSL。

---

# 37. 推荐目录与环境

```text
/home/<user>/
│
├── projects/
│   ├── java/
│   ├── typescript/
│   ├── python/
│   └── docker/
│
├── .ssh/
├── .gitconfig
├── .config/
└── .vscode-server/
```

项目统一：

`~/projects`

VS Code：

```bash
code .
```

Git：

`WSL Git`

Runtime：

`WSL Runtime`

Docker：

`WSL Docker CLI`

这会形成比较干净的开发环境边界。

---

# 38. 本课需要掌握

* [ ] 理解 VS Code WSL 的 Client / Server 架构
* [ ] 知道 VS Code 应安装在 Windows
* [ ] 理解 VS Code Server 运行在 WSL
* [ ] 会使用 `code .`
* [ ] 会通过 Command Palette 连接 WSL
* [ ] 理解 Terminal 实际运行在 WSL
* [ ] 理解 Local Extension 与 WSL Extension
* [ ] 理解 Runtime 应安装在 WSL
* [ ] 理解 Git 应与 Repository 保持同一环境
* [ ] 理解 Remote Settings
* [ ] 理解 Debugger 在 WSL 执行应用
* [ ] 知道 `~/.vscode-server`
* [ ] 知道 `server-env-setup` 的用途
* [ ] 能通过 `which` 排查 Toolchain 混用
* [ ] 理解 WSL + Dev Container 的层级关系

---

# 下一课

下一节：

[[WSL2与Git]]

重点：

* Windows Git vs WSL Git
* `.gitconfig`
* SSH Key
* GitHub SSH
* Credential Manager
* Line Ending
* `.gitattributes`
* `core.autocrlf`
* 文件权限
* `core.fileMode`
* 大小写
* Repository 放置位置
* Windows / WSL Git 不混用的原因

之后再进入：

[[WSL2与Docker]]

---

# 相关笔记

* [[WSL2]]
* [[WSL2文件系统]]
* [[WSL2网络]]
* [[WSL2配置]]
* [[WSL2-systemd]]
* [[WSL2与Git]]
* [[WSL2与Docker]]
* [[Dockerfile]]
* [[Docker Compose]]
* [[Dev Containers]]
