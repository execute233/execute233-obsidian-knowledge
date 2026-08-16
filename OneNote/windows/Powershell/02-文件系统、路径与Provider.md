# PowerShell 课程 02：文件系统、路径与 Provider

> [!info] 本课目标
> 学完这一课，你应该能够：
>
> * 熟练浏览文件系统
> * 理解相对路径和绝对路径
> * 创建、复制、移动、重命名和删除文件
> * 使用通配符批量处理文件
> * 使用递归搜索文件
> * 判断文件或目录是否存在
> * 理解 `$HOME`、`$PWD`、`$PSScriptRoot`
> * 理解 PowerShell Provider
> * 使用 PowerShell 操作环境变量和注册表路径
> * 完成一个 Downloads 自动分类器

---

# 1. 从 `cd` 和 `ls` 开始

如果你使用过 CMD、Bash 或 Linux，那么下面两个命令应该非常熟悉：

```powershell
cd C:\Projects
ls
```

它们在 PowerShell 里确实可以使用。

但是：

```powershell
cd
ls
```

实际上只是别名。

查看：

```powershell
Get-Alias cd
```

可能看到：

```text
cd -> Set-Location
```

查看：

```powershell
Get-Alias ls
```

可能看到：

```text
ls -> Get-ChildItem
```

所以 PowerShell 原生命令实际上是：

```powershell
Set-Location
Get-ChildItem
```

---

# 2. 查看当前位置

执行：

```powershell
Get-Location
```

输出类似：

```text
Path
----
C:\Users\Ema
```

也可以：

```powershell
$PWD
```

例如：

```powershell
$PWD.Path
```

得到：

```text
C:\Users\Ema
```

---

## `$PWD` 是什么？

`$PWD` 是一个自动变量。

它保存：

> 当前 PowerShell 工作目录。

可以查看类型：

```powershell
$PWD.GetType()
```

你会再次发现：

> PowerShell 中很多东西都是对象。

---

# 3. 切换目录

使用：

```powershell
Set-Location C:\Projects
```

简写：

```powershell
cd C:\Projects
```

进入子目录：

```powershell
Set-Location .\Demo
```

返回上一级：

```powershell
Set-Location ..
```

或者：

```powershell
cd ..
```

---

# 4. 相对路径和绝对路径

这是脚本开发中必须掌握的基础。

## 绝对路径

完整写出位置：

```text
C:\Projects\PowerShell\demo.ps1
```

这种路径称为：

```text
Absolute Path
绝对路径
```

PowerShell：

```powershell
Get-Item C:\Projects\PowerShell\demo.ps1
```

---

## 相对路径

假设当前目录：

```text
C:\Projects\PowerShell
```

那么：

```powershell
Get-Item .\demo.ps1
```

就是：

```text
C:\Projects\PowerShell\demo.ps1
```

其中：

```text
.
```

代表：

```text
当前目录
```

而：

```text
..
```

代表：

```text
父目录
```

例如：

```powershell
Get-ChildItem ..
```

就是查看上一级目录。

---

# 5. `$HOME`

PowerShell 提供：

```powershell
$HOME
```

表示：

> 当前用户的 Home 目录。

Windows 通常类似：

```text
C:\Users\Ema
```

所以：

```powershell
Get-ChildItem $HOME
```

等价于：

```powershell
Get-ChildItem C:\Users\Ema
```

非常适合写跨机器脚本。

例如：

```powershell
$downloadPath = "$HOME\Downloads"
```

而不要写死：

```powershell
$downloadPath = "C:\Users\Ema\Downloads"
```

因为换一台电脑用户名就可能不同。

---

# 6. 路径拼接

初学者可能会这样写：

```powershell
$path = "$HOME\Downloads\Images"
```

这当然可以。

但是更规范的方法是：

```powershell
Join-Path $HOME "Downloads"
```

例如：

```powershell
$downloads = Join-Path $HOME "Downloads"
$images = Join-Path $downloads "Images"
```

查看：

```powershell
$images
```

得到：

```text
C:\Users\Ema\Downloads\Images
```

