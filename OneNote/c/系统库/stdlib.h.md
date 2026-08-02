---
title: stdlib.h
tags: [c, stdlib.h, 内存管理, 排序, 随机数, 标准库]
aliases: []
---

# stdlib.h

## 排序与搜索

### void qsort(void * _Base, size_t _NumOfElements, size_t _SizeOfElements, int (* _PtFuncCompare)(void *, void *))

快速排序，传入的参数如下：

| 参数 | 含义 |
|---|---|
| `_Base` | 待排序数组 |
| `_NumOfElements` | 待排序数量（一开始是数组长度） |
| `_SizeOfElement` | 元素大小，一般是 `sizeof(元素类型)` |
| `_PtFuncCompare` | 排序规则，返回值为正数则是大于，默认是升序排序 |

举个例子：

```c
int compare(const void *a, const void *b) {
    return *(int *)a - *(int *)b;
}
int main() {
    int arr[] = {5, 3, 4, 2, 1, 6, 7, 9, 8, 0};
    qsort(arr, sizeof(arr) / sizeof(arr[0]), sizeof(arr[0]), compare);
}
```

### void * bsearch(void * key, void * base, size_t nitems, size_t size, int (compar)(void *, void *))

二分搜索。

## 程序控制

### void exit(int _Code)

退出程序，其中 `_Code` 有 `EXIT_SUCCESS` 和 `EXIT_FAILURE` 两个字段选择。

### void abort()

使一个异常程序终止。

### int atexit(void (* func)(void))

当程序正常终止时，调用函数 `func`。

## 环境

### char * getenv(char *)

获取环境变量的值。

## 内存管理

### void * malloc(size_t _Size)

申请指定大小的一段内存空间。

### void * realloc(void *, size_t)

重新调整之前 `malloc` 分配的内存块大小。

### void free(void * _Memory)

与 `malloc()` 对应，对内存空间进行释放。

## 类型转换

### 指定类型 atof / atoi / atol / atoll(char *, ...)

将字符串转为指定的类型（`double` / `int` / `long` / `long long`）。跳过前面的空格，直到正负号/数字开始转换，遇到非数字停止（可以传地址存无法转换的内容）。

### 指定类型 strtod / strtof / strtold / strtol / strtoll / strtoul / strtoull(char *, ...)

将字符串转为指定的类型（`float` / `int` / `double` / `long long` / `unsigned long` / `unsigned long long`）。跳过前面的空格，直到正负号/数字开始转换，遇到非数字停止（可以传地址存无法转换的内容）。

## 数学

### int abs(int)

取绝对值。

### div_t div(int, int), ldiv_t ldiv(long, long)

分子除以分母。

## 随机数

### int rand()

返回一个范围在 `0` 到 `RAND_MAX` 之间的伪随机数。

### void srand(unsigned int)

传入随机数种子。