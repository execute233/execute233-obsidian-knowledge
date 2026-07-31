# Spring-高级特性

1. Bean Aware
2. 任务调度
3. 监听器
在Spring中提供了一些以Aware结尾的接囗，实现了Aware接囗的bean在被初始化之后，可以获取相资源。
简单来说，他就是一个标识，实现此接囗的类会获得某些感知能力，Springe器会在Bean被加载时，根据类实现的感知接囗，会调用类中实现的对应感知方法，有这些接口和更多的使用
BeanNameAware - 获取该Bean名称
ApplicationContextAware - 获得ApplicationContext引用，但会导致代码与Spring框架耦合
BeanFactoryAware - 获得BeanFactory引用
EnvironmentAware - 获得Environment对象
ResourceLoaderAware - 获得ResourceLoader
MessageSourceAware- 获得MessageSource用于国际化消息
ApplicationEnventPublisherAware - 获得ApplicationEnventPublisher用于发布事件
为了执行某些任务，我们可能需要一些非常规的操作，比如我们希望使用线程来处理我们的结果或是执行一些定时任务，到达指定时间后再去执行。这时我们首先想到的就是创建一个新的线程来处理，或是使用TimerTask来完成定时任务，但是我们有了Spring框架之后，就不用这样了，因为Spring框架为我们提供了更加便捷的方式进行任务调度。

异步方法调用
首先要开启异步支持，在@Configuration修饰类在修饰@EnableAsync
然后在Bean类的成员方法(返回void或Future)打上@Async，之后得到该Bean对象调用相应的方法就可以异步执行了
定时任务（会让程序一直运行）
首先要开启定时任务支持，在@Configuration修饰类在修饰@EnableScheduling
然后在Bean类的成员方法打上@Scheduled，无需主动调用就可以定时运行这个方法了
fixedRate - 固定速率执行，单位毫秒
fixedDelay - 固定延迟执行（前一次完成后延迟指定时间到下一次），单位毫秒
initialDelay - 应用启动一段时间后开始第一次执行
cron - 复杂时间规则
cron表达式由6或7个字段组成
秒 分 时 日 月 周 [年]
有以下字段
* - 任意值
, - 多个值
- 指定范围
/ - 指定步长
? - 不指定值（只在日期和星期有效）
L - 最后一个，通常用于月份和星期字段
W - 最近的工作日，仅在日期字段有效
# - 每个月的第几个星期几，比如2#3是每个月第三个星期二
例子：
0 0 6 * * ？ 每天早上6点
0 0 */1 * * 每个小时整点
0 0 0 1 * ? 每月一号午夜进行
要编写监听器，我们只需要让Bean继承ApplicationListener<T>就可以了，并且将类型指定为对应的Event事件，这样，当发生某个时就会通知我们，比如ContextRefreshedEvent，这个事件会在Spring容器初始化完成会触发一次