---

# 7. 为什么推荐 `Join-Path`？

因为直接字符串拼接：

```powershell
$HOME + "\Downloads"
```

很容易出现：

```text
\\
```

或者：

```text
/
\
```

混用的问题。

更重要的是，PowerShell 7 是跨平台的。

Linux 路径可能是：

```text
/home/ema/Downloads
```

所以写：

```powershell
Join-Path $HOME "Downloads"
```

比手写分隔符更稳。

---

# 8. 查看目录内容：`Get-ChildItem`

这是文件操作中最重要的命令之一。

执行：

```powershell
Get-ChildItem
```

它会列出当前目录内容。

常见别名：

```powershell
ls
dir
gci
```

---

## 指定路径

```powershell
Get-ChildItem C:\Projects
```

或者：

```powershell
Get-ChildItem -Path C:\Projects
```

---

# 9. 只查看文件

```powershell
Get-ChildItem -File
```

只返回文件。

---

# 10. 只查看目录

```powershell
Get-ChildItem -Directory
```

只返回目录。

例如：

```powershell
Get-ChildItem $HOME -Directory
```

---

# 11. 文件对象

执行：

```powershell
Get-ChildItem -File |
    Get-Member
```

你可能看到：

```text
System.IO.FileInfo
```

目录则通常是：

```text
System.IO.DirectoryInfo
```

也就是说：

```text
Get-ChildItem
       ↓
FileInfo / DirectoryInfo 对象
```

而不是字符串。

---

# 12. 查看文件属性

例如：

```powershell
$file = Get-ChildItem -File | Select-Object -First 1
```

查看：

```powershell
$file.Name
```

```powershell
$file.FullName
```

```powershell
$file.Extension
```

```powershell
$file.Length
```

```powershell
$file.CreationTime
```

```powershell
$file.LastWriteTime
```

---

这些属性以后会非常常用。

---

# 13. 找出最大的文件

现在利用上一课的对象管道思维。

需求：

> 找出当前目录最大的 5 个文件。

```powershell
Get-ChildItem -File |
    Sort-Object Length -Descending |
    Select-Object -First 5 Name, Length
```

这里：

```text
Length
```

就是：

```text
FileInfo.Length
```

单位是：

```text
Byte
```

---

# 14. 计算文件大小 MB

可以：

```powershell
Get-ChildItem -File |
    Select-Object Name,
        @{
            Name = "SizeMB"
            Expression = {
                [Math]::Round($_.Length / 1MB, 2)
            }
        }
```

这里第一次正式看到：

```powershell
1KB
1MB
1GB
1TB
```

PowerShell 原生支持这些容量单位。

例如：

```powershell
1KB
```

实际上：

```text
1024
```

而：

```powershell
1MB
```

等于：

```text
1048576
```

所以：

```powershell
$file.Length / 1MB
```

就是：

```text
文件大小 / 1048576
```

---

# 15. 递归搜索：`-Recurse`

假设目录：

```text
Projects/
├── A/
│   └── test.java
├── B/
│   └── src/
│       └── Main.java
└── README.md
```

执行：

```powershell
Get-ChildItem -File
```

只看当前目录。

如果：

```powershell
Get-ChildItem -File -Recurse
```

就会递归进入所有子目录。

---

例如：

```powershell
Get-ChildItem C:\Projects -Recurse -File
```

意思：

> 找出 C:\Projects 下所有文件。

---

# 16. 搜索 Java 文件

```powershell
Get-ChildItem C:\Projects `
    -Recurse `
    -File `
    -Filter *.java
```

也可以写成一行：

```powershell
Get-ChildItem C:\Projects -Recurse -File -Filter *.java
```

---

# 17. `-Filter`

例如：

```powershell
Get-ChildItem -Filter *.log
```

找到：

```text
application.log
error.log
server.log
```

---

再比如：

```powershell
Get-ChildItem -Filter *.json
```

---

# 18. 通配符

PowerShell 支持常见通配符。

## `*`

匹配任意数量字符。

例如：

```powershell
Get-ChildItem *.log
```

匹配：

```text
app.log
error.log
server.log
```

---

## `?`

匹配一个字符。

例如：

```text
file?.txt
```

可以匹配：

```text
file1.txt
fileA.txt
fileX.txt
```

但不会匹配：

```text
file10.txt
```

---

# 19. 使用对象属性搜索

例如：

```powershell
Get-ChildItem -File |
    Where-Object Extension -EQ ".log"
