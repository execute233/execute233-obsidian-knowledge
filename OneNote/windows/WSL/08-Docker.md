---

title: WSL2与Docker
tags: [windows, linux, wsl, wsl2, docker]
aliases: [WSL2 Docker, Docker Desktop WSL2]
-------------------------------------------

# WSL2 与 Docker

> [!abstract]
> Windows 上推荐的 Linux Container 开发架构：
>
> **Windows → Docker Desktop → WSL 2 Backend → Linux Containers**
>
> 日常开发则通常：
>
> **VS Code Windows UI → WSL Project → Docker CLI / Compose → Docker Desktop Engine**

---

# 1. 整体架构

当前 Docker Desktop 可以直接使用 `WSL 2` 作为 Linux Container Backend。Docker 官方要求至少使用 WSL `2.1.5`，并建议保持 WSL 为最新版本。

```text
Windows
│
├── VS Code
├── Browser
├── Docker Desktop
│
└── WSL 2
    │
    ├── Ubuntu
    │   ├── ~/projects
    │   ├── Git
    │   ├── Docker CLI
    │   └── docker compose
    │
    └── docker-desktop
        │
        └── Docker Engine
            │
            ├── Images
            ├── Containers
            ├── Networks
            └── Volumes
```

最重要的一点：

`Ubuntu` 和 `docker-desktop` 不是同一个 Distribution。

你的：

* 源代码
* Git
* Shell
* Java / Node.js / Python Toolchain

通常位于自己的 `Ubuntu`。

Docker Desktop Backend 则运行在 Docker Desktop 管理的 WSL 环境中。

---

# 2. 不要在 Ubuntu 里再安装一套 Docker Engine

如果使用 Docker Desktop 的 WSL 2 Backend，Docker 官方明确建议先删除直接安装在 WSL Distribution 中的 Docker Engine / Docker CLI，否则可能发生冲突。

也就是说，不推荐这种结构：

```text
Ubuntu
├── Docker Engine A
│
└── Docker Desktop
    └── Docker Engine B
```

推荐：

```text
Ubuntu
└── Docker CLI
        │
        ▼
Docker Desktop
└── Docker Engine
```

Docker Desktop 的 `WSL Integration` 会让 Ubuntu Terminal 可以直接使用：

```bash
docker
docker compose
```

而不是要求你自己在 Ubuntu 中维护另一套 Docker Daemon。

---

# 3. 开启 WSL 2 Backend

Docker Desktop：

`Settings → General`

启用：

`Use WSL 2 based engine`

在当前支持 WSL 2 的 Docker Desktop 环境中，这个选项可能已经默认开启，甚至不再显示。

然后：

`Settings → Resources → WSL Integration`

启用你的 Distribution，例如：

`Ubuntu`

Docker Desktop 默认会对默认 WSL Distribution 启用 Integration。

---

# 4. 验证环境

PowerShell：

```powershell
wsl --version
wsl -l -v
```

确认 Ubuntu：

```text
NAME      STATE      VERSION
Ubuntu    Running    2
```

进入 Ubuntu：

```powershell
wsl
```

检查：

```bash
docker version
```

```bash
docker info
```

测试：

```bash
docker run --rm hello-world
```

Compose：

```bash
docker compose version
```

Docker Context：

```bash
docker context ls
```

如果这些正常，WSL Integration 基本已经完成。

---

# 5. Docker CLI 和 Docker Engine 不在同一层

执行：

```bash
docker ps
```

时，可以理解为：

```text
Ubuntu
│
└── docker CLI
       │
       │ Docker API
       ▼
Docker Desktop Backend
       │
       ▼
Docker Engine
       │
       ▼
Containers
```

所以在 Ubuntu 中输入 Docker 命令，并不意味着 Docker Engine 本身安装在 Ubuntu。

在默认 Docker Desktop 配置下，Windows Docker CLI 和启用了 WSL Integration 的 Linux CLI 都连接 Docker Desktop Backend，因此通常看到的是同一套 Docker Desktop Containers / Images；如果主动切换 `docker context`，则另当别论。这个结论是由 Docker Desktop 同时向 Windows CLI 和 WSL Integration 暴露其 Backend 推导出的。

---

# 6. 当前 Docker Desktop WSL 架构

很多旧教程会让你执行：

