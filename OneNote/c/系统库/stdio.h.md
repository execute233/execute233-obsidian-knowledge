---
title: stdio.h
tags: [c, stdio.h, 标准IO, 文件IO, 标准库]
aliases: []
---

# stdio.h

stdio.h 提供标准 IO,字符串 IO 见 [[c/基本/字符串|字符串]],格式化输出规则见 [[c/基本/变量|变量]] 中的格式控制符。

## std 输入

### int scanf(char * format, * target…)

从 `stdin` 以指定格式化的方式输入到 `target`，返回成功输入数据的个数，失败给 0。

请注意，该函数并不安全，建议使用 `scanf_s`（非标准）函数或者设置项目或关闭安全检查。

### int scanf_s(char * format, * target…) — 非标准

### char getchar()

### char * gets(char *) — C11 就无了

### char * gets_s(char *, size) — 非标准

遇到换行截止，但换行符仍保留在缓冲区。

同 `printf` 一样，可以使用格式化（别写其他字符），多个格式化字符则建议空格分隔，如：

- `format: "%d%c%d"`，输入 `"1+1"` ✓，输入 `"1 + 1"` ✗
- `format: "%d %c %d"`，输入 `"1+1"` ✓，输入 `"1 + 1"` ✓

这里空白字符的意思是忽略空格符与换行符，这对读取单个字符来说使用 `" %c"` 更好。

有些特殊的接收格式化符：

- `%[]` — 不接收任何数据
- `%[A-Z]` — 只接收大写字母
- `%[A-z]` — 只接收字母
- `%[0-9]` — 只接收数字
- `%[^0-9]` — 只接收除数字的字符（`^` 字符用在其它地方同理）
- `%[^\n]` — 只有换行才结束

但注意越界，可使用 `"%限制的字符数s"`，但剩下的仍会保留在缓冲区，还是 `fflush` 吧。

更安全地读取 `stdin`，注意不同的是，输入字符或数字的时候，还要指定缓冲区长度，如：

```c
char inputs[20];
scanf_s(" %s", inputs, 20); // 如果读取单个字符就指定 1
```

获取一个字符；从缓冲区读取字符串，不同于 `scanf`，缓冲区没东西就截止到换行，有东西直接不鸟你。这也是不安全的，建议使用 `gets_s` 或 `fgets`。获取字符串，但是更安全。

## std 输出

### printf(char *format, …)

格式化输出，详见 基本 - 变量 - 2, 3。

### putchar(char)

输出一个字符。

### puts(char *)

输出一个字符串，并且在结尾追加换行。

## 文件 IO 流

### FILE * fopen(char * fileName, char * mode)

以指定的方式打开文件，还是得记得关闭流。

| 模式 | 含义 | 说明 |
|---|---|---|
| `r` | 只读 | 文件必须存在，否则打开失败 |
| `w` | 只写 | 创建/覆写文件，写入内容 |
| `a` | 追加只写 | 若文件存在则追加写入，文件不存在失败 |
| `r+` | 读写 | 文件必须存在 |
| `w+` | 读写 | — |
| `a+` | 读写 | — |
| `rb` | 二进制读 | — |
| `wb` | 二进制写 | — |
| `ab` | 二进制追加 | — |
| `rb+`, `wb+`, `ab+` | — | — |

### int fclose(FILE *stream)

### input

#### int fgetc(FILE *)

读取一个字符，读到尾或者失败返回 EOF。

#### char * fgets(char * _Buffer, int _MaxCount, FILE * _Stream)

读取一个字符串，成功时返回字符数组首地址，否则 NULL（开始在文件末尾也会）。

- `_Buffer`：字符数组
- `_MaxCount`：要读取的字符数量（不超过 `_MaxCount` 大小）
- `_Stream`：文件指针

注意在读取到 `MaxCount - 1` 前，出现了换行或者到末尾则读取结束。

#### int fscanf(FILE * _Stream, char * format, …)

格式化读，自己回去翻。

#### size_t fread(void * Buffer, size_t ElementSize, size_t ElementCount, FILE * Stream)

二进制读，参数相关详见 `fwrite`，返回成功读取的块数，小于预期可能到末尾或发生错误，可使用 `ferror()` 或 `feof()` 检测。

### output

#### int fputc(char, FILE *)

写入字符。

#### int fputs(char *, FILE *)

写入文件。

#### int fprintf(FILE * _Stream, char * format, …)

格式化写，自己回去翻。

#### int sprintf(char * str, char * format, …)

发送格式化输出到指定字符串。

#### int vfprintf(FILE * stream, char * format, va_list arg)

使用参数列表发送格式化输出到流 `stream` 中。

#### size_t fwrite(void * Buffer, size_t ElementSize, size_t ElementCount, FILE * Stream)

二进制写。

- `Buffer`：内存区块指针，可以是数组、变量、结构体等，存放要读取/写入的数据
- `ElementSize`：每个数据块的字节数
- `ElementCount`：要读写的数据块的块数
- `Stream`：文件指针

理论上，每次都会读写 `size * count` 个字节的数据，返回值是成功写入的块数，小于预期肯定错误，使用 `ferror()` 检测。

## other

### void rewind(FILE *)

将指针移动到文件开头。

### void fseek(FILE * Stream, long offset, int origin)

将指针移动到指定位置。

- `offset`：偏移量，可以正或负，代表向前还是向后
- `origin`：起始位置，也就是从哪里开始计算偏移量，可以是
  - `SEEK_SET`：文件开头
  - `SEEK_CUR`：当前位置
  - `SEEK_END`：文件末尾

### long ftell(FILE *)

得到当前指针相对于文件首的偏移字节长度。

### int fgetpos(FILE *, fpos_t *)

获取文件指针当前的位置，并写入到 `pos`。

### int remove(char *)

删除指定文件，成功返回 0。

### int rename(char * OldFileName, char * NewFileName)

重命名文件，成功返回 0。如果 `oldname` 和 `newname` 指定不同路径且系统支持，则移动文件；如果 `newname` 命名现有文件，可能失败或覆盖，具体取决于系统和库。

### void clearerr(FILE *)

清除文件的文件结束和错误符。

### int feof(FILE *)

文件是否读取结束。

### int ferror(FILE *)

文件是否发生错误。

### int fflush(FILE *)

刷新输出缓冲区。

### void setbuf(FILE *, char *)

定义流文件如何缓冲。

### int setvbuf(FILE *, stream, char * buffer, int mode, size_t size)

定义流如何缓冲。

### FILE * tmpfile()

用 `wb+` 的方式创建缓冲文件。

### char * tmpnam(char *)

生成并返回一个有效的临时文件名，该文件名之前是不存在的。

## 库变量

- `size_t`：无符号整数类型，是 `sizeof` 关键字的结果。
- `FILE`：适合存储文件流信息的对象类型。
- `fpos_t`：适合存储文件中任何位置的对象类型。