---
title: 库-fmt
tags: [go, fmt, 格式化, IO]
aliases: []
---

# 库-fmt

格式化输出常涉及类型转换,见 [[go/go基础/库-strconv]];日志输出见 [[go/go基础/库-log]];时间格式化字符串见 [[go/go基础/库-time]]。

## 向控制台输出

`Print` 函数直接输出内容,`Printf` 函数支持格式化输出字符串,`Println` 函数会在输出内容的结尾添加一个换行符。

```go
func Print(a ...interface{}) (n int, err error)
func Printf(format string, a ...interface{}) (n int, err error)
func Println(a ...interface{}) (n int, err error)
```

## 向 Writer 输出

```go
func Fprint(w io.Writer, a ...interface{}) (n int, err error)
func Fprintf(w io.Writer, format string, a ...interface{}) (n int, err error)
func Fprintln(w io.Writer, a ...interface{}) (n int, err error)
```

## 向字符串输出

```go
func Sprint(a ...interface{}) string
func Sprintf(format string, a ...interface{}) string
func Sprintln(a ...interface{}) string
```

还有格式化字符串为错误的:

```go
func Errorf(format string, a ...interface{}) error
```

## 获取输入

`Scan` 从标准输入扫描文本,读取由空白符分隔的值保存到传递给本函数的参数中,换行符视为空白符。

```go
func Scan(a ...interface{}) (n int, err error)
```

`Scanf` 从标准输入扫描文本,根据 `format` 参数指定的格式去读取由空白符分隔的值保存到传递给本函数的参数中。

```go
func Scanf(format string, a ...interface{}) (n int, err error)
```

类似 `Scan`,它在遇到换行时才停止扫描。最后一个数据后面必须有换行或者到达结束位置。

```go
func Scanln(a ...interface{}) (n int, err error)
```

有时候我们想完整获取输入的内容,而输入的内容可能包含空格,这种情况下可以使用 bufio 包来实现。示例代码如下:

```go
func bufioDemo() {
    reader := bufio.NewReader(os.Stdin) // 从标准输入生成读对象
    fmt.Print("请输入内容: ")
    text, _ := reader.ReadString('\n') // 读到换行
    text = strings.TrimSpace(text)
    fmt.Printf("%#v\n", text)
}
```

这几个函数功能分别类似于 fmt.Scan、fmt.Scanf、fmt.Scanln 三个函数,只不过它们不是从标准输入中读取数据而是从 io.Reader 中读取数据。

```go
func Fscan(r io.Reader, a ...interface{}) (n int, err error)
func Fscanln(r io.Reader, a ...interface{}) (n int, err error)
func Fscanf(r io.Reader, format string, a ...interface{}) (n int, err error)
```

这几个函数功能分别类似于 fmt.Scan、fmt.Scanf、fmt.Scanln 三个函数,只不过它们不是从标准输入中读取数据而是从指定字符串中读取数据。

```go
func Sscan(str string, a ...interface{}) (n int, err error)
func Sscanln(str string, a ...interface{}) (n int, err error)
func Sscanf(str string, format string, a ...interface{}) (n int, err error)
```

## 格式化占位符

### 通用占位符

| 占位符 | 说明 |
| --- | --- |
| `%v` | 值的默认格式表示 |
| `%+v` | 类似 `%v`,但输出结构体时会添加字段名 |
| `%#v` | 值的 Go 语法表示 |
| `%T` | 打印值的类型 |
| `%%` | 百分号 |

### 布尔型

| 占位符 | 说明 |
| --- | --- |
| `%t` | `true` 或 `false` |

### 整型

| 占位符 | 说明 |
| --- | --- |
| `%b` | 表示为二进制 |
| `%c` | 该值对应的 unicode 码值 |
| `%d` | 表示为十进制 |
| `%o` | 表示为八进制 |
| `%x` | 表示为十六进制,使用 a-f |
| `%X` | 表示为十六进制,使用 A-F |
| `%U` | 表示为 Unicode 格式:U+1234,等价于 "U+%04X" |
| `%q` | 该值对应的单引号括起来的 go 语法字符字面值,必要时会采用安全的转义表示 |

### 浮点数与复数

| 占位符 | 说明 |
| --- | --- |
| `%b` | 无小数部分、二进制指数的科学计数法,如 `-123456p-78` |
| `%e` | 科学计数法,如 `-1234.456e+78` |
| `%E` | 科学计数法,如 `-1234.456E+78` |
| `%f` | 有小数部分但无指数部分,如 `123.456` |
| `%F` | 等价于 `%f` |
| `%g` | 根据实际情况采用 `%e` 或 `%f` 格式(以获得更简洁、准确的输出) |
| `%G` | 根据实际情况采用 `%E` 或 `%F` 格式(以获得更简洁、准确的输出) |

### 字符串和 []byte

| 占位符 | 说明 |
| --- | --- |
| `%s` | 直接输出字符串或者 []byte |
| `%q` | 该值对应的双引号括起来的 go 语法字符串字面值,必要时会采用安全的转义表示 |
| `%x` | 每个字节用两字符十六进制数表示(使用 a-f) |
| `%X` | 每个字节用两字符十六进制数表示(使用 A-F) |

### 指针

| 占位符 | 说明 |
| --- | --- |
| `%p` | 表示为十六进制,并加上前导的 `0x` |

### 宽度标识符

| 占位符 | 说明 |
| --- | --- |
| `%f` | 默认宽度,默认精度 |
| `%9f` | 宽度 9,默认精度 |
| `%.2f` | 默认宽度,精度 2 |
| `%9.2f` | 宽度 9,精度 2 |
| `%9.f` | 宽度 9,精度 0 |

### 其他 flag

| flag | 说明 |
| --- | --- |
| `'+'` | 总是输出数值的正负号;对 `%q`(`%+q`)会生成全部是 ASCII 字符的输出(通过转义) |
| `' '` | 对数值,正数前加空格而负数前加负号;对字符串采用 `%x` 或 `%X` 时(`% x` 或 `% X`)会给各打印的字节之间加空格 |
| `'-'` | 在输出右边填充空白而不是默认的左边(即从默认的右对齐切换为左对齐) |
| `'#'` | 八进制数前加 0(`%#o`),十六进制数前加 `0x`(`%#x`)或 `0X`(`%#X`),指针去掉前面的 `0x`(`%#p`);对 `%q`(`%#q`),对 `%U`(`%#U`)会输出空格和单引号括起来的 go 字面值 |
| `'0'` | 使用 0 而不是空格填充,对于数值类型会把填充的 0 放在正负号后面 |
