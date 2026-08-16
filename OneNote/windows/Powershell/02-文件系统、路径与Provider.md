---
title: PowerShell 文件系统、路径与 Provider
tags: [powershell, 文件系统, 路径, provider]
aliases: [PowerShell File System, PowerShell Files, PowerShell Provider]
---

# PowerShell 文件系统、路径与 Provider

> [!abstract]
> 本课重点：
>
> * 浏览文件系统
> * 理解相对路径与绝对路径
> * 创建、复制、移动、重命名与删除文件
> * 通配符与递归搜索
> * `$HOME`、`$PWD`、`$PSScriptRoot`
> * PowerShell Provider：把环境变量、注册表、变量、Alias 当成文件系统操作
> * 实战：Downloads 自动分类器

---

# 1. 从 `cd` 和 `ls` 开始

`cd`、`ls` 在 PowerShell 里其实只是别名：

```powershell
Get-Alias cd
Get-Alias ls
```

可能看到：

```text
cd -> Set-Location
ls -> Get-ChildItem
```

PowerShell 原生命令是 `Set-Location` 与 `Get-ChildItem`。

---

# 2. 查看当前位置

```powershell
Get-Location
```

或者：

```powershell
$PWD
$PWD.Path
```

`$PWD` 是自动变量，保存当前 PowerShell 工作目录。

---

# 3. 切换目录

```powershell
Set-Location C:\Projects

Set-Location .\Demo

Set-Location ..
```

简写：`cd`、`cd ..`。

---

# 4. 相对路径与绝对路径

绝对路径：

```text
C:\Projects\PowerShell\demo.ps1
```

相对路径以 `.` 表示当前目录，以 `..` 表示父目录：

```powershell
Get-Item .\demo.ps1
Get-ChildItem ..
```

---

# 5. `$HOME`

`$HOME` 表示当前用户的 Home 目录，通常类似：

```text
C:\Users\Ema
```

```powershell
Get-ChildItem $HOME
```

写跨机器脚本时推荐使用：

```powershell
$downloadPath = "$HOME\Downloads"
```

而不是写死 `C:\Users\Ema\Downloads`。

---

# 6. 路径拼接：Join-Path

```powershell
$downloads = Join-Path $HOME "Downloads"
$images    = Join-Path $downloads "Images"
```

直接字符串拼接 `$HOME + "\Downloads"` 容易出现 `\` `/` 混用，PowerShell 7 跨平台时更容易出问题。`Join-Path` 自动适配分隔符。

---

# 7. Get-ChildItem

这是文件操作中最重要的命令之一。

```powershell
Get-ChildItem                # 列出当前目录
Get-ChildItem -File          # 只看文件
Get-ChildItem -Directory     # 只看目录
Get-ChildItem C:\Projects    # 指定路径
```

常见别名：`ls`、`dir`、`gci`。

`Get-ChildItem` 返回的是 `FileInfo` / `DirectoryInfo` 对象，不是字符串。

---

# 8. 文件对象属性

```powershell
$file = Get-ChildItem -File | Select-Object -First 1

$file.Name
$file.FullName
$file.Extension
$file.Length
$file.CreationTime
$file.LastWriteTime
```

---

# 9. 计算文件大小 MB

PowerShell 支持 `1KB` / `1MB` / `1GB` / `1TB` 等二进制乘数：

```powershell
$file.Length / 1MB
```

找出当前目录最大的 5 个文件：

```powershell
Get-ChildItem -File |
    Sort-Object Length -Descending |
    Select-Object -First 5 Name,
        @{
            Name = "SizeMB"
            Expression = {
                [Math]::Round($_.Length / 1MB, 2)
            }
        }
```

---

# 10. 递归搜索

```powershell
Get-ChildItem C:\Projects -Recurse -File
```

表示找出 `C:\Projects` 下所有文件。

---

# 11. Filter 与通配符

```powershell
Get-ChildItem -Filter *.log
Get-ChildItem -Filter *.json
```

通配符：

```text
*  匹配任意数量字符
?  匹配一个字符
```

例如 `file?.txt` 可匹配 `file1.txt`、`fileA.txt`，但不匹配 `file10.txt`。

---

# 12. 使用对象属性过滤

```powershell
Get-ChildItem -File |
    Where-Object Extension -EQ ".log"
```

多种类型：

```powershell
Get-ChildItem -File |
    Where-Object Extension -In ".jpg", ".png", ".webp"
```

`-in` 表示当前值是否存在于某个集合，相当于 Java 的 `contains`。

---

# 13. New-Item

```powershell
New-Item test.txt                        # 默认创建文件
New-Item -Path test.txt -ItemType File
New-Item -Path Images   -ItemType Directory
```

目录已存在时会报错，更安全的写法：

```powershell
if (-not (Test-Path Images)) {
    New-Item Images -ItemType Directory
}
```

---

# 14. Test-Path

```powershell
Test-Path ".\config.json"
```

返回 `True` / `False`：

```powershell
if (Test-Path ".\config.json") {
    "配置文件存在"
}
```

---

# 15. Get-Item

`Get-ChildItem` 获取目录中的子项，`Get-Item` 获取指定项目：

```powershell
$file = Get-Item .\application.log