```

也可以：

```powershell
Get-ChildItem -File |
    Where-Object {
        $_.Extension -eq ".log"
    }
```

---

如果想找多种类型：

```powershell
Get-ChildItem -File |
    Where-Object Extension -In ".jpg", ".png", ".webp"
```

这里：

```powershell
-in
```

表示：

> 是否存在于某个集合。

相当于 Java：

```java
extensions.contains(file.getExtension())
```

---

# 20. 创建文件：`New-Item`

创建文件：

```powershell
New-Item test.txt
```

最好明确：

```powershell
New-Item -Path test.txt -ItemType File
```

---

创建目录：

```powershell
New-Item -Path Images -ItemType Directory
```

---

# 21. 如果目录已经存在怎么办？

如果执行：

```powershell
New-Item Images -ItemType Directory
```

而目录已经存在，可能报错。

常见做法：

```powershell
if (-not (Test-Path Images)) {
    New-Item Images -ItemType Directory
}
```

后面我们还会学习更简洁、更适合脚本工程的写法。

---

# 22. `Test-Path`

这个命令非常重要。

```powershell
Test-Path ".\config.json"
```

返回：

```text
True
```

或者：

```text
False
```

所以：

```powershell
if (Test-Path ".\config.json") {
    "配置文件存在"
}
```

---

检查目录：

```powershell
Test-Path ".\logs"
```

---

# 23. 获取文件对象：`Get-Item`

`Get-ChildItem` 是：

> 获取目录中的子项。

而：

```powershell
Get-Item
```

通常用于：

> 获取某一个指定项目。

例如：

```powershell
Get-Item .\application.log
```

然后：

```powershell
$file = Get-Item .\application.log
```

访问：

```powershell
$file.Length
$file.FullName
$file.LastWriteTime
```

---

# 24. 复制：`Copy-Item`

复制文件：

```powershell
Copy-Item .\test.txt .\backup\
```

---

指定目标名称：

```powershell
Copy-Item .\test.txt .\backup\test-backup.txt
```

---

复制目录：

```powershell
Copy-Item .\config .\backup -Recurse
```

---

# 25. 移动：`Move-Item`

例如：

```powershell
Move-Item .\test.txt .\Documents\
```

移动整个目录：

```powershell
Move-Item .\Images .\Backup\
```

---

# 26. 重命名：`Rename-Item`

例如：

```powershell
Rename-Item .\test.txt demo.txt
```

---

批量重命名以后会非常有用。

例如：

```text
IMG_001.jpg
IMG_002.jpg
IMG_003.jpg
```

批量改名：

```text
travel-001.jpg
travel-002.jpg
travel-003.jpg
```

后续会专门练习。

---

# 27. 删除：`Remove-Item`

删除文件：

```powershell
Remove-Item .\test.txt
```

删除目录：

```powershell
Remove-Item .\Demo -Recurse
```

---

## 强制删除

```powershell
Remove-Item .\Demo -Recurse -Force
```

但是：

> [!danger]
> `Remove-Item -Recurse -Force` 是危险操作。
>
> 尤其不要对不确定的路径直接执行。

---

# 28. PowerShell 的安全神器：`-WhatIf`

很多具有破坏性的 Cmdlet 支持：

```powershell
-WhatIf
```

例如：

```powershell
Remove-Item .\Demo -Recurse -WhatIf
```

它不会真的删除。

只会显示：

```text
What if: Performing the operation "Remove Directory"...
```

这意味着：

> 假如真的执行，会发生什么？

---

以后看到：

```text
删除
移动
覆盖
停止服务
修改系统
```

这种操作时，建议先考虑：

```powershell
-WhatIf
```

---

# 29. `-Confirm`

例如：

```powershell
Remove-Item .\test.txt -Confirm
```

PowerShell 会要求确认。

---

# 30. 读取文件内容

使用：

```powershell
Get-Content
```

例如：

```powershell
Get-Content .\application.log
```

常见别名：

```powershell
cat
gc
```

---

# 31. 只读取最后几行

日志分析非常常用：

```powershell
Get-Content .\application.log -Tail 20
```

意思：

> 查看日志最后 20 行。

类似 Linux：

```bash
tail -n 20 application.log
```

---

# 32. 实时查看日志

PowerShell：

```powershell
Get-Content .\application.log -Tail 20 -Wait
```

效果类似：

```bash
tail -f application.log
```

文件增加新内容时，会实时输出。

Spring Boot 开发时非常实用。

---

# 33. 写入文件

使用：

```powershell
Set-Content
```

例如：

```powershell
Set-Content .\test.txt "Hello PowerShell"
```

注意：

`Set-Content` 默认会：

> 覆盖原内容。

---

# 34. 追加内容

使用：

```powershell
Add-Content
```

例如：

```powershell
Add-Content .\test.txt "Second Line"
```

文件：

```text
Hello PowerShell
Second Line
```

---

# 35. 输出重定向

PowerShell 也支持：

```powershell
"Hello" > test.txt
```

追加：

```powershell
"World" >> test.txt
```

但正式脚本中通常更建议：

```powershell
Set-Content
Add-Content
```

可读性更明确。

---

# 36. `Resolve-Path`

如果想把：

```text
.\logs
```

解析成完整路径：

```powershell
Resolve-Path .\logs
```

可能返回：

```text
C:\Projects\App\logs
```

---

# 37. `$PSScriptRoot`

这是以后写 `.ps1` 文件非常重要的变量。

假设：

```text
Project/
├── script.ps1
└── config/
    └── app.json
