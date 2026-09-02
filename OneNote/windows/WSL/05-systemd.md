---

title: WSL2-systemd
tags: [windows, linux, wsl, wsl2, systemd]
aliases: [WSL2 systemd, systemd]
---

# WSL2 systemd

> [!abstract]
> `systemd` 是 Linux 的系统与服务管理器，作为 `PID 1` 运行，并负责启动和管理系统中的其他服务。
>
> 在 WSL 2 中启用 systemd 后，可以正常使用 `systemctl`、`journalctl`、`.service`、`.timer` 等标准 Linux 服务管理能力。

---

# 1. WSL 2 中的 systemd

启用 systemd 后，进程层级大致为：

```text
WSL 2
│
└── systemd (PID 1)
    │
    ├── systemd-journald
    ├── systemd-logind
    ├── ssh.service
    ├── postgresql.service
    ├── redis-server.service
    └── WSL init
```

WSL 为支持 systemd 调整了自身架构：`systemd` 成为 `PID 1`，原来的 WSL init 变成 systemd 的子进程，同时继续负责 Windows 与 Linux 之间的互操作。

检查：

```bash
ps -p 1 -o pid,comm,args
```

正常情况下可以看到：

```text
PID COMMAND
1   systemd
```

也可以：

```bash
systemctl status
```

---

# 2. 是否需要手动启用？

通过当前 `wsl --install` 默认安装的 Ubuntu 已默认启用 systemd。其他 Distribution 是否默认启用取决于发行版。

先直接检查：

```bash
systemctl status
```

如果出现 systemd 未运行，再检查：

```bash
cat /etc/wsl.conf
```

配置：

```ini
[boot]
systemd=true
```

然后在 PowerShell：

```powershell
wsl --shutdown
```

重新启动 WSL。Microsoft 要求 WSL `0.67.6+` 才支持这一机制，可通过 `wsl --version` 检查。

---

# 3. systemd 的核心：Unit

systemd 管理的对象统一称为 `Unit`。

常见类型：

| Unit         | 用途                |
| ------------ | ----------------- |
| `.service`   | 后台服务              |
| `.socket`    | Socket Activation |
| `.timer`     | 定时任务              |
| `.mount`     | 文件系统挂载            |
| `.automount` | 自动挂载              |
| `.path`      | 文件路径监听            |
| `.target`    | 一组 Unit 的逻辑集合     |

日常开发最重要的是：

`service`、`timer`、`target`

---

# 4. Service

例如：

`ssh.service`

`docker.service`

`postgresql.service`

`redis-server.service`

本质上都是 systemd 管理的 Service Unit。

查看：

```bash
systemctl list-units --type=service
```

查看所有已安装的 Service Unit：

```bash
systemctl list-unit-files --type=service
```

两者区别：

* `list-units`：当前加载到 systemd 中的 Unit
* `list-unit-files`：磁盘中安装的 Unit File

Microsoft 官方也使用 `systemctl list-unit-files --type=service` 作为 WSL systemd 验证方式之一。

---

# 5. `systemctl status`

查看 Service：

```bash
systemctl status ssh
```

等价于：

```bash
systemctl status ssh.service
```

输出重点关注：

```text
Loaded:
Active:
Main PID:
Process:
```

例如：

```text
Loaded: loaded (...; enabled)
Active: active (running)
Main PID: 1234
```

这里有两个完全不同的状态：

`active`

表示：

> 现在是否正在运行。

`enabled`

表示：

> systemd 启动时是否自动启动这个 Service。

---

# 6. `start` 与 `enable`

这是 systemd 最重要的区别之一。

启动：

```bash
sudo systemctl start nginx
```

只改变：

`当前运行状态`

不会自动设置下次启动。

启用：

```bash
sudo systemctl enable nginx
```

设置：

`下次 systemd 启动时自动启动`

但通常不会立即启动。

同时完成：

```bash
sudo systemctl enable --now nginx
```

等价于：

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

所以：

```text
start
→ 现在运行

enable
→ 下次自动启动

enable --now
→ 两者都做
```

---

# 7. 常用生命周期命令

启动：

```bash
sudo systemctl start nginx
```

停止：

```bash
sudo systemctl stop nginx
```

重启：

```bash
sudo systemctl restart nginx
```

Reload：

```bash
sudo systemctl reload nginx
```

查看：

```bash
systemctl status nginx
```

启用：

```bash
sudo systemctl enable nginx
```

禁用：

```bash
sudo systemctl disable nginx
```

立即启用：

```bash
sudo systemctl enable --now nginx
```

立即禁用并停止：

