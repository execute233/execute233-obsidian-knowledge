---
title: Docker Compose
tags: [docker]
aliases: [Docker Compose, Docker多容器编排, Compose]
---

# Docker Compose

> [!abstract]
> Dockerfile 负责描述单个镜像如何构建；Docker Compose 负责描述一组容器如何一起运行。
>
> Compose 用一个 YAML 文件描述整个应用：
>
> * 有哪些服务
> * 使用哪些镜像
> * 哪些服务需要构建
> * 开放哪些端口
> * 使用哪些环境变量
> * 挂载哪些数据卷
> * 容器之间如何通信
> * 服务之间有什么依赖
> * 应用如何整体启动和停止
>
> 一次 `docker compose up` 就能启动整个应用。

---

# 1. Docker Compose 是什么

假设一个 Web 项目由三个组件组成：

```text
Web API
PostgreSQL
Redis
```

不使用 Docker Compose 时需要分别执行：

```bash
docker run ...
docker run ...
docker run ...
```

并自己处理网络、端口、Volume、环境变量、容器依赖、容器名称。项目复杂后非常麻烦。

Docker Compose 把这些配置统一写进 `compose.yaml`，然后只需：

```bash
docker compose up
```

即可启动整个应用。

Dockerfile 与 Compose 的关系：

```text
Dockerfile
    ↓
构建应用 Image

compose.yaml
    ↓
描述 Services
    ↓
创建 Containers / Networks / Volumes
    ↓
组成完整应用
```

---

# 2. 第一个 compose.yaml

例如启动 `Web` 和 `Redis`：

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  redis:
    image: redis:alpine
```

```bash
docker compose up
```

Compose 会创建并启动两个服务。

```bash
docker compose ps
```

查看运行状态。

```bash
docker compose down
```

停止并删除。

---

# 3. Compose 的核心心智模型

```text
Project 一个 Compose 应用整体
│
├── Service 容器配置模板
│   ├── Container
│   └── Container
│
├── Network
│
└── Volume
```

---

# 4. services

Compose 最核心的配置：

```yaml
services:
  web:
    image: nginx

  db:
    image: postgres

  redis:
    image: redis
```

定义了 `web` / `db` / `redis` 三个服务。

---

# 5. image

`image` 表示服务使用什么镜像。

```yaml
services:
  redis:
    image: redis:alpine
```

如果本地没有镜像，Docker 可从 Registry 拉取。建议尽量固定版本。

---

# 6. build

如果应用需要自己的 Dockerfile：

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
```

`context` 表示 Build Context，`dockerfile` 指定使用哪个 Dockerfile。

## build.args

Dockerfile：

```dockerfile
ARG APP_ENV=production
```

Compose：

```yaml
services:
  web:
    build:
      context: .
      args:
        APP_ENV: development
```

相当于：

```bash
docker build \
  --build-arg APP_ENV=development \
  .
```

---

# 7. image 与 build 的区别

直接使用现成镜像：

```yaml
services:
  redis:
    image: redis:alpine
```

使用自己的镜像：

```yaml
services:
  web:
    build: .
```

也可以同时写：

```yaml
services:
  web:
    build: .
    image: my-web:dev
```

初学阶段建议保持简单：

```text
第三方组件 → image
自己的应用 → build
```

---

# 8. ports

`ports` 将宿主机端口映射到容器端口：

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

## 多个端口

```yaml
ports:
  - "8080:80"
  - "8443:443"
```

## 指定宿主机 IP

```yaml
ports:
  - "127.0.0.1:5432:5432"
```

---

# 9. expose

```yaml
services:
  api:
    expose:
      - "8000"
```

描述服务内部使用的容器端口，但不会像 `ports` 那样发布到宿主机。

---

# 10. Docker Compose 网络

即使没有写 `networks:`，Compose 也会创建一个默认网络，所有服务都会加入它。

```yaml
services:
  web:
    image: my-web

  db:
    image: postgres:18

  redis:
    image: redis:alpine
```

默认所有服务都在同一网络，可直接互相通信。

---

# 11. Service Name 就是 DNS Name

假设：

