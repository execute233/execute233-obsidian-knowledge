---

title: Docker Compose
tags: [docker]
aliases: [Docker Compose, Docker多容器编排, Compose]
---

# Docker Compose

> [!abstract] 一句话理解
> **Dockerfile 负责描述“一个镜像怎么构建”，Docker Compose 负责描述“一组容器怎么一起运行”。**
>
> Docker Compose 使用一个 YAML 文件描述整个应用，包括：
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

---

# 1. Docker Compose 是什么？

假设一个 Web 项目由三个组件组成：

```text
Web API
PostgreSQL
Redis
```

如果不使用 Docker Compose，需要分别执行：

```bash
docker run ...
docker run ...
docker run ...
```

还需要自己处理：

```text
网络
端口
Volume
环境变量
容器依赖
容器名称
```

项目复杂以后会非常麻烦。

Docker Compose 可以把这些配置统一写进：

```text
compose.yaml
```

然后只需要：

```bash
docker compose up
```

就可以启动整个应用。

---

## Dockerfile 与 Docker Compose

Dockerfile：

```text
描述一个镜像如何构建
```

Docker Compose：

```text
描述多个服务如何组合运行
```

整体关系：

```text
Dockerfile
    ↓
docker build
    ↓
Image
    ↓
    ├──────────────┐
    │              │
    ▼              ▼
Container       Container
    │              │
    └──────┬───────┘
           │
     Docker Compose
           │
           ▼
     整个应用系统
```

更加准确地说：

```text
Dockerfile
    ↓
构建应用 Image

compose.yaml
    ↓
描述 Services
    ↓
创建 Containers
    ↓
创建 Networks
    ↓
创建 Volumes
    ↓
组成完整应用
```

---

# 3. 第一个 compose.yaml

例如启动：

```text
Web
Redis
```

可以写：

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  redis:
    image: redis:alpine
```

然后：

```bash
docker compose up
```

Compose 会创建并启动两个服务。

查看运行状态：

```bash
docker compose ps
```

停止并删除：

```bash
docker compose down
```

---

# 4. Compose 的核心心智模型

Compose 最重要的概念是：

```text
Project 一个 Compose 应用整体
│
├── Service 某类容器应该如何运行的配置模板
│   ├── Container
│   └── Container
│
├── Service 某类容器应该如何运行的配置模板
│   └── Container
│
├── Network
│
└── Volume
```

---

# 7. services

Compose 最核心的配置：

```yaml
services:
```

例如：

```yaml
services:
  web:
    image: nginx

  db:
    image: postgres

  redis:
    image: redis
```

定义了：

```text
web
db
redis
```

三个服务。

---

# 8. image

`image` 表示服务使用什么镜像。

例如：

```yaml
services:
  redis:
    image: redis:alpine
```

如果本地没有镜像，Docker 可以从 Registry 拉取。
不过要尽量指定脚本

---

# 9. build

如果应用不是直接使用现成镜像，而是需要自己的：

```text
Dockerfile
```

就可以使用：

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
```

其中：

```text
context
```

表示：

```text
Docker Build Context
```

而：

```text
dockerfile
```

表示使用哪个 Dockerfile。

---

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

# 10. image 与 build 的区别

直接使用别人构建好的镜像：

```yaml
services:
  redis:
    image: redis:alpine
```

自己的镜像：

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

这类配置还会受到 `pull_policy` 等构建/拉取策略影响。

初学阶段可以先保持简单：

```text
第三方组件 → image

自己的应用 → build
```

---

# 11. ports

`ports` 用来将宿主机端口映射到容器端口

例如：

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

---

## 指定宿主机 IP

```yaml
ports:
  - "127.0.0.1:5432:5432"
```

---

# 13. expose

```yaml
services:
  api:
    expose:
      - "8000"
```

它描述服务内部使用的容器端口，但不会像：

```yaml
ports:
```

一样发布到宿主机。

---

# 14. Docker Compose 网络

Compose 网络是非常重要的知识点。

假设：

```yaml
services:
  web:
    image: my-web

  db:
    image: postgres:18

  redis:
    image: redis:alpine
```

即使没有写：

```yaml
networks:
```

Compose 也会创建一个：

```text
默认网络
```

然后：

```text
web
db
redis
```

都会加入这个网络。

---

# 15. Service Name 就是 DNS Name

这是 Compose 最重要的规则之一。

假设：

```yaml
services:
  web:
    image: my-web

  db:
    image: postgres:18
```

那么：

```text
web
```

访问数据库时，可以直接使用：

```text
db
```

作为 hostname。

---

# 17. 容器通信不使用 Host Port

假设：

```yaml
services:
  db:
    image: postgres:18
    ports:
      - "15432:5432"
```

宿主机访问数据库：

```text
localhost:15432
```

但是另外一个容器访问数据库应该使用：

```text
db:5432
```

而不是：

```text
db:15432
```

原因：

```text
15432
```

是 Host Port。

```text
5432
```

才是数据库容器真正监听的 Container Port。

记忆：

```text
Host → Container
localhost:15432

Container → Container
db:5432
```

---

# 18. 自定义 Network

简单项目默认网络已经够用。

复杂项目可以主动划分网络：

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

# 19. external network

如果 Network 已经在 Compose 外部创建：

```bash
docker network create shared-network
```

可以：

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

这表示：

```text
Compose 不负责创建该 Network
```

而是使用已经存在的：

```text
shared-network
```

---

# 20. environment

环境变量可以直接写：

```yaml
services:
  web:
    image: my-web
    environment:
      APP_ENV: production
      PORT: "8000"
```

容器中就会存在：

```text
APP_ENV=production
PORT=8000
```

---

# 21. 环境变量插值

Compose 文件中可以：

```yaml
services:
  web:
    image: my-app:${APP_VERSION}
```

然后环境中存在：

```text
APP_VERSION=1.0
```

最终就会得到：

