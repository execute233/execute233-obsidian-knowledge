# PowerShell 课程 01：PowerShell 入门与核心思维

> [!info] 本课目标
> 学完这一课，你应该能够：
>
> * 理解 PowerShell 到底是什么
> * 区分 PowerShell、CMD、Bash
> * 理解 `Cmdlet`
> * 理解 PowerShell 的「对象」思想
> * 初步理解对象管道
> * 学会自己查找 PowerShell 命令
> * 学会使用 `Get-Command`、`Get-Help`、`Get-Member`
> * 能够组合几个简单命令完成实际任务

---

# 1. PowerShell 到底是什么？

很多人第一次看到 PowerShell，会把它理解成：

> Windows 上更高级的 CMD。

这个理解不能说完全错误，但严重低估了 PowerShell。

PowerShell 实际上同时包含三个东西：

```text
PowerShell
├── Shell
├── 脚本语言
└── 自动化平台
```

也就是说，你既可以像使用 CMD、Bash 一样：

```powershell
cd C:\Projects
ls
```

也可以编写完整程序：

```powershell
$name = "Spring Boot"

if ($name -eq "Spring Boot") {
    Write-Output "这是一个 Java 项目"
}
```

甚至可以：

* 管理进程
* 管理 Windows 服务
* 查询端口
* 操作注册表
* 调用 REST API
* 处理 JSON
* 操作文件
* 批量管理服务器
* 调用 Git
* 调用 Docker
* 调用 Java
* 调用 Maven / Gradle
* 编写 CI/CD 脚本

所以 PowerShell 更准确的理解是：

> **以 .NET 对象为核心的数据处理与自动化 Shell。**

---

# 2. PowerShell、CMD、Bash 有什么区别？

先看三个 Shell 做同一件事：

> 找出 Java 进程。

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

表面看起来差不多。

但是它们背后的思维完全不同。

---

# 3. 文本 Shell 与对象 Shell

## 3.1 Bash / CMD 的典型思维

传统 Shell 很大程度上围绕：

```text
文本
```

例如：

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

本质上是在：

```text
程序
 ↓
生成字符串
 ↓
grep 搜索字符串
```

于是经常会见到：

```bash
grep
awk
sed
cut
sort
xargs
```

因为你需要不停地处理文本。

---

# 4. PowerShell 的核心：对象

PowerShell 的思路不同。

执行：

```powershell
Get-Process
```

你看到的虽然是：

```text
 NPM(K)    PM(M)     WS(M)    CPU(s)      Id  SI ProcessName
 ------    -----     -----    ------      --  -- -----------
     20    50.22     120.30     8.12    1234   1 chrome
     30   150.12     300.22    20.53    5678   1 java
```

但这里有一个非常重要的地方：

> **这并不是普通文本。**

PowerShell 实际返回的是：

```text
System.Diagnostics.Process
```

也就是：

```text
.NET Process 对象
```

---

# 5. 第一个重要实验

执行：

```powershell
Get-Process
```

然后执行：

```powershell
Get-Process | Get-Member
```

你会看到类似：

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

这里揭示了 PowerShell 最重要的一件事情：

```text
Get-Process
      ↓
产生
      ↓
Process 对象
```

而这个对象有：

```text
属性 Property
方法 Method
```

如果主人有 Java 基础，可以直接这么理解：

```java
class Process {

    int id;

    String processName;

    double cpu;

    void kill() {
    }

}
```

PowerShell 得到的实际上类似：

```powershell
$process.Id
$process.ProcessName
$process.CPU
```

而不是去解析一行字符串。

---

# 6. PowerShell 对 Java 开发者为什么很好理解？

例如：

```powershell
$p = Get-Process -Name java
```

现在：

```powershell
$p
```

其实就相当于：

```java
Process p;
```

然后：

```powershell
$p.Id
```

相当于：

```java
p.getId();
```

再比如：

```powershell
$p.ProcessName
```

