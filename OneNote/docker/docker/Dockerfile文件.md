---

title: Dockerfile
tags: [docker]
aliases: [Dockerfile, Dockerfile学习笔记, Docker镜像构建]
---

# Dockerfile

## Dockerfile 是什么？

Dockerfile 是一个用于描述 **Docker 镜像构建过程** 的文本文件。

可以简单理解为：

```text
Dockerfile
    ↓ docker build
Image 镜像
    ↓ docker run
Container 容器
```

也可以把它理解成：

```text
Dockerfile = 制作镜像的配方
Image      = 按照配方制作出来的成品
Container  = 把镜像运行起来后的实例
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

构建镜像。

然后执行：

```bash
docker run my-app
```

启动容器。

---

## Dockerfile 基本结构

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

## FROM

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

## WORKDIR

`WORKDIR` 用于设置容器中的工作目录。

例如：

```dockerfile
WORKDIR /app
```

之后执行：

```dockerfile
COPY . .
RUN python test.py
CMD ["python", "app.py"]
```

都会以 `/app` 为当前工作目录。

可以近似理解为 Linux 中：

```bash
cd /app
```

推荐：

```dockerfile
WORKDIR /app
```

而不是：

```dockerfile
RUN cd /app
```

因为不同的 `RUN` 属于不同的构建步骤。

---

## COPY

`COPY` 用于把文件复制进镜像。

语法：

```dockerfile
COPY 源路径 目标路径
```

例如：

```dockerfile
COPY app.py /app/app.py
```

如果已经设置：

```dockerfile
WORKDIR /app
```

那么：

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

## RUN

`RUN` 用于在 **构建镜像时执行命令**。

例如：

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

需要记住：

```text
RUN
 ↓
docker build 时执行
```

例如：

```bash
docker build -t my-app .
```

执行构建时，Docker 才会运行 Dockerfile 中的：

```dockerfile
RUN pip install -r requirements.txt
```

---

## CMD

`CMD` 用于指定 **容器启动后的默认命令**。

例如：

```dockerfile
CMD ["python", "app.py"]
```

当执行：

```bash
docker run my-app
```

实际上会运行：

```bash
python app.py
```

推荐使用这种形式：

```dockerfile
CMD ["python", "app.py"]
```

而不是：

```dockerfile
CMD python app.py
```

前者称为 Exec Form。

---

## RUN 和 CMD 的区别

这是 Dockerfile 中非常重要的区别。

| 指令    | 执行时间           | 用途   |
| ----- | -------------- | ---- |
| `RUN` | `docker build` | 构建镜像 |
| `CMD` | `docker run`   | 启动应用 |

例如：

```dockerfile
RUN pip install flask
```

表示：

```text
制作镜像的时候安装 Flask
```

而：

```dockerfile
CMD ["python", "app.py"]
```

表示：

```text
容器启动的时候运行 app.py
```

记忆：

```text
RUN = 构建时运行

CMD = 容器启动时运行
```

---

## ENTRYPOINT

`ENTRYPOINT` 用于定义容器的固定入口程序。

例如：

```dockerfile
ENTRYPOINT ["python"]
```

然后：

```dockerfile
CMD ["app.py"]
```

组合以后相当于：

```bash
python app.py
```

如果执行：

```bash
docker run my-app test.py
```

那么最终会执行：

```bash
python test.py
```

因此可以简单理解：

```text
ENTRYPOINT = 固定执行程序

CMD = 默认参数
```

---

## ENV

`ENV` 用来定义环境变量。

例如：

```dockerfile
ENV APP_ENV=production
```

或者：

```dockerfile
ENV PORT=8000
```

Python 中可以读取：

```python
import os

env = os.getenv("APP_ENV")
print(env)
```

运行容器时还可以覆盖：

```bash
docker run -e APP_ENV=development my-app
```

---

## ARG

`ARG` 用来定义 **镜像构建参数**。

例如：

```dockerfile
ARG VERSION=1.0
```

构建时：

```bash
docker build \
  --build-arg VERSION=2.0 \
  -t my-app .
```

可以理解为：

```text
ARG = docker build 使用

ENV = docker run 后的程序使用
```

简单对比：

| 特性                 | ARG | ENV |
| ------------------ | --- | --- |
| 构建阶段使用             | ✅   | ✅   |
| 容器运行阶段默认存在         | ❌   | ✅   |
| `--build-arg` 修改   | ✅   | ❌   |
| `docker run -e` 修改 | ❌   | ✅   |

不要使用 `ARG` 或 `ENV` 保存密码、Token、API Key 等敏感数据。

---

## EXPOSE

`EXPOSE` 用于声明应用监听的端口。

例如：

```dockerfile
EXPOSE 8000
```

表示应用预计监听：

```text
8000
```

但需要注意：

```dockerfile
EXPOSE 8000
```

并不会自动完成宿主机端口映射。

运行时仍然通常需要：

```bash
docker run -p 8000:8000 my-app
```

表示：

```text
宿主机 8000
      ↓
