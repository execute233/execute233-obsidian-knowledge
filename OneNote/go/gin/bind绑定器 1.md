---
title: bind绑定器 1
tags: [gin, go, bind, 验证]
aliases: []
---

# bind绑定器 1

本质上绑定数据到对象，有这些方式。

## 查询参数绑定

```go
type User struct {
    Name string `form:"name"`
    Age  int    `form:"age"`
}
var user User
err := c.ShouldBindQuery(&user)
```

## 动态/路径（URI）参数绑定

```go
type User struct {
    Name string `uri:"name"`
    Id   int    `uri:"id"`
}
var user User
err := c.ShouldBindUri(&user)
```

## 表单参数绑定

```go
type User struct {
    Name string `form:"name"`
    Age  int    `form:"age"`
}
var user User
// 注意不能解析 x-www-form-urlencoded
err := c.ShouldBind(&user)
```

## JSON 绑定

```go
type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}
var user User
err := c.ShouldBindJSON(&user)
```

## Header 绑定

```go
type User struct {
    Name string `header:"name"`
    Age  int    `header:"age"`
}
var user User
err := c.ShouldBindHeader(&user)
```

## 内置规则

写在结构体标签里的，比如：

```go
type User struct {
    Name string `header:"name" binding:"required"`
    Age  int    `header:"age" binding:"required"`
}
```

有以下规则可以使用（有多个规则使用 `,` 分隔）：

| 规则 | 说明 | 示例 |
| --- | --- | --- |
| `required` | 不能为空，并且不能没有这个字段 | `binding:"required"` |
| `min` | 针对字符串最小长度 | `binding:"min=5"` |
| `max` | 针对字符串最大长度 | `binding:"max=10"` |
| `len` | 针对字符串指定长度 | `binding:"len=6"` |
| `contains` | 针对字符串包含子串 |  |
| `excludes` | 针对字符串不包含子串 |  |
| `startswith` | 针对字符串包含前缀 |  |
| `endswith` | 针对字符串包含前缀 |  |
| `eq` | 针对数字等于 | `binding:"eq=3"` |
| `ne` | 针对数字不等于 | `binding:"ne=12"` |
| `gt` | 针对数字大于 |  |
| `gte` | 针对数字大于等于 |  |
| `lt` | 针对数字小于 |  |
| `lte` | 针对数字小于等于 |  |
| `eqfield` | 等于其他字段的值 | `binding:"eqfield=Password"` |
| `nefield` | 不等于其他字段的值 |  |
| - | 忽略字段 | `binding:"-"` 或者不写 |
| `oneof` | 枚举，只能是枚举的字段 | `binding:"one of=red green"` |
| `ip` / `ipv4` / `ipv6` / `uri` / `url` | 网络验证 | `binding:"ip"` |
| `datetime` | 日期验证 | `binding:"datetime"` |
| `dive` | 对数组每一项应用验证 |  |

## 自定义规则

```go
// 获取翻译器
v, _ := binding.Validator.Engine().(*validator.Validate)
// 注册自定义标签
err := v.RegisterValidation("fip", func(fl validator.FieldLevel) bool {
    fl.Field()          // 对应的值
    fl.FieldName()      // 处理后的字段名（貌似没用）
    fl.StructFieldName() // 字段名
    fl.Parent()         // 父项
    fl.Top()            // 顶项
    fl.Param()          // 写 binding 标签对应的值
})
```