类似：

```java
p.getProcessName();
```

所以 PowerShell 的：

```text
对象
属性
方法
类型
```

和 Java / C# 的对象模型非常接近。

---

# 7. PowerShell 的管道

PowerShell 最经典的符号：

```text
|
```

叫：

```text
Pipeline
管道
```

例如：

```powershell
Get-Process |
    Where-Object CPU -GT 10
```

很多初学者会理解成：

```text
Get-Process 输出文本
        ↓
Where-Object 过滤文本
```

实际上不是。

真正发生的是：

```text
Get-Process

      ↓

Process Object
Process Object
Process Object
Process Object

      ↓

Where-Object

      ↓

判断每个 Process.CPU

      ↓

符合条件的 Process Object
```

也就是：

```text
对象 → 对象 → 对象
```

---

# 8. 一个非常重要的例子

假设我们想：

> 找出 CPU 使用时间最高的 5 个进程。

可以写：

```powershell
Get-Process |
    Sort-Object CPU -Descending |
    Select-Object -First 5
```

把它拆开来看。

第一步：

```powershell
Get-Process
```

得到：

```text
Process[]
```

然后：

```powershell
Sort-Object CPU -Descending
```

意思是：

> 根据 Process 对象的 `CPU` 属性排序。

然后：

```powershell
Select-Object -First 5
```

取前五个对象。

所以：

```text
Get-Process
     ↓
Process[]
     ↓
Sort-Object
     ↓
排序后的 Process[]
     ↓
Select-Object
     ↓
5 个 Process
```

这就是 PowerShell 的核心哲学。

---

# 9. Cmdlet

PowerShell 中很多原生命令叫：

```text
Cmdlet
```

读作大概：

```text
command-let
```

Cmdlet 有一个非常统一的命名方式：

```text
Verb-Noun
动词-名词
```

例如：

```powershell
Get-Process
```

就是：

```text
Get
获取

Process
进程
```

---

常见动词：

| Verb        | 含义      |
| ----------- | ------- |
| Get         | 获取      |
| Set         | 设置      |
| New         | 创建      |
| Remove      | 删除      |
| Start       | 启动      |
| Stop        | 停止      |
| Restart     | 重启      |
| Test        | 测试      |
| Invoke      | 调用 / 执行 |
| Import      | 导入      |
| Export      | 导出      |
| ConvertTo   | 转换为     |
| ConvertFrom | 从某格式转换  |

于是你看到：

```powershell
Get-Service
```

即使没学过，也大概能猜：

> 获取服务。

看到：

```powershell
Restart-Service
```

也能猜：

> 重启服务。

这是一种非常重要的可发现性设计。

---

# 10. 不要背 PowerShell 命令

学习 PowerShell 有一个很大的误区：

> 我要记住几百个命令。

其实完全没必要。

真正应该掌握的是：

```text
我需要什么
 ↓
如何找到对应命令
 ↓
如何查看命令参数
 ↓
如何观察结果对象
 ↓
如何把它接入管道
```

所以 PowerShell 最重要的三个学习命令是：

```powershell
Get-Command
Get-Help
Get-Member
```

它们甚至比：

```powershell
Get-Process
Get-Service
Get-ChildItem
```

更加重要。

---

# 11. Get-Command：寻找命令

不知道有哪些进程相关命令？

```powershell
Get-Command *Process*
```

可能看到：

```text
Get-Process
Start-Process
Stop-Process
Wait-Process
Debug-Process
```

于是就知道：

```text
Get
Start
Stop
Wait
Debug
```

都可以操作 Process。

---

## 按动词搜索

例如：

```powershell
Get-Command -Verb Get
```

查询所有：

```text
Get-*
```

命令。

---

## 按名词搜索

```powershell
Get-Command -Noun Process
```

---

## 通配符搜索

```powershell
Get-Command *Service*
```

或者：

```powershell
Get-Command *File*
```

---