```text
my-app:1.0
```

---

## 默认值

可以：

```yaml
image: my-app:${APP_VERSION:-latest}
```

## 强制要求变量存在

可以：

```yaml
environment:
  DATABASE_URL: ${DATABASE_URL:?DATABASE_URL is required}
```


---

# 22. .env

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

Compose：

```yaml
services:
  web:
    image: my-app
    ports:
      - "${APP_PORT}:8000"
    environment:
      APP_ENV: ${APP_ENV}
```

Compose 在解析 YAML 时进行变量替换。

---

# 23. .env 与 env_file 的区别

这个地方非常容易混淆。

## .env

主要用于：

```text
Compose 配置变量插值
```

比如：

```yaml
ports:
  - "${APP_PORT}:8000"
```

---

## env_file

表示：

```text
把 .env 中的变量传入 web 容器
```

简单记忆：

```text
.env
↓
Compose 自己读取
↓
用于 ${VAR} 插值

env_file
↓
把环境变量传给 Container
```

注意：

> `.env` 文件里的变量，并不会因为文件叫 `.env` 就全部自动进入容器。

---

# 24. env_file

例如：

```text
app.env
```

内容：

```dotenv
APP_ENV=production
APP_PORT=8000
DATABASE_HOST=db
```

Compose：

```yaml
services:
  web:
    env_file:
      - ./app.env
```

容器中就会出现这些变量，多个 env_file后面覆盖前面的相同变量。

---

# 25. 环境变量优先级

环境变量可能同时来自：

```text
Dockerfile ENV
env_file
environment
宿主机环境变量
.env
docker compose run -e
```

因此发生冲突时必须理解优先级。

对于最终进入容器的环境变量，可以先记住这个常见顺序：

```text
docker compose run -e
        ↓
Compose 中经过插值的 environment / env_file
        ↓
environment
        ↓
env_file
        ↓
Dockerfile ENV
```

实际项目遇到环境变量异常时，建议执行：

```bash
docker compose config
```

观察 Compose 最终解析出来的配置。

还可以查看 Compose 用于插值的环境：

```bash
docker compose config --environment
```

---

# 27. volumes

Container 自己内部的数据并不适合作为永久存储。

例如：

```text
PostgreSQL Container
        ↓
数据库数据
```

如果数据只存在容器自己的 writable layer 中：

```text
Container 删除
        ↓
数据也可能消失
```

因此数据库通常使用：

```text
Volume
```

---

# 28. Named Volume

例如：

```yaml
services:
  db:
    image: postgres:18
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

这里：`postgres-data` 是`Named Volume`挂载到`/var/lib/postgresql/data`

## 结构

```text
Docker Host

postgres-data
     │
     ▼
┌─────────────────────┐
│ PostgreSQL Container│
│                     │
│ /var/lib/postgresql │
│ /data               │
└─────────────────────┘
```

Container 即使重新创建：

```text
postgres-data
```

仍然可以存在。

---

# 29. docker compose down 与 Volume

执行：

```bash
docker compose down
```

通常会删除：

```text
Containers
Compose 创建的 Networks
```

但是 Named Volume 默认保留。

因此：

```bash
docker compose down
docker compose up
```

数据库数据通常仍然存在。

如果执行：

```bash
docker compose down -v
```

则：

```text
-v
```

表示连 Compose 管理的 Volume 一起删除。

> [!danger]
> 对数据库项目使用 `docker compose down -v` 前一定要确认数据是否可以删除。

---

# 30. Bind Mount

除了 Named Volume，还有：

```text
Bind Mount
```

例如：

```yaml
services:
  web:
    volumes:
      - ./src:/app/src
```

表示：

```text
宿主机 ./src
      ↓
容器 /app/src
```

结构：

```text
Host
./src
  │
  │ bind mount
  ▼
Container
/app/src
```

这在开发环境非常常见。

例如修改：

```text
Host ./src/app.py
```

容器立即可以看到修改后的文件。

---

# 31. Named Volume 与 Bind Mount

简单理解：

| 类型           | 常见用途            |
| ------------ | --------------- |
| Named Volume | 数据库、Redis、持久化数据 |
| Bind Mount   | 开发源码、配置文件       |

例如数据库：

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

开发源码：

```yaml
volumes:
  - ./src:/app/src
```

---

# 32. Read Only Mount

如果容器不应该修改宿主机文件：

```yaml
volumes:
  - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

其中：

```text
ro
```

表示：

```text
read only
```

即：

```text
只读
```

---

# 33. Volume 长语法

简单写法：

```yaml
volumes:
  - ./src:/app/src
```

也可以写成长格式：

```yaml
volumes:
  - type: bind
    source: ./src
    target: /app/src
    read_only: true
```

Named Volume：

```yaml
volumes:
  - type: volume
    source: app-data
    target: /app/data

volumes:
  app-data:
```

长语法更详细，适合复杂项目。

---

# 34. depends_on

假设：

```text
Web
 ↓
Database
```

Web 依赖 Database。

可以：

```yaml
services:
  web:
    image: my-web
    depends_on:
      - db

  db:
    image: postgres:18
```

表示：

```text
创建/启动顺序上
db 在 web 之前
```

但是这里有一个非常重要的问题。

---

# 35. depends_on 不代表服务已经 Ready

例如 PostgreSQL：

```text
Container started
```

并不代表：

```text
PostgreSQL 已经完成初始化
并且可以接受连接
```

可能发生：

```text
db Container 启动
       ↓
web Container 启动
       ↓
web 尝试连接数据库
       ↓
PostgreSQL 仍在初始化
       ↓
Connection refused
```

因此：

```yaml
depends_on:
  - db
```

并不足以解决所有启动时序问题。

---

# 36. healthcheck

可以给服务增加健康检查：

```yaml
services:
  db:
    image: postgres:18

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s
```

含义：

