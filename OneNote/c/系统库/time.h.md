---
title: time.h
tags: [c, time.h, 时间函数, 日期函数, 标准库]
aliases: []
---

# time.h

## 库变量

- `clock_t`：适合存储处理器时间的类型。
- `time_t`：适合存储日历时间类型。
- `struct tm`：用于保存时间和日期的结构。

```c
struct tm {
    int tm_sec;   // 秒，0 ~ 59
    int tm_min;   // 分，0 ~ 59
    int tm_hour;  // 小时，0 ~ 23
    int tm_mday;  // 一月中的第几天，1 ~ 31
    int tm_mon;   // 月，0 ~ 11
    int tm_year;  // 年
    int tm_wday;  // 一周中的第几天，0 ~ 6
    int tm_yday;  // 一年中的第几天
    int tm_isdst; // 夏令时，无用
};
```

## 库函数

### time_t time(time_t *)

计算当前日历时间，一般传入 `NULL`。

### char * asctime(struct tm *)

返回结构的日期和时间。

### char * ctime(time_t *)

返回表示当地时间的字符串。

### clock_t clock()

返回程序执行起所用的时间。

### double difftime(time_t, time_t)

计算前者时间与后者时间相差秒数。

### struct tm * gmtime(time_t *)

`timer` 的值被分解为 `tm` 结构，并用协调世界时（UTC，也被称为格林尼治标准时间（GMT））表示。

### struct tm * localtime(time_t *)

分解为 `tm` 结构，并用本地时区表示。

### time_t mktime(struct tm *)

转换为一个依据本地时区的 `time_t` 值。

### size_t strftime(char * str, size_t maxsize, char * format, struct tm * timeptr)

根据 `format` 中定义的格式化规则，格式化结构 `timeptr` 表示的时间，并把它存储在 `str` 中。