```powershell
wsl -l -v
```

然后寻找：

`docker-desktop-data`

但这已经不能作为现代 Docker Desktop 的通用判断依据。

Docker Desktop 从 `4.36` 开始将 WSL 2 安装迁移到了统一的 single-distribution architecture；当前仍使用 `docker-desktop` 作为 Docker Desktop Backend。

因此不要依赖旧教程中的：

`docker-desktop-data`

判断 Docker 是否安装正确。

更可靠的是：

```bash
docker info
docker version
```

以及 Docker Desktop Dashboard。

---

# 7. 项目必须优先放 WSL 文件系统

Docker 官方明确推荐把需要 Bind Mount 到 Linux Container 的源码放在 Linux 文件系统中。

推荐：

`~/projects/backend`

不推荐：

`/mnt/c/Users/<user>/projects/backend`

例如：

```bash
mkdir -p ~/projects
cd ~/projects

git clone git@github.com:example/backend.git
cd backend

code .
```

---

# 8. 为什么 `/mnt/c` 对 Docker 不理想？

例如：

```yaml
services:
  app:
    build: .
    volumes:
      - .:/app
```

如果项目位于：

`~/projects/app`

数据路径大致为：

```text
WSL ext4
   ↓
Docker
   ↓
Container
```

如果项目位于：

`/mnt/c/projects/app`

则变成：

```text
Windows NTFS
    ↓
WSL 文件系统边界
    ↓
Docker
    ↓
Container
```

Docker 官方指出，Linux 文件系统中的 Bind Mount 性能明显更高，并且 Linux Container 的 `inotify` 文件变化事件在源码位于 Linux 文件系统时工作更可靠。

这会直接影响：

* Vite / Webpack Watch
* TypeScript Watch
* Spring DevTools
* Python Reload
* Node.js Hot Reload
* 大量小文件 Build

---

# 9. Bind Mount 与 Named Volume

在 WSL + Docker Desktop 环境下，这两个概念不要混淆。

### Bind Mount

```yaml
volumes:
  - ./src:/app/src
```

数据属于项目文件。

推荐源路径：

`~/projects/app/src`

---

### Named Volume

```yaml
services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

数据由 Docker Engine 管理。

例如：

```bash
docker volume ls
docker volume inspect postgres-data
```

Named Volume 不应该被理解为：

`~/postgres-data`

它属于 Docker Desktop Backend 的 Docker 数据存储。

---

# 10. 推荐开发结构

```text
~/projects/my-app/
├── compose.yaml
├── Dockerfile
├── .dockerignore
├── pom.xml / package.json / pyproject.toml
└── src/
```

在 WSL：

```bash
cd ~/projects/my-app
docker compose up -d --build
```

查看：

```bash
docker compose ps
```

日志：

```bash
docker compose logs -f
```

进入 Container：

```bash
docker compose exec app sh
```

停止：

```bash
docker compose down
```

整个 Docker 开发流程都可以留在 WSL Terminal 中。Docker 官方推荐的 WSL 开发流程也是 `wsl → project → code .`，并从 Linux Distribution 中使用 Docker。

---

# 11. 三层网络模型

WSL + Docker 最容易混乱的是网络层级。

实际上至少有三层：

```text
Windows
   │
   ▼
WSL 2 Network
   │
   ▼
Docker Network
   │
   ├── api
   ├── redis
   └── postgres
```

所以：

**WSL Network ≠ Docker Network**

---

# 12. Container → Container

Compose：

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"

  redis:
    image: redis:alpine
```

`api` 访问 Redis：

`redis:6379`

不是：

`localhost:6379`

也不是 WSL IP。

这是 Docker Network 层：

```text
api
 │
 │ redis:6379
 ▼
redis
```

---

# 13. Windows → Container

Compose：

```yaml
ports:
  - "8080:8080"
```

Windows Browser：

`http://localhost:8080`

Docker Desktop 会负责 Published Port 到 Container 的转发。

```text
Windows Browser
      │
      │ localhost:8080
      ▼
Docker Desktop
      │
      ▼
Container :8080
```

---

# 14. Container → Windows Host

Container 如果需要访问 Windows Host 中运行的服务，不要硬编码 Host IP。

Docker Desktop 提供：

`host.docker.internal`

例如 Windows 上：