```yaml
services:
  web:
    image: my-web

  db:
    image: postgres:18
```

`web` 访问数据库时，可直接使用 `db` 作为 hostname。

---

# 12. 容器通信不使用 Host Port

```yaml
services:
  db:
    image: postgres:18
    ports:
      - "15432:5432"
```

宿主机访问数据库：`localhost:15432`。

但另一个容器访问数据库应使用：

```text
db:5432
```

而不是 `db:15432`。`15432` 是 Host Port，`5432` 才是容器真正监听的 Container Port。

记忆：

```text
Host → Container
localhost:15432

Container → Container
db:5432
```

---

# 13. 自定义 Network

简单项目默认网络已经够用。复杂项目可主动划分：

```yaml
services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: my-api
    networks:
      - frontend
      - backend

  db:
    image: postgres:18
    networks:
      - backend

networks:
  frontend:
  backend:
```

结构：

```text
            frontend
               │
        ┌──────┴──────┐
        │             │
       web           api
                      │
                      │ backend
                      │
                     db
```

---

# 14. external network

如果网络已在 Compose 外部创建：

```bash
docker network create shared-network
```

```yaml
services:
  web:
    image: nginx
    networks:
      - shared

networks:
  shared:
    external: true
    name: shared-network
```

表示 Compose 不负责创建该网络，而是使用已存在的 `shared-network`。

---

# 15. environment

环境变量可直接写：

```yaml
services:
  web:
    image: my-web
    environment:
      APP_ENV: production
      PORT: "8000"
```

容器中就会存在 `APP_ENV=production` 与 `PORT=8000`。

---

# 16. 环境变量插值

Compose 文件中可使用 `${VAR}`：

```yaml
services:
  web:
    image: my-app:${APP_VERSION}
```

环境中存在 `APP_VERSION=1.0` 时，最终得到 `my-app:1.0`。

默认值：

```yaml
image: my-app:${APP_VERSION:-latest}
```

强制要求变量存在：

```yaml
environment:
  DATABASE_URL: ${DATABASE_URL:?DATABASE_URL is required}
```

---

# 17. .env

项目：

```text
my-app/
├── compose.yaml
└── .env
```

`.env`：

```dotenv
APP_PORT=8000
APP_ENV=development
```

Compose 会自动加载 `.env`，其中变量可在 `compose.yaml` 中用 `${VAR}` 引用。

---

# 18. env_file

把环境变量放进单独文件：

```yaml
services:
  web:
    image: my-web
    env_file:
      - web.env
```

`web.env`：

```dotenv
APP_ENV=production
PORT=8000
```

容器启动时这些变量会被注入。

---

# 19. .env 与 env_file 的区别

| 配置       | 作用范围          | 用途       |
| -------- | ------------- | -------- |
| `.env`   | Compose 文件本身  | `${VAR}` 插值 |
| `env_file` | 容器内部          | 注入到容器进程环境变量 |

简单记忆：

```text
.env      → 控制 Compose 文件本身
env_file  → 传给容器进程
```

---

# 20. 环境变量优先级

从高到低：

```text
1. docker compose run -e / --env

2. shell 环境中已经存在的同名变量

3. environment 字段

4. env_file

5. .env 文件
```

---

# 21. volumes

`volumes` 用于挂载数据。

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

这是 Named Volume，Compose 会自动创建并管理。

---

# 22. docker compose down 与 Volume

`docker compose down` 默认不会删除 Named Volume：

```bash
docker compose down           # 保留 Volume
docker compose down --volumes # 删除 Volume
```

---

# 23. Bind Mount

```yaml
services:
  web:
    image: nginx
    volumes:
      - ./html:/usr/share/nginx/html
```

宿主机 `./html` 直接映射到容器 `/usr/share/nginx/html`，开发期修改宿主机文件即可立即看到效果。

---

# 24. Named Volume 与 Bind Mount

| 类型           | 谁管理     | 适合场景          |
| ------------ | ------ | ------------- |
| Named Volume | Docker | 数据库数据、生产数据持久化 |
| Bind Mount   | 用户     | 开发期代码热更新、配置调试  |

---

