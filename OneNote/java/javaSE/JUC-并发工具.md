---
title: JUC-并发工具
tags: [java, javaSE]
aliases: [JUC-并发工具]
---

# JUC-并发工具

**计数器锁** **CountDownLatch**
比如有一个需求：

- 有20个计算任务，我们需要先将这些任务的结果全部计算出来，每个任务的执行时间未知
- 当所有任务结束之后，立即整合统计最终结果

new CountDownLatch（20）； // 创建一个初始值为20的计数器锁
… // 这里运行多个线程，任务完成后调用countDown方法，使计数器减1
主线程即可调用其await方法，当计数器为0时恢复运行
**循环屏障 CyclicBarrier**
假如现在游戏房间内一共5人，但是游戏开始需要10人，所以我们必须等待剩下5人到来之后才能开始游戏，并且保证游戏开始时所有玩家都是同时进入，那么怎么实现这个功能呢？我们可以使用CyclicBarrier，翻译过来就是循环屏障，那么这个屏障正式为了解决这个问题而出现的。

- new CyclicBarrier（10， （） -> {…}）； // 创建需要10人的循环屏障，指定人等够后执行的任务
- … 创建多个线程，每个线程里都调用其await方法，会让当前线程等待 …
- 当然，这是个循环屏障，冲破后是重新计数可以再次冲破

注意在等待的线程被中断，会导致屏障被损坏，只能通过reset方法重置
**信号量 Semaphore**
通过使用信号量，我们可以决定某个资源同一时间能够被访问的最大线程数，它相当于对某个资源的访问进行了流量控制。
简单来说，它就是一个可以被N个线程占用的排它锁（因此也支持公平和非公平模式），我们可以在最开始设定Semaphore的许可证数量，每个线程都可以获得1个或n个许可证，当许可证耗尽或不足以供其他线程获取时，其他线程将被阻塞。
通过构造方法来指定许可证的配额，acquire和release来申请和归还指定数量的许可证
**数据交换 Exchanger<T>**
两个线程调用同一个exchange方法，有一个线程会阻塞，该方法的返回值是另一个线程传入的数据
**Fork/Join 框架**
在JDK7时，出现了一个新的框架用于并行执行任务，它的目的是为了把大型任务拆分为多个小任务，最后汇总多个小任务的结果，得到整大任务的结果，并且这些小任务都是同时在进行，大大提高运算效率。Fork就是拆分，Join就是合并。

![[_assets/JUC-并发工具/JUC-并发工具__09-20-32-0.png]]

它不仅仅只是拆分任务并使用多线程，而且还可以利用工作窃取算法，提高线程的利用率。

![[_assets/JUC-并发工具/JUC-并发工具__09-20-37-1.png]]

首先需要new ForkJoinPool，这东西类似于线程池，同样的可以submit，但需要继承RecursiveTask<T>类，其中泛型是返回的结果类型，可以通过自定义方法构造实现传入数据，这里以1到100求和为例
```java
public class Main {
public static void main(String[] args) throws InterruptedException, ExecutionException {
ForkJoinPool pool = new ForkJoinPool();
System.out.println(pool.submit(new SubTask(1, 1000)).get());
```
}


```xml
  	//继承RecursiveTask,这样才可以作为一个任务,泛型就是计算结果类型
    private static class SubTask extends RecursiveTask\<Integer\> {
        private final int start;   //比如我们要计算一个范围内所有数的和,那么就需要限定一下范围,这里用了两个int存放
        private final int end;
```

```java
        public SubTask(int start, int end) {
            this.start = start;
            this.end = end;
        }
```

```java
        @Override
        protected Integer compute() {
            if(end - start \> 125) {    //每个任务最多计算125个数的和,如果大于继续拆分,小于就可以开始算了
                SubTask subTask1 = new SubTask(start, (end + start) / 2);
                subTask1.fork();    //会继续划分子任务执行
                SubTask subTask2 = new SubTask((end + start) / 2 + 1, end);
                subTask2.fork();   //会继续划分子任务执行
                return subTask1.join() + subTask2.join();   //越玩越有递归那味了
            } else {
                System.out.println(Thread.currentThread().getName()+" 开始计算 "+start+"-"+end+" 的值!");
                int res = 0;
                for (int i = start; i \<= end; i++) {
                    res += i;
                }
                return res;   //返回的结果会作为join的结果
            }
        }
    }
}
```