$file.Length
$file.FullName
$file.LastWriteTime
```

---

# 16. Copy-Item

```powershell
Copy-Item .\test.txt .\backup\

Copy-Item .\test.txt .\backup\test-backup.txt

Copy-Item .\config .\backup -Recurse
```

---

# 17. Move-Item

```powershell
Move-Item .\test.txt .\Documents\

Move-Item .\Images .\Backup\
```

---

# 18. Rename-Item

```powershell
Rename-Item .\test.txt demo.txt
```

---

# 19. Remove-Item

```powershell
Remove-Item .\test.txt

Remove-Item .\Demo -Recurse
```

强制删除：

```powershell
Remove-Item .\Demo -Recurse -Force
```

> [!warning]
> `Remove-Item -Recurse -Force` 是危险操作，不要对不确定路径直接执行。

---

# 20. -WhatIf

很多破坏性 Cmdlet 支持 `-WhatIf`：

```powershell
Remove-Item .\Demo -Recurse -WhatIf
```

只显示：

```text
What if: Performing the operation "Remove Directory"...
```

不会真正删除。

---

# 21. -Confirm

```powershell
Remove-Item .\test.txt -Confirm
```

PowerShell 会要求确认。

---

# 22. Get-Content

```powershell
Get-Content .\application.log
```

常见别名：`cat`、`gc`。

只读最后 20 行：

```powershell
Get-Content .\application.log -Tail 20
```

类似 Linux `tail -n 20`。

实时查看日志：

```powershell
Get-Content .\application.log -Tail 20 -Wait
```

类似 `tail -f`，Spring Boot 开发时常用。

---

# 23. Set-Content / Add-Content

覆盖写入：

```powershell
Set-Content .\test.txt "Hello PowerShell"
```

追加：

```powershell
Add-Content .\test.txt "Second Line"
```

---

# 24. 输出重定向

```powershell
"Hello" > test.txt
"World" >> test.txt
```

正式脚本更建议用 `Set-Content` / `Add-Content`，可读性更明确。

---

# 25. Resolve-Path

```powershell
Resolve-Path .\logs
```

把相对路径解析成完整路径，例如 `C:\Projects\App\logs`。

---

# 26. $PSScriptRoot

`$PSScriptRoot` 表示当前脚本文件所在目录。

假设：

```text
Project/
├── script.ps1
└── config/
    └── app.json
```

```powershell
$configPath = Join-Path $PSScriptRoot "config\app.json"
```

这是写 `.ps1` 脚本加载配置的标准方式。

---

# 27. $PWD vs $PSScriptRoot

假设 `C:\Projects\Demo\script.ps1`，执行时位于 `C:\Users\Ema`：

```text
$PWD         = 当前 Shell 的工作目录
$PSScriptRoot = 当前脚本所在目录
```

写配置文件加载代码时优先使用 `$PSScriptRoot`，否则脚本运行时的 `$PWD` 不一定是脚本所在目录。

---

# 28. PowerShell Provider

```powershell
Get-PSProvider
```

可能看到：

```text
Alias
Environment
FileSystem
Function
Registry
Variable
```

PowerShell 把不同数据源（文件系统、环境变量、注册表、变量、Alias、函数）抽象成"类似文件系统"的统一结构，称为 `Provider`。

---

# 29. Get-PSDrive

```powershell
Get-PSDrive
```

可能看到：

```text
C
D
Env
HKCU
HKLM
Variable
Alias
Function
```

`C:`、`D:` 是磁盘；`Env:`、`HKCU:`、`Variable:`、`Alias:`、`Function:` 显然不是磁盘，但可按类似方式浏览。

---

# 30. Env Drive

```powershell
Set-Location Env:

Get-ChildItem
```

```text
PATH
JAVA_HOME
TEMP
USERNAME
...
```

读取单个环境变量：

```powershell
$env:JAVA_HOME
```

修改（仅当前进程有效）：

```powershell
$env:JAVA_HOME = "C:\Java\jdk-21"
```

---

# 31. Registry Provider

```powershell
Get-ChildItem HKCU:
```

`HKCU` = `HKEY_CURRENT_USER`，`HKLM` = `HKEY_LOCAL_MACHINE`。

```powershell
Set-Location HKCU:
Get-ChildItem
```

PowerShell 会像浏览目录一样浏览注册表。

---

# 32. Variable Provider

```powershell
Get-ChildItem Variable:
```

显示当前 PowerShell 中的变量，例如 `HOME`、`PWD`、`PSVersionTable`、`Error`、`Host`。

---

# 33. Alias Provider

```powershell
Get-ChildItem Alias:
```

```text
ls
cat
cd
dir
gci
```

---

# 34. Provider 的核心意义

```text
文件系统 / 环境变量 / 注册表 / 变量 / Alias / 函数
        ↓
统一为 Provider
        ↓