```

脚本：

```powershell
Get-Content ".\config\app.json"
```

看起来没问题。

但如果你在：

```text
C:\
```

执行：

```powershell
C:\Project\script.ps1
```

此时：

```text
.
```

通常指：

```text
C:\
```

不是：

```text
C:\Project
```

于是脚本找不到：

```text
.\config\app.json
```

---

正确做法：

```powershell
$configPath = Join-Path $PSScriptRoot "config\app.json"
```

这样：

```text
$PSScriptRoot
```

代表：

> 当前脚本文件所在目录。

所以以后写脚本时，经常应该使用：

```powershell
$PSScriptRoot
```

而不是依赖：

```powershell
$PWD
```

---

# 38. `$PWD` VS `$PSScriptRoot`

这个区别非常重要。

假设：

```text
C:\Projects\Demo\script.ps1
```

你现在位于：

```text
C:\Users\Ema
```

然后执行：

```powershell
C:\Projects\Demo\script.ps1
```

此时：

```text
$PWD
```

可能是：

```text
C:\Users\Ema
```

而：

```text
$PSScriptRoot
```

是：

```text
C:\Projects\Demo
```

所以：

```text
$PWD
=
当前 Shell 的工作目录

$PSScriptRoot
=
当前脚本所在目录
```

这一点以后写配置文件加载代码时非常关键。

---

# 39. PowerShell Provider

现在进入本课最特别的知识。

执行：

```powershell
Get-PSProvider
```

你可能看到：

```text
Name
----
Alias
Environment
FileSystem
Function
Registry
Variable
```

PowerShell 有一个非常有趣的设计：

> 它把很多不同的数据源抽象成“类似文件系统”的结构。

这就叫：

```text
PowerShell Provider
```

---

# 40. Drive

再执行：

```powershell
Get-PSDrive
```

可能看到：

```text
Name
----
C
D
Env
HKCU
HKLM
Variable
Alias
Function
```

你会发现：

```text
C:
D:
```

是磁盘。

但是：

```text
Env:
HKCU:
Variable:
Alias:
Function:
```

显然不是磁盘。

PowerShell 却允许你像浏览文件夹一样浏览它们。

这就是 Provider 的威力。

---

# 41. 环境变量其实是一个 Drive

例如：

```powershell
Set-Location Env:
```

然后：

```powershell
Get-ChildItem
```

你会看到：

```text
PATH
JAVA_HOME
TEMP
USERNAME
...
```

也就是说：

```text
Env:
```

像一个虚拟文件系统。

---

可以：

```powershell
Get-ChildItem Env:
```

查看全部环境变量。

也可以：

```powershell
Get-Item Env:JAVA_HOME
```

---

更常用的是：

```powershell
$env:JAVA_HOME
```

例如：

```powershell
$env:PATH
```

---

# 42. 临时修改环境变量

例如：

```powershell
$env:JAVA_HOME = "C:\Java\jdk-21"
```

注意：

这通常只影响：

> 当前 PowerShell 进程以及它启动的子进程。

关闭窗口后可能消失。

---

# 43. Registry Provider

Windows 注册表也能当成文件系统浏览。

例如：

```powershell
Get-ChildItem HKCU:
```

其中：

```text
HKCU
```

代表：

```text
HKEY_CURRENT_USER
```

而：

```text
HKLM
```

代表：

```text
HKEY_LOCAL_MACHINE
```

---

进入：

```powershell
Set-Location HKCU:
```

然后：

```powershell
Get-ChildItem
```

PowerShell 会像浏览目录一样浏览注册表。

这个概念在 Windows 自动化里非常强。

---

# 44. Variable Provider

执行：

```powershell
Get-ChildItem Variable:
```

你会看到当前 PowerShell 中的变量。

例如：

```text
HOME
PWD
PSVersionTable
Error
Host
```

所以：

```powershell
$HOME
```

背后也可以通过 Provider 查看：

```powershell
Get-Item Variable:HOME
```

---

# 45. Alias Provider

执行：

```powershell
Get-ChildItem Alias:
```

可以看到所有 Alias。

例如：

```text
ls
cat
cd
dir
gci
```

---

于是：

```powershell
Get-Item Alias:ls
```

就能看到 `ls` 指向什么。

---

# 46. Provider 的核心意义

把这些东西统一起来：

```text
文件系统
环境变量
注册表
变量
函数
Alias
```

PowerShell 给你一个相似的操作方式：

```powershell
Get-Item
Get-ChildItem
Set-Item
New-Item
Remove-Item
```

于是：

```text
不同系统资源
       ↓