```powershell
python -m http.server 9000
```

Container：

```bash
curl http://host.docker.internal:9000
```

Docker Desktop 会让 `host.docker.internal` 解析到 Host 的内部地址。

另外还有：

`gateway.docker.internal`

表示 Docker VM Gateway。

---

# 15. 网络关系速查

| 来源        | 目标                  | 推荐地址                        |
| --------- | ------------------- | --------------------------- |
| Windows   | Published Container | `localhost:PORT`            |
| Container | Compose Service     | `service-name:PORT`         |
| Container | Windows Host        | `host.docker.internal:PORT` |
| WSL       | Windows             | 见 [[WSL2网络]]                |
| Windows   | WSL Service         | `localhost:PORT`            |

不要把这些网络层混在一起。

---

# 16. Docker 资源实际上受 WSL 2 VM 影响

使用 WSL 2 Backend 时，CPU、Memory 和 Swap 的底层限制由 WSL 2 Utility VM 控制，而不是传统 Docker Desktop VM 的资源滑块。Docker 官方当前设置文档明确要求 WSL 2 模式通过 WSL 配置资源限制。

例如：

`%UserProfile%\.wslconfig`

```ini
[wsl2]
memory=16GB
processors=12
swap=4GB
```

这个限制作用于整个 WSL 2 VM，因此不仅影响 Docker，还会影响 Ubuntu 等其他 WSL Distribution。Microsoft 当前文档说明 `.wslconfig` 是 WSL 2 全局 VM 配置。

详见：

[[WSL2配置]]

---

# 17. Docker Build 后内存为什么没有马上下降？

例如执行：

```bash
docker build .
```

Linux Kernel 可能保留大量 Page Cache。

因此任务结束后，Windows Task Manager 中看到 WSL 占用的内存不一定立即下降。

Docker 官方建议结合 WSL 的 `autoMemoryReclaim` 机制改善这一行为。

当前 Microsoft WSL 文档中，实验配置 `autoMemoryReclaim` 的默认值已列为：

`dropCache`

可选：

* `disabled`
* `gradual`
* `dropCache`

所以新版本 WSL 通常不需要为了 Docker 单独手工添加这一配置。

---

# 18. Resource Saver

Docker Desktop 提供 `Resource Saver`。

但 WSL Backend 下它的行为和 Hyper-V Backend 不一样。

在 WSL 环境中，Resource Saver：

**只暂停 `docker-desktop` 中的 Docker Engine，而不会关闭整个 WSL VM。**

因为所有 WSL Distribution 共用底层 WSL VM，Docker Desktop 无权为了自己直接关闭整个 WSL 环境。

因此：

```text
Resource Saver
↓
减少 Docker CPU 活动

≠

wsl --shutdown
```

如果目标是关闭整个 WSL：

```powershell
wsl --shutdown
```

---

# 19. Docker 数据存在哪里？

当前 Docker Desktop WSL Backend 默认数据目录位于：

`%LOCALAPPDATA%\Docker\wsl`

Docker Desktop 可以通过：

`Settings → Resources → Advanced`

修改数据存储位置。

Docker 的：

* Images
* Container writable layers
* Named Volumes
* Build Cache

都可能持续增加这里的磁盘使用量。

---

# 20. Docker 数据 VHDX

当前 Docker Desktop 的 Docker 数据最终保存在虚拟磁盘中。

官方 Backup 文档给出的 Windows 数据文件为：

`%LOCALAPPDATA%\Docker\wsl\data\docker_data.vhdx`

所以应该区分：

```text
Ubuntu
└── ext4.vhdx
```

和：

```text
Docker Desktop
└── docker_data.vhdx
```

两者不是同一个磁盘。

这点后面在：

[[WSL2磁盘管理]]

详细讨论。

---

# 21. 不要直接手动移动 Docker VHDX

如果希望把 Docker 数据从 `C:` 移到其他磁盘，优先使用：

`Docker Desktop → Settings → Resources → Advanced`

Docker Desktop 当前正式支持移动 WSL 2 Backend 的数据存储位置。

不要直接：

```text
剪切 docker_data.vhdx
↓
粘贴到 D:
```

然后期待 Docker Desktop 自动识别。

---

# 22. Docker 数据备份

Images 可以：

```bash
docker image save -o images.tar image-name
```

