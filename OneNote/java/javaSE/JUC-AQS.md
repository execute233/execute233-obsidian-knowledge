# JUC-AQS

比如我们执行了ReentrantLock的lock()方法，那它的内部是怎么在执行的呢？
它的内部实际上啥都没做，而是交给了Sync对象在进行，并且，不只是这个方法，其他的很多方法都是依靠Sync对象在进行
可以看到，公平锁和非公平锁都是继承自Sync，而Sync是继承自AbstractQueuedSynchronizer，简称队列同步器(AQS)
**底层实现**
AbstractQueuedSynchronizer（下面称为AQS）是实现锁机制的基础，它的内部封装了包括锁的获取、释放、以及等待队列。
一个锁（排他锁为例）的基本功能就是获取锁、释放锁、当锁被占用时，其他线程来争抢会进入等待队列，AQS已经将这些基本的功能封装完成了，其中等待队列是核心内容，等待队列是由双向链表数据结构实现的，每个等待状态下的线程都可以被封装进结点中并放入双向链表中，而对于双向链表是以队列的形式进行操作的，它像这样：

![[_assets/JUC-AQS/JUC-AQS__09-20-07-0.png]]

AQS中有一个head字段和一个tail字段分别记录双向链表的头结点和尾结点，而之后的一系列操作都是围绕此队列来进行的。我们先来了解一下每个结点都包含了哪些内容：
//每个处于等待状态的线程都可以是一个节点，并且每个节点是有很多状态的
static final class Node {
//每个节点都可以被分为独占模式节点或是共享模式节点，分别适用于独占锁和共享锁
static final Node SHARED = new Node();
static final Node EXCLUSIVE = null;
//等待状态，这里都定义好了
static final int CANCELLED = 1; // 唯一一个大于0的状态，表示已失效，可能是由于超时或中断，此节点被取消。
static final int SIGNAL = -1; // 此节点后面的节点被挂起（进入等待状态）
static final int CONDITION = -2; // 在条件队列中的节点才是这个状态
static final int PROPAGATE = -3; // 传播，一般用于共享锁
volatile int waitStatus; //等待状态值
volatile Node prev; //双向链表基操
volatile Node next;
volatile Thread thread; //每一个线程都可以被封装进一个节点进入到等待队列
Node nextWaiter; //在等待队列中表示模式，条件队列中作为下一个结点的指针
…
}
在一开始的时候，head和tail都是null，state为默认值0：
不用担心双向链表不会进行初始化，初始化是在实际使用时才开始的，先不管，我们接着来看其他的初始化内容：
//直接使用Unsafe类进行操作
private static final Unsafe unsafe = Unsafe.getUnsafe();
//记录类中属性的在内存中的偏移地址，方便Unsafe类直接操作内存进行赋值等（直接修改对应地址的内存）
private static final long stateOffset; //这里对应的就是AQS类中的state成员字段
private static final long headOffset; //这里对应的就是AQS类中的head头结点成员字段
private static final long tailOffset;
private static final long waitStatusOffset;
private static final long nextOffset;
static { //静态代码块，在类加载的时候就会自动获取偏移地址
…
}
//通过CAS操作来修改头结点
private final boolean compareAndSetHead(Node update) {
//调用的是Unsafe类的compareAndSwapObject方法，通过CAS算法比较对象并替换
return unsafe.compareAndSwapObject(this, headOffset, null, update);
}
//同上，省略部分代码
private final boolean compareAndSetTail(Node expect, Node update) {
private static final boolean compareAndSetWaitStatus(Node node, int expect, int update)
private static final boolean compareAndSetNext(Node node, Node expect, Node update)
对于AbstractQueuedSynchronizer类，它提供了一些可重写的方法（根据不同的锁类型和机制，可以自由定制规则，并且为独占式和非独占式锁都提供了对应的方法），以及一些已经写好的模板方法（模板方法会调用这些可重写的方法），使用此类只需要将可重写的方法进行重写，并调用提供的模板方法，从而实现锁功能
//独占式获取同步状态，查看同步状态是否和参数一致，如果返没有问题，那么会使用CAS操作设置同步状态并返回true
protected boolean tryAcquire(int arg) {throw new UnsupportedOperationException();}
//独占式释放同步状态
protected boolean tryRelease(int arg) { throw new UnsupportedOperationException();}
//共享式获取同步状态，返回值大于0表示成功，否则失败
protected int tryAcquireShared(int arg) {throw new UnsupportedOperationException();}
//共享式释放同步状态
protected boolean tryReleaseShared(int arg) {throw new UnsupportedOperationException();}
//是否在独占模式下被当前线程占用（锁是否被当前线程持有）
protected boolean isHeldExclusively() { throw new UnsupportedOperationException();}
**底层加锁实现**
先来看看ReentrantLock中的公平锁是如何借助AQS实现的
public void lock() {sync.lock();}
再来看该方法的具体细节：
@ReservedStackAccess //这个是JEP 270添加的新注解，它会保护被注解的方法，通过添加一些额外的空间，防止在多线程运行的时候出现栈溢出，下同
public final void acquire(int arg) {
if (!tryAcquire(arg) &&
acquireQueued(addWaiter(Node.EXCLUSIVE), arg)) //节点为独占模式Node.EXCLUSIVE
selfInterrupt();
}
首先会调用tryAcquire()方法（这里是由FairSync类实现的），如果尝试加独占锁失败（返回false了）说明可能这个时候有其他线程持有了此独占锁，所以当前线程得先等着，那么会调用addWaiter()方法将线程加入等待队列中：
private Node addWaiter(Node mode) {
Node node = new Node(Thread.currentThread(), mode);
// 先尝试使用CAS直接入队，如果这个时候其他线程也在入队（就是不止一个线程在同一时间争抢这把锁）就进入enq()
Node pred = tail;
if (pred != null) {
node.prev = pred;
if (compareAndSetTail(pred, node)) {
pred.next = node;
return node;
}
}
//此方法是CAS快速入队失败时调用
enq(node);
return node;
}
private Node enq(final Node node) {
//自旋形式入队，可以看到这里是一个无限循环
for (;;) {
Node t = tail;
if (t == null) { //这种情况只能说明头结点和尾结点都还没初始化
if (compareAndSetHead(new Node())) //初始化头结点和尾结点
tail = head;
} else {
node.prev = t;
if (compareAndSetTail(t, node)) {
t.next = node;
return t; //只有CAS成功的情况下，才算入队成功，如果CAS失败，那说明其他线程同一时间也在入队，并且手速还比当前线程快，刚好走到CAS操作的时候，其他线程就先入队了，那么这个时候node.prev就不是我们预期的节点了，而是另一个线程新入队的节点，所以说得进下一次循环再来一次CAS，这种形式就是自旋
}
}
}
}
addWaiter()会返回已经加入的节点，acquireQueued()在得到返回的节点时，也会进入自旋状态，等待唤醒（也就是开始进入到拿锁的环节了）：
@ReservedStackAccess
final boolean acquireQueued(final Node node, int arg) {
boolean failed = true;
try {
boolean interrupted = false;
for (;;) {
final Node p = node.predecessor();
if (p == head && tryAcquire(arg)) { //可以看到当此节点位于队首(node.prev == head)时，会再次调用tryAcquire方法获取锁，如果获取成功，会返回此过程中是否被中断的值
setHead(node); //新的头结点设置为当前结点
p.next = null; // 原有的头结点没有存在的意义了
failed = false; //没有失败
return interrupted; //直接返回等待过程中是否被中断
}
//依然没获取成功，
if (shouldParkAfterFailedAcquire(p, node) && //将当前节点的前驱节点等待状态设置为SIGNAL，如果失败将直接开启下一轮循环，直到成功为止，如果成功接着往下
parkAndCheckInterrupt()) //挂起线程进入等待状态，等待被唤醒，如果在等待状态下被中断，那么会返回true，直接将中断标志设为true，否则就是正常唤醒，继续自旋
interrupted = true;
}
} finally {
if (failed)
cancelAcquire(node);
}
}
private final boolean parkAndCheckInterrupt() {
LockSupport.park(this); //通过unsafe类操作底层挂起线程（会直接进入阻塞状态）
return Thread.interrupted();
}
有个静态方法注意下：
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
int ws = pred.waitStatus;
if (ws == Node.SIGNAL)
return true; //已经是SIGNAL，直接true
if (ws > 0) { //不能是已经取消的节点，必须找到一个没被取消的
do {
node.prev = pred = pred.prev;
} while (pred.waitStatus > 0);
pred.next = node; //直接抛弃被取消的节点
} else {
//不是SIGNAL，先CAS设置为SIGNAL（这里没有返回true因为CAS不一定成功，需要下一轮再判断一次）
compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
}
return false; //返回false，马上开启下一轮循环
}
最后再来看看公平锁的tryAcquire

