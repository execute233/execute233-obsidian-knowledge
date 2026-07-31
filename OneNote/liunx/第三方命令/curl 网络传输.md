curl（Client URL）是一个强大的命令行工具，用于在 Linux/Unix 系统中传输数据。它支持多种协议，包括 HTTP、HTTPS、FTP、SFTP 等，是开发者和系统管理员日常工作中不可或缺的工具。

基本语法结构：

curl [options] [URL...]
-O 最常用，下载到文件

2. 请求头相关参数选项
3. 响应头相关参数选项
4. cookie
5. 代理
6. 数据传输

-H "name: value" 或 --header "name: value" 添加一个http请求头
--H "name" 或 --header "name" 删除一个http请求头
-A "string" 或 --user-agent "string" 设置请求头User-Agent
-e <URL> 或 -referer <URL>告诉http服务器从哪个页面进入到这个页面，相当于 -H "Referer: <URL>"
-l 或 -head 输出页面的http头(HTTP)或文件大小和最后修改时间(FTP/FILE)
-i 或 --include 输出HTTP头和返回内容
-D <file> 或 --dump-header <file> 转储http响应头到指定文件
-b data 或 --cookie data 发送cookie，data的格式是"key1=value1;key2=value2;.."
-c filename 或 --cookie-jar 将服务器返回的cookies保存到指定的文件,指定为-则是控制台
-j 或 --junk-session-cookies 丢弃所有的"session cookie"
设置代理：未指定端口默认8080,protocol默认是http_proxy,其他值可以是https_proxy、socks4、socks4a、socks5
-x host:prot
-x [protocol://[user:pwd@]host[:port]
--proxy [protocol://[user:pwd@]host[:port]
列如：-x "http_proxy://aiezu:123@aiezu.com:80"
-p 或 --proxytunnel 将“-x”参数的代理，作为通道的方式去代理非HTTP协议，如ftp
使用不同类型的socket代理：注意会覆盖-x参数
--socks4 <host[:port]>
--socks4a <host[:port]>
--socks5 <host[:port]>
http代理认证方式：
--proxy-anyauth
--proxy-basic
--proxy-diges
--proxy-negotiate
--proxy-ntlm
设置代理的用户名和密码：
-U <user:password>
--proxy-user <user:password>
-G 或 --get 如果使用了该参数，将-d/ --data --data-binary 参数设置的数据，附加在url上，以GET方式请求
使用HTTP POST方式发送key/value对数据，相当于表单属性(method="POST";enctype="application/x-www.form-urlencoded")
-d @file
-d "string"
--data "string"
--data-ascii "string"
--data-binary "string"
--data-urlencode "string"
使用HTTP POST方式发送类似“表单字段”的多类型数据，相当于同时设置浏览器表单属性（method="POST"，enctype="multipart/form-data"）
-F name=@file
-F name=<file
-F name=content
--form name=content
--form-string <key=value> 类似于"--form",但是@ < 无特殊含义
通过“put”的方式将文件传输到远程网址，如果参数使用-会使用stdin读入文件内容
-T file
-upload-file file