```bash
sudo systemctl disable --now nginx
```

---

# 8. `restart` 与 `reload`

`restart`：

```bash
sudo systemctl restart nginx
```

通常意味着：

```text
Stop
↓
Start
```

进程会重新创建。

`reload`：

```bash
sudo systemctl reload nginx
```

告诉程序：

> 重新读取配置，但尽可能不停止进程。

前提是对应 Service 本身支持 reload。

例如 Nginx 通常支持：

```bash
sudo systemctl reload nginx
```

但不是所有应用都支持。

---

# 9. `enabled` 与 `active` 是两个维度

可能出现：

```text
enabled + active
enabled + inactive
disabled + active
disabled + inactive
```

例如：

```bash
sudo systemctl start nginx
```

可能得到：

```text
active
disabled
```

因为服务现在运行，但下次 systemd 启动不会自动启动。

检查：

```bash
systemctl is-active nginx
```

```bash
systemctl is-enabled nginx
```

这两个命令在 Shell Script 和自动化检查中很好用。

---

# 10. Unit File 在哪里？

常见目录：

```text
/etc/systemd/system/
/usr/lib/systemd/system/
/lib/systemd/system/
```

发行版安装的软件通常把 Unit 放在：

`/usr/lib/systemd/system`

或：

`/lib/systemd/system`

管理员自己创建的 Unit 推荐放：

`/etc/systemd/system`

因此：

> 自己写 Service 时优先使用 `/etc/systemd/system`。

---

# 11. 查看 Unit File

例如：

```bash
systemctl cat ssh
```

比直接猜文件位置更方便。

查看实际 Fragment：

```bash
systemctl show ssh -p FragmentPath
```

例如：

```text
FragmentPath=/usr/lib/systemd/system/ssh.service
```

---

# 12. Service Unit 基本结构

典型：

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/my-app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

主要分为：

```text
[Unit]
[Service]
[Install]
```

---

# 13. `[Unit]`

描述 Unit 本身以及依赖关系。

例如：

```ini
[Unit]
Description=My Backend Service
After=network.target
```

`Description`：

```text
服务描述
```

`After`：

```text
启动顺序
```

这里：

```ini
After=network.target
```

表示该 Unit 应排在 `network.target` 之后启动。

> [!important]
> `After=` 主要描述顺序，不等同于“强依赖”。

如果需要依赖关系，还会使用：

`Requires=`

`Wants=`

---

# 14. `Requires` 与 `Wants`

例如：

```ini
[Unit]
Requires=postgresql.service
After=postgresql.service
```

表示应用需要 PostgreSQL。

`Requires=` 是较强依赖。

如果 PostgreSQL 无法启动，当前 Unit 通常也不会正常启动。

较弱依赖：

```ini
Wants=redis-server.service
```

意味着：

> 希望 Redis 一起启动，但它失败不一定阻止当前 Unit。

常见理解：

```text
Requires
→ 强依赖

Wants
→ 弱依赖

After
→ 顺序
```

依赖与顺序是不同概念。

---

# 15. `[Service]`

定义进程如何运行：

```ini
[Service]
Type=simple
WorkingDirectory=/home/ema/projects/backend
ExecStart=/usr/bin/python3 app.py
Restart=on-failure
```

最重要的是：

`ExecStart`

例如：

```ini
ExecStart=/usr/bin/java -jar /opt/app/app.jar
```

或者：

```ini
ExecStart=/usr/bin/node /opt/app/server.js
```

systemd 推荐使用明确的可执行文件路径，而不是依赖交互式 Shell 的环境。

---

# 16. `WorkingDirectory`

例如：

```ini
WorkingDirectory=/home/ema/projects/backend
```

相当于程序启动前：

```bash
cd /home/ema/projects/backend
```

适合依赖相对路径的应用。

---

# 17. `User`

系统 Service 默认通常以 `root` 身份执行。

应用服务一般不应该无理由使用 root。

例如：

```ini
[Service]
User=ema
Group=ema
```

实际用户名可以通过：

```bash
whoami
```

确认。

---

# 18. Environment

可以：

```ini
[Service]
Environment=APP_ENV=production
Environment=PORT=8080
```

也可以：

```ini
EnvironmentFile=/etc/my-app/my-app.env
```

例如 `/etc/my-app/my-app.env`：

```dotenv
APP_ENV=production
PORT=8080
DATABASE_HOST=localhost
```

相比把大量配置塞进 Unit File，`EnvironmentFile` 更容易维护。

敏感信息仍应考虑更合理的 Secret 管理方式。

---

# 19. Restart Policy

常见：

