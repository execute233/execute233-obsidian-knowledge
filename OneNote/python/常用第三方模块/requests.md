QuicklyStart

1. **requests.****各种类型的请求****()**
2. **response context**

```
data - 发送请求的数据（如果有）  
params - 拼接在URL的数据  
header - 请求头信息  
allow_redirects - 允许重定向  
stream - 处理大相应时，逐块接收数据  
json - 上传json数据  
timeout - 超时时间  
proxies - 代理设置  
verify - SSL设置  
.text - 文本数据，自动使用字符集  
.encoding - 字符集，可自己指定  
.content - 二进制数据(gzip,deflate会自动解码  
.json() - 将返回的数据转为json  
.raw - 原始包数据  
.status_code - 响应状态码  
.headers - 响应头  
.cookies - 服务器返回的cookies  
.history - 重定向历史记录  
高级功能
```

1. 持久化管理

```
with requests.Session() as session:  
session.update.haeder(xxxx)  
session.auth = …
```