```text
interval
↓
多久检查一次

timeout
↓
一次检查最多等待多久

retries
↓
连续失败多少次后认为 unhealthy

start_period
↓
启动初期给予多少准备时间
```

---

# 37. depends_on + service_healthy

然后：

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $${POSTGRES_USER}
      interval: 5s
      timeout: 3s
      retries: 5
```

流程：

```text
启动 db
   ↓
运行 healthcheck
   ↓
db healthy
   ↓
启动 web
```

这比：

```text
sleep 10
```

可靠得多。

---

# 38. depends_on condition

常见 condition：

```text
service_started
service_healthy
service_completed_successfully
```

---

## service_started

```yaml
depends_on:
  redis:
    condition: service_started
```

表示：

```text
依赖服务已经启动
```

---

## service_healthy

```yaml
depends_on:
  db:
    condition: service_healthy
```

表示：

```text
依赖服务的 healthcheck 已经通过
```

---

## service_completed_successfully

适合：

```text
Migration
初始化脚本
一次性任务
```

例如：

```yaml
services:
  migration:
    image: my-app
    command: python manage.py migrate

  web:
    image: my-app
    depends_on:
      migration:
        condition: service_completed_successfully
```

表示：

```text
Migration 成功完成
        ↓
再启动 Web
```

---

# 39. restart

Compose 可以设置 Container Restart Policy。

例如：

```yaml
services:
  web:
    image: my-web
    restart: unless-stopped
```

常见值：

```text
no
always
on-failure
on-failure:3
unless-stopped
```

---

## no

```yaml
restart: "no"
```

容器退出后不自动重启。

---

## always

```yaml
restart: always
```

容器退出后持续尝试重启。

---

## on-failure

```yaml
restart: on-failure
```

程序以错误状态退出时重启。

也可以：

```yaml
restart: on-failure:3
```

限制重试次数。

---

## unless-stopped

```yaml
restart: unless-stopped
```

除非人为停止，否则会尝试保持运行。

对于很多长期运行的服务：

```yaml
restart: unless-stopped
```

是比较常见的配置。

---

# 40. command

Dockerfile 中可能存在：

```dockerfile
CMD ["python", "app.py"]
```

Compose 可以覆盖它：

```yaml
services:
  web:
    build: .
    command: python dev.py
```

相当于：

```text
覆盖 Dockerfile CMD
```

---

## List 形式

也可以：

```yaml
command:
  - python
  - app.py
```

---

# 41. entrypoint

Dockerfile：

```dockerfile
ENTRYPOINT ["python"]
```

Compose 可以：

```yaml
services:
  web:
    entrypoint:
      - python
```

它可以覆盖镜像本身的：

```text
ENTRYPOINT
```

一般项目不需要频繁修改。

---

# 42. working_dir

可以覆盖镜像中的工作目录：

```yaml
services:
  web:
    image: python:3.12-slim
    working_dir: /app
```

类似 Dockerfile：

```dockerfile
WORKDIR /app
```

---

# 43. container_name

可以主动指定容器名：

```yaml
services:
  web:
    image: nginx
    container_name: my-web
```

但很多时候：

```text
不需要手动指定
```

Compose 会自动生成名称。

例如：

```text
myproject-web-1
```

而且指定：

```yaml
container_name:
```

会限制该 service 扩展为多个 container。

因此一般推荐：

```text
使用 service name
```

而不是依赖固定：

```text
container_name
```

---

# 44. Service Scaling

例如有一个 Worker：

```yaml
services:
  worker:
    image: my-worker
```

可以：

```bash
docker compose up -d --scale worker=3
```

得到类似：

```text
worker-1
worker-2
worker-3
```

因此 Compose 中：

```text
Service
```

和：

```text
Container
```

并不是完全相同的概念。

一个 Service 可以运行多个 Container 实例。

---

# 45. profiles

有些服务不希望默认启动。

例如：

```text
Adminer
Debug Tool
数据库管理工具
开发工具
```

可以使用：

```yaml
profiles:
```

例如：

```yaml
services:
  web:
    image: my-web

  db:
    image: postgres:18

  adminer:
    image: adminer
    profiles:
      - debug
```

正常执行：

```bash
docker compose up
```

不会启动：

```text
adminer
```

如果：

```bash
docker compose --profile debug up
```

才会启用：

```text
debug
```

profile。

---

# 46. 多个 Profile

例如：

```yaml
services:
  frontend:
    image: my-frontend
    profiles:
      - frontend

  adminer:
    image: adminer
    profiles:
      - debug

  backend:
    image: my-backend

  db:
    image: postgres:18
```

可以：

```bash
docker compose \
  --profile frontend \
  --profile debug \
  up
```

---

# 47. configs

有一些配置文件：

```text
nginx.conf
application.conf
prometheus.yml
```

并不一定要打进镜像。

Compose 提供：

```yaml
configs:
```

例如：

```yaml
services:
  nginx:
    image: nginx
    configs:
      - source: nginx-config
        target: /etc/nginx/nginx.conf

configs:
  nginx-config:
    file: ./nginx.conf
```

这样：

```text
nginx.conf
```

可以作为配置文件提供给容器。

---

# 48. secrets

密码、Token、API Key 等敏感数据，不推荐直接写：

```yaml
environment:
  API_KEY: abc123
```

Compose 提供：

```yaml
secrets:
```

例如：

```text
secrets/
└── api_key.txt
```

Compose：

```yaml
services:
  web:
    image: my-web
    secrets:
      - api_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
```

容器中可以从：

```text
/run/secrets/api_key
```

读取。

---

## Secret 心智模型

```text
Host
secrets/api_key.txt
        │
        ▼
Docker Compose Secret
        │
        ▼