统一为 Provider
       ↓
使用相似 Cmdlet 操作
```

这是 PowerShell 非常漂亮的设计之一。

---

# 47. Java 开发者视角理解 Provider

可以把 Provider 想象成：

```java
interface Provider {

    List<Item> getChildren();

    Item getItem(String path);

    void setItem(String path, Object value);

    void removeItem(String path);
}
```

然后：

```text
FileSystemProvider
RegistryProvider
EnvironmentProvider
VariableProvider
```

都实现统一接口。

PowerShell 上层就可以使用：

```powershell
Get-ChildItem
```

去操作不同数据源。

---

# 48. 小实验：比较三个 Provider

运行：

```powershell
Get-ChildItem C:\
```

然后：

```powershell
Get-ChildItem Env:
```

然后：

```powershell
Get-ChildItem Variable:
```

虽然背后的数据完全不同，却使用了同一个：

```powershell
Get-ChildItem
```

这就是 Provider。

---

# 49. 实战：找出 Downloads 中所有图片

```powershell
$downloads = Join-Path $HOME "Downloads"

Get-ChildItem $downloads -File |
    Where-Object Extension -In ".jpg", ".jpeg", ".png", ".webp"
```

---

# 50. 实战：找出 Downloads 最大的 10 个文件

```powershell
$downloads = Join-Path $HOME "Downloads"

Get-ChildItem $downloads -File |
    Sort-Object Length -Descending |
    Select-Object -First 10 Name,
        @{
            Name = "SizeMB"
            Expression = {
                [Math]::Round($_.Length / 1MB, 2)
            }
        }