```java
static final class FairSync extends Sync {
  	//
```

可重入独占锁的公平实现

```java
    @ReservedStackAccess
    protected final boolean tryAcquire(int acquires) {
        final Thread current = Thread.currentThread();   //
```

先获取当前线程的`Thread`对象
`int c = getState(); //`获取当前`AQS`对象状态（独占模式下`0`为未占用，大于`0`表示已占用）
`if (c == 0) { //`如果是`0`，那就表示没有占用，现在我们的线程就要来尝试占用它
`if (!hasQueuedPredecessors() && //`等待队列是否不为空且当前线程没有拿到锁，其实就是看看当前线程有没有必要进行排队，如果没必要排队，就说明可以直接获取锁
`compareAndSetState(0, acquires)) { //CAS`设置状态，如果成功则说明成功拿到了这把锁，失败则说明可能这个时候其他线程在争抢，并且还比你先抢到
`setExclusiveOwnerThread(current); //`成功拿到锁，会将独占模式所有者线程设定为当前线程（这个方法是父类`AbstractOwnableSynchronizer`中的，就表示当前这把锁已经是这个线程的了）
`return true; //`占用锁成功，返回

```java
true
            }
        }
        else if (current == getExclusiveOwnerThread()) {   //
```

如果不是`0`，那就表示被线程占用了，这个时候看看是不是自己占用的，如果是，由于是可重入锁，可以继续加锁
`int nextc = c + acquires; //`多次加锁会将状态值进行增加，状态值就是加锁次数
`if (nextc \< 0) //`加到`int`值溢出了？

