---

title: WSL2与Git
tags: [windows, linux, wsl, wsl2, git]
aliases: [WSL2 Git, Git WSL]
---

# WSL2 与 Git

> [!abstract]
> WSL 2 开发推荐保持一条清晰边界：
>
> **WSL Repository → WSL Git → WSL SSH / Credential → Linux Toolchain**
>
> 尽量不要让 Windows Git 与 WSL Git 交替操作同一个仓库。

Microsoft 的 WSL 开发指南也将 Git 作为 WSL 内的独立开发工具链进行配置。

---

# 1. 推荐架构

```text
Windows
│
├── VS Code UI
│
└── WSL 2
    │
    ├── ~/projects
    │   └── Repository
    │
    ├── /usr/bin/git
    ├── ~/.gitconfig
    ├── ~/.ssh
    └── Linux Toolchain
```

仓库推荐位于：

`~/projects`

例如：

```bash
cd ~/projects
git clone git@github.com:example/backend.git
```

而不是长期将 Linux 项目放在 `/mnt/c/...`。

---

# 2. Windows Git 与 WSL Git

Windows Git 和 WSL Git 是两套独立安装。

WSL：

```bash
which git
```

推荐得到：

```text
/usr/bin/git
```

查看版本：

```bash
git --version
```

安装：

```bash
sudo apt update
sudo apt install -y git
```

Windows Git 则通常是 `git.exe`。

因此：

`Git for Windows`

和：

`Git inside WSL`

不要当成同一个 Git。

---

# 3. Git 配置也是分开的

WSL Git 的用户级配置：

`~/.gitconfig`

Windows Git 的用户配置通常位于：

`%UserProfile%\.gitconfig`

Microsoft 特别指出，这两套配置是独立的；如果 WSL Git 调用 Windows 版 Git Credential Manager，GCM 默认读取的是 Git for Windows 的配置，因此 Proxy 等配置可能需要分别处理。

查看 WSL Git 配置：

```bash
git config --global --list
```

更推荐排错时使用：

```bash
git config --list --show-origin --show-scope
```

这样可以看到：

* 配置值
* 配置作用域
* 配置来自哪个文件

Git 支持 `system`、`global`、`local`、`worktree`、命令级等不同配置 Scope。

---

# 4. Git 配置层级

主要可以理解为：

```text
System
  ↓
Global
  ↓
Local
  ↓
Worktree
  ↓
Command
```

常见文件：

| Scope    | 位置                     |
| -------- | ---------------------- |
| System   | `/etc/gitconfig`       |
| Global   | `~/.gitconfig`         |
| Local    | `.git/config`          |
| Worktree | `.git/config.worktree` |

Repository 配置通常可以覆盖 Global 配置。

---

# 5. 基础 Identity

WSL 中：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

查看：

```bash
git config --global user.name
git config --global user.email
```

或者：

```bash
git config --global --edit
```

对应：

```gitconfig
[user]
    name = Your Name
    email = you@example.com
```

---

# 6. Repository 放在哪里？

如果主要使用：

* WSL Git
* Node.js
* Java
* Python
* Docker
* Linux Shell

推荐：

`~/projects/repository`

例如：

```bash
mkdir -p ~/projects
cd ~/projects

git clone git@github.com:example/project.git
```

不要把 Linux Git 仓库默认放：

`/mnt/c/Users/<user>/projects`

原因见：

[[WSL2文件系统]]

核心原则仍然是：

**工具链和工作目录尽量位于同一个文件系统。**

---

# 7. 不要混用两个 Git

例如同一个 Repository：

今天：

```bash
/usr/bin/git status
```

明天从 Windows：

```text
git.exe status
```

虽然很多时候能够工作，但容易引入：

* `.gitconfig` 差异
* SSH 环境差异
* Credential 差异
* Line Ending 差异
* File Mode 差异
* Hooks 环境差异
* PATH 差异

推荐：

```text
WSL Repository
    ↓
WSL Git
```

Windows Repository：

```text
Windows Repository
    ↓
Git for Windows
```

---

# 8. SSH 是比较干净的认证方案