# 12. Get-Help：学习一个命令

发现：

```powershell
Get-Process
```

之后，不知道怎么使用？

执行：

```powershell
Get-Help Get-Process
```

查看详细帮助：

```powershell
Get-Help Get-Process -Full
```

最推荐初学者使用：

```powershell
Get-Help Get-Process -Examples
```

它会直接告诉你很多使用示例。

所以以后遇到陌生命令：

```text
Get-Command
      ↓
Get-Help
```

---

# 13. Get-Member：观察对象

这是整个 PowerShell 学习过程中最重要的命令之一。

例如：

```powershell
Get-Process | Get-Member
```

告诉你：

```text
Process 对象有哪些属性？
Process 对象有哪些方法？
Process 对象是什么类型？
```

再例如：

```powershell
Get-Service | Get-Member
```

会发现它返回的是另一种对象。

---

# 14. PowerShell 中的变量

PowerShell 变量使用：

```text
$
```

例如：

```powershell
$name = "Ema"
```

输出：

```powershell
$name
```

---

存对象：

```powershell
$process = Get-Process -Name explorer
```

然后：

```powershell
$process.Id
```

或者：

```powershell
$process.ProcessName
```

---

查看对象类型：

```powershell
$process.GetType()
```

---

# 15. 属性访问

假设：

```powershell
$p = Get-Process -Name explorer
```

访问：

```powershell
$p.Id
```

```powershell
$p.ProcessName
```

```powershell
$p.CPU
```

```powershell
$p.WorkingSet64
```

这种：

```text
对象.属性
```

对于 Java 开发者应该非常熟悉：

```java
object.field
```

---

# 16. Select-Object：选择属性

执行：

```powershell
Get-Process
```

默认会显示很多内容。

如果我们只想要：

```text
进程名
PID
CPU
```

可以：

```powershell
Get-Process |
    Select-Object ProcessName, Id, CPU
```

输出：

```text
ProcessName    Id      CPU
-----------    --      ---
java         4821    32.14
chrome       9012   112.53
explorer     3321    20.11
```

注意：

`Select-Object` 不是在：

> 截取字符串的第几列。

而是在：

> 选择对象中的属性。

---

# 17. Where-Object：过滤对象

例如：

```powershell
Get-Process |
    Where-Object CPU -GT 10
```

意思是：

```text
找出：

Process.CPU > 10
```

的所有进程。

---

完整写法是：

```powershell
Get-Process |
    Where-Object {
        $_.CPU -GT 10
    }
```

这里出现一个非常重要的变量：

```text
$_
```

意思是：

> 当前正在通过管道处理的对象。

所以：

```powershell
$_.CPU
```

就是：

```text
当前 Process 对象的 CPU 属性
```

---

# 18. `$_` 是什么意思？

假设管道里有：

```text
Process A
Process B
Process C
```

执行：

```powershell
Where-Object {
    $_.CPU -GT 10
}
```

PowerShell 实际类似：

```text
$_ = Process A
检查 $_.CPU

$_ = Process B
检查 $_.CPU

$_ = Process C
检查 $_.CPU
```

如果主人熟悉 Java Stream，可以把：

```powershell
Where-Object {
    $_.CPU -GT 10
}
```

理解为：

```java
.filter(process -> process.getCpu() > 10)
```

是不是一下就亲切很多了？🌸

---

# 19. PowerShell 管道 VS Java Stream

PowerShell：

```powershell
Get-Process |
    Where-Object CPU -GT 10 |
    Sort-Object CPU -Descending |
    Select-Object -First 5
```

思想非常接近 Java：

```java
processes.stream()
        .filter(p -> p.getCpu() > 10)
        .sorted(...)
        .limit(5)
        .toList();
```

对应关系：

| PowerShell     | Java Stream        |
| -------------- | ------------------ |
| 管道 `\|`        | Stream             |
| Where-Object   | filter             |
| ForEach-Object | map / forEach      |
| Sort-Object    | sorted             |
| Select-Object  | map / projection   |
| Measure-Object | count / statistics |

