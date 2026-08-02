---
title: string.h
tags: [c, string.h, 字符串函数, 标准库]
aliases: []
---

# string.h

字符串基础见 [[c/基本/字符串]];字符串 IO 配合 [[c/系统库/stdio.h]] 使用。

### size_t strlen(const char * _Str)

计算传入的字符串长度，包括 `\0` 字符。

### char * strcat(char * Dest, const char * Source)

拼接两个字符串到第一个字符串中，前提是第一个字符串装得下第二个字符串。

### char * strcpy(char * Dest, const char * Source)

将后面的字符串拷贝到前面的字符串中。

### int strcmp(const char * _Str1, const char * _Str2)

返回第一个不同字符的 ASCII 码之差，若所有字符相等则返回 0。