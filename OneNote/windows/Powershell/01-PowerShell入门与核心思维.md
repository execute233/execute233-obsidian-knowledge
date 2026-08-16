---
title: PowerShell 入门与核心思维
tags: [powershell, 入门, 核心思维]
aliases: [PowerShell Intro, PowerShell Beginner, PowerShell Basics]
---

# PowerShell 入门与核心思维

> [!abstract]
> 本课重点：
>
> * PowerShell 不只是 CMD 升级版，而是"以 .NET 对象为核心的数据处理与自动化 Shell"
> * 区分 PowerShell、CMD、Bash
> * `Cmdlet` 与 Verb-Noun 命名
> * 一切皆对象
> * 初步理解 Pipeline：对象在命令之间流动
> * `Get-Command` / `Get-Help` / `Get-Member` 三大自学习工具
> * 实战：Java 进程、内存 Top、服务查询

---

# 1. PowerShell 是什么

PowerShell 同时包含三个东西：

```text
PowerShell
├── Shell
├── 脚本语言
└── 自动化平台
```

既能像 CMD、Bash 一样使用：

```powershell
cd C:\Projects
ls
```

也能编写完整程序：

```powershell
$name = "Spring Boot"

if ($name -eq "Spring Boot") {
    Write-Output "这是一个 Java 项目"
}
```

还能管理进程、服务、注册表，调用 REST API、JSON、文件批量、服务器、Git、Docker、Java、Maven/Gradle、CI/CD 脚本。

更准确的理解：

> 以 .NET 对象为核心的数据处理与自动化 Shell。

---

# 2. PowerShell、CMD、Bash 的区别

以"找出 Java 进程"为例。

CMD：

```cmd
tasklist | findstr java
```

Bash：

```bash
ps aux | grep java
```

PowerShell：

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*"
```

表面看起来差不多，但背后的思维完全不同。

---

# 3. 文本 Shell vs 对象 Shell

## 3.1 Bash / CMD 的思维

传统 Shell 围绕"文本"工作：

```bash
ps aux
```

输出类似：

```text
root      1234  0.3  java ...
user      5678  0.1  nginx ...
```

然后：

```bash
ps aux | grep java
```

本质是：

```text
程序
 ↓
生成字符串
 ↓
grep 搜索字符串
```

经常用到 `grep` / `awk` / `sed` / `cut` / `sort` / `xargs`，因为需要不停处理文本。

## 3.2 PowerShell 的对象思维

```powershell
Get-Process
```

虽然显示类似：

```text
 NPM(K)    PM(M)     WS(M)    CPU(s)      Id  SI ProcessName
 ------    -----     -----    ------      --  -- -----------
     20    50.22     120.30     8.12    1234   1 chrome
     30   150.12     300.22    20.53    5678   1 java
```

但实际上返回的是 `System.Diagnostics.Process` 对象：

```text
.NET Process 对象
   ├── Id
   ├── ProcessName
   ├── CPU
   ├── WorkingSet64
   └── ...
```

Java 类比：

```java
class Process {
    int id;
    String processName;
    double cpu;
    void kill() { }
}
```

PowerShell 可以直接：

```powershell
$process.Id
$process.ProcessName
$process.CPU
```

而不是去解析字符串。

---

# 4. 第一个重要实验

```powershell
Get-Process | Get-Member
```

可能看到：

```text
TypeName: System.Diagnostics.Process

Name             MemberType
----             ----------
Kill             Method
Start            Method
CPU              Property
Id               Property
ProcessName      Property
WorkingSet64     Property
...
```

这说明 PowerShell 真正返回的是有属性、有方法的对象。`Get-Process` 产生 `Process` 对象，`Get-Member` 可以观察对象结构。

---

# 5. Pipeline：对象在命令之间流动

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*" |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 5 ProcessName, Id, WorkingSet64
```

逻辑图：

```text
Get-Process
      │ Process 对象
      ▼
Where-Object
      │ 过滤后的 Process 对象
      ▼
Sort-Object
      │ 排序后的 Process 对象
      ▼
Select-Object
      │ 投影后的新对象
      ▼
输出
```

PowerShell Pipeline 传递的是 `.NET` 对象，而不是字符串。这是 PowerShell 与传统 Shell 最核心的区别。

---

# 6. Pipeline 与 Java Stream 的对照

PowerShell：

```powershell
Get-Process |
    Where-Object WorkingSet64 -gt 500MB |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 5 ProcessName, Id
```