Container
/run/secrets/api_key
```

相比直接把密码长期写在：

```yaml
environment:
```

中，Secret 更适合敏感信息。

---

# 49. 一个完整的 Compose 网络架构

例如：

```text
                Host
                 │
                 │ :8000
                 ▼
        ┌─────────────────┐
        │       web       │
        │     FastAPI     │
        └────────┬────────┘
                 │
       backend network
          ┌──────┴──────┐
          │             │
          ▼             ▼
    ┌──────────┐   ┌──────────┐
    │ Postgres │   │  Redis   │
    │    db    │   │  redis   │
    └────┬─────┘   └──────────┘
         │
         ▼
 postgres-data
    Volume
```

这里：

```text
Host → web
```

通过：

```text
localhost:8000
```

而：

```text
web → PostgreSQL
```

通过：

```text
db:5432
```

```text
web → Redis
```

通过：

```text
redis:6379
```

---

# 50. 完整 Compose 示例

项目：

```text
my-app/
├── compose.yaml
├── Dockerfile
├── .dockerignore
├── .env
├── requirements.txt
├── app.py
└── secrets/
    └── db_password.txt
```

Compose：

```yaml
name: my-app

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile

    ports:
      - "${APP_PORT:-8000}:8000"

    environment:
      APP_ENV: ${APP_ENV:-development}

      DB_HOST: db
      DB_PORT: "5432"
      DB_NAME: ${POSTGRES_DB:-app}
      DB_USER: ${POSTGRES_USER:-app}

      REDIS_HOST: redis
      REDIS_PORT: "6379"

    depends_on:
      db:
        condition: service_healthy

      redis:
        condition: service_healthy

    secrets:
      - db_password

    networks:
      - backend

    restart: unless-stopped

  db:
    image: postgres:18

    environment:
      POSTGRES_DB: ${POSTGRES_DB:-app}
      POSTGRES_USER: ${POSTGRES_USER:-app}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password

    volumes:
      - postgres-data:/var/lib/postgresql/data

    secrets:
      - db_password

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s

    networks:
      - backend

    restart: unless-stopped

  redis:
    image: redis:alpine

    volumes:
      - redis-data:/data

    healthcheck:
      test:
        - CMD
        - redis-cli
        - ping
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 5s

    networks:
      - backend

    restart: unless-stopped

networks:
  backend:

volumes:
  postgres-data:
  redis-data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

`.env`：

```dotenv
APP_PORT=8000
APP_ENV=development

POSTGRES_DB=app
POSTGRES_USER=app
```

秘密密码放：

```text
secrets/db_password.txt
```

例如：

```text
your-password
```

并确保：

```text
secrets/
```

不要提交到 Git。

`.gitignore`：

```gitignore
.env
secrets/
```

---

# 51. 完整示例启动流程

首先检查 Compose：

```bash
docker compose config
```

如果没有问题：

```bash
docker compose up
```

后台启动：

```bash
docker compose up -d
```

重新构建并启动：

```bash
docker compose up -d --build
```

查看：

```bash
docker compose ps
```

---

# 52. docker compose up

最核心的命令：

```bash
docker compose up
```

作用可以理解为：

```text
读取 compose.yaml
      ↓
构建需要构建的 Image
      ↓
创建 Network
      ↓
创建 Volume
      ↓
创建 Container
      ↓
启动 Service
```

---

## 后台运行

```bash
docker compose up -d
```

其中：

```text
-d
```

代表：

```text
detached
```

即后台运行。

---

## 强制构建

```bash
docker compose up --build
```

常用：

```bash
docker compose up -d --build
```

---

# 53. docker compose down

停止并删除 Compose 应用：

```bash
docker compose down
```

一般会删除：

```text
Containers
Compose Networks
```

但默认不会删除 Named Volumes。

---

## 删除 Volume

```bash
docker compose down -v
```

注意：

```text
数据库数据可能会一起被删除
```

---

# 54. docker compose stop

只停止容器：

```bash
docker compose stop
```

不会像：

```bash
docker compose down
```

那样删除这些 Container。

重新启动：

```bash
docker compose start
```

---

# 55. stop、start、down 的区别

```text
docker compose stop
↓
停止 Container
但 Container 仍然存在

docker compose start
↓
重新启动已有 Container

docker compose down
↓
停止并删除 Compose 创建的 Container
以及相关 Network
```

---

# 56. docker compose restart

重新启动：

```bash
docker compose restart
```

单独重启：

```bash
docker compose restart web
```

但是要注意：

> 如果你修改了 Compose 文件中的环境变量、Volume、Port 等配置，仅执行 `restart` 并不会重新创建容器。

这时通常应该：

```bash
docker compose up -d
```

让 Compose 根据新配置重新创建需要变化的 Container。

---

# 57. docker compose ps

查看 Compose Service：

```bash
docker compose ps
```

查看全部：

```bash
docker compose ps -a
```

---

# 58. docker compose logs

查看所有 Service 日志：

```bash
docker compose logs
```

持续跟踪：

```bash
docker compose logs -f
```

只查看：

```text
web
```

```bash
docker compose logs web
```

实时：

```bash
docker compose logs -f web
```

---

# 59. docker compose exec

进入正在运行的 Container：

```bash
docker compose exec web sh
```

如果有 Bash：

```bash
docker compose exec web bash
```

进入数据库：

```bash
docker compose exec db bash
```

执行单条命令：

```bash
docker compose exec web env
```

---

# 60. docker compose exec 与 docker exec

普通 Docker：

```bash
docker exec -it my-app-web-1 sh
```

Compose：

```bash
docker compose exec web sh
```

Compose 更推荐使用：

```text
Service Name
```

不需要记：

```text
Container Name
```

所以：

```bash
docker compose exec web sh
```

通常更加方便。

---

# 61. docker compose run

执行一次性任务：

```bash
docker compose run web python manage.py migrate
```

例如：

```bash
docker compose run --rm web pytest
```

其中：

```text
--rm
```

表示命令结束后删除这个临时 Container。

非常适合：

```text
数据库 Migration
测试
CLI 工具
一次性脚本
```

需要注意：

```text
docker compose run
```

