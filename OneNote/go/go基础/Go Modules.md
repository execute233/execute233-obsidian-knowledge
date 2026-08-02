---
title: Go Modules
tags: [go, modules, 包管理]
aliases: []
---

# Go Modules

## go mod 命令

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-16-0.png)

## 相关环境变量

使用 `go env` 查看。

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-18-1.png)

## 导入包

### 方式一:命令行

例如引入第三方包 `github.com/q1mi/hello`,使用命令手动下载:

```bash
go get -u github.com/q1mi/hello
```

也可以指定版本号:

```bash
go get -u github.com/q1mi/hello@v0.1.0
```

### 方式二:修改 go.mod

```go
require (
    "xxx" vxx.xx.xx
)
```

> 注:版本也可以写 commit hash,然后可以 `go mod download` 下载。

### 方式三:导入外部包

仍可以像方式二那样写,但需要 `replace` 语句替换为使用相对路径的包:

```go
replace xxx.com/pack => ../pack
```

### 修改版本

```bash
go mod edit replace=<包名@版本>=<包名@新的版本>
```

## 发布包

假设已有一个 git 项目,需要把代码 push 到远程分支并打上 tag:

```bash
git tag -a v0.1.0 -m "release version v0.1.0"
git push origin v0.1.0
```

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-19-2.png)

## 发布新的主版本
