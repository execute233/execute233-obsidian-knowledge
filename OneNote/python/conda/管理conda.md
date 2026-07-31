# 管理conda

Conda是Anaconda中一个强大的包和环境管理工具，可以在Windows的Anaconda Prompt命令行使用，也可以在macOS或者Linux系统的终端窗口(terminal window)的命令行使用。

## 查看conda版本
## 查看conda的环境配置
## 设置镜像
## 更新

```python
查看某个命令的帮助
```

```bash
conda --version
conda config --show
#设置清华镜像
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/)
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/)
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/)
conda config --add channels [https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/)
#设置bioconda
conda config --add channels bioconda
conda config --add channels conda-forge
#设置搜索时显示通道地址
conda config --set show_channel_urls yes
conda update conda或conda update Anaconda
conda 命令 --help
```