```ini
Restart=on-failure
```

可用策略包括：

`no`

`always`

`on-success`

`on-failure`

`on-abnormal`

例如：

```ini
Restart=on-failure
RestartSec=3
```

程序异常退出：

```text
Process Exit
    ↓
等待 3 秒
    ↓
Restart
```

和 Docker Compose 的：

`restart: on-failure`

概念非常接近。

---

# 20. `[Install]`

例如：

```ini
[Install]
WantedBy=multi-user.target
```

它主要影响：

```bash
systemctl enable
```

时 Unit 如何挂接到启动目标。

`multi-user.target` 可以粗略理解为正常的多用户、非图形系统运行状态。

对于普通后台 Service，这是非常常见的目标。

---

# 21. 自定义 Service

假设项目：

`~/projects/demo-api`

为了方便演示，可以让 systemd 管理一个 Python HTTP Server。

创建：

```bash
sudo vim /etc/systemd/system/demo-api.service
```

内容：

```ini
[Unit]
Description=Demo API
After=network.target

[Service]
Type=simple
User=ema
WorkingDirectory=/home/ema/projects/demo-api
ExecStart=/usr/bin/python3 -m http.server 8080
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

将其中的 `ema` 和路径替换成自己的 Linux 用户。

---

# 22. `daemon-reload`

新增或修改 Unit File 后：

```bash
sudo systemctl daemon-reload
```

告诉 systemd：

> 重新读取磁盘上的 Unit 配置。

然后：

```bash
sudo systemctl start demo-api
```

查看：

```bash
systemctl status demo-api
```

测试：

```bash
curl http://localhost:8080
```

---

# 23. 为什么改 Unit 后需要 `daemon-reload`？

systemd 并不会每次执行 `start` 时重新扫描所有 Unit File。

因此：

```text
修改 Unit File
      ↓
daemon-reload
      ↓
restart/start
```

典型工作流：

```bash
sudo vim /etc/systemd/system/demo-api.service

sudo systemctl daemon-reload
sudo systemctl restart demo-api
```

---

# 24. 设置自动启动

```bash
sudo systemctl enable demo-api
```

或者：

```bash
sudo systemctl enable --now demo-api
```

查看：

```bash
systemctl is-enabled demo-api
```

---

# 25. 一个非常重要的 WSL 2 特性

在普通 Linux Server 上：

```text
systemctl enable
```

意味着机器 Boot 时启动服务。

WSL 2 中需要多理解一层：

```text
Windows
↓
WSL Distribution 启动
↓
systemd 启动
↓
enabled Service 启动
```

也就是说 `enable` 是：

> **WSL Distribution / systemd 启动时启动 Service。**

并不简单等价于：

> Windows 开机时永久后台运行。

---

# 26. systemd Service 不会让 WSL 永久存活

这是 WSL 2 与普通长期运行 Linux Server 非常重要的差异。

Microsoft 明确说明：

> systemd Service 不会因为自身存在而让 WSL Instance 永久保持运行。

因此：

```text
systemctl enable nginx
```

不应该被理解成：

```text
Windows 开机
↓
WSL 永远后台运行
↓
Nginx 永远运行
```

WSL 自己仍有独立生命周期。

所以如果目标是真正长期提供 Production Service：

> 不要把个人 Windows + WSL 2 当成 Linux Server 的等价替代。

---

# 27. `wsl --shutdown` 会发生什么？

PowerShell：

```powershell
wsl --shutdown
```

会立即终止所有运行中的 Distribution 和 WSL 2 Utility VM。

因此 WSL 内：

```text
nginx
postgresql
redis
自定义 systemd Service
```

都会停止。

之后重新运行：

```powershell
wsl
```

systemd 再次启动，已经 `enabled` 的服务也会按配置启动。

---

# 28. `journalctl`

systemd 的日志系统是：

`systemd-journald`

查询工具：

`journalctl`

`journalctl` 用于读取 systemd journal 中记录的日志。

查看全部：

```bash
journalctl
```

通常实际排错不会直接这样看，因为内容太多。

---

# 29. 查看某个 Service

```bash
journalctl -u demo-api
```

最近日志：

```bash
journalctl -u demo-api -n 100
```

实时跟踪：

```bash
journalctl -u demo-api -f
```

这和：

```bash
docker compose logs -f api
```

非常类似。

官方 `journalctl` 也支持通过 `-u` 过滤 Unit，并通过 `-f` 持续输出新日志。

---

# 30. 查看当前 Boot

```bash
journalctl -b
```

只查看本次 systemd Boot 的日志。

某个 Service：

```bash
journalctl -u nginx -b
```

排查“WSL 这次启动以后为什么服务失败”时非常实用。

---

# 31. 按时间过滤

例如：

```bash
journalctl --since "10 minutes ago"
```

```bash
journalctl --since today
```

指定 Unit：

```bash
journalctl -u nginx --since "1 hour ago"
```

---

# 32. 按日志级别过滤

例如：

```bash
journalctl -p err
```

查看错误等级以上的日志。

指定 Service：

```bash
journalctl -u nginx -p warning
```

常见级别：

```text
emerg
alert
crit
err
warning
notice
info
debug
```

---

# 33. Service 排错流程

服务启动失败时，不要只反复：

```bash
systemctl restart app
```

推荐顺序：

### 1. 查看状态

```bash
systemctl status app
```

### 2. 查看日志

```bash
journalctl -u app -n 100 --no-pager
```

### 3. 查看 Unit

```bash
systemctl cat app
```

### 4. 检查 Unit 是否存在

```bash
systemctl list-unit-files | grep app
```

### 5. 修改 Unit 后

```bash
sudo systemctl daemon-reload
```

### 6. 再启动

```bash
sudo systemctl restart app
```

---

# 34. Failed State

如果 Service 多次启动失败，可能进入：

`failed`

查看：

```bash
systemctl --failed
```

清除 Failed State：

```bash
sudo systemctl reset-failed app
```

官方 `systemctl` 文档说明，`reset-failed` 除了清除 failed 状态，还会重置 Service 的 Restart Counter 和 Start Rate Limit Counter。

---

# 35. `mask`

比 `disable` 更强的是：

```bash
sudo systemctl mask nginx
```

被 Mask 的 Service 无法正常启动。

恢复：

```bash
sudo systemctl unmask nginx
```

区别：

```text
disable
→ 不自动启动
→ 仍然可以手动 start