默认不会像正常 service 一样自动发布 `ports` 中声明的端口。

如果确实需要 service ports，可以了解：

```text
--service-ports
```

---

# 62. docker compose build

只构建：

```bash
docker compose build
```

只构建某个 Service：

```bash
docker compose build web
```

不使用缓存：

```bash
docker compose build --no-cache web
```

---

# 63. docker compose pull

拉取 Compose 中需要的镜像：

```bash
docker compose pull
```

例如：

```yaml
services:
  db:
    image: postgres:18

  redis:
    image: redis:alpine
```

执行：

```bash
docker compose pull
```

可以提前拉取这些镜像。

---

# 64. docker compose config

这是一个非常重要的调试命令：

```bash
docker compose config
```

它会：

```text
读取 Compose 文件
        ↓
处理环境变量
        ↓
合并多个 Compose 文件
        ↓
展开部分简写
        ↓
输出最终配置
```

当你遇到：

```text
.env 为什么没生效？
变量为什么不对？
override 到底覆盖成什么了？
YAML 是不是写错了？
```

优先执行：

```bash
docker compose config
```

---

# 65. 常用命令速查

| 命令                                | 作用          |
| --------------------------------- | ----------- |
| `docker compose up`               | 创建并启动应用     |
| `docker compose up -d`            | 后台启动        |
| `docker compose up -d --build`    | 重新构建并后台启动   |
| `docker compose down`             | 停止并删除应用资源   |
| `docker compose down -v`          | 同时删除 Volume |
| `docker compose stop`             | 停止服务        |
| `docker compose start`            | 启动已经存在的服务   |
| `docker compose restart`          | 重启服务        |
| `docker compose ps`               | 查看服务状态      |
| `docker compose logs`             | 查看日志        |
| `docker compose logs -f`          | 实时查看日志      |
| `docker compose exec web sh`      | 进入运行中的服务    |
| `docker compose run --rm web ...` | 执行一次性任务     |
| `docker compose build`            | 构建镜像        |
| `docker compose pull`             | 拉取镜像        |
| `docker compose config`           | 查看最终解析配置    |

---

# 66. 多 Compose 文件

真实项目通常存在：

```text
开发环境
测试环境
生产环境
```

可以使用多个 Compose 文件。

例如：

```text
compose.yaml
compose.override.yaml
compose.prod.yaml
```

---

# 67. compose.override.yaml

Docker Compose 默认可以把：

```text
compose.yaml
```

和：

```text
compose.override.yaml
```

组合起来。

例如：

`compose.yaml`：

```yaml
services:
  web:
    image: my-app

  db:
    image: postgres:18
```

开发环境：

`compose.override.yaml`：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
```

执行：

```bash
docker compose up
```

Compose 会组合：

```text
compose.yaml
+
compose.override.yaml
```

---

# 68. 使用 -f

例如：

```text
compose.yaml
compose.prod.yaml
```

执行：

```bash
docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  up -d
```

Compose 按顺序合并。

简单理解：

```text
前面的文件
     ↓
基础配置

后面的文件
     ↓
覆盖 / 补充前面的配置
```

---

# 69. 查看合并结果

一定要善用：

```bash
docker compose \
  -f compose.yaml \
  -f compose.prod.yaml \
  config
```

不要仅凭肉眼猜：

```text
最终到底是什么配置
```

让 Compose 自己告诉你。

---

# 70. include

大型项目可能出现：

```text
compose.yaml
infra.yaml
observability.yaml
ai-services.yaml
```

现代 Compose 支持：

```yaml
include:
```

例如：

```yaml
include:
  - path: ./infra.yaml

services:
  web:
    build: .
```

`infra.yaml`：

```yaml
services:
  redis:
    image: redis:alpine

  db:
    image: postgres:18

volumes:
  postgres-data:
```

这样可以把：

```text
业务服务
基础设施
监控系统
```

拆成不同 Compose 文件。

---

# 71. Compose Watch

开发环境中，如果代码改变：

```text
修改源码
   ↓
重新 build
   ↓
重新创建 container
```

每次手动执行会很麻烦。

现代 Compose 提供：

```text
Compose Watch
```

例如：

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
          path: ./requirements.txt
```

然后：

```bash
docker compose up --watch
```

---

# 72. Watch Action

常见：

```text
sync
sync+restart
rebuild
restart
```

---

## sync

```yaml
- action: sync
  path: ./src
  target: /app/src
```

代码变化：

```text
Host
./src
 ↓
同步
 ↓
Container
/app/src
```

---

## rebuild

```yaml
- action: rebuild
  path: ./requirements.txt
```

当：

```text
requirements.txt
```

变化时重新：

```text
docker build
```

非常合理，因为新增 Python 依赖通常需要重新构建 Image。

---

## sync + rebuild

典型开发思路：

```yaml
develop:
  watch:
    - action: sync
      path: ./src
      target: /app/src

    - action: rebuild
      path: ./requirements.txt
```

含义：

```text
Python 源码变化
↓
直接同步

requirements.txt 变化
↓
重新构建 Image
```

---

# 73. YAML Anchor

当多个 Service 有重复配置：

```yaml
services:
  api:
    environment:
      APP_ENV: production
      TZ: Asia/Shanghai

  worker:
    environment:
      APP_ENV: production
      TZ: Asia/Shanghai
```

可以使用 YAML Anchor。

例如：

```yaml
x-common-env: &common-env
  APP_ENV: production
  TZ: Asia/Shanghai

services:
  api:
    image: my-api
    environment:
      <<: *common-env

  worker:
    image: my-worker
    environment:
      <<: *common-env
```

其中：

```text
&common-env
```

定义 Anchor。

```text
*common-env
```

引用 Anchor。

```text
<<
```

合并 Mapping。

---

# 74. x- Extension

Compose 允许使用：

```text
x-
```

开头的扩展字段组织可复用配置。

例如：