```java
                throw new Error("Maximum lock count exceeded");
            setState(nextc);   //
```

设置为新的加锁次数

```java
            return true;
        }
        return false;   //
```

其他任何情况都是加锁失败

```java
    }
}
```
 **底层解锁实现**
实际上还是委托给AbstractQueuedSynchronizer的release方法,参数1表示解锁一次state值-1
@ReservedStackAccess
public final boolean release(int arg) {
if (tryRelease(arg)) { //和tryAcquire一样，也得子类去重写，释放锁操作
Node h = head; //释放锁成功后，获取新的头结点
if (h != null && h.waitStatus != 0) //如果新的头结点不为空并且不是刚刚建立的结点（初始状态下status为默认值0，而上面在进行了shouldParkAfterFailedAcquire之后，会被设定为SIGNAL状态，值为-1）
unparkSuccessor(h); //唤醒头节点下一个节点中的线程
return true;
}
return false;
}
来看unparkSuccessor是如何唤醒下一个节点的：
private void unparkSuccessor(Node node) {
// 将等待状态waitStatus设置为初始值0
int ws = node.waitStatus;
if (ws < 0)
compareAndSetWaitStatus(node, ws, 0);

```java
    //获取下一个结点
    Node s = node.next;
    if (s == null || s.waitStatus \> 0) {   //如果下一个结点为空或是等待状态是已取消，那肯定是不能通知unpark的，这时就要遍历所有节点再另外找一个符合unpark要求的节点了
        s = null;
        for (Node t = tail; t != null && t != node; t = t.prev)   //这里是从队尾向前，因为enq()方法中的t.next = node是在CAS之后进行的，而 node.prev = t 是CAS之前进行的，所以从后往前一定能够保证遍历所有节点
            if (t.waitStatus \<= 0)
                s = t;
    }
    if (s != null)   //要是找到了，就直接unpark，要是还是没找到，那就算了
        LockSupport.unpark(s.thread);
}
再来看如何tryRelease释放锁：
@ReservedStackAccess
protected final boolean tryRelease(int releases) {
    int c = getState() - releases;   //先计算本次解锁之后的状态值
    if (Thread.currentThread() != getExclusiveOwnerThread())   //因为是独占锁，那肯定这把锁得是当前线程持有才行
        throw new IllegalMonitorStateException();   //否则直接抛异常
    boolean free = false;
    if (c == 0) {  //如果解锁之后的值为0，表示已经完全释放此锁
        free = true;
        setExclusiveOwnerThread(null);  //将独占锁持有线程设置为null
    }
    setState(c);   //状态值设定为c
    return free;  //如果不是0表示此锁还没完全释放，返回false，是0就返回true
}
综上，流程图：
```

![[_assets/JUC-AQS/JUC-AQS__09-20-09-1.png]]

**Condition****实现原理**
通过前面的学习，我们知道`Condition`类实际上就是用于代替传统对象的`wait/notify`操作的，同样可以实现等待`/`通知模式，并且同一把锁下可以创建多个`Condition`对象。那么我们接着来看看，它又是如何实现的呢，我们先从单个`Condition`对象进行分析：

在`AQS`中，`Condition`有一个实现类`ConditionObject`，而这里也是使用了链表实现了条件队列：
public class ConditionObject implements Condition, java.io.Serializable {
private static final long serialVersionUID = 1173984872572414699L;
/** 条件队列的头结点 */
private transient Node firstWaiter;
/** 条件队列的尾结点 */
private transient Node lastWaiter;
…
这里是直接使用了AQS中的Node类，但是使用的是Node类中的nextWaiter字段连接节点，并且Node的status为CONDITION：

![[_assets/JUC-AQS/JUC-AQS__09-20-14-2.png]]

而这里的条件队列，正是用于存储这些处于等待状态的线程。
我们先来看看最关键的await()方法是如何实现的，为了防止一会绕晕，在开始之前，我们先明确此方法的目标：

- 只有已经持有锁的线程才可以使用此方法
- 当调用此方法后，会直接释放锁，无论加了多少次锁
- 只有其他线程调用signal()或是被中断时才会唤醒等待中的线程
- 被唤醒后，需要等待其他线程释放锁，拿到锁之后才可以继续执行，并且会恢复到之前的状态（await之前加了几层锁唤醒后依然是几层锁）

await源码如下：
public final void await() throws InterruptedException {
if (Thread.interrupted())
throw new InterruptedException(); //如果在调用await之前就被添加了中断标记，那么会直接抛出中断异常
Node node = addConditionWaiter(); //为当前线程创建一个新的节点，并将其加入到条件队列中
int savedState = fullyRelease(node); //完全释放当前线程持有的锁，并且保存一下state值，因为唤醒之后还得恢复
int interruptMode = 0; //用于保存中断状态
while (!isOnSyncQueue(node)) { //循环判断是否位于同步队列中，如果等待状态下的线程被其他线程唤醒，那么会正常进入到AQS的等待队列中（之后我们会讲）
LockSupport.park(this); //如果依然处于等待状态，那么继续挂起
if ((interruptMode = checkInterruptWhileWaiting(node)) != 0) //看看等待的时候是不是被中断了
break;
}
//出了循环之后，那线程肯定是已经醒了，这时就差拿到锁就可以恢复运行了
if (acquireQueued(node, savedState) && interruptMode != THROW_IE) //直接开始acquireQueued尝试拿锁（之前已经讲过了）从这里开始基本就和一个线程去抢锁是一样的了
interruptMode = REINTERRUPT;
//已经拿到锁了，基本可以开始继续运行了，这里再进行一下后期清理工作
if (node.nextWaiter != null)
unlinkCancelledWaiters(); //将等待队列中，不是Node.CONDITION状态的节点移除
if (interruptMode != 0) //依然是响应中断
reportInterruptAfterWait(interruptMode);
//OK，接着该干嘛干嘛
}
实际上await()方法比较中规中矩，大部分操作也在我们的意料之中，那么我们接着来看signal()方法是如何实现的，同样的，为了防止各位绕晕，先明确signal的目标：

- 只有持有锁的线程才能唤醒锁所属的Condition等待的线程
- 优先唤醒条件队列中的第一个，如果唤醒过程中出现问题，接着找往下找，直到找到一个可以唤醒的
- 唤醒操作本质上是将条件队列中的结点直接丢进AQS等待队列中，让其参与到锁的竞争中
- 拿到锁之后，线程才能恢复运行
![[_assets/JUC-AQS/JUC-AQS__09-20-16-3.png]]

源码如下：
public final void signal() {
if (!isHeldExclusively()) //先看看当前线程是不是持有锁的状态
throw new IllegalMonitorStateException(); //不是？那你不配唤醒别人
Node first = firstWaiter; //获取条件队列的第一个结点
if (first != null) //如果队列不为空，获取到了，那么就可以开始唤醒操作
doSignal(first);
}
private void doSignal(Node first) {
do {
if ( (firstWaiter = first.nextWaiter) == null) //如果当前节点在本轮循环没有后继节点了，条件队列就为空了
lastWaiter = null; //所以这里相当于是直接清空
first.nextWaiter = null; //将给定节点的下一个结点设置为null，因为当前结点马上就会离开条件队列了
} while (!transferForSignal(first) && //接着往下看
(first = firstWaiter) != null); //能走到这里只能说明给定节点被设定为了取消状态，那就继续看下一个结点
}
final boolean transferForSignal(Node node) {
/*
* 如果这里CAS失败，那有可能此节点被设定为了取消状态
*/
if (!compareAndSetWaitStatus(node, Node.CONDITION, 0))
return false;

```java
    //CAS成功之后，结点的等待状态就变成了默认值0，接着通过enq方法直接将节点丢进AQS的等待队列中，相当于唤醒并且可以等待获取锁了
  	//这里enq方法返回的是加入之后等待队列队尾的前驱节点，就是原来的tail
    Node p = enq(node);
    int ws = p.waitStatus;   //保存前驱结点的等待状态
  	//如果上一个节点的状态为取消, 或者尝试设置上一个节点的状态为SIGNAL失败（可能是在ws\>0判断完之后马上变成了取消状态，导致CAS失败）
    if (ws \> 0 || !compareAndSetWaitStatus(p, ws, Node.SIGNAL))
        LockSupport.unpark(node.thread);  //直接唤醒线程
    return true;
}
其实最让人不理解的就是倒数第二行，明明上面都正常进入到AQS等待队列了，应该是可以开始走正常流程了，那么这里为什么还要提前来一次unpark呢？
这里其实是为了进行优化而编写，直接unpark会有两种情况：
```

- 如果插入结点前，AQS等待队列的队尾节点就已经被取消，则满足wc > 0
- 如果插入node后，AQS内部等待队列的队尾节点已经稳定，满足tail.waitStatus == 0，但在执行ws >0之后!compareAndSetWaitStatus(p, ws,Node.SIGNAL)之前被取消，则CAS也会失败，满足compareAndSetWaitStatus(p, ws,Node.SIGNAL) == false

如果这里被提前unpark，那么在await()方法中将可以被直接唤醒，并跳出while循环，直接开始争抢锁，因为前一个等待结点是被取消的状态，没有必要再等它了。
所以大致流程如下：

![[_assets/JUC-AQS/JUC-AQS__09-20-17-4.png]]