```

---

# 51. 实战：搜索项目中的所有 `application.yml`

```powershell
Get-ChildItem C:\Projects `
    -Recurse `
    -File `
    -Filter application.yml
```

如果也想找：

```text
application.yaml
```

可以：

```powershell
Get-ChildItem C:\Projects -Recurse -File |
    Where-Object Name -In "application.yml", "application.yaml"
```

---

# 52. 实战：找到最近修改的文件

例如：

> 找出最近 24 小时修改的文件。

```powershell
Get-ChildItem C:\Projects -Recurse -File |
    Where-Object {
        $_.LastWriteTime -GT (Get-Date).AddDays(-1)
    }
```

这里非常有 PowerShell 风格。

因为：

```powershell
Get-Date
```

也是返回对象。

于是：

```powershell
(Get-Date).AddDays(-1)
```

调用：

```text
DateTime.AddDays()
```

方法。

---

# 53. 本课项目：Downloads 自动分类器

现在完成我们的第一个真正实用项目。

目标：

```text
Downloads/
├── Images/
├── Archives/
├── Documents/
├── Videos/
└── Others/
```

根据扩展名自动分类。

---

# 54. 第一步：获取 Downloads

```powershell
$downloads = Join-Path $HOME "Downloads"
```

---

# 55. 第二步：创建目标目录

```powershell
$folders = @(
    "Images",
    "Archives",
    "Documents",
    "Videos",
    "Others"
)
```

然后：

```powershell
foreach ($folder in $folders) {

    $path = Join-Path $downloads $folder

    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory
    }
}
```

这里提前使用了一点：

```powershell
foreach
```

下一阶段会正式学习。

现在只需要知道：

> 对 `$folders` 中的每个元素执行一次。

---

# 56. 第三步：定义扩展名

```powershell
$imageExtensions = @(
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp"
)
```

压缩文件：

```powershell
$archiveExtensions = @(
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz"
)
```

文档：

```powershell
$documentExtensions = @(
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".md"
)
```

视频：

```powershell
$videoExtensions = @(
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm"
)
```

---

# 57. 第四步：遍历文件

```powershell
Get-ChildItem $downloads -File |
    ForEach-Object {

        $file = $_

    }
```

这里：

```powershell
$_
```

就是当前正在处理的文件对象。

---

# 58. 第五步：判断扩展名

```powershell
if ($file.Extension -in $imageExtensions) {

}
elseif ($file.Extension -in $archiveExtensions) {

}
```

---

# 59. 完整版本

```powershell
$downloads = Join-Path $HOME "Downloads"

$imageExtensions = @(
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp"
)

$archiveExtensions = @(
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz"
)

$documentExtensions = @(
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".md"
)

$videoExtensions = @(
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm"
)

$folders = @(
    "Images",
    "Archives",
    "Documents",
    "Videos",
    "Others"
)

foreach ($folder in $folders) {

    $path = Join-Path $downloads $folder

    if (-not (Test-Path $path)) {
        New-Item `
            -Path $path `
            -ItemType Directory
    }
}

Get-ChildItem $downloads -File |
    ForEach-Object {

        $file = $_

        if ($file.Extension -in $imageExtensions) {
            $destination = Join-Path $downloads "Images"
        }
        elseif ($file.Extension -in $archiveExtensions) {
            $destination = Join-Path $downloads "Archives"
        }
        elseif ($file.Extension -in $documentExtensions) {
            $destination = Join-Path $downloads "Documents"
        }
        elseif ($file.Extension -in $videoExtensions) {
            $destination = Join-Path $downloads "Videos"
        }
        else {
            $destination = Join-Path $downloads "Others"
        }

        Move-Item `
            -Path $file.FullName `
            -Destination $destination
    }
```

---

# 60. 不要直接拿 Downloads 测试

> [!warning]
> 第一次运行时，不建议直接操作真实的 Downloads。

先创建实验目录：

```powershell
$test = Join-Path $HOME "PowerShell-Lab"

New-Item $test -ItemType Directory
```

创建一些测试文件：