```yaml
x-common: &common
  restart: unless-stopped

services:
  api:
    <<: *common
    image: my-api

  worker:
    <<: *common
    image: my-worker
```

对于大型 Compose 文件，可以减少重复配置。

初学阶段不用急着大量使用。

---

# 75. 开发环境常见 Compose

例如：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"

    volumes:
      - ./src:/app/src

    environment:
      APP_ENV: development
      DB_HOST: db

    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:18

    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: development-only-password

    volumes:
      - postgres-data:/var/lib/postgresql/data

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $${POSTGRES_USER}
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  postgres-data:
```

开发时：

```bash
docker compose up -d --build
```

查看日志：

```bash
docker compose logs -f web
```

进入：

```bash
docker compose exec web sh
```

关闭：

```bash
docker compose down
```

---

# 76. Compose 最佳实践

## 不写 version

新项目：

```yaml
services:
```

即可。

不要继续照搬旧教程：

```yaml
version: "3.8"
```

---

## 使用 compose.yaml

推荐：

```text
compose.yaml
```

让项目命名保持统一。

---

## 使用 docker compose

使用：

```bash
docker compose up
```

而不是旧的：

```bash
docker-compose up
```

---

## 服务之间使用 Service Name

正确：

```text
db:5432
redis:6379
api:8000
```

不要依赖：

```text
Container IP
```

---

## 不要把 Container 间通信写成 localhost

错误：

```text
DATABASE_HOST=localhost
```

正确：

```text
DATABASE_HOST=db
```

---

## 不必要的端口不要发布

例如数据库仅供 Backend 使用：

```yaml
db:
  image: postgres:18
```

不一定需要：

```yaml
ports:
  - "5432:5432"
```

因为 Backend 可以：

```text
db:5432
```

直接访问。

这样数据库也不会直接暴露给 Host 网络。

---

## 必须发布时考虑绑定 127.0.0.1

开发数据库：

```yaml
ports:
  - "127.0.0.1:5432:5432"
```

比直接：

```yaml
ports:
  - "5432:5432"
```

更明确地限制为本机访问。

---

## 数据库使用 Named Volume

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data
```

不要把重要数据只留在 Container writable layer 中。

---

## 开发源码使用 Bind Mount 或 Compose Watch

Bind Mount：

```yaml
volumes:
  - ./src:/app/src
```

或者：

```yaml
develop:
  watch:
    - action: sync
      path: ./src
      target: /app/src
```

---

## 使用 healthcheck

不要只依赖：

```yaml
depends_on:
  - db
```

数据库类服务更推荐：

```yaml
depends_on:
  db:
    condition: service_healthy
```

配合：

```yaml
healthcheck:
```

---

## 不要用 sleep 猜服务什么时候准备完成

例如：

```bash
sleep 10
```

只能表示：

```text
等十秒
```

不能证明：

```text
数据库已经 Ready
```

优先使用：

```text
healthcheck
```

---

## 敏感数据不要直接写在 Compose 中

避免：

```yaml
environment:
  DATABASE_PASSWORD: my-super-password
  API_KEY: abc123
```

优先考虑：

```text
Secrets
Secret Manager
运行环境注入
```

---

## 修改配置后不要只 restart

如果修改：

```text
environment
ports
volumes
image
```

只执行：

```bash
docker compose restart
```

可能不会应用新的 Container 配置。

通常使用：

```bash
docker compose up -d
```

让 Compose 根据新的配置进行 reconcile。

---

## 经常使用 docker compose config

尤其是在：

```text
环境变量很多
多个 Compose 文件
Profile
Override
Include
```

的项目中。

执行：

```bash
docker compose config
```

可以减少大量排查时间。

---

# 77. 常见错误

## 错误 1：仍然写 version

旧：

```yaml
version: "3.8"

services:
  web:
    image: nginx
```

现代新文件直接：

```yaml
services:
  web:
    image: nginx
```

---

## 错误 2：使用 docker-compose

旧教程：

```bash
docker-compose up
```

现在学习：

```bash
docker compose up
```

---

## 错误 3：写错端口方向

看到：

```yaml
ports:
  - "8080:80"
```

正确理解：

```text
Host 8080
   ↓
Container 80
```

---

## 错误 4：Container 使用 localhost 找其他 Service

错误：

```text
DATABASE_URL=postgres://user:pass@localhost:5432/app
```

正确：

```text
DATABASE_URL=postgres://user:pass@db:5432/app
```

---

## 错误 5：使用容器 IP

错误：

```text
redis://172.19.0.3:6379
```

正确：

```text
redis://redis:6379
```

---

## 错误 6：数据库没有 Volume

```yaml
db:
  image: postgres:18
```

如果需要长期保留数据，应该考虑：

```yaml
db:
  image: postgres:18
  volumes:
    - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

---

## 错误 7：认为 depends_on 等于 Ready

错误理解：

```text
db started
=
database ready
```

实际：

```text
Container started
≠
Application ready
```

应该使用：

```text
healthcheck
+
condition: service_healthy
```

---

## 错误 8：误删 Volume

执行：

```bash
docker compose down -v
```

然后发现：

```text
数据库没了
```

因为：

```text
-v
```

会删除 Compose 管理的 Volume。

---

## 错误 9：以为 .env 自动全部进入 Container

`.env`：

```dotenv
PASSWORD=123456
```

不代表 Container 一定存在：

```text
PASSWORD
```

需要：

```yaml
environment:
  PASSWORD: ${PASSWORD}
```

或者：

```yaml
env_file:
  - .env
```

---

## 错误 10：为所有 Service 设置 container_name

例如：

```yaml
container_name: web
```

经常没有必要。

Compose 自己管理命名更加灵活，而且固定 `container_name` 会影响 Service Scaling。

---

# 78. Dockerfile + Compose 的职责

这是非常重要的边界。

Dockerfile：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

负责：

```text
Python 环境
安装依赖
复制代码
应用默认启动命令
```

Compose：

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db

  db:
    image: postgres:18
```

