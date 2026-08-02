---
title: screen
tags: [liunx, 第三方命令]
aliases: [screen]
---

# screen

后台进程管理见 [[liunx/linux命令/系统操作相关]]。

```bash
screen [-opts] [cmd [args]]
```

## 状态介绍

通常情况下，screen 创建的虚拟终端有两个工作模式：

- **Attached**：表示当前 screen 正在作为主终端使用，为活跃状态。
- **Detached**：表示当前 screen 正在后台使用，为非激活状态。

## 查看终端列表

```bash
screen -ls    # 查验已经创建的终端
```

## 终端创建

```bash
screen -R name    # 创建指定名称的终端
```

- 使用 `-R` 创建时，如果有同名的 screen，则直接进入之前创建的 screen。
- 使用 `-S` 创建或直接输入 `screen` 创建的虚拟终端，不会检索之前创建的 screen。
- 后面也可以直接写命令来后台跑。

## 回到终端

```bash
screen -R [pid/name]
```

## 退出终端

按住 `Ctrl+a`，再按 `d`。

## 清除终端

比较推荐的方法是进入对应虚拟终端，然后输入：

```bash
exit
```

也可以：

```bash
screen -R [pid/Name] -X quit
```

## 绑定键

在虚拟终端内，输入 `Ctrl+a` 将等待接受预先设置的绑定键，这个时候可以输入对应的一些命令来操作虚拟终端：

| 键 | 说明 |
|----|------|
| `d` | 保存会话，后台运行该虚拟终端 |
| `k` | 关闭对话，等同输入 `exit` |
| `c` | 新建一个虚拟终端 |
| `?` | 显示所有绑定键盘 |