# 25. Read Only Mount

```yaml
volumes:
  - ./config:/app/config:ro
```

`:ro` 表示容器内只读。常用于配置文件挂载。

---

# 26. Volume 长语法

```yaml
services:
  db:
    volumes:
      - type: volume
        source: db-data
        target: /var/lib/postgresql/data
      - type: bind
        source: ./init
        target: /docker-entrypoint-initdb.d
        read_only: true

volumes:
  db-data:
```

长语法支持更精细控制，如 bind 来源、读写权限等。

---

# 27. depends_on

`depends_on` 控制启动顺序：

```yaml
services:
  web:
    image: my-web
    depends_on:
      - db

  db:
    image: postgres:18
```

`web` 会在 `db` 之后启动。

---

# 28. depends_on 不代表服务已经 Ready

`depends_on` 只控制容器启动顺序，不等待服务真正可用。例如 PostgreSQL 容器虽然 `Up`，但内部仍在初始化。

`depends_on` 也不传播到其他 Compose 文件中的服务。

---

# 29. healthcheck

为服务添加健康检查：

```yaml
services:
  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
```

这样 Compose 能知道 `db` 是否真正可用。

---

# 30. depends_on + service_healthy

```yaml
services:
  web:
    image: my-web
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
```

现在 `web` 会等到 `db` 健康后才启动。

---

# 31. depends_on condition

支持的 condition：

```text
service_started    # 容器已启动
service_healthy    # 健康检查通过
service_completed_successfully  # 一次性任务成功完成
```

---

# 32. restart

```yaml
services:
  web:
    image: my-web
    restart: always
```

常用值：

| 值                | 行为                  |
| ---------------- | ------------------- |
| `no`             | 默认，不自动重启           |
| `always`         | 总是重启                |
| `on-failure`     | 失败时重启               |
| `unless-stopped` | 手动 stop 时不重启，否则重启 |

---

# 33. command

覆盖镜像默认启动命令：

```yaml
services:
  web:
    image: node:22-slim
    command: ["node", "server.js"]
```

或 Shell Form：

```yaml
command: node server.js
```

---

# 34. entrypoint

覆盖默认入口程序：

```yaml
services:
  web:
    image: my-image
  entrypoint: ["/app/start.sh"]
```

---

# 35. working_dir

设置容器内工作目录：

```yaml
services:
  web:
    image: my-image
    working_dir: /app
```

---

# 36. container_name

指定固定容器名：

```yaml
services:
  web:
    image: nginx
    container_name: my-nginx
```

仅适合单实例场景，因为 Compose 默认命名保证唯一，便于 scale。

---

# 37. Service Scaling

```bash
docker compose up -d --scale web=3
```

启动 3 个 `web` 容器实例。注意固定 `container_name` 不能与 scale 共存。

---

# 38. profiles

`profiles` 让某些服务只在指定 profile 下启动：

```yaml
services:
  web:
    image: my-web

  debug:
    image: my-debug
    profiles: ["debug"]
```

默认 `docker compose up` 不会启动 `debug`：

```bash
docker compose --profile debug up
```

适合区分开发/调试工具。

---

# 39. 多个 Profile

```yaml
services:
  web:
    image: my-web

  debug:
    profiles: ["debug", "dev"]

  tools:
    profiles: ["tools"]
```

可同时激活多个 profile：

```bash
docker compose --profile debug --profile tools up
```

---

# 40. configs

把配置文件作为服务的一部分注入：

```yaml
services:
  web:
    image: my-web
    configs:
      - source: app-config
        target: /etc/app/config.yaml

configs:
  app-config:
    file: ./config/app.yaml
```

---

# 41. secrets

```yaml
services:
  db:
    image: postgres:18
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

容器内 `/run/secrets/db_password` 可读取。

---

# 42. 一个完整的 Compose 网络架构

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - frontend

  api:
    image: my-api
    networks:
      - frontend
      - backend

  worker:
    image: my-worker
    networks:
      - backend

  db:
    image: postgres:18
    networks:
      - backend

networks:
  frontend:
  backend:
```

结构：