负责：

```text
运行几个 Container
Container 如何连接
使用哪些环境变量
端口如何映射
数据如何持久化
服务之间有什么依赖
```

---

# 79. Dockerfile 和 Compose 不要混淆

不要把：

```text
pip install
npm install
apt install
```

这种镜像构建逻辑大量塞进 Compose：

```yaml
command:
```

正确思路通常是：

```text
Dockerfile
↓
构建环境

Compose
↓
组合运行环境
```

---

# 80. 一套完整开发流程

项目：

```text
my-app/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env
├── requirements.txt
└── src/
```

第一步：

```bash
docker compose config
```

检查配置。

第二步：

```bash
docker compose up -d --build
```

构建并启动。

第三步：

```bash
docker compose ps
```

确认状态。

第四步：

```bash
docker compose logs -f
```

观察日志。

第五步：

```bash
docker compose exec web sh
```

进入容器调试。

开发结束：

```bash
docker compose down
```

如果确定连数据也不要了：

```bash
docker compose down -v
```

---

# 81. Compose 调试思路

遇到 Compose 问题时，可以按照：

```text
第一步
↓
配置是否合法？

docker compose config
```

然后：

```text
第二步
↓
Container 是否运行？

docker compose ps
```

然后：

```text
第三步
↓
程序报了什么错？

docker compose logs -f service
```

然后：

```text
第四步
↓
Container 内部环境是否正确？

docker compose exec service sh
```

然后检查：

```text
环境变量
DNS
文件
端口
进程
网络
```

---

# 82. 网络问题排查

假设：

```text
web
```

访问不了：

```text
db
```

首先检查：

```bash
docker compose ps
```

然后进入：

```bash
docker compose exec web sh
```

检查 DNS：

```bash
getent hosts db
```

如果镜像有：

```text
ping
```

也可以：

```bash
ping db
```

然后检查目标端口。

关键思路：

```text
Service 是否运行？
      ↓
是否处于同一 Network？
      ↓
Service Name 能否解析？
      ↓
目标程序是否真正监听端口？
      ↓
应用配置使用的是不是 Container Port？
```

---

# 83. Compose 项目推荐目录

例如：

```text
my-app/
├── compose.yaml
├── compose.override.yaml
├── Dockerfile
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   └── ...
├── config/
│   └── ...
└── secrets/
    └── ...
```

其中：

```text
compose.yaml
↓
基础服务定义

compose.override.yaml
↓
开发环境配置

Dockerfile
↓
应用 Image

.env
↓
本地 Compose 变量

.env.example
↓
可提交的环境变量模板

secrets/
↓
本地敏感信息
```

---

# 84. .env.example

例如真正的：

```text
.env
```

不提交：

```gitignore
.env
```

但是可以创建：

```text
.env.example
```

例如：

```dotenv
APP_PORT=8000
APP_ENV=development

POSTGRES_DB=app
POSTGRES_USER=app

API_URL=
```

提交：

```text
.env.example
```

让其他开发者知道需要配置哪些变量。

---

# 85. Compose 心智模型

写 Compose 时，可以不断问自己：

```text
1. 我的系统有几个 Service？

2. 哪些 Service 使用现成 Image？

3. 哪些 Service 需要 Dockerfile build？

4. 哪些 Service 需要让 Host 访问？

5. Service 之间怎么通信？

6. 哪些数据需要持久化？

7. 哪些目录开发时需要同步？

8. 有哪些环境变量？

9. 有哪些 Secret？

10. 哪些 Service 有启动依赖？

11. 如何判断依赖真正 Ready？

12. 哪些 Service 应该默认启动？

13. 哪些 Service 只属于 Debug / Development？
```

然后分别对应：

```text
services
image
build
ports
networks
volumes
bind mount / watch
environment / env_file
secrets
depends_on
healthcheck
profiles
```

---

# 86. Compose 通用模板

可以先记住：

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

    environment:
      APP_ENV: development
      DB_HOST: db

    depends_on:
      db:
        condition: service_healthy

    networks:
      - backend

  db:
    image: postgres:18

    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: change-me

    volumes:
      - db-data:/var/lib/postgresql/data

    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U $${POSTGRES_USER}
      interval: 5s
      timeout: 3s
      retries: 5

    networks:
      - backend

networks:
  backend:

volumes:
  db-data:
```

理解这个模板后，大部分基础 Compose 项目就已经能自己编写了。

---

# 87. Compose 关键配置速查

| 配置              | 作用                    |
| --------------- | --------------------- |
| `services`      | 定义服务                  |
| `image`         | 使用镜像                  |
| `build`         | 构建镜像                  |
| `ports`         | Host → Container 端口映射 |
| `expose`        | 描述内部端口                |
| `environment`   | 设置容器环境变量              |
| `env_file`      | 从文件加载容器环境变量           |
| `volumes`       | 数据持久化 / 文件挂载          |
| `networks`      | 配置容器网络                |
| `depends_on`    | 服务依赖                  |
| `healthcheck`   | 健康检查                  |
| `restart`       | Restart Policy        |
| `command`       | 覆盖 Dockerfile CMD     |
| `entrypoint`    | 覆盖 ENTRYPOINT         |
| `working_dir`   | 工作目录                  |
| `profiles`      | 可选 Service            |
| `configs`       | 配置数据                  |
| `secrets`       | 敏感数据                  |
| `develop.watch` | 开发文件监听                |
| `include`       | 拆分 Compose 项目         |

---

# 88. 一句话记住主要配置

```text
services
↓
我要运行什么？

image
↓
使用什么镜像？

build
↓
镜像怎么构建？

ports
↓
Host 怎么访问 Container？

environment
↓
应用需要什么变量？

volumes
↓
数据放在哪里？

networks
↓
Container 怎么通信？

depends_on
↓
谁依赖谁？

healthcheck
↓
服务真的准备好了吗？