恢复：

```bash
docker image load -i images.tar
```

Container 本身通常应该通过：

`Dockerfile + compose.yaml`

重新创建。

Named Volume 数据则需要单独备份。

如果 Docker Desktop 本身无法启动，官方恢复方案才会直接处理：

`docker_data.vhdx`

---

# 23. Docker Desktop + VS Code

推荐组合：

```text
Windows
│
└── VS Code UI
        │
        ▼
WSL Extension
        │
        ▼
Ubuntu
├── ~/projects
├── Git
├── Docker CLI
└── docker compose
        │
        ▼
Docker Desktop
        │
        ▼
Containers
```

Docker 官方明确推荐代码放在 Linux Distribution，而 IDE 仍然运行在 Windows，通过 VS Code WSL Extension 工作。

也就是：

```bash
cd ~/projects/backend
code .
```

---

# 24. Dev Containers

还可以继续增加一层：

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
└── Docker Desktop
      │
      ▼
Dev Container
```

如果已经通过 WSL Extension 打开项目：

`Ctrl + Shift + P`

执行：

`Dev Containers: Reopen in Container`

VS Code 会进一步把开发环境连接到 Container 内部。VS Code 官方支持直接将位于 WSL 文件系统中的项目 Reopen 到 Docker Dev Container。

---

# 25. 为什么 Dev Container 项目更应该放 WSL？

Microsoft 当前 Dev Containers 文档特别强调：

推荐：

`/home/<user>/projects`

不推荐：

`C:\Users\<user>\projects`

因为 Docker 对 Windows 文件系统进行跨 OS File Sharing 会增加 I/O 成本，而 WSL 文件系统能够直接使用 Linux I/O，对 Build 和 File Watch 性能更好。

---

# 26. GPU Container

如果机器有 NVIDIA GPU，Docker Desktop 当前 Windows GPU Container 支持只提供给：

`WSL 2 Backend`

Docker Desktop 使用 WSL 2 的 NVIDIA GPU Paravirtualization，让 Linux Container 可以访问 GPU。

前置条件包括：

* NVIDIA GPU
* 支持 WSL 的新驱动
* 最新 WSL Kernel
* Docker Desktop WSL 2 Backend

更新 WSL：

```powershell
wsl --update
```

这对于 AI / CUDA workload 很有价值。

---

# 27. 推荐开发工作流

PowerShell：

```powershell
wsl
```

进入项目：

```bash
cd ~/projects/backend
```

打开 VS Code：

```bash
code .
```

构建：

```bash
docker compose build
```

启动：

```bash
docker compose up -d
```

检查：

```bash
docker compose ps
```

日志：

```bash
docker compose logs -f
```

开发结束：

```bash
docker compose down
```

形成：

```text
WSL ext4
   │
   ├── Source Code
   ├── Git
   ├── VS Code Server
   └── Docker CLI
           │
           ▼
     Docker Desktop
           │
           ▼
       Containers
```

---

# 28. 常见错误

## 在 Ubuntu 中另外安装 Docker Engine

如果使用 Docker Desktop WSL Integration，不要再维护第二个 Engine。Docker 官方明确建议避免这种安装方式。

---

## 项目放 `/mnt/c`

不推荐：

`/mnt/c/Users/.../project`

尤其涉及：

* Bind Mount
* File Watch
* Hot Reload
* `node_modules`

推荐：

`~/projects/project`

---

## Container 访问 Host 使用 `localhost`

Container 中：

`localhost`

代表 Container 自己。

访问 Windows Host：

`host.docker.internal`

---

## Container 访问其他 Service 使用 Host Port

错误：

`redis:16379`

如果 Compose：

```yaml
ports:
  - "16379:6379"