这个类比以后会非常有用。

---

# 20. 一个完整例子

需求：

> 找出内存占用最高的 10 个进程，只显示进程名称、PID 和内存。

首先：

```powershell
Get-Process
```

检查对象：

```powershell
Get-Process | Get-Member
```

发现：

```text
WorkingSet64
```

表示进程工作集内存。

于是：

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id, WorkingSet64
```

现在已经能完成需求。

但是：

```text
WorkingSet64
```

单位是字节。

可读性不好。

以后我们会学习「计算属性」，最终可以写成：

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 `
        ProcessName,
        Id,
        @{Name = "MemoryMB"; Expression = {
            [Math]::Round($_.WorkingSet64 / 1MB, 2)
        }}
```

输出类似：

```text
ProcessName       Id MemoryMB
-----------       -- --------
chrome          3124   824.25
idea64          5721   712.53
java            8472   534.12
```

现在已经很接近一个真正的小工具了。

---

# 21. Alias：PowerShell 的快捷命令

你可能会发现：

```powershell
ls
```

可以运行。

```powershell
cd
```

也可以。

甚至：

```powershell
cat
```

也可以。

这是因为 PowerShell 提供：

```text
Alias
别名
```

例如：

```powershell
Get-Alias ls
```

可能看到：

```text
ls -> Get-ChildItem
```

---

常见：

```text
ls
dir
gci
```

可能都指向：

```powershell
Get-ChildItem
```

---

但是写正式脚本时，仆建议尽量写：

```powershell
Get-ChildItem
```

而不是：

```powershell
ls
```

原因是：

```text
可读性
+
跨环境一致性
+
别人一看就知道命令是什么
```

交互式命令行则随意一些：

```powershell
ls
```

完全没问题。

---

# 22. Windows PowerShell 和 PowerShell

在 Windows 上经常会同时看到两个东西。

旧版：

```text
Windows PowerShell
```

启动程序：

```text
powershell.exe
```

通常对应：

```text
Windows PowerShell 5.1
```

现代版本：

```text
PowerShell
```

启动程序：

```text
pwsh.exe
```

属于：

```text
PowerShell 7+
```

课程以后默认使用：

```text
PowerShell 7
```

启动：

```powershell
pwsh
```

查看版本：

```powershell
$PSVersionTable
```

重点关注：

```text
PSVersion
PSEdition
OS
Platform
```

---

# 23. PowerShell 命令的基本结构

Cmdlet 基本格式：

```text
Command -Parameter Value
```

例如：

```powershell
Get-Process -Name java
```

结构：

```text
Get-Process
    ↓
Command

-Name
    ↓
Parameter

java
    ↓
Value
```

多个参数：

```powershell
Get-ChildItem -Path C:\Projects -Recurse -File
```

---

# 24. 参数补全

PowerShell 非常依赖：

```text
Tab
```

例如输入：

```powershell
Get-Pro
```

然后：

```text
Tab
```

PowerShell 可以补全：

```powershell
Get-Process
```

再输入：

```powershell
Get-Process -
```

按：

```text
Tab
```

可以循环补全参数。

这也是为什么：

> PowerShell 不需要死记很多东西。

---

# 25. 第一套「生存命令」

从现在开始，把下面三个命令刻进脑袋：

```powershell
Get-Command
Get-Help
Get-Member
```

遇到不会的问题：

```text
不知道有没有这个功能
        ↓
Get-Command

不知道命令怎么用
        ↓
Get-Help

不知道返回结果是什么
        ↓
Get-Member
```

这就是 PowerShell 的：

```text
自我学习三件套
```

---

# 26. 实战：寻找 Java 进程

假设机器上运行了 Java。

执行：

```powershell
Get-Process -Name java
```

如果没有 Java 进程，可能报：

```text
Cannot find a process with the name "java"
```

也可以写：

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*"
```