mask
→ 禁止启动
```

---

# 36. Target

`Target Unit` 用于组织其他 Unit。

查看：

```bash
systemctl list-units --type=target
```

常见：

`multi-user.target`

`network.target`

`network-online.target`

例如：

```ini
[Install]
WantedBy=multi-user.target
```

本质是在 enable 时建立 Unit 与 Target 之间的关系。

---

# 37. Timer

systemd 可以用 `.timer` 替代很多传统 `cron` 场景。

例如：

`backup.service`

```ini
[Unit]
Description=Backup Project

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-project
```

对应：

`backup.timer`

```ini
[Unit]
Description=Run Backup Daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
```

查看：

```bash
systemctl list-timers
```

---

# 38. `Type=oneshot`

普通长期运行服务：

```ini
Type=simple
```

一次性任务：

```ini
Type=oneshot
```

例如：

```ini
[Service]
Type=oneshot
ExecStart=/usr/local/bin/database-migration
```

非常适合：

* 初始化
* Migration
* Backup
* Maintenance Script

---

# 39. User Service

除了系统级：

```text
/etc/systemd/system/
```

systemd 还支持用户级 Service：

```text
~/.config/systemd/user/
```

例如：

```bash
mkdir -p ~/.config/systemd/user
```

管理时：

```bash
systemctl --user daemon-reload
systemctl --user start my-app
systemctl --user status my-app
```

用户级 Service 不需要 `sudo`。

对于：

* 开发工具
* Agent
* 用户级后台程序
* 不需要 root 权限的任务

通常比系统 Service 更合理。

---

# 40. System Service 与 User Service

| 类型          | System Service        | User Service             |
| ----------- | --------------------- | ------------------------ |
| Unit 路径     | `/etc/systemd/system` | `~/.config/systemd/user` |
| 命令          | `systemctl`           | `systemctl --user`       |
| 默认权限        | 系统级                   | 当前用户                     |
| 修改通常需要 root | ✅                     | ❌                        |
| 适合          | 数据库、SSH、系统服务          | 开发工具、Agent               |

---

# 41. 不要把 Shell 初始化放进 systemd

例如：

`.bashrc`

`.zshrc`

用于：

> Interactive Shell 初始化。

systemd Service 通常不会读取这些文件。

因此不要依赖：

```bash
export JAVA_HOME=...
export PATH=...
```

只写在 `.bashrc`，然后期待 systemd 自动获得。

Service 应明确配置：

```ini
Environment=
EnvironmentFile=
```

或者直接使用绝对路径：

```ini
ExecStart=/usr/bin/java ...
```

---

# 42. systemd 与开发语言

Java：

```ini
ExecStart=/usr/bin/java -jar /opt/app/app.jar
```

Node.js：

```ini
ExecStart=/usr/bin/node /opt/app/server.js
```

Python：

```ini
ExecStart=/home/ema/projects/api/.venv/bin/python /home/ema/projects/api/main.py
```

真正需要注意的不是语言，而是：

* executable 使用绝对路径
* Working Directory
* Environment
* User
* Restart Policy
* Log
* Dependency

---

# 43. systemd 与 Docker Compose

两者有很多相似概念：

| systemd              | Docker Compose           |
| -------------------- | ------------------------ |
| Unit / Service       | Service                  |
| `ExecStart`          | `command` / `ENTRYPOINT` |
| `Environment`        | `environment`            |
| `Restart=`           | `restart:`               |
| `Requires` / `After` | `depends_on`             |
| `journalctl`         | `docker compose logs`    |
| `systemctl start`    | `docker compose up`      |

但它们管理的层级不同：

```text
systemd
↓
Linux Process / Service