对于主要在 WSL 中开发的仓库，可以直接让认证也留在 WSL：

```text
WSL Git
   ↓
OpenSSH
   ↓
~/.ssh
   ↓
GitHub
```

GitHub 官方支持使用 SSH Key 对 Git 操作进行身份认证。

---

# 9. 检查 SSH Key

```bash
ls -la ~/.ssh
```

可能已有：

`id_ed25519`

`id_ed25519.pub`

不要覆盖已有 Key，除非明确知道用途。

---

# 10. 创建 Ed25519 Key

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

默认生成：

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

其中：

`id_ed25519` 是 Private Key。

`id_ed25519.pub` 是 Public Key。

Private Key 不应该上传或提交到任何 Repository。

GitHub 当前官方文档推荐优先生成 Ed25519 Key；不支持 Ed25519 的旧系统才需要考虑 RSA。

---

# 11. Passphrase

生成 Key 时可以给 Private Key 设置 Passphrase。

这样即使：

`id_ed25519`

文件泄漏，也还有一层保护。

之后可以使用：

`ssh-agent`

缓存解密后的 Key，避免每次 Git 操作都输入 Passphrase。GitHub 官方也推荐通过 `ssh-agent` 管理带 Passphrase 的 Key。

---

# 12. ssh-agent

启动：

```bash
eval "$(ssh-agent -s)"
```

加入 Key：

```bash
ssh-add ~/.ssh/id_ed25519
```

查看：

```bash
ssh-add -l
```

如果没有 Identity：

```text
The agent has no identities.
```

重新：

```bash
ssh-add ~/.ssh/id_ed25519
```

---

# 13. 添加 Public Key 到 GitHub

查看：

```bash
cat ~/.ssh/id_ed25519.pub
```

将 Public Key 添加到 GitHub：

`Settings → SSH and GPG keys → New SSH key`

也可以使用 GitHub CLI：

```bash
gh ssh-key add ~/.ssh/id_ed25519.pub
```

GitHub 要求将生成的 Public Key 添加到账户后，才能使用对应 Private Key 进行 SSH Git 认证。

---

# 14. 测试 GitHub SSH

```bash
ssh -T git@github.com
```

首次连接会要求确认 Server Host Key。

验证成功后，GitHub 会返回包含用户名的认证成功信息；GitHub 本身不提供普通 SSH Shell，因此该测试命令的退出行为与普通 SSH Server 不完全相同。

如果出现：

```text
Permission denied (publickey)
```

调试：

```bash
ssh -vT git@github.com
```

需要更多信息：

```bash
ssh -vvT git@github.com
```

---

# 15. Clone

SSH：

```bash
git clone git@github.com:owner/repository.git
```

查看 Remote：

```bash
git remote -v
```

从 HTTPS 改成 SSH：

```bash
git remote set-url origin git@github.com:owner/repository.git
```

---

# 16. `~/.ssh/config`

有多个 Key 时，不要依赖 SSH 猜测。

例如：

```sshconfig
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

这样：

```bash
git clone git@github.com:owner/repo.git
```

会明确使用：

`~/.ssh/id_ed25519`

---

# 17. 多 GitHub 账号

例如：

* Personal
* Work

准备两个 Key：

```text
~/.ssh/id_ed25519_personal
~/.ssh/id_ed25519_work
```

`~/.ssh/config`：

```sshconfig
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
    IdentitiesOnly yes
```

Personal Repository：

```bash
git clone git@github-personal:username/project.git
```

Work Repository：

```bash
git clone git@github-work:company/project.git
```

---

# 18. 多 Identity：`includeIf`

如果同时存在个人和公司项目，可以让 Git 根据 Repository 路径自动加载不同配置。

Git 官方支持通过 `includeIf "gitdir:..."` 根据 `.git` 所在路径条件加载其他配置文件。

例如目录：

```text
~/projects/
├── personal/
└── work/
```

`~/.gitconfig`：

```gitconfig
[includeIf "gitdir:~/projects/personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir:~/projects/work/"]
    path = ~/.gitconfig-work