```text
            frontend
               │
        ┌──────┴──────┐
        │             │
      nginx          api
                       │
                       │ backend
                  ┌────┴────┐
                  │         │
                worker      db
```

---

# 43. 完整 Compose 示例

Web 应用 + 数据库 + 缓存：

```yaml
services:
  web:
    build: .
    image: my-web:dev
    ports:
      - "8080:8000"
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/app
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:18
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      retries: 5

  cache:
    image: redis:alpine

volumes:
  db-data:
```

---

# 44. 完整示例启动流程

```bash
docker compose up -d
docker compose ps
docker compose logs -f web
docker compose down
```

---

# 45. docker compose up

常用选项：

```bash
docker compose up -d           # 后台运行
docker compose up --build      # 强制重新构建
docker compose up --force-recreate  # 重新创建容器
```

---

# 46. docker compose down

```bash
docker compose down            # 停止并删除容器、网络
docker compose down --volumes  # 同时删除 Volume
docker compose down --remove-orphans  # 删除孤儿容器
```

---

# 47. docker compose stop

```bash
docker compose stop            # 停止但不删除
docker compose stop web        # 只停止 web
```

与 `down` 的区别：

```text
stop  → 停止容器，保留容器对象
down  → 停止并删除容器、网络
```

---

# 48. stop、start、down 的区别

| 命令   | 停止 | 删除容器 | 删除网络 | 删除 Volume |
| ---- | -- | ---- | ---- | -------- |
| stop | ✅  | ❌    | ❌    | ❌        |
| down | ✅  | ✅    | ✅    | ❌（默认）    |

---

# 49. docker compose restart

```bash
docker compose restart
docker compose restart web
```

相当于对服务执行 `stop` + `start`，配置变更不会生效。

---

# 50. docker compose ps

```bash
docker compose ps             # 当前项目
docker compose ps -a          # 包含已停止
```

展示服务状态、端口映射、命令等。

---

# 51. docker compose logs

```bash
docker compose logs -f
docker compose logs --tail 100 web
```

`-f` 跟踪日志，类似 `tail -f`。

---

# 52. docker compose exec

```bash
docker compose exec web sh
docker compose exec db psql -U app
```

在运行中的容器内执行命令。

---

# 53. docker compose exec 与 docker exec

`docker compose exec` 自动找到项目中的容器：

```bash
docker compose exec web sh
```

`docker exec` 需要指定容器名：

```bash
docker exec -it my-web-1 sh
```

Compose 项目中推荐用 `docker compose exec`。

---

# 54. docker compose run

```bash
docker compose run --rm web python manage.py migrate
```

启动一次性命令，`--rm` 运行后自动删除容器。

---

# 55. docker compose build

```bash
docker compose build          # 构建所有有 build 的服务
docker compose build web      # 只构建 web
```

---

# 56. docker compose pull

```bash
docker compose pull
```

拉取所有 `image:` 配置的镜像，不构建。

---

# 57. docker compose config

```bash
docker compose config
```

校验并展示合并后的最终 Compose 配置。调试 Compose 文件时非常有用。

---

# 58. 常用命令速查

```bash
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
docker compose exec web sh
docker compose run --rm web command
docker compose build
docker compose pull
docker compose config
docker compose restart
docker compose stop
docker compose start
```

---

# 59. 多 Compose 文件

Compose 支持多个文件叠加：

```bash
docker compose -f compose.yaml -f compose.override.yaml up
```

主文件：`compose.yaml`，覆盖文件：`compose.override.yaml`。

---

# 60. compose.override.yaml

默认情况下，`docker compose up` 会自动加载 `compose.override.yaml`。

例如把开发期配置放在 `compose.override.yaml`：

```yaml
services:
  web:
    volumes:
      - ./src:/app/src
```

正式环境只使用 `compose.yaml`。

---

# 61. 使用 -f 显式指定

```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

通常约定：

```text
compose.yaml        基础配置
compose.override.yaml  开发期覆盖
compose.prod.yaml   生产环境覆盖
```

---

# 62. 查看合并结果

```bash
docker compose config
```

会显示所有 Compose 文件合并并展开变量后的最终配置，便于排查问题。

---

# 63. include

Compose v2.20+ 支持 `include`：

```yaml
include:
  - ./db/compose.yaml
  - ./cache/compose.yaml