```powershell
New-Item "$test\photo.jpg"
New-Item "$test\document.pdf"
New-Item "$test\archive.zip"
New-Item "$test\movie.mp4"
New-Item "$test\data.bin"
```

然后把脚本中的：

```powershell
$downloads = Join-Path $HOME "Downloads"
```

暂时改成：

```powershell
$downloads = Join-Path $HOME "PowerShell-Lab"
```

确认效果正确后再操作真实目录。

---

# 61. 更安全的调试方式：`-WhatIf`

移动文件时：

```powershell
Move-Item `
    -Path $file.FullName `
    -Destination $destination `
    -WhatIf
```

这样只展示：

```text
准备把什么文件移动到哪里
```

但不会真正移动。

这是以后写自动化脚本非常重要的习惯：

```text
先查询
   ↓
再预览
   ↓
最后执行
```

---

# 62. PowerShell 自动化安全习惯

建议形成以下流程：

```text
Get
↓
看看目标是什么

Test
↓
检查条件

-WhatIf
↓
模拟操作

确认结果
↓
真正执行
```

而不是直接：

```text
Remove
Move
Stop
```

---

# 63. 课堂练习 1

查看当前目录中：

> 所有 `.ps1` 文件。

要求使用：

```powershell
Get-ChildItem
```

---

# 64. 课堂练习 2

搜索：

```text
C:\Projects
```

下面所有：

```text
pom.xml
```

文件。

---

# 65. 课堂练习 3

找出当前目录：

> 最大的 3 个文件。

只显示：

```text
Name
Length
```

---

# 66. 课堂练习 4

找出当前目录：

> 最近 7 天修改过的文件。

提示：

```powershell
LastWriteTime
```

以及：

```powershell
(Get-Date).AddDays(-7)
```

---

# 67. 课堂练习 5

创建：

```text
PowerShell-Test/
├── src/
├── logs/
└── config/
```

要求只使用 PowerShell 命令。

---

# 68. 课堂练习 6

检查：

```text
config.json
```

是否存在。

如果存在：

```text
Config exists
```

否则：

```text
Config missing
```

---

# 69. 挑战题 1

找出：

```text
C:\Projects
```

下所有：

```text
.java
```

文件。

然后按照：

```text
文件大小
```

从大到小排序。

只显示：

```text
FullName
SizeKB
```

---

# 70. 挑战题 2

找出 Downloads 中：

> 超过 100MB 的文件。

提示：

```powershell
$_.Length -GT 100MB
```

---

# 71. 挑战题 3

找出当前项目中：

> 最近 24 小时修改过的 `.java` 文件。

组合使用：

```text
Extension
LastWriteTime
```

---

# 72. 参考答案

> [!warning]
> 推荐先自己完成。

## 练习 1

```powershell
Get-ChildItem -File -Filter *.ps1
```

---

## 练习 2

```powershell
Get-ChildItem C:\Projects `
    -Recurse `
    -File `
    -Filter pom.xml
```

---

## 练习 3

```powershell
Get-ChildItem -File |
    Sort-Object Length -Descending |
    Select-Object -First 3 Name, Length
```

---

## 练习 4

```powershell
Get-ChildItem -File |
    Where-Object {
        $_.LastWriteTime -GT (Get-Date).AddDays(-7)
    }
```

---

## 练习 5

```powershell
New-Item PowerShell-Test -ItemType Directory

New-Item PowerShell-Test\src `
    -ItemType Directory

New-Item PowerShell-Test\logs `
    -ItemType Directory

New-Item PowerShell-Test\config `
    -ItemType Directory
```

---

## 练习 6

```powershell
if (Test-Path .\config.json) {
    "Config exists"
}
else {
    "Config missing"
}
```

---

## 挑战题 1

```powershell
Get-ChildItem C:\Projects `
    -Recurse `
    -File `
    -Filter *.java |
    Sort-Object Length -Descending |
    Select-Object FullName,
        @{
            Name = "SizeKB"
            Expression = {
                [Math]::Round($_.Length / 1KB, 2)
            }
        }
```

---

## 挑战题 2