然后：

```powershell
Get-Process |
    Where-Object ProcessName -Like "*java*" |
    Select-Object ProcessName, Id, CPU
```

这里已经形成一个完整的数据处理链：

```text
获取所有进程
     ↓
过滤 Java
     ↓
选择属性
     ↓
输出结果
```

---

# 27. 实战：寻找最吃内存的程序

执行：

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id, WorkingSet64
```

思考一下：

为什么：

```powershell
Sort-Object WorkingSet64
```

知道如何排序？

答案是：

> 因为进入管道的是对象，而对象具有 `WorkingSet64` 属性。

这就是本节课最核心的知识。

---

# 28. 实战：查询 Windows 服务

执行：

```powershell
Get-Service
```

然后：

```powershell
Get-Service | Get-Member
```

观察：

```text
ServiceController
```

对象。

筛选运行中的服务：

```powershell
Get-Service |
    Where-Object Status -EQ Running
```

只看：

```text
Name
DisplayName
Status
```

：

```powershell
Get-Service |
    Where-Object Status -EQ Running |
    Select-Object Name, DisplayName, Status
```

---

# 29. PowerShell 运算符的特殊之处

你可能发现：

```powershell
$_.CPU -GT 10
```

为什么不是：

```text
>
```

PowerShell 很多比较运算符使用：

```text
-eq
-ne
-gt
-ge
-lt
-le
```

分别对应：

```text
==
!=
>
>=
<
<=
```

例如：

```powershell
10 -gt 5
```

返回：

```text
True
```

详细内容后面会专门学习。

---

# 30. 本课核心思维模型

请记住这一张脑内图：

```text
          ┌────────────────┐
          │   Get-Process  │
          └───────┬────────┘
                  │
                  │ Process Object
                  ▼
        ┌───────────────────┐
        │   Where-Object    │
        │     CPU > 10      │
        └────────┬──────────┘
                 │
                 │ Process Object
                 ▼
        ┌───────────────────┐
        │    Sort-Object    │
        │       CPU         │
        └────────┬──────────┘
                 │
                 │ Process Object
                 ▼
        ┌───────────────────┐
        │   Select-Object   │
        │ Name / Id / CPU   │
        └───────────────────┘
```

PowerShell 的世界里：

```text
命令
 ↓
对象
 ↓
管道
 ↓
对象
 ↓
管道
 ↓
对象
```

而不是简单的：

```text
字符串
 ↓
字符串
 ↓
字符串
```

---

# 31. 今日必须掌握的命令

```powershell
Get-Command
```

查找命令。

```powershell
Get-Help
```

查看帮助。

```powershell
Get-Member
```

观察对象。

```powershell
Get-Process
```

查询进程。

```powershell
Get-Service
```

查询服务。

```powershell
Where-Object
```

过滤对象。

```powershell
Select-Object
```

选择属性。

```powershell
Sort-Object
```

排序。

---

# 32. 今日必须理解的概念

不要急着背命令。

必须真正理解：

```text
Cmdlet
Object
Property
Method
Pipeline
Parameter
Alias
```

特别是：

> PowerShell 管道里传递的通常是对象。

这是整门课程最重要的一句话。

---

# 33. 课堂练习

不要直接看答案，自己尝试完成。

## 练习 1

查看：

```powershell
Get-Process
```

返回对象的类型。

提示：

```powershell
Get-Member
```

---

## 练习 2

找出：

```text
CPU > 5
```

的所有进程。

---

## 练习 3

找出 CPU 最高的 5 个进程。

只显示：

```text
ProcessName
Id
CPU
```

---

## 练习 4

找出所有：

```text
Running
```

状态的 Windows 服务。

只显示：

```text
Name
DisplayName
Status
```

---

## 练习 5

不知道：

```powershell
Stop-Process
```

怎么使用。

不要搜索互联网。

只使用 PowerShell 自己的命令查找：

```text
Stop-Process 有哪些使用例子？
```

---

# 34. 挑战题

尝试写出一条管道：

> 找出内存占用最大的 10 个进程，并按照内存从大到小排列，只显示进程名、PID、内存。

暂时允许直接使用：

```text
WorkingSet64
```

作为内存。

最终应该得到类似：

```text
ProcessName    Id     WorkingSet64
-----------    --     ------------
chrome        1234    912345678
idea64        5678    812345678
java          9012    712345678
```

---

# 35. 参考答案

> [!warning]
> 推荐先自己完成练习，再展开答案。

## 练习 1

```powershell
Get-Process | Get-Member
```

---

## 练习 2

```powershell
Get-Process |
    Where-Object CPU -GT 5