services:
  web:
    image: my-web
```

把多个子 Compose 文件合并到当前项目。

---

# 64. Compose Watch

`watch` 在开发期监听宿主机文件变化并自动更新容器：

```yaml
services:
  web:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: ./package.json
```

启动：

```bash
docker compose watch
```

---

# 65. Watch Action

常用 Action：

```text
sync     把宿主机文件同步到容器
rebuild  触发镜像重新构建
restart  重启容器
```

---

# 66. YAML Anchor

YAML 支持 Anchor 和 Alias，适合在 Compose 中复用配置块：

```yaml
x-common-env: &common-env
  LOG_LEVEL: info
  TZ: Asia/Shanghai

services:
  web:
    environment:
      <<: *common-env

  worker:
    environment:
      <<: *common-env
```

---

# 67. x- Extension

以 `x-` 开头的顶层 key 会被 Compose 忽略，可用于自定义扩展：

```yaml
x-defaults: &defaults
  restart: unless-stopped

services:
  web:
    <<: *defaults
    image: my-web
```

---

# 68. 开发环境常见 Compose

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8000"
    volumes:
      - ./src:/app/src
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      retries: 5

volumes:
  db-data:
```

---

# 69. Compose 最佳实践

```text
用 Named Volume 保存数据库数据
避免把数据库数据放 Bind Mount
depends_on 配合 healthcheck 使用
用 .env.example 提供变量模板
不用固定 container_name 才能 scale
Compose 文件保持最小，扩展用 override
敏感数据使用 secrets 而非 environment
```

---

# 70. 常见错误

## 服务名写错

```yaml
DATABASE_URL: postgres://app:secret@postgres:5432/app
```

应为 `db:5432`，不是 `postgres:5432`。

## 容器通信用了 Host Port

```yaml
DATABASE_URL: postgres://app:secret@db:15432/app
```

容器之间应用 `db:5432`。

## 把密码写进 compose.yaml

```yaml
POSTGRES_PASSWORD: mypassword
```

敏感数据应放 `.env` 或 `secrets`。

## depends_on 等于服务 Ready

`depends_on` 不代表服务可用，必须配合 `healthcheck`。

## Volume 误删

`docker compose down --volumes` 会删除 Named Volume，生产环境慎用。

## 镜像不固定版本

```yaml
image: nginx
```

应固定版本：

```yaml
image: nginx:1.27-alpine
```

---

# 71. Dockerfile + Compose 的职责

```text
Dockerfile = 镜像构建
Compose    = 多容器运行
```

应用镜像应通过 `Dockerfile` 构建，第三方组件直接使用 `image:`。

---

# 72. Dockerfile 和 Compose 不要混淆

| 关注点         | Dockerfile       | Compose           |
| ----------- | ---------------- | ----------------- |
| 作用          | 构建镜像            | 编排多容器            |
| 配置格式        | Dockerfile 指令    | YAML              |
| 构建入口        | `docker build`   | `docker compose up` |
| 端口映射        | `EXPOSE`（仅声明）   | `ports`（真实映射）    |
| 环境变量        | `ENV`            | `environment`     |
| 数据持久化       | Volume 在运行时挂载   | `volumes`         |
| 网络          | 一般不显式管理         | 自动创建 Network     |

---

# 73. 一套完整开发流程

```text
编写应用代码
    ↓
写 Dockerfile
    ↓
docker build 构建镜像
    ↓
写 compose.yaml
    ↓
docker compose up 启动应用
    ↓
docker compose logs 调试
    ↓
修改代码
    ↓
docker compose up -d --build 重新构建
```

---

# 74. Compose 调试思路

```text
1. docker compose config  校验配置
2. docker compose ps        查看状态
3. docker compose logs -f   查看日志
4. docker compose exec sh   进入容器
5. docker compose restart   重启服务
```

---

# 75. 网络问题排查

```text
1. 进入容器 docker compose exec web sh
2. ping 其他服务名（如 db）
3. nslookup db 检查 DNS
4. curl db:5432 验证端口
5. 检查 docker network inspect <network>
```

