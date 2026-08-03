---
title: WSL
tags: [windows, 可选功能]
aliases: [WSL]
---

# WSL

适用于 Linux 的 Windows 子系统（WSL）是 Windows 的一项功能，可用于在 Windows 计算机上运行 Linux 环境，而无需单独的虚拟机或双重启动。WSL 内的文件系统布局与 Linux 一致，详见 [[liunx/基础知识/文件系统|文件系统]]；日常文件操作命令见 [[liunx/linux命令/文件操作|文件操作]]。

更多参考 [Windows Subsystem for Linux](https://learn.microsoft.com/zh-cn/windows/wsl/) 文档 | Microsoft Learn。

## 安装

```bash
wsl --install
```

安装 WSL 和 Linux 的默认 Ubuntu 分发版。了解详细信息。还可以使用此命令通过运行 `wsl --install <Distribution Name>` 来安装其他 Linux 分发版。对于有效的发行版名称列表，请运行 `wsl --list --online`。

### 选项

- `--distribution`：指定要安装的 Linux 分发版。可以通过运行 `wsl --list --online` 来查找可用的分发版。
- `--no-launch`：安装 Linux 分发版，但不自动启动它。
- `--web-download`：从联机源安装，而不是使用 Microsoft Store。

### 未安装 WSL 时的选项

- `--inbox`：使用 Windows 组件而不是使用 Microsoft 应用商店安装 WSL（WSL 更新将通过 Windows 更新接收，而不是通过应用商店按可用方式推送）。
- `--enable-wsl1`：在安装 Microsoft Store 版本的 WSL 时启用"适用于 Linux 的 Windows 子系统"可选组件，从而启用 WSL 1。
- `--no-distribution`：安装 WSL 时不要安装分发版。

## 常用命令

### 列出已安装的 Linux 分发版（包括运行状态）

```bash
wsl -l -v
```

### 运行特定的 Linux 分发版

```bash
wsl -d <Distribution Name> -u <User Name>
```

### 检查 WSL 状态

```bash
wsl --status
```

### 检查 WSL 版本

```bash
wsl --version
```

### Help 命令

```bash
wsl --help
```

### 关机

```bash
wsl --shutdown
```

立即终止所有正在运行的分发版和 WSL 2 轻型实用工具虚拟机。

### 终止

```bash
wsl --terminate <Distribution Name>
```

### 标识 IP 地址

### 注销或卸载 Linux 分发版

```bash
wsl --unregister <DistributionName>
```

### 装载磁盘或设备

```bash
wsl --mount <DiskPath>
```

#### 选项

- `--vhd`：指定 `<Disk>` 引用虚拟硬盘。
- `--name`：使用装入点的自定义名称装载磁盘。
- `--bare`：将磁盘附加到 WSL2，但不装载它。
- `--type <Filesystem>`：在装载磁盘时使用的文件系统类型，如果未指定，则默认为 ext4。此命令也可以输入为：`wsl --mount -t <Filesystem>`。可以使用 `blkid <BlockDevice>` 命令检测文件系统类型。
- `--partition <Partition Number>`：要装载的分区的索引号（如果未指定）默认为整个磁盘。
- `--options <MountOptions>`：装载磁盘时，可以包含一些特定于文件系统的选项。