```powershell
Get-ChildItem (Join-Path $HOME "Downloads") -File |
    Where-Object {
        $_.Length -GT 100MB
    } |
    Select-Object Name,
        @{
            Name = "SizeMB"
            Expression = {
                [Math]::Round($_.Length / 1MB, 2)
            }
        }
```

---

## 挑战题 3

```powershell
Get-ChildItem -Recurse -File |
    Where-Object {
        $_.Extension -eq ".java" -and
        $_.LastWriteTime -gt (Get-Date).AddDays(-1)
    }
```

---

# 73. 本课重点命令

```powershell
Get-Location
```

查看当前目录。

```powershell
Set-Location
```

切换目录。

```powershell
Get-ChildItem
```

列出子项。

```powershell
Get-Item
```

获取某个项目。

```powershell
New-Item
```

创建。

```powershell
Copy-Item
```

复制。

```powershell
Move-Item
```

移动。

```powershell
Rename-Item
```

重命名。

```powershell
Remove-Item
```

删除。

```powershell
Test-Path
```

检查路径。

```powershell
Resolve-Path
```

解析路径。

```powershell
Join-Path
```

组合路径。

```powershell
Get-Content
```

读取内容。

```powershell
Set-Content
```

覆盖写入。

```powershell
Add-Content
```

追加内容。

```powershell
Get-PSProvider
```

查看 Provider。

```powershell
Get-PSDrive
```

查看 PowerShell Drive。

---

# 74. 本课必须掌握的自动变量

```powershell
$HOME
```

用户 Home 目录。

```powershell
$PWD
```

当前工作目录。

```powershell
$PSScriptRoot
```

当前脚本所在目录。

```powershell
$_
```

当前 Pipeline 对象。

```powershell
$env:PATH
```

环境变量访问方式。

---

# 75. 本课核心知识地图

```text
PowerShell 路径
│
├── FileSystem
│   ├── C:
│   └── D:
│
├── Env:
│   └── 环境变量
│
├── HKCU:
│   └── 注册表
│
├── Variable:
│   └── PowerShell 变量
│
├── Alias:
│   └── 命令别名
│
└── Function:
    └── PowerShell 函数
```

它们背后虽然完全不同：

```text
磁盘
环境变量
注册表
变量
Alias
```

但是 PowerShell 通过：

```text
Provider
```

为它们提供统一的操作模型。

---

# 76. 第一课和第二课串起来

第一课我们学到：

```text
Cmdlet
  ↓
Object
  ↓
Pipeline
```

第二课则变成：

```text
Get-ChildItem
      ↓
FileInfo Object
      ↓
Where-Object
      ↓
Sort-Object
      ↓
Select-Object
```

例如：

```powershell
Get-ChildItem C:\Projects -Recurse -File |
    Where-Object Extension -eq ".java" |
    Sort-Object Length -Descending |
    Select-Object -First 10 Name, Length
```

这已经是一个完整的：

```text
查询
↓
过滤
↓
排序
↓
投影
```

数据处理流程。

---

# 77. 本课一句话总结

> **PowerShell 不只是把磁盘当成文件系统，它把很多系统资源都抽象成可以通过统一 Cmdlet 操作的 Provider。**

同时牢记：

```text
$PWD
=
我现在站在哪里

$PSScriptRoot
=
这个脚本住在哪里
```

这两个概念以后写自动化脚本时会反复出现。

---

# 下一课

## PowerShell 课程 03：对象管道深入

下一课将真正深入 PowerShell 最核心的部分：

* `Where-Object`
* `Select-Object`
* `Sort-Object`
* `ForEach-Object`
* `Group-Object`
* `Measure-Object`
* `Tee-Object`
* `Compare-Object`
* `$_`
* ScriptBlock
* 计算属性
* 对象投影
* Pipeline 参数绑定
* Java Stream 与 PowerShell Pipeline 对照

并完成：

> **进程与系统资源分析器**

最终可以做到类似：

```text
Top CPU Processes
Top Memory Processes
Process Count By Name
Total Memory Usage
Java Process Analysis
```

这一课会是 PowerShell 整个课程里非常核心的一节。
