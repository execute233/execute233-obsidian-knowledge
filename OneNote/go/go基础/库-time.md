**时间类型**  
使用time.Time类型表示时间。我们可以通过time.Now函数获取当前的时间对象，然后从时间对象中可以获取到年、月、日、时、分、秒等信息  
**Location****和****time zone**

![Exported image](_assets/%E5%BA%93-time/%E5%BA%93-time__13-00-46-0.png)

**Unix Time**  
可通过time.Time获取Unix时间  
**时间间隔**

![Exported image](_assets/%E5%BA%93-time/%E5%BA%93-time__13-00-47-1.png)

**时间操作****(Time****的操作****)**  
Add 增加时间  
Sub 两个时间之间的差值  
Equal 判断两个时间是否相同  
Before 是否在指定时间前  
After 是否在指定时间后  
**定时器**  
使用time.Tick来设置定时器，定时器的本质上是一个通道

![Exported image](_assets/%E5%BA%93-time/%E5%BA%93-time__13-00-49-2.png)

**时间格式化****time.Format**  
奇怪的

![Exported image](_assets/%E5%BA%93-time/%E5%BA%93-time__13-00-51-3.png)

**解析字符串格式的时间**

![Exported image](_assets/%E5%BA%93-time/%E5%BA%93-time__13-00-52-4.png)