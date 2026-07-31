# screen

screen [-opts] [cmd [args]]
状态介绍
通常情况下，screen创建的虚拟终端，有两个工作模式：

- Attached：表示当前screen正在作为主终端使用，为活跃状态。
- Detached：表示当前screen正在后台使用，为非激发状态。

查看终端列表
screen -ls 查验已经创建的终端
终端创建
screen -R name 创建指定名称的终端
使用-R创建，如果有同名的screen，则直接进入之前创建的screen
使用-S创建和直接输入screen创建的虚拟终端，不会检录之前创建的screen
后面也可以直接写命令来后台跑
回到终端
screen -R [pid/name]
退出终端
按住ctrl+a+d
清除终端
比较推荐的方法，是进入对应虚拟终端，然后输入：exit
也可以screen -R [pid/Name] -X quit
绑定键
在虚拟终端内，输入Ctril+a将等待接受预先设置的绑定键，这个时候可以输入对应的一些命令，来操作虚拟终端，如：
d：保存会话，后台运行改虚拟终端
k：关闭对话，等同输入：exit
c：新建一个虚拟终端
?：显示所有绑定键盘