Docker Compose
↓
Container / Container Application
```

不要因为概念相似就把两者视为同一种工具。

---

# 44. 常用命令速查

查看状态：

```bash
systemctl status nginx
```

启动：

```bash
sudo systemctl start nginx
```

停止：

```bash
sudo systemctl stop nginx
```

重启：

```bash
sudo systemctl restart nginx
```

Enable：

```bash
sudo systemctl enable nginx
```

立即 Enable：

```bash
sudo systemctl enable --now nginx
```

Disable：

```bash
sudo systemctl disable nginx
```

重新读取 Unit：

```bash
sudo systemctl daemon-reload
```

查看 Unit：

```bash
systemctl cat nginx
```

查看失败服务：

```bash
systemctl --failed
```

查看日志：

```bash
journalctl -u nginx
```

实时日志：

```bash
journalctl -u nginx -f
```

本次启动：

```bash
journalctl -u nginx -b
```

最近 100 行：

```bash
journalctl -u nginx -n 100
```

---

# 45. 核心工作流

创建：

```text
/etc/systemd/system/my-app.service
```

然后：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now my-app
```

检查：

```bash
systemctl status my-app
```

排错：

```bash
journalctl -u my-app -f
```

修改 Unit：

```bash
sudo vim /etc/systemd/system/my-app.service
```

应用：

```bash
sudo systemctl daemon-reload
sudo systemctl restart my-app
```

这是最值得形成肌肉记忆的一套流程。

---

# 46. WSL 2 下需要额外记住

普通 Linux：

```text
Machine Boot
↓
systemd
↓
enabled Services
```

WSL 2：

```text
Windows
↓
WSL Distribution 启动
↓
systemd
↓
enabled Services
```

而且：

> systemd Service 本身不会保证 WSL Instance 永久保持运行。

因此 WSL 2 非常适合学习和开发 Linux Service，但不要自动把它当成长期运行 Production Linux Host。

---

# 47. 本课需要掌握

* [ ] 理解 systemd 是 `PID 1`
* [ ] 知道如何确认 WSL 2 是否运行 systemd
* [ ] 理解 `Unit`
* [ ] 理解 `.service`
* [ ] 理解 `active` 与 `enabled`
* [ ] 理解 `start` 与 `enable`
* [ ] 会使用 `enable --now`
* [ ] 理解 `restart` 与 `reload`
* [ ] 会使用 `systemctl status`
* [ ] 会使用 `systemctl cat`
* [ ] 知道自定义 Unit 应放 `/etc/systemd/system`
* [ ] 理解 `[Unit]`、`[Service]`、`[Install]`
* [ ] 理解 `ExecStart`
* [ ] 理解 `Restart=`
* [ ] 理解 `Requires`、`Wants`、`After`
* [ ] 修改 Unit 后知道执行 `daemon-reload`
* [ ] 会使用 `journalctl -u`
* [ ] 会使用 `journalctl -f`
* [ ] 理解 User Service
* [ ] 理解 WSL 生命周期与 systemd 生命周期不是一回事

---

# 下一课

下一节：

[[WSL2与VS Code]]

重点：

* WSL Extension
* VS Code Client / Server 架构
* `code .`
* Extension 安装位置
* Terminal
* Language Server
* Java / TypeScript / Python Toolchain
* Debugger
* Git
* WSL 文件系统
* Remote Development
* VS Code 配置边界

---

# 相关笔记

* [[WSL2]]
* [[WSL2配置]]
* [[WSL2网络]]
* [[WSL2文件系统]]
* [[WSL2与VS Code]]
* [[WSL2与Docker]]
* [[Linux-systemd]]
* [[Docker Compose]]