restart
↓
挂了以后怎么办？

profiles
↓
哪些服务是可选的？

secrets
↓
敏感数据怎么提供？

develop.watch
↓
开发时代码怎么自动同步？
```

---

# 89. 一句话记住 Compose 网络

```text
同一个 Compose Network：

Service Name
=
DNS Hostname
```

例如：

```yaml
services:
  api:
    ...

  db:
    ...

  redis:
    ...
```

那么：

```text
api → db:5432

api → redis:6379
```

而不是：

```text
api → localhost:5432
```

也不是：

```text
api → 172.x.x.x:5432
```

这是 Compose 网络最值得牢牢记住的知识点之一。

---

# 90. 学习检查清单

学完后应该能够回答：

* [ ] Dockerfile 和 Docker Compose 有什么区别？
* [ ] 为什么现在通常不需要 `version: "3.8"`？
* [ ] `services` 是什么？
* [ ] Service 与 Container 有什么区别？
* [ ] `image` 与 `build` 有什么区别？
* [ ] `ports: "8080:80"` 两边分别是什么？
* [ ] `ports` 与 `expose` 有什么区别？
* [ ] 为什么容器之间不应该使用 IP 地址通信？
* [ ] 为什么 `db` 可以直接作为 hostname？
* [ ] Container 中的 `localhost` 指向谁？
* [ ] Container 间通信应该使用 Host Port 还是 Container Port？
* [ ] `.env` 和 `env_file` 有什么区别？
* [ ] `${VAR}` 是谁进行插值？
* [ ] `$$VAR` 有什么作用？
* [ ] Named Volume 与 Bind Mount 有什么区别？
* [ ] `docker compose down` 会删除 Named Volume 吗？
* [ ] `docker compose down -v` 会发生什么？
* [ ] `depends_on` 为什么不一定代表服务 Ready？
* [ ] `healthcheck` 是什么？
* [ ] `service_healthy` 有什么作用？
* [ ] `docker compose exec` 与 `docker compose run` 有什么区别？
* [ ] `restart` 与重新创建 Container 有什么区别？
* [ ] 为什么不推荐滥用 `container_name`？
* [ ] Profile 有什么用途？
* [ ] Secret 为什么比直接写敏感环境变量更合理？
* [ ] `compose.override.yaml` 有什么用途？
* [ ] `docker compose config` 为什么非常重要？
* [ ] Compose Watch 解决了什么问题？

如果这些问题都能比较清楚地回答，就已经掌握 Docker Compose 的核心了。

---

# 91. 推荐学习路线

```mermaid
flowchart TD
    A[Docker 基础] --> B[Dockerfile]
    B --> C[Compose services]
    C --> D[image / build]
    D --> E[ports]
    E --> F[environment]
    F --> G[volumes]
    G --> H[network]
    H --> I[depends_on]
    I --> J[healthcheck]
    J --> K[profiles]
    K --> L[secrets / configs]
    L --> M[Multiple Compose Files]
    M --> N[Compose Watch]
    N --> O[生产环境实践]
```

---

# 92. 与 Docker 知识体系的关系

```text
Docker
│
├── Image
│   └── Dockerfile
│
├── Container
│
├── Network
│
├── Volume
│
└── Docker Compose
    │
    ├── Services
    ├── Networks
    ├── Volumes
    ├── Configs
    ├── Secrets
    ├── Profiles
    └── Develop
```

因此学习 Docker Compose 之前，最好已经理解：

```text
Image
Container
Dockerfile
Network
Volume
```

Compose 本质上是在把这些 Docker 能力：

```text
统一声明
+
统一管理
+
统一启动
```

---

# 93. 相关笔记

* [[Docker]]
* [[Dockerfile]]
* [[Docker镜像与容器]]
* [[Docker网络管理]]
* [[Docker数据卷]]
* [[Docker Build Context]]
* [[Docker Multi-stage Build]]
* [[Docker镜像优化]]
* [[Docker Compose网络]]
* [[Docker Compose环境变量]]
* [[Docker Compose Volume]]
* [[Docker Compose Healthcheck]]
* [[Docker Compose生产环境]]
* [[Kubernetes]]

---

# 总结

Docker Compose 的核心并不是：

```text
记住所有 YAML 参数
```

而是理解：

```text
一个应用
    ↓
拆成多个 Service
    ↓
每个 Service 使用一个 Image
    ↓
Image 可以通过 Dockerfile 构建
    ↓
Service 通过 Network 通信
    ↓
Service Name 作为 DNS Name
    ↓
需要持久化的数据进入 Volume
    ↓
Host 通过 ports 访问需要公开的 Service
    ↓
environment 提供运行配置
    ↓
depends_on 描述依赖
    ↓
healthcheck 判断服务是否真正 Ready
    ↓
Compose 统一管理整个生命周期
```

最初最值得掌握：

```text
services
image
build
ports
environment
volumes
networks
depends_on
healthcheck
```

然后熟练：

```text
docker compose up -d
docker compose down
docker compose ps
docker compose logs -f
docker compose exec
docker compose config
```

最后再学习：

```text
profiles
secrets
configs
override
include
Compose Watch
YAML Anchor
生产环境配置
```

最终应该形成这样的认识：

> **Dockerfile 解决“这个应用怎么装进镜像”，Docker Compose 解决“这些容器怎么组成一个完整系统并一起运行”。**

当看到：

```yaml
services:
  web:
  db:
  redis:
```

脑中应该能够自动转换为：

```text
         Docker Compose Project
                  │
          ┌───────┼───────┐
          │       │       │
         web      db     redis
          │       │       │
          └───────┼───────┘
                  │
             Docker Network
                  │
           ┌──────┴──────┐
           │             │
       Host Ports      Volumes
```

理解这个模型后，Compose YAML 就不再是一堆需要死记硬背的参数，而是在用配置文件描述一个完整的容器化应用架构。