Java Stream：

```java
processes.stream()
    .filter(p -> p.getWorkingSet64() > MB * 500)
    .sorted(
        comparing(Process::getWorkingSet64).reversed()
    )
    .limit(5)
    .map(p -> new ProcView(p.getProcessName(), p.getId()))
    .toList();
```

> [!tip]
> 这是数据处理思路的对照，不意味着 PowerShell Pipeline 与 Java Stream 在执行模型上完全相同。

---

# 7. Cmdlet

`Cmdlet` 是 PowerShell 的内置命令，命名遵循 `Verb-Noun` 模式：

```powershell
Get-Process
Get-Service
Get-ChildItem
Get-Help
Get-Command
Get-Member
Set-Location
New-Item
Remove-Item
Where-Object
Select-Object
Sort-Object
ForEach-Object
Group-Object
Measure-Object
```

`Verb-Noun` 设计让命令高度可预测。看到 `Get-` 就知道是"获取"，看到 `-Process` / `-Service` / `-ChildItem` 就知道目标对象。

PowerShell 7.6 官方文档将 Cmdlet 定义为内置命令，通常遵循 `Verb-Noun` 命名。

---

# 8. Get-Command：寻找命令

```powershell
Get-Command Get-Process

Get-Command -Verb Get

Get-Command -Noun Process
```

不确定命令名时，可以按 Verb 或 Noun 过滤查找。

---

# 9. Get-Help：学习一个命令

```powershell
Get-Help Get-Process

Get-Help Get-Process -Examples

Get-Help Get-Process -Full
```

`-Examples` 直接展示示例；`-Full` 显示参数说明、输入输出类型等。

---

# 10. Get-Member：观察对象

```powershell
Get-Process | Get-Member
```

列出当前命令输出对象的属性与方法。这是探索 PowerShell 对象最快的方式。

---

# 11. 不要背 PowerShell 命令

记忆负担很重。推荐工作流：

```text
1. 不知道命令 → Get-Command
2. 不会用 →     Get-Help -Examples / -Full
3. 想看对象 →   Get-Member
```

熟练以后自然记住常用命令。

---

# 12. PowerShell 中的变量

变量以 `$` 开头：

```powershell
$processes = Get-Process
$name = "java"
```

变量名不区分大小写。

PowerShell 变量默认没有固定类型约束，同一个变量可先后保存整数、字符串、对象。下一课会详细讲。

---

# 13. 属性访问

```powershell
$process = Get-Process -Name pwsh -ErrorAction SilentlyContinue | Select-Object -First 1

$process.Id
$process.ProcessName
$process.WorkingSet64
```

PowerShell 7 中更安全写法：

```powershell
if ($null -ne $process) {
    $process.ProcessName
}
```

（`$null` 在比较运算符左侧的原因见下一课。）

---

# 14. Select-Object：选择属性

```powershell
Get-Process |
    Select-Object ProcessName, Id
```

只投影需要的字段。这是 Pipeline 中非常重要的"对象瘦身"步骤。

---

# 15. Where-Object：过滤对象

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*"
```

只保留满足条件的对象。

---

# 16. $_ 是什么意思

```powershell
Get-Process |
    Where-Object {
        $_.WorkingSet64 -gt 500MB
    }
```

`$_` 代表 Pipeline 中当前正在处理的对象。`Where-Object` / `ForEach-Object` 等 ScriptBlock 中经常用到。

Java Lambda 对照：

```java
processes.stream()
    .filter(p -> p.getWorkingSet64() > MB * 500);
