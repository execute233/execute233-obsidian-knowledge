---
title: 库-net-http
tags: [go, net-http, http客户端, http服务端]
aliases: []
---

# 库-net-http

HTTP 协议背景见 [[computer/计算机网络/HTTP协议]];基于 TCP,见 [[computer/计算机网络/TCP连接]];`http` 第三方库对比见 [[go/go基础/库-http]];gin 框架基于此包,见 [[go/gin/路由]] / [[go/gin/请求]] / [[go/gin/bind绑定器]]。

## HTTP 客户端

```go
resp, err := http.Get("http://example.com/")
...
resp, err := http.Post("http://example.com/upload", "image/jpeg", &buf)
...
resp, err := http.PostForm("http://example.com/form",
    url.Values{"key": {"Value"}, "id": {"123"}})
```

使用完 response 后必须关闭回复的主体。

```go
resp, err := http.Get("http://example.com/")
if err != nil {
    // handle error
}
defer resp.Body.Close()
body, err := ioutil.ReadAll(resp.Body)
// ...
```

带参数的 GET 请求示例:

```go
apiUrl := "http://127.0.0.1:9090/get"
// URL param
data := url.Values{}
data.Set("name", "小王子")
data.Set("age", "18")
u, err := url.ParseRequestURI(apiUrl)
if err != nil {
    fmt.Printf("parse url requestUrl failed, err:%v\n", err)
}
u.RawQuery = data.Encode() // URL encode
fmt.Println(u.String())
resp, err := http.Get(u.String())
if err != nil {
    fmt.Printf("post failed, err:%v\n", err)
    return
}
defer resp.Body.Close()
b, err := ioutil.ReadAll(resp.Body)
if err != nil {
    fmt.Printf("get resp failed, err:%v\n", err)
    return
}
fmt.Println(string(b))
```

POST 请求示例:

```go
url := "http://127.0.0.1:9090/post"
// 表单数据
//contentType := "application/x-www-form-urlencoded"
//data := "name=小王子&age=18"
// json
contentType := "application/json"
data := `{"name":"小王子","age":18}`
resp, err := http.Post(url, contentType, strings.NewReader(data))
if err != nil {
    fmt.Printf("post failed, err:%v\n", err)
    return
}
defer resp.Body.Close()
b, err := ioutil.ReadAll(resp.Body)
if err != nil {
    fmt.Printf("get resp failed, err:%v\n", err)
    return
}
fmt.Println(string(b))
```

## 自定义 Client

如果要管理客户端的头域、重定向策略等等,可以用 `http.Client`。

```go
client := &http.Client{
    CheckRedirect: redirectPolicyFunc,
}
resp, err := client.Get("http://example.com")
// ...
req, err := http.NewRequest("GET", "http://example.com", nil)
// ...
req.Header.Add("If-None-Match", `W/"wyzzy"`)
resp, err := client.Do(req)
// ...
```

## 自定义 Transport

自定义管理代理、TLS 配置、keep-alive、压缩和其他设置。

```go
tr := &http.Transport{
    TLSClientConfig:    &tls.Config{RootCAs: pool},
    DisableCompression: true,
}
client := &http.Client{Transport: tr}
resp, err := client.Get("https://example.com")
```

## 服务端

可以直接用包的 `Handle` 来处理,这用的是默认的 `DefaultServeMux`。

```go
http.HandleFunc("/", sayHello)
err := http.ListenAndServe(":9090", nil)
if err != nil {
    fmt.Printf("http server failed, err:%v\n", err)
    return
}
```

自定义服务端:

```go
s := &http.Server{
    Addr:           ":8080",
    Handler:        myHandler,
    ReadTimeout:    10 * time.Second,
    WriteTimeout:   10 * time.Second,
    MaxHeaderBytes: 1 << 20,
}
log.Fatal(s.ListenAndServe())
```