使用相似 Cmdlet 操作

Get-Item
Get-ChildItem
Set-Item
New-Item
Remove-Item
```

这是 PowerShell 非常漂亮的设计之一。

---

# 35. 小实验

```powershell
Get-ChildItem C:\

Get-ChildItem Env:

Get-ChildItem Variable:
```

三个完全不同的数据源，背后却使用了同一个 `Get-ChildItem`，这就是 Provider。

---

# 36. 实战：找出 Downloads 中的图片

```powershell
$downloads = Join-Path $HOME "Downloads"

Get-ChildItem $downloads -File |
    Where-Object Extension -In ".jpg", ".jpeg", ".png", ".webp"
```

---

# 37. 实战：Downloads 最大的 10 个文件

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

# 38. 实战：搜索所有 application.yml

```powershell
Get-ChildItem C:\Projects -Recurse -File -Filter application.yml
```

同时找 `application.yaml`：

```powershell
Get-ChildItem C:\Projects -Recurse -File |
    Where-Object Name -In "application.yml", "application.yaml"
```

---

# 39. 实战：最近 24 小时修改的文件

```powershell
Get-ChildItem C:\Projects -Recurse -File |
    Where-Object {
        $_.LastWriteTime -GT (Get-Date).AddDays(-1)
    }
```

`Get-Date` 返回 `DateTime` 对象，`.AddDays(-1)` 调用其方法，体现了 PowerShell 的 Object-first 思维。

---

# 40. 实战：Downloads 自动分类器

目标：

```text
Downloads/
├── Images/
├── Archives/
├── Documents/
├── Videos/
└── Others/
```

按扩展名自动分类。

完整脚本：

```powershell
$downloads = Join-Path $HOME "Downloads"

$imageExtensions = @(
    ".jpg", ".jpeg", ".png", ".gif", ".webp"
)

$archiveExtensions = @(
    ".zip", ".7z", ".rar", ".tar", ".gz"
)

$documentExtensions = @(
    ".pdf", ".doc", ".docx",
    ".xls", ".xlsx",
    ".ppt", ".pptx",
    ".txt", ".md"
)

$videoExtensions = @(
    ".mp4", ".mkv", ".avi", ".mov", ".webm"
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

# 41. 不要直接拿 Downloads 测试

> [!warning]
> 第一次运行时，不建议直接操作真实的 Downloads。

先创建实验目录：

```powershell
$test = Join-Path $HOME "PowerShell-Lab"

New-Item $test -ItemType Directory

New-Item "$test\photo.jpg"
New-Item "$test\document.pdf"
New-Item "$test\archive.zip"
New-Item "$test\movie.mp4"
New-Item "$test\data.bin"
```

把脚本中 `$downloads` 临时改成 `$HOME\PowerShell-Lab`，确认效果后再操作真实目录。

---

# 42. 更安全的调试方式：-WhatIf

```powershell
Move-Item `
    -Path $file.FullName `
    -Destination $destination `
    -WhatIf
```

只展示"准备把什么文件移动到哪里"，不会真正移动。

---

# 43. PowerShell 自动化安全习惯

```text
Get      看看目标是什么
Test     检查条件
-WhatIf  模拟操作
确认结果
真正执行
```

而不是直接：

```text
Remove / Move / Stop
```

---

# 44. 本课需要掌握

* [ ] 知道 `cd`/`ls` 是 `Set-Location`/`Get-ChildItem` 的别名
* [ ] 理解 `$PWD`、`$HOME`、`$PSScriptRoot`
* [ ] 熟练使用 `Get-ChildItem`、`New-Item`、`Copy-Item`、`Move-Item`、`Remove-Item`、`Rename-Item`
* [ ] 理解绝对路径与相对路径
* [ ] 知道 `Join-Path` 比字符串拼接更稳
* [ ] 能用 `-Recurse` / `-Filter` 搜索文件
* [ ] 能用 `Where-Object` 按属性过滤
* [ ] 知道 `Get-Content` 的 `-Tail` / `-Wait`
* [ ] 理解 PowerShell Provider 的概念
* [ ] 能浏览 `Env:`、`HKCU:`、`Variable:`、`Alias:`
* [ ] 形成 Get / Test / -WhatIf / 执行的自动化习惯

---

# 下一课

下一节：

[[03-对象管道深入-过滤、投影、转换、分组与统计]]

重点：

* Pipeline 传递什么
* `$_` 与 ScriptBlock
* `Where-Object`、`Select-Object`、`Sort-Object`
* `ForEach-Object`、`Group-Object`、`Measure-Object`
* `Tee-Object`、`Compare-Object`
* Calculated Property
* Parameter Binding：`ByValue` / `ByPropertyName`
* 与 Java Stream 对照

---

# 相关笔记

* [[01-PowerShell入门与核心思维]]
* [[03-对象管道深入-过滤、投影、转换、分组与统计]]
* [[04-变量、类型、集合与运算符]]
* [[PowerShell Provider]]
* [[PowerShell Pipeline]]