---
title: 库-time
tags: [go, time, 时间]
aliases: []
---

# 库-time

## 时间类型

使用 `time.Time` 类型表示时间。我们可以通过 `time.Now` 函数获取当前的时间对象,然后从时间对象中可以获取到年、月、日、时、分、秒等信息。

## Location 和 time zone

```go
// timezoneDemo 时区示例
func timezoneDemo() {
    // 中国没有夏令时,使用一个固定的8小时的UTC时差。
    // 对于很多其他国家需要考虑夏令时。
    secondsEastOfUTC := int((8 * time.Hour).Seconds())
    // FixedZone 返回始终使用给定区域名称和偏移量(UTC 以东秒)的 Location。
    beijing := time.FixedZone("Beijing Time", secondsEastOfUTC)

    // 如果当前系统有时区数据库,则可以加载一个位置得到对应的时区
    // 例如,加载纽约所在的时区
    newYork, err := time.LoadLocation("America/New_York") // UTC-05:00
    if err != nil {
        fmt.Println("load America/New_York location failed", err)
        return
    }
    fmt.Println()
    // 加载上海所在的时区
    //shanghai, err := time.LoadLocation("Asia/Shanghai") // UTC+08:00
    // 加载东京所在的时区
    //tokyo, err := time.LoadLocation("Asia/Tokyo") // UTC+09:00

    // 创建时间对象需要指定位置。常用的位置是 time.Local(当地时间)和 time.UTC(UTC时间)。
    //timeInLocal := time.Date(2009, 1, 1, 20, 0, 0, 0, time.Local) // 系统本地时间
    timeInUTC := time.Date(2009, 1, 1, 12, 0, 0, 0, time.UTC)
    sameTimeInBeijing := time.Date(2009, 1, 1, 20, 0, 0, 0, beijing)
    sameTimeInNewYork := time.Date(2009, 1, 1, 7, 0, 0, 0, newYork)

    // 北京时间(东八区)比UTC早8小时,所以上面两个时间看似差了8小时,但表示的是同一个时间
    timesAreEqual := timeInUTC.Equal(sameTimeInBeijing)
    fmt.Println(timesAreEqual)

    // 纽约(西五区)比UTC晚5小时,所以上面两个时间看似差了5小时,但表示的是同一个时间
    timesAreEqual = timeInUTC.Equal(sameTimeInNewYork)
    fmt.Println(timesAreEqual)
}
```

## Unix Time

可通过 `time.Time` 获取 Unix 时间。

## 时间间隔

```go
const (
    Nanosecond  Duration = 1
    Microsecond          = 1000 * Nanosecond
    Millisecond          = 1000 * Microsecond
    Second               = 1000 * Millisecond
    Minute               = 60 * Second
    Hour                 = 60 * Minute
)
```

## 时间操作(Time 的操作)

- `Add`:增加时间
- `Sub`:两个时间之间的差值
- `Equal`:判断两个时间是否相同
- `Before`:是否在指定时间前
- `After`:是否在指定时间后

## 定时器

使用 `time.Tick` 来设置定时器,定时器的本质上是一个通道。

```go
func tickDemo() {
    ticker := time.Tick(time.Second) //定义一个1秒间隔的定时器
    for i := range ticker {
        fmt.Println(i)//每秒都会执行的任务
    }
}
```

## 时间格式化 time.Format

(格式很奇怪的 Go 参考时间格式)

```go
// formatDemo 时间格式化
func formatDemo() {
    now := time.Now()
    // 格式化的模板为 2006-01-02 15:04:05

    // 24小时制
    fmt.Println(now.Format("2006-01-02 15:04:05.000 Mon Jan"))
    // 12小时制
    fmt.Println(now.Format("2006-01-02 03:04:05.000 PM Mon Jan"))

    // 小数点后写0,因为有3个0所以格式化输出的结果也保留3位小数
    fmt.Println(now.Format("2006/01/02 15:04:05.000")) // 2022/02/27 00:10:42.960
    // 小数点后写9,会省略末尾可能出现的0
    fmt.Println(now.Format("2006/01/02 15:04:05.999")) // 2022/02/27 00:10:42.96

    // 只格式化时分秒部分
    fmt.Println(now.Format("15:04:05"))
    // 只格式化日期部分
    fmt.Println(now.Format("2006.01.02"))
}
```

## 解析字符串格式的时间

```go
// parseDemo 指定时区解析时间
func parseDemo() {
    // 在没有时区指示符的情况下,time.Parse 返回UTC时间
    timeObj, err := time.Parse("2006/01/02 15:04:05", "2022/10/05 11:25:20")
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(timeObj) // 2022-10-05 11:25:20 +0000 UTC

    // 在有时区指示符的情况下,time.Parse 返回对应时区的时间表示
    // RFC3339     = "2006-01-02T15:04:05Z07:00"
    timeObj, err = time.Parse(time.RFC3339, "2022-10-05T11:25:20+08:00")
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(timeObj) // 2022-10-05 11:25:20 +0800 CST
}
```
