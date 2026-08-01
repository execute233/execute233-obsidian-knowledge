**库变量**  
clock_t - 适合存储处理器时间的类型  
time_t - 适合存储日历时间类型  
struct tm - 用于保存时间和日期的结构  
struct tm {  
int tm_sec; // 秒, 0 ~ 59  
int tm_min; // 分, 0 ~ 59  
int tm_hour; // 小时, 0 ~ 23  
int tm_mday; // 一月中的第几天, 1 ~ 31  
int tm_mon; // 月, 0 ~ 11  
int tm_year; // 年  
int tm_wday; // 一周中的第几天, 0 ~ 6  
int tm_yday; // 一年中的第几天  
int tm_isdst; // 夏令时，无用  
}  
**库函数**

```
time_t time(time_t*)
```

```
char* asctime(struct tm*)
```

```
char* ctime(time_t*)
```

```
clock_t clock()
```

```
double difftime(time_t, time_t)
```

```
struct tm* gmtime(time_t* )
```

```
struct tm* localtime(time_t*)
```

```
tim_t mktime(struct tm*)
```

```
size_t strftime(char* str,size_t maxsize, char* format,tstruct tm* timeptr)
```
   

```
计算当前日历时间，一般传入NULL  
返回结构的日期和时间  
返回表示当地时间的字符串  
返回程序执行起所用的时间  
计算前者时间与后者时间相差秒数  
timer的值被分解为tm结构，并用协调世界时(UTC)也被称为格林尼治标准时间(GMT)表示  
分解为tm结构，并用本地时区表示  
转换为一个依据本地时区的time_t值。  
根据format中定义的格式化规则，格式化结构timeptr表示的时间，并把它存储在str中。
```