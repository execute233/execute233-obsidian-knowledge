---
title: 管理conda
tags: [python, conda]
aliases: [管理conda]
---

# 管理conda

Conda 是 Anaconda 中一个强大的包和环境管理工具。包管理详见 [[包管理]],环境管理详见 [[环境管理]]。 Anaconda 中一个强大的包和环境管理工具，可以在 Windows 的 Anaconda Prompt 命令行使用，也可以在 macOS 或者 Linux 系统的终端窗口（terminal window）的命令行使用。

## 查看conda版本

```bash
conda --version
```

## 查看conda的环境配置

```bash
conda config --show
```

## 设置镜像

```bash
# 设置清华镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
# 设置bioconda
conda config --add channels bioconda
conda config --add channels conda-forge
# 设置搜索时显示通道地址
conda config --set show_channel_urls yes
```

## 更新

```bash
conda update conda
# 或
conda update anaconda
```

## 查看命令帮助

```bash
conda <命令> --help
```