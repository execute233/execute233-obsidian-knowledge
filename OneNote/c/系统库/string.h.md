1. size_t strlen(const char * _Str);

计算传入的字符串长度，包括\0字符

3. strcat(char * Dest, char * Source);

拼接两个字符串到第一个支符串中，前提是第一个字符串装得下第二个字符串

5. strcpychar(char * Dest, char * Source)

将后面的字符串拷贝到前面的字符串中

7. int strcmp(const char *_Str1,const char *_Str2)

返回第一个不同字符的ASCII码之差，若所有字符相等则返回0