容器 8000
```

---

## USER

`USER` 用于指定容器中的运行用户。

例如：

```dockerfile
RUN useradd -m appuser

USER appuser
```

生产环境中通常不建议应用一直以 `root` 用户运行。

例如：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN useradd -m appuser

USER appuser

CMD ["python", "app.py"]
```

---

## ADD 与 COPY

Dockerfile 中还有：

```dockerfile
ADD
```

普通文件复制优先使用：

```dockerfile
COPY . /app
```

简单记忆：

```text
普通文件复制
    ↓
COPY

确实需要 ADD 的额外能力
    ↓
ADD
```

绝大多数项目中使用 `COPY` 就够了。

---

# Build Context

执行：

```bash
docker build -t my-app .
```

最后面的：

```text
.
```

代表：

```text
Build Context
```

例如：

```text
project/
├── Dockerfile
├── app.py
├── requirements.txt
└── src/
```

进入：

```bash
cd project
```

执行：

```bash
docker build -t my-app .
```

那么 `project` 就是本次构建的 Build Context。

Dockerfile：

```dockerfile
COPY app.py /app/
```

可以读取：

```text
project/app.py
```

---

# .dockerignore

项目中通常应该创建：

```text
.dockerignore
```

它的作用类似：

```text
.gitignore
```

例如：

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

这样可以避免一些无关文件进入 Docker 构建上下文。

尤其需要注意：

```text
.env
```

通常应该排除，避免密码、Token 等敏感数据被复制进镜像。

---

# Docker Layer

Docker 镜像可以理解为由多个 Layer 组成。

例如：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

可以粗略理解成：

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

Docker 构建时会尽可能复用缓存。

因此 Dockerfile 的指令顺序会影响构建速度。

---

# Docker 构建缓存

例如下面这种写法：

```dockerfile
COPY . .

RUN pip install -r requirements.txt
```

如果只修改：

```text
app.py
```

`COPY . .` 就发生了变化。

后面的：

```dockerfile
RUN pip install -r requirements.txt
```

也可能重新执行。

更好的写法是：

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

# Python Dockerfile 示例

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

# Node.js Dockerfile 示例

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

构建：

```bash
docker build -t node-app .
```

运行：

```bash
docker run -p 3000:3000 node-app
```

---

# Multi-stage Build

Multi-stage Build 即：

```text
多阶段构建
```

一个 Dockerfile 中可以出现多个：

```dockerfile
FROM
```

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

这样最终镜像不需要保留：

```text
编译器
构建工具
项目源码
开发依赖
```

---

## Go 多阶段构建

例如：

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

第一个阶段：

```text
golang 镜像
    ↓
下载依赖
    ↓
编译 server
```

第二个阶段：

```text
alpine 镜像
    ↓
复制 server
    ↓
运行 server
```

关键：

```dockerfile
COPY --from=builder /app/server ./server
```

表示：

```text
从 builder 阶段
复制 /app/server
到当前镜像
```

---

# RUN 多条命令

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

# 常见错误

## 把 CMD 当成 RUN

错误：

```dockerfile
CMD pip install -r requirements.txt
```

这意味着容器每次启动时安装依赖。

应该写：

```dockerfile
RUN pip install -r requirements.txt
```

---

## 使用 RUN 启动应用

错误：

```dockerfile
RUN python app.py
```

因为 `RUN` 是：

```text
docker build
```

阶段执行。

应该：

```dockerfile
CMD ["python", "app.py"]
```

---

## 认为 EXPOSE 会自动映射端口

Dockerfile：

```dockerfile
EXPOSE 8000
```

运行时通常还是需要：

```bash
docker run -p 8000:8000 my-app
```

---

## 直接 COPY 所有文件

不推荐：

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

这样可以更好地利用 Docker 构建缓存。

---

# Dockerfile 常用指令速查

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

# Dockerfile 编写思路

写 Dockerfile 时可以按照以下问题思考：

```text
1. 我的应用需要什么基础环境？

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

# Dockerfile 通用模板

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

# 核心记忆

```text
FROM
↓
从哪个基础镜像开始

WORKDIR
↓
在哪里工作

COPY
↓
复制哪些文件

RUN
↓
构建镜像时执行什么

ENV
↓
设置什么环境变量

EXPOSE
↓
应用监听什么端口

USER
↓
以什么用户运行

ENTRYPOINT
↓
容器固定执行什么程序

CMD
↓
容器默认如何启动
```

最初只需要牢牢记住：

```text
FROM
WORKDIR
COPY
RUN
CMD
```

基本就可以开始自己编写 Dockerfile 了。

---

# 相关笔记

* [[Docker]]
* [[Docker镜像与容器]]
* [[Docker网络管理]]
* [[Docker数据卷]]
* [[Docker Compose]]
* [[Docker Build Context]]
* [[Docker Multi-stage Build]]
* [[Docker镜像优化]]
