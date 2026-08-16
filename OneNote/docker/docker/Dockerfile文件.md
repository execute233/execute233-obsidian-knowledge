---
title: Dockerfile
tags: [docker]
aliases: [Dockerfile, Dockerfile学习笔记, Docker镜像构建]
---

# Dockerfile

> [!abstract]
> Dockerfile 是一个文本文件，描述 Docker 镜像如何构建。
>
> * `FROM` 选择基础镜像
> * `WORKDIR` 设置容器内工作目录
> * `COPY` 把文件复制进镜像
> * `RUN` 在构建镜像时执行命令
> * `CMD` 指定容器启动后的默认命令
>
> 编写思路通常是：选基础镜像 → 设工作目录 → 复制依赖 → 安装依赖 → 复制代码 → 声明端口 → 设置启动命令。

---

# 1. Dockerfile 是什么

Dockerfile 是一个用于描述 Docker 镜像构建过程的文本文件。

```text
Dockerfile
    ↓ docker build
Image 镜像
    ↓ docker run
Container 容器
```

假设有一个 Python 项目：

```text
my-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

可以执行：

```bash
docker build -t my-app .
```

构建镜像，然后执行：

```bash
docker run my-app
```

启动容器。

也可以理解为：

```text
Dockerfile = 制作镜像的配方
Image      = 按配方做出来的成品
Container  = 把镜像运行起来后的实例
```

---

# 2. Dockerfile 基本结构

一个简单的 Python Dockerfile：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

基本流程：

```text
选择基础镜像
    ↓
设置工作目录
    ↓
复制依赖文件
    ↓
安装依赖
    ↓
复制业务代码
    ↓
设置启动命令
```

---

# 3. `FROM`

`FROM` 用于指定基础镜像。

格式：

```dockerfile
FROM 镜像名:版本
```

例如：

```dockerfile
FROM ubuntu:24.04
```

---

# 4. `WORKDIR`

`WORKDIR` 用于设置容器中的工作目录。

```dockerfile
WORKDIR /app
```

之后执行 `COPY`、`RUN`、`CMD` 时都以 `/app` 为当前工作目录。

可以近似理解为 Linux 中的：

```bash
cd /app
```

推荐使用 `WORKDIR /app`，而不是 `RUN cd /app`，因为不同 `RUN` 属于不同的构建步骤。

---

# 5. `COPY`

`COPY` 用于把文件复制进镜像。

语法：

```dockerfile
COPY 源路径 目标路径
```

例如：

```dockerfile
COPY app.py /app/app.py
```

如果已经设置了 `WORKDIR /app`，那么：

```dockerfile
COPY . .
```

可以理解为：

```text
项目当前目录
      ↓
容器 /app
```

其中两个 `.` 分别表示：

```text
第一个 . = Build Context 当前目录
第二个 . = 容器当前 WORKDIR
```

---

# 6. `RUN`

`RUN` 用于在构建镜像时执行命令。

```dockerfile
RUN pip install flask
```

Python 项目：

```dockerfile
RUN pip install -r requirements.txt
```

Node.js：

```dockerfile
RUN npm install
```

Ubuntu：

```dockerfile
RUN apt-get update
```

`RUN` 在 `docker build` 时执行。

---

# 7. `CMD`

`CMD` 用于指定容器启动后的默认命令。

```dockerfile
CMD ["python", "app.py"]
```

执行 `docker run my-app` 时实际运行：

```bash
python app.py
```

推荐使用 Exec Form：

```dockerfile
CMD ["python", "app.py"]
```

而不是 Shell Form：

```dockerfile
CMD python app.py
```

---

# 8. `RUN` VS `CMD`

| 指令    | 执行时间           | 用途   |
| ----- | -------------- | ---- |
| `RUN` | `docker build` | 构建镜像 |
| `CMD` | `docker run`   | 启动应用 |

记忆：

```text
RUN  = 构建时运行
CMD  = 容器启动时运行
```

---

# 9. `ENTRYPOINT`

`ENTRYPOINT` 用于定义容器的固定入口程序。

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

组合后相当于：

```bash
python app.py
```

执行 `docker run my-app test.py` 时：

```bash
python test.py
```

因此：

```text
ENTRYPOINT = 固定执行程序
CMD        = 默认参数
```

---

# 10. `ENV`

`ENV` 用来定义环境变量。

```dockerfile
ENV APP_ENV=production
ENV PORT=8000
```

Python 中读取：

```python
import os