```

`~/.gitconfig-personal`：

```gitconfig
[user]
    name = Your Name
    email = personal@example.com
```

`~/.gitconfig-work`：

```gitconfig
[user]
    name = Your Name
    email = you@company.com
```

这样不需要每个 Repository 手工修改 `user.email`。

---

# 19. HTTPS 与 Git Credential Manager

如果使用 HTTPS：

```text
https://github.com/owner/repository.git
```

另一种方案是 Git Credential Manager，简称 `GCM`。

Microsoft 当前 WSL 指南支持：

```text
WSL Git
    ↓
Windows Git Credential Manager
    ↓
Windows Credential Store
```

这样 WSL Git 可以利用 Windows 的凭据存储和认证能力。

---

# 20. GCM 与 Git for Windows

Microsoft 当前推荐安装 Git for Windows 来获得 GCM，然后允许 WSL Git 调用 Windows GCM。

典型配置类似：

```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

实际安装路径可能不同。

检查：

```bash
git config --global credential.helper
```

GCM 官方 WSL 文档也使用这种 Windows / WSL Interop 方式。

---

# 21. SSH 还是 GCM？

两种都没问题。

### SSH

```text
Git
↓
OpenSSH
↓
~/.ssh
```

优点：

* Linux 环境边界干净
* Server / CI 场景通用
* 多账号配置灵活
* 不依赖 Windows Credential Store

### HTTPS + GCM

```text
Git
↓
HTTPS
↓
GCM
↓
Windows Credential Store
```

优点：

* OAuth / Browser 登录体验方便
* 可以利用 Windows Credential Manager
* 企业环境可能更方便

如果主要把 WSL 当 Linux 开发环境，SSH 是很自然的方案。

如果希望与 Windows Credential Manager 深度集成，则考虑 GCM。

---

# 22. Line Ending

Windows 常见：

`CRLF`

Linux 常见：

`LF`

对于 WSL Repository，工作目录通常应该保持 `LF`。

Git 官方说明，Repository 中的文本内容通常可以规范化为 `LF`，Working Tree 的具体换行策略则由 `.gitattributes`、`core.autocrlf`、`core.eol` 等控制。

---

# 23. `.gitattributes` 优先于机器习惯

跨平台项目推荐直接在 Repository 中声明规则。

例如：

```gitattributes
* text=auto

*.sh  text eol=lf
*.py  text eol=lf
*.java text eol=lf
*.ts  text eol=lf
*.tsx text eol=lf

*.bat text eol=crlf
*.cmd text eol=crlf

*.png binary
*.jpg binary
*.pdf binary
```

Git 官方也推荐使用 `.gitattributes` 显式声明文本、二进制以及特定文件的 EOL 行为。

---

# 24. `core.autocrlf`

查看：

```bash
git config --global core.autocrlf
```

在 WSL / Linux 环境，一个常见配置是：

```bash
git config --global core.autocrlf input
```

`input` 表示：

* Commit / Add 时可以把 `CRLF` 规范化为 `LF`
* Checkout 时不把 `LF` 转换成 `CRLF`

Git 官方对 `core.autocrlf=input` 的定义就是“不进行输出转换”。

不过项目存在 `.gitattributes` 时，优先让 Repository 自己定义规则。

---

# 25. 推荐策略

跨平台项目：

```text
.gitattributes
↓
项目级统一规则
```

开发机：

```text
core.autocrlf=input
```

作为 Linux / WSL 环境的辅助默认值。

不要让每个开发者仅依赖自己机器上的 Git 设置。

---

# 26. 修复已经混乱的 Line Ending

先完善：

`.gitattributes`

然后可以：

```bash
git add --renormalize .
```

检查：

```bash
git status
git diff --cached
```

确认没有意外修改后再 Commit。

不要在大型 Repository 中直接运行后无脑提交。

---

# 27. File Mode

Linux `ext4` 支持 Executable Bit。

例如：

```bash
chmod +x scripts/deploy.sh
```

Git 可以跟踪这个权限变化。

查看：

```bash
git diff --summary
```

可能看到：

```text
mode change 100644 => 100755
```

