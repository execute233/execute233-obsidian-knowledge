```
qsort(void *_Base,size_t _NumOfElements,size_t _SizeOfElements,int (*_PtFuncCompare)(void *,void *))
```

```
void* bsearch(void* key, void base, size_t nitems, size_t size, int (compar) (void*, void*))
```

```
exit(int _Code)
```

```
void * malloc(size_t _Size)
```

```
void* realloc(void*, size_t)
```

```
free(void *_Memory)
```

```
abort()
```

```
int atexit(void (*func)(void))
```

```
char* getenv(char*)
```

```
指定类型 atof/i/l/ll(char*, ..)
```

```
指定类型 strtod/f/l/ld/ll/ul/ull(char*, ..)
```

```
int abs(int)
```

```
div_t div(int, int), ldiv_t ldiv(long, long)
```

```
int rand()
```

```
void srand(unsigned int)
```

快速排序，传入的参数如下、

|   |   |
|---|---|
|_Base|待排序数组|
|_NumOfElements|待排序数量(一开始是数组长度)|
|_SizeOfElement|元素大小，一般是sizeof(元素类型)|
|_PtFuncCompare|排序规则，返回值为正数则是大于，默认是升序排序|

举个例子  
int compare(const void *a, const void *b) {  
return *(int *)a - *(int *)b;  
}  
int main() {  
int arr[] = {5, 3, 4, 2, 1, 6, 7, 9, 8, 0};  
qsort(arr, sizeof(arr) / sizeof(arr[0]), sizeof(arr[0]), compare);  
}  
二分搜索  
退出程序,其中_Code有EXIT_SUCCESS和EXIT_FAILURE两字段选择  
申请指定大小的一段内存空间  
重新调整之前malloc分配的内存块大小  
与malloc()对应,对内存空间进行释放  
使一个异常程序终止  
当程序正常终止时，调用函数func  
获取环境变量的值  
将字符串转为指定的类型（double/ int/ long/ long long）  
跳过前面的空格，直到正负号/数字开始转换，遇到非数字停止（可以传地址存无法转换的内容）  
将字符串转为指定的类型（float/ int/ double/ long long/ unsigned long/ unsigned long long）  
跳过前面的空格，直到正负号/数字开始转换，遇到非数字停止（可以传地址存无法转换的内容）  
取绝对值  
分子除以分母  
返回一个范围在0到RAND_MAX之间的伪随机数  
传入随机数种子