go mod命令

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-16-0.png)

相关环境变量(go env查看)

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-18-1.png)

导入包  
方式一：命令行  
比如我们需要引入第三方包 github.com/q1mi/hello  
使用命令手动下载 go get -u github.com/q1mi/hello  
也可以指定版本号 go get -u github.com/q1mi/hello@v0.1.0  
方式二：修改mod.go  
require (  
"xxx" vxx.xx.xx  
)  
注：版本也可以写commit hash  
然后可以go mod download下载  
方式三：如果想要导入外部包  
仍可以像方式二那样写，但需要replace语句替换为使用相对路径的包  
如：replace xxx.com/pack =\> ../pack  
修改版本  
go mod edit replace=\<包名@版本\>=\<包名@新的版本\>  
发布包  
假设已有一个go git项目  
需要把代码push到远程分支还需要打上tag  
git tag -a v0.1.0 -m "release version v0.1.0"  
git push origin v0.1.0

![Exported image](_assets/Go%20Modules/Go%20Modules__13-00-19-2.png)

发布新的主版本