专用于可变长参数的库，参数列表也是用…表示的  
比如：  
void print(int a, …) {  
va_list ap;  
va_steart(ap, a); // 准备开始遍历  
int val = va_arg(ap, int); // 取第一个可变参数  
char * arr = va_arg(ap, char *); // 取第二个可变参数  
va_end(ap); // 结束  
}