env = os.getenv("APP_ENV")
print(env)
```

运行时可覆盖：

```bash
docker run -e APP_ENV=development my-app
```

---

# 11. `ARG`

`ARG` 用来定义镜像构建参数。

```dockerfile
ARG VERSION=1.0
```

构建时传入：

```bash
docker build \
  --build-arg VERSION=2.0 \
  -t my-app .
```

简单对比：

| 特性                 | ARG | ENV |
| ------------------ | --- | --- |
| 构建阶段使用             | ✅   | ✅   |
| 容器运行阶段默认存在        | ❌   | ✅   |
| `--build-arg` 修改   | ✅   | ❌   |
| `docker run -e` 修改 | ❌   | ✅   |

不要用 `ARG` 或 `ENV` 保存密码、Token、API Key 等敏感数据。

---

# 12. `EXPOSE`

`EXPOSE` 用于声明应用监听的端口。

```dockerfile
EXPOSE 8000
```

但 `EXPOSE 8000` 不会自动完成宿主机端口映射，运行时通常仍然需要：

```bash
docker run -p 8000:8000 my-app
```

---

# 13. `USER`

`USER` 用于指定容器中的运行用户。

```dockerfile
RUN useradd -m appuser

USER appuser
```

生产中通常不建议应用一直以 `root` 运行。完整示例：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN useradd -m appuser

USER appuser

CMD ["python", "app.py"]
```

---

# 14. `ADD` 与 `COPY`

普通文件复制优先使用 `COPY`：

```dockerfile
COPY . /app
```

只有确实需要 `ADD` 的额外能力（如自动解压远程包）时才使用 `ADD`。

简单记忆：

```text
普通文件复制 → COPY
确实需要 ADD 的额外能力 → ADD
```

绝大多数项目使用 `COPY` 就够了。

---

# 15. Build Context

执行：

```bash
docker build -t my-app .
```

最后面的 `.` 代表 Build Context。

例如：

```text
project/
├── Dockerfile
├── app.py
├── requirements.txt
└── src/
```

进入 `project/` 后执行构建，那么 `project` 就是本次构建的 Build Context。

Dockerfile 中 `COPY app.py /app/` 可以读取 `project/app.py`，但读不到 Build Context 之外的文件。

---

# 16. `.dockerignore`

通常应创建 `.dockerignore`，作用类似 `.gitignore`：

```dockerignore
.git
.env

node_modules

__pycache__
*.pyc

dist
build

.idea
.vscode
```

尤其需要排除 `.env`，避免密码、Token 等敏感数据被复制进镜像。

---

# 17. Docker Layer

Docker 镜像由多个 Layer 组成。例如：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

可以粗略理解为：

```text
Python 基础镜像
      ↓
WORKDIR
      ↓
COPY requirements.txt
      ↓
RUN pip install
      ↓
COPY 项目代码
      ↓
CMD
```

Docker 构建时会尽可能复用缓存，因此 Dockerfile 指令顺序会影响构建速度。

---

# 18. Docker 构建缓存

例如：

```dockerfile
COPY . .

RUN pip install -r requirements.txt
```

如果只修改 `app.py`，`COPY . .` 会发生变化，后续 `RUN pip install` 也可能重新执行。

更好的写法：

```dockerfile
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
```

流程变成：

```text
requirements.txt 没修改
        ↓
继续复用 pip install 缓存
        ↓
只重新复制业务代码
```

Node.js 同理：

```dockerfile
COPY package.json package-lock.json ./

RUN npm ci

COPY . .
```

---

# 19. Python Dockerfile 示例

项目：

```text
python-app/
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── app.py
```

Dockerfile：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

构建：

```bash
docker build -t python-app .
```

运行：

```bash
docker run -p 8000:8000 python-app
```

后台运行：

```bash
docker run -d \
  --name python-app \
  -p 8000:8000 \
  python-app
```

---

# 20. Node.js Dockerfile 示例

项目：

```text
node-app/
├── Dockerfile
├── .dockerignore
├── package.json
├── package-lock.json
└── src/
```

Dockerfile：

```dockerfile
FROM node:22-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

构建并运行：

```bash
docker build -t node-app .

docker run -p 3000:3000 node-app
```

---

# 21. Multi-stage Build

Multi-stage Build 即多阶段构建，一个 Dockerfile 中可以出现多个 `FROM`。

典型流程：

```text
构建环境
    ↓
编译程序
    ↓
得到程序产物
    ↓
复制到运行环境
```

最终镜像不需要保留编译器、构建工具、项目源码和开发依赖。

## Go 多阶段构建

```dockerfile
FROM golang:1.24 AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 go build -o server .


FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/server ./server