---

# 76. Compose 项目推荐目录

```text
my-app/
├── compose.yaml
├── compose.override.yaml
├── .env
├── .env.example
├── Dockerfile
├── .dockerignore
├── app/
└── README.md
```

---

# 77. .env.example

把变量模板放进 `.env.example`，方便团队成员复制：

```dotenv
APP_PORT=8000
APP_ENV=development
DATABASE_URL=postgres://app:secret@db:5432/app
POSTGRES_PASSWORD=changeme
```

注意：`.env.example` 可提交，`.env` 不应提交。

---

# 78. Compose 心智模型

```text
Project
│
├── Service 定义（YAML）
│       │
│       ▼
│   Container
│
├── Network
│
└── Volume
```

---

# 79. Compose 通用模板

```yaml
services:
  app:
    build: .
    image: my-app:dev
    ports:
      - "8080:8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

volumes:
  db-data:
```

---

# 80. Compose 关键配置速查

| 配置                     | 作用       |
| ---------------------- | -------- |
| `services.<name>.image`  | 使用现成镜像   |
| `services.<name>.build`  | 构建镜像     |
| `services.<name>.ports`  | 端口映射     |
| `services.<name>.environment` | 容器环境变量   |
| `services.<name>.env_file` | 注入环境变量文件 |
| `services.<name>.volumes` | 挂载 Volume |
| `services.<name>.networks` | 加入网络     |
| `services.<name>.depends_on` | 启动依赖     |
| `services.<name>.healthcheck` | 健康检查     |
| `services.<name>.profiles` | Profile 分组 |
| `services.<name>.restart` | 重启策略     |
| `volumes`               | 声明 Volume |
| `networks`              | 声明 Network |
| `secrets`               | 声明 Secrets |
| `configs`               | 声明 Configs |
| `include`               | 包含其他 Compose 文件 |

---

# 81. 一句话记住主要配置

```text
image / build    用什么镜像
ports            暴露什么端口
environment      传什么环境变量
volumes          挂什么数据卷
depends_on       依赖谁
networks         加入哪个网络
```

---

# 82. 一句话记住 Compose 网络

```text
Service 名就是 DNS 主机名
容器之间用 服务名:容器端口 互相访问
```

---

# 83. 学习检查清单

* [ ] 能写 `compose.yaml` 启动多容器应用
* [ ] 能用 `image` 和 `build` 配置镜像
* [ ] 能用 `ports` 做端口映射
* [ ] 知道容器之间使用 Service Name 作为 DNS
* [ ] 能用 `volumes` 持久化数据
* [ ] 能用 `depends_on` + `healthcheck` 控制启动顺序
* [ ] 能用 `.env` + `${VAR}` 做变量插值
* [ ] 能用 `profiles` 区分可选服务
* [ ] 能用 `docker compose up / down / logs / exec / ps` 日常操作
* [ ] 能用 `compose.override.yaml` 区分开发与生产

---

# 84. 推荐学习路线

```text
1. 一个简单 Web + DB compose.yaml

2. 加入 volumes / networks

3. 加入 healthcheck + depends_on

4. 区分 .env / env_file

5. 引入 profiles / secrets

6. 拆分多 Compose 文件
```

---

# 85. 与 Docker 知识体系的关系

```text
Dockerfile
    ↓ 构建
Image
    ↓ docker compose
Container
    ↓ compose 编排
Project
```

Compose 把 Dockerfile 产出的镜像组织成完整的可运行系统。

---

# 86. 相关笔记

* [[Docker]]
* [[dockerfile]]
* [[docker-build-context]]
* [[docker-multi-stage-build]]
* [[docker-network]]
* [[docker-volume]]
* [[docker-secret]]

---

# 总结

Docker Compose 用一个 YAML 文件描述完整应用，是本地开发和小规模部署的核心工具。掌握 `services` / `image` / `build` / `ports` / `volumes` / `networks` / `depends_on` / `healthcheck` / `environment` 之后，配合 Dockerfile 就足以搭建典型的多容器应用。