```

Container 间应该：

`redis:6379`

---

## 把 WSL Network 和 Docker Network 混在一起

`WSL NAT / mirrored`

和：

`Docker bridge network`

属于不同层级。

---

## 根据旧教程寻找 `docker-desktop-data`

当前 Docker Desktop WSL 架构已经发生变化。

不要把这个 Distribution 是否存在当成 Docker 正常与否的判断条件。

---

## 手动移动 Docker VHDX

应该通过 Docker Desktop 的 Data Location 设置进行迁移，而不是直接移动 VHDX 文件。

---

# 29. 排错顺序

Docker Desktop 是否运行：

```bash
docker version
```

如果 Client 有信息，但 Server 连接失败，优先检查 Docker Desktop。

检查 WSL：

```powershell
wsl -l -v
wsl --version
```

检查 Integration：

`Docker Desktop → Settings → Resources → WSL Integration`

检查 Context：

```bash
docker context ls
```

检查 Engine：

```bash
docker info
```

检查 Container：

```bash
docker ps -a
```

Compose：

```bash
docker compose ps
docker compose logs
```

检查磁盘：

```bash
docker system df
```

检查 Build：

```bash
docker build --progress=plain .
```

---

# 30. `docker system df`

Docker 数据不断增长时：

```bash
docker system df
```

查看：

* Images
* Containers
* Local Volumes
* Build Cache

不要一看到磁盘大就直接：

```bash
docker system prune -a --volumes
```

因为这可能删除：

* 未使用 Image
* Build Cache
* Stopped Container
* 未使用 Volume

尤其 Volume 可能包含数据库数据。

---

# 31. 推荐心智模型

```text
Windows
│
├── Browser
├── VS Code UI
├── Docker Desktop
│
└── WSL 2
    │
    ├── Ubuntu
    │   │
    │   ├── ~/projects
    │   ├── Git
    │   ├── Java / Node / Python
    │   ├── VS Code Server
    │   └── Docker CLI
    │
    └── Docker Desktop Backend
        │
        └── Docker Engine
            │
            ├── Images
            ├── Containers
            ├── Docker Networks
            └── Docker Volumes
```

最值得记住的边界：

| 层级             | 负责                                   |
| -------------- | ------------------------------------ |
| Windows        | GUI、Browser、Docker Desktop           |
| Ubuntu WSL     | Source Code、Git、Toolchain、Docker CLI |
| Docker Desktop | Docker Engine                        |
| Container      | Application Runtime                  |
| WSL Network    | Windows ↔ WSL                        |
| Docker Network | Container ↔ Container                |

---

# 32. 本课需要掌握

* [ ] 理解 Docker Desktop WSL 2 Backend 架构
* [ ] 理解 Ubuntu 与 `docker-desktop` 的区别
* [ ] 理解 Docker CLI 与 Docker Engine 的区别
* [ ] 知道为什么不应该额外安装第二套 Docker Engine
* [ ] 会启用 WSL Integration
* [ ] 会使用 `docker info` 验证 Engine
* [ ] 理解当前 Docker Desktop 不应依赖 `docker-desktop-data`
* [ ] 理解为什么项目推荐放 `~/projects`
* [ ] 理解 WSL Bind Mount 性能
* [ ] 理解 `inotify` 与 Linux 文件系统的关系
* [ ] 理解 Bind Mount 与 Named Volume 的数据位置差异
* [ ] 理解 Windows / WSL / Docker 三层网络
* [ ] 会使用 `host.docker.internal`
* [ ] 理解 Docker 资源受 WSL VM 配置影响
* [ ] 理解 Resource Saver 与 `wsl --shutdown` 的区别
* [ ] 知道 Docker 数据存储在独立 VHDX 中
* [ ] 理解 VS Code + WSL + Docker 的推荐工作流
* [ ] 理解 Dev Containers 所在层级
* [ ] 知道 WSL 2 Backend 可以支持 NVIDIA GPU Container

---

# 下一课

[[WSL2磁盘管理]]

重点：

* WSL Distribution 的 `ext4.vhdx`
* Docker 的 `docker_data.vhdx`
* Dynamic VHDX
* `df` 与 Windows 磁盘占用为什么不一致
* VHDX 为什么只增长不立即缩小
* Sparse VHD
* 自动磁盘回收
* 磁盘扩容
* WSL Distribution 迁移到其他磁盘
* Docker Data 迁移
* 清理 Docker Build Cache
* 安全释放磁盘空间

之后：

[[WSL2备份与迁移]]

---

# 相关笔记

* [[WSL2]]
* [[WSL2文件系统]]
* [[WSL2网络]]
* [[WSL2配置]]
* [[WSL2与VS Code]]
* [[WSL2与Git]]
* [[WSL2磁盘管理]]
* [[Docker]]
* [[Dockerfile]]
* [[Docker Compose]]
* [[Dev Containers]]