CMD ["./server"]
```

第一个阶段在 `golang` 镜像中下载依赖并编译 `server`。第二个阶段从 `alpine` 镜像复制 server 并运行。

关键指令：

```dockerfile
COPY --from=builder /app/server ./server
```

表示从 `builder` 阶段复制产物到当前镜像。

---

# 22. 合并 `RUN` 多条命令

例如：

```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
```

通常可以整理为：

```dockerfile
RUN apt-get update \
    && apt-get install -y \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*
```

把逻辑相关的命令放在一起，同时及时删除不再需要的包管理缓存。

---

# 23. 常见错误

## 把 `CMD` 当成 `RUN`

```dockerfile
CMD pip install -r requirements.txt
```

这意味着容器每次启动时安装依赖。应改为：

```dockerfile
RUN pip install -r requirements.txt
```

## 用 `RUN` 启动应用

```dockerfile
RUN python app.py
```

`RUN` 在 `docker build` 阶段执行。应改为：

```dockerfile
CMD ["python", "app.py"]
```

## 认为 `EXPOSE` 会自动映射端口

```dockerfile
EXPOSE 8000
```

运行时通常仍需：

```bash
docker run -p 8000:8000 my-app
```

## 直接 `COPY . .` 然后 `npm install`

```dockerfile
COPY . .

RUN npm install
```

更推荐：

```dockerfile
COPY package.json package-lock.json ./

RUN npm ci

COPY . .
```

这样能更好地利用 Docker 构建缓存。

---

# 24. Dockerfile 常用指令速查

| 指令           | 作用      |
| ------------ | ------- |
| `FROM`       | 指定基础镜像  |
| `WORKDIR`    | 设置工作目录  |
| `COPY`       | 复制文件    |
| `ADD`        | 添加文件    |
| `RUN`        | 构建时执行命令 |
| `CMD`        | 默认启动命令  |
| `ENTRYPOINT` | 容器入口    |
| `ENV`        | 环境变量    |
| `ARG`        | 构建参数    |
| `EXPOSE`     | 声明端口    |
| `USER`       | 指定运行用户  |

---

# 25. Dockerfile 编写思路

写 Dockerfile 时按以下问题思考：

```text
1. 应用需要什么基础环境？

2. 应用放在哪个目录？

3. 有哪些依赖？

4. 如何安装依赖？

5. 哪些代码需要复制？

6. 应用监听哪个端口？

7. 最终如何启动应用？
```

对应：

```dockerfile
FROM ...

WORKDIR /app

COPY 依赖文件 .

RUN 安装依赖

COPY . .

EXPOSE 端口

CMD ["启动命令"]
```

---

# 26. Dockerfile 通用模板

```dockerfile
FROM <base-image>

WORKDIR /app

COPY <dependency-files> ./

RUN <install-dependencies>

COPY . .

EXPOSE <port>

CMD ["<command>", "<arg>"]
```

Python：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

Node.js：

```dockerfile
FROM node:22-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

---

# 27. 核心记忆

最初只需要牢牢记住：

```text
FROM
WORKDIR
COPY
RUN
CMD
```

基本就可以开始自己编写 Dockerfile 了。

之后逐步加入：

```text
ENV       设置环境变量
EXPOSE    声明端口
USER      指定运行用户
ENTRYPOINT 容器固定入口
```

---

# 28. 本课需要掌握

* [ ] 理解 Dockerfile / Image / Container 三者关系
* [ ] 能用 `FROM` 选择基础镜像
* [ ] 能用 `WORKDIR`、`COPY`、`RUN`、`CMD` 编写简单 Dockerfile
* [ ] 理解 `RUN` 与 `CMD` 的执行时机区别
* [ ] 理解 `ENTRYPOINT` 与 `CMD` 的关系
* [ ] 理解 `ARG` 与 `ENV` 的区别
* [ ] 理解 `EXPOSE` 不会自动映射宿主机端口
* [ ] 理解 `.dockerignore` 的作用
* [ ] 理解 Docker Layer 与构建缓存
* [ ] 能写出 Python / Node.js Dockerfile
* [ ] 理解 Multi-stage Build 适合编译型语言

---

# 下一课

下一节：

[[docker-compose]]

重点：

* `services` / `image` / `build`
* `ports` / `expose`
* `networks` 与 Service Name DNS
* `volumes` 与 Bind Mount
* `depends_on` 与 `healthcheck`
* `environment` / `env_file` / `.env`
* `profiles`
* `docker compose up / down / logs / exec`
* 多 Compose 文件

---

# 相关笔记

* [[Docker]]
* [[docker-compose]]
* [[docker-build-context]]
* [[docker-multi-stage-build]]