```

或者：

```powershell
Get-Process |
    Where-Object {
        $_.CPU -GT 5
    }
```

---

## 练习 3

```powershell
Get-Process |
    Sort-Object CPU -Descending |
    Select-Object -First 5 ProcessName, Id, CPU
```

---

## 练习 4

```powershell
Get-Service |
    Where-Object Status -EQ Running |
    Select-Object Name, DisplayName, Status
```

---

## 练习 5

```powershell
Get-Help Stop-Process -Examples
```

---

## 挑战题

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id, WorkingSet64
```

---

# 36. 本课小项目：Process Explorer Mini

最终完成一个简单的「PowerShell 进程排行榜」。

要求：

找出：

```text
内存最大的 10 个进程
```

并显示：

```text
进程名
PID
CPU
内存
```

第一阶段：

```powershell
Get-Process |
    Sort-Object WorkingSet64 -Descending |
    Select-Object -First 10 ProcessName, Id, CPU, WorkingSet64
```

下一课之后，我们会继续改进它：

```text
WorkingSet64
      ↓
转换为 MB

输出表格
      ↓
格式优化

增加条件
      ↓
过滤进程

最终
      ↓
封装成脚本
```

这个小工具会伴随前几节课不断升级。

---

# 37. 本课知识地图

```text
PowerShell
│
├── Shell
├── 脚本语言
└── 自动化平台
        │
        ▼
      Cmdlet
        │
        ▼
      Object
      ├── Property
      └── Method
        │
        ▼
     Pipeline
        │
        ├── Where-Object
        ├── Sort-Object
        └── Select-Object
        │
        ▼
    自动化脚本
```

---

# 38. 本课总结

PowerShell 最重要的不是记住：

```powershell
Get-Process
```

而是理解：

```text
Get-Process
        ↓
返回 Process 对象
        ↓
对象具有属性和方法
        ↓
对象可以进入 Pipeline
        ↓
其他 Cmdlet 可以继续处理这些对象
```

以后面对陌生需求：

```text
我要管理某个东西
        ↓
Get-Command 找命令

找到命令
        ↓
Get-Help 看怎么用

拿到结果
        ↓
Get-Member 看对象

了解属性
        ↓
Where / Sort / Select

组合成 Pipeline
```

这才是真正的：

> **PowerShell 思维。**

---

# 下一课

## PowerShell 课程 02：文件系统与 Provider

下一节将学习：

* `Get-ChildItem`
* `Set-Location`
* `New-Item`
* `Copy-Item`
* `Move-Item`
* `Remove-Item`
* `Test-Path`
* 相对路径与绝对路径
* `$HOME`
* `$PWD`
* `$PSScriptRoot`
* 通配符
* 递归搜索
* PowerShell Provider

并完成第一个真正有用的小项目：

> **自动整理 Downloads 文件夹**

将：

```text
jpg / png / webp
        ↓
Images/

zip / 7z / rar
        ↓
Archives/

pdf / docx / xlsx
        ↓
Documents/
```

自动分类。

---

> [!tip] 一句话记住第一课
>
> **Bash 经常是在管道中处理文本，而 PowerShell 更擅长在管道中处理对象。**
