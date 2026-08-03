---
title: ssh
tags: [liunx, 第三方命令]
aliases: [ssh]
---

# ssh

ssh 基于 TCP,见 [[computer/计算机网络/TCP连接|TCP连接]];sshd 服务管理见 [[liunx/linux命令/系统操作相关|系统操作相关]]。

## 隧道转发

### 本地端口转发

```bash
ssh -L 本地端口:localhost:目标端口 用户@SSH服务器
```

### 远程端口转发

```bash
ssh -R 远程端口:localhost:本地端口 用户@SSH服务器
```