```

`$_` 类似 lambda 里的参数 `p`。

---

# 17. Alias：PowerShell 的快捷命令

```powershell
Get-Alias
```

可看到大量常用别名：

```text
ls   → Get-ChildItem
dir  → Get-ChildItem
cat  → Get-Content
cp   → Copy-Item
mv   → Move-Item
rm   → Remove-Item
gci  → Get-ChildItem
```

别名是为了让有 Bash / CMD 经验的用户更快过渡。但生产脚本推荐使用完整 Cmdlet 名，便于阅读。

---

# 18. Windows PowerShell 与 PowerShell

```text
Windows PowerShell 5.1   内置于 Windows，基于 .NET Framework
PowerShell 7              跨平台，基于 .NET Core / .NET 5+
```

新项目应该使用 PowerShell 7。本课程示例默认基于 PowerShell 7.6 官方文档。

---

# 19. PowerShell 命令的基本结构

```powershell
Get-Process -Name java -ErrorAction SilentlyContinue
```

结构：

```text
Cmdlet 名
↓
参数 -Name
↓
参数值 java
↓
公共参数 -ErrorAction
↓
公共参数值 SilentlyContinue
```

公共参数可被大多数 Cmdlet 接受，例如：

```text
-ErrorAction      遇到错误时怎么办
-Verbose          显示详细输出
-Debug            进入调试
-WarningAction    处理警告
```

---

# 20. 参数补全

PowerShell 提供强大的 Tab 补全：

```text
Tab          补全命令名 / 参数名
Tab          参数值（部分命令支持）
```

例如输入 `Get-` 后按 Tab，会依次循环所有 `Get-*` 命令。这是日常使用的加速器。

---

# 21. 第一套"生存命令"

```powershell
Get-Process
Get-Service
Get-ChildItem
Get-Help
Get-Command
Get-Member
Get-Location
Set-Location
Get-Content
Select-Object
Where-Object
Sort-Object
ForEach-Object
```

记住这一套基本可以开始用 PowerShell 了。

---

# 22. 实战：寻找 Java 进程

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*" |
    Sort-Object Id |
    Select-Object Id, ProcessName, StartTime
```

---

# 23. 实战：寻找最吃内存的程序

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 `
        ProcessName,
        Id,
        @{
            Name = "MemoryMB"
            Expression = {
                [Math]::Round(
                    $_.WorkingSet64 / 1MB,
                    2
                )
            }
        }
```

`@{}` 是 Calculated Property，后面会详细讲。

---

# 24. 实战：查询 Windows 服务

```powershell
Get-Service |
    Where-Object Status -eq "Running"
```

---

# 25. PowerShell 运算符的特殊之处

PowerShell 运算符与传统语言不一样：

```text
==   → -eq
!=   → -ne
>    → -gt
<    → -lt
&&   → -and
||   → -or
!    → -not
```

字符串比较默认忽略大小写：

```powershell
"PowerShell" -eq "powershell"      # True
```

集合与标量比较返回匹配元素：

```powershell
1, 2, 3 -eq 2     # 2
```

下一课会深入讲解。

---

# 26. 本课核心思维模型

```text
Cmdlet
  ↓
输出 .NET 对象
  ↓
进入 Pipeline
  ↓
Where-Object 过滤
  ↓
Sort-Object 排序
  ↓
Select-Object 投影
  ↓
新对象
```

一句话：

> **PowerShell = 对象 + Pipeline + Cmdlet。**

---

# 27. 自学习工作流

```text
不知道命令名     → Get-Command -Verb / -Noun
不会用           → Get-Help -Examples / -Full
想看对象结构     → Get-Member
想看对象属性值   → 直接访问或 Select-Object
```

习惯这套工作流后，PowerShell 的学习成本会大幅下降。

---

# 28. 本课需要掌握

* [ ] 知道 PowerShell 是什么，与 CMD / Bash 的核心区别
* [ ] 理解"对象 vs 文本"是 PowerShell 的根本思维
* [ ] 知道 `Cmdlet` 与 `Verb-Noun` 命名规则
* [ ] 能用 `Get-Command` / `Get-Help` / `Get-Member` 自学命令
* [ ] 理解 Pipeline 传递的是对象
* [ ] 知道 `$_` 的作用
* [ ] 能用 `Select-Object` / `Where-Object` / `Sort-Object`
* [ ] 理解 Alias 与完整 Cmdlet 的关系
* [ ] 知道 Windows PowerShell 与 PowerShell 7 的差别
* [ ] 能写出第一组 Java 进程 / 内存 Top / Windows 服务查询

---

# 下一课

下一节：

[[02-文件系统、路径与Provider]]

重点：

* 浏览文件系统
* 相对路径 / 绝对路径
* `$HOME` / `$PWD` / `$PSScriptRoot`
* `Get-ChildItem` / `New-Item` / `Copy-Item` / `Move-Item` / `Remove-Item`
* `Get-Content` / `Set-Content`
* PowerShell Provider
* 实战：Downloads 自动分类器

---

# 相关笔记

* [[02-文件系统、路径与Provider]]
* [[03-对象管道深入-过滤、投影、转换、分组与统计]]
* [[04-变量、类型、集合与运算符]]
* [[PowerShell 对象]]
* [[PowerShell Cmdlet]]
* [[PowerShell Pipeline]]