Git 的 `core.fileMode` 控制是否关注 Working Tree 中的 Executable Bit。Git 在 `clone` / `init` 时会探测底层文件系统并自动设置这一行为。

---

# 28. 不要全局关闭 `core.fileMode`

如果 Repository 位于 WSL `ext4`：

通常应该让 Git 正常跟踪 Executable Bit。

不要习惯性：

```bash
git config --global core.fileMode false
```

否则可能漏掉：

```text
chmod +x script.sh
```

这样的真实变更。

如果某个特殊 Repository 因底层文件系统导致 Permission Diff，再针对该 Repository：

```bash
git config core.fileMode false
```

---

# 29. Case Sensitivity

WSL `ext4` 默认大小写敏感。

因此：

`UserService.ts`

和：

`userservice.ts`

不是同一个文件。

Git 的 `core.ignoreCase` 会根据初始化或 Clone 时检测到的文件系统行为自动设置；Git 官方不建议随意修改，因为它依赖实际文件系统语义。

所以不要习惯性：

```bash
git config --global core.ignoreCase true
```

或：

```bash
git config --global core.ignoreCase false
```

让 Git 根据 Repository 所在文件系统处理即可。

---

# 30. 只修改大小写

例如：

`userService.ts`

改：

`UserService.ts`

跨平台 Repository 有时可以显式：

```bash
git mv userService.ts temp.ts
git mv temp.ts UserService.ts
```

这样 Git 能明确记录 Rename。

---

# 31. Git Hooks

Hooks：

`.git/hooks`

在 WSL Repository 中由 Linux Git 执行。

因此 Hook：

```bash
#!/usr/bin/env bash
```

运行的是 WSL Bash。

如果项目使用：

* Husky
* lint-staged
* pre-commit
* 自定义 Shell Hook

那么对应：

* Node
* Python
* Bash

也应该存在于 WSL Toolchain。

这又是不要混用 Windows Git 和 WSL Git 的原因之一。

---

# 32. Credential 与 SSH 排错

## 当前 Remote

```bash
git remote -v
```

如果是：

```text
git@github.com:...
```

使用 SSH。

如果是：

```text
https://github.com/...
```

使用 HTTPS Credential。

先确认协议，再排错。

---

# 33. SSH 排错

查看 Key：

```bash
ssh-add -l
```

测试：

```bash
ssh -T git@github.com
```

详细日志：

```bash
ssh -vT git@github.com
```

查看 SSH Config：

```bash
cat ~/.ssh/config
```

确认 Remote：

```bash
git remote -v
```

---

# 34. Git 配置排错

非常推荐：

```bash
git config --list --show-origin --show-scope
```

例如可以发现：

```text
global  file:/home/ema/.gitconfig
local   file:.git/config
```

从而判断最终值到底来自哪里。

---

# 35. 查看某个配置来源

例如：

```bash
git config --show-origin --get user.email
```

查看：

```bash
git config --show-origin --get core.autocrlf
```

这比直接：

```bash
cat ~/.gitconfig
```

更加可靠，因为配置可能来自多个 Scope 或 `includeIf`。

---

# 36. 推荐 WSL Git 配置

一个比较干净的基础配置：

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

git config --global core.autocrlf input
git config --global init.defaultBranch main
```

然后由每个 Repository 的：

`.gitattributes`

定义具体 Line Ending。

如果存在 Personal / Work Identity，再使用：

`includeIf`

拆分。

---

# 37. 推荐项目结构

```text
~/projects/
├── personal/
│   ├── project-a/
│   └── project-b/
│
└── work/
    ├── backend/
    └── frontend/
```

可以配合：

```gitconfig
[includeIf "gitdir:~/projects/personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir:~/projects/work/"]
    path = ~/.gitconfig-work
```

同时 SSH：

```text
~/.ssh/
├── id_ed25519_personal
├── id_ed25519_personal.pub
├── id_ed25519_work
├── id_ed25519_work.pub
└── config
```

这样 Identity 与 Authentication 都比较清晰。

---

# 38. 推荐工作流

进入 WSL：

```bash
cd ~/projects
```

Clone：

```bash
git clone git@github.com:owner/project.git
```

进入：

```bash
cd project
```

确认 Git：

```bash
which git
```

确认 Remote：

```bash
git remote -v
```

确认 Identity：

```bash
git config user.name
git config user.email
```

查看最终配置：

```bash
git config --list --show-origin --show-scope
```

然后：

```bash
code .
```

形成：

```text
WSL File System
      ↓
WSL Git
      ↓
WSL SSH
      ↓
VS Code WSL
      ↓
Linux Toolchain
```

---

# 39. 常见错误

## WSL Repository 使用 Windows Git

Repository 在：

`~/projects/app`

却从 Windows Git 操作。

保持：

`WSL Repo → WSL Git`

更简单。

---

## SSH Key 放在 `/mnt/c`

不推荐：

`/mnt/c/Users/.../.ssh/id_ed25519`

然后让 Linux SSH 直接使用。

更推荐：

`~/.ssh/id_ed25519`

可以保持标准 Linux Permission 和环境边界。

---

## Private Key Permission 错误

检查：

```bash
ls -la ~/.ssh
```

Private Key 通常应该限制权限，例如：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
```

---

## Windows 与 WSL 共用同一个 Global Git Config

两套 Git 可以配置成共享部分配置，但默认并不是同一个环境。

除非明确设计过，否则不要假设：

```text
Windows git config --global
```

会自动影响：

```text
WSL git config --global
```

---

## 全局强制 `core.ignoreCase`

不推荐。

让 Git 根据实际 File System 自动配置。

---

## 全局关闭 `core.fileMode`

对于 WSL `ext4` Repository 通常不合理。

否则可能漏掉 Linux Script 的 Executable Bit 变化。

---

# 40. 核心心智模型

```text
Windows
│
└── VS Code
      │
      ▼
WSL 2
│
├── ~/projects
│      │
│      └── Git Repository
│
├── /usr/bin/git
│
├── ~/.gitconfig
│
├── ~/.ssh
│
└── Linux Toolchain
```

推荐保持：

```text
Repository
+
Git
+
SSH
+
Hooks
+
Runtime
```

都处于 WSL 环境。

---

# 41. 本课需要掌握

* [ ] 理解 Windows Git 与 WSL Git 是两套环境
* [ ] 知道 WSL Global Config 位于 `~/.gitconfig`
* [ ] 会使用 `--show-origin --show-scope`
* [ ] Repository 优先放 `~/projects`
* [ ] 理解为什么不要混用 Windows Git / WSL Git
* [ ] 会生成 Ed25519 SSH Key
* [ ] 理解 Public Key / Private Key
* [ ] 会使用 `ssh-agent`
* [ ] 会使用 `ssh -T git@github.com`
* [ ] 理解 SSH 与 HTTPS + GCM 两种认证模型
* [ ] 理解 `CRLF` / `LF`
* [ ] 理解 `.gitattributes`
* [ ] 理解 `core.autocrlf=input`
* [ ] 理解 `core.fileMode`
* [ ] 理解 `core.ignoreCase`
* [ ] 理解 Git Hooks 运行环境
* [ ] 会使用 `includeIf` 管理多 Identity
* [ ] 能配置多个 SSH Account

---

# 下一课

下一节：

[[WSL2与Docker]]

重点：

* Docker Desktop WSL 2 Backend
* Docker Desktop 与 WSL Distribution 的关系
* WSL Integration
* Docker Engine 在哪里运行
* Docker CLI 在哪里运行
* `docker-desktop`
* Linux Container
* Docker Volume 与 WSL VHDX
* Bind Mount
* `~/projects` 与 `/mnt/c` 性能差异
* Docker Compose
* Windows / WSL / Container 三层网络
* Resource Limit
* VS Code + WSL + Docker
* Dev Containers

---

# 相关笔记

* [[WSL2]]
* [[WSL2文件系统]]
* [[WSL2配置]]
* [[WSL2与VS Code]]
* [[WSL2与Docker]]
* [[Git]]
* [[SSH]]
* [[Docker]]
