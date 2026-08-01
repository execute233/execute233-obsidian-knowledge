---
title: JUC-并发容器
tags: [java, javaSE]
aliases: [JUC-并发容器]
---

# JUC-并发容器

JDK 提供的这些容器大部分在 `java.util.concurrent` 包中。

- `ConcurrentHashMap`:线程安全的 HashMap。
- `CopyOnWriteArrayList`:线程安全的 List,在读多写少的场合性能非常好,远远好于 Vector。
- `CopyAndWrite`:线程安全的 ArrayList。
- `ConcurrentLinkedQueue`:高效的并发队列,使用链表实现。可以看做一个线程安全的 LinkedList,这是一个非阻塞队列。
- `ArrayBlockingQueue`:有界带缓冲阻塞队列(就是队列是有容量限制的,装满了肯定是不能再装的,只能阻塞,数组实现)。
- `LinkedBlockingQueue`:无界带缓冲阻塞队列(没有容量限制,也可以限制容量,也会阻塞,链表实现)。
- `PriorityBlockingQueue`:支持优先级的无界阻塞队列。
- `SynchronousQueue`:无缓冲阻塞队列(相当于没有容量的 ArrayBlockingQueue,因此只有阻塞的情况)。
- `ConcurrentSkipListMap`:跳表的实现。这是一个 Map,使用跳表的数据结构进行快速查找。

## ConcurrentHashMap

HashMap 是线程不安全的,如果在并发场景下使用,一种常见的解决方式是通过 `Collections.synchronizedMap()` 方法对 HashMap 进行包装,使其变为线程安全。不过,这种方式是通过一个全局锁来同步不同线程间的并发访问,会导致严重的性能瓶颈,尤其是在高并发场景下。

为了解决这一问题,`ConcurrentHashMap` 应运而生,作为 HashMap 的线程安全版本,它提供了更高效的并发处理能力。

### JDK 1.7

`ConcurrentHashMap` 对整个桶数组进行了分割分段(`Segment`,分段锁),每一把锁只锁容器其中一部分数据(下面有示意图),多线程访问容器里不同数据段的数据,就不会存在锁竞争,提高并发访问率。

![[_assets/JUC-并发容器/JUC-并发容器__09-20-24-0.png]]

### JDK 1.8

取消了 Segment 分段锁,采用 Node + CAS + synchronized 来保证并发安全。数据结构跟 HashMap 1.8 的结构类似,数组 + 链表 / 红黑二叉树。Java 8 在链表长度超过一定阈值(8)时将链表(寻址时间复杂度为 O(N))转换为红黑树(寻址时间复杂度为 O(log N))。

同时,锁粒度更细,`synchronized` 只锁定当前链表或红黑二叉树的首节点,这样只要 hash 不冲突,就不会产生并发,就不会影响其他 Node 的读写,效率大幅提升。

![[_assets/JUC-并发容器/JUC-并发容器__09-20-26-1.png]]

## CopyOnWriteArrayList

### before JDK 1.5

对于并发安全的 List 只能选择 Vector,它只是对 CURD 操作基本都加了 `synchronized`。

### JDK 1.5

引入了该类,操作思想与 `ReentrantReadWriteLock` 类似,不同的是写入操作是不会阻塞读取操作的,只有写写互斥,主要是采用了写时复制(Copy On Write)策略,进行修改操作时是先修改副本,修改完后副本再更新回去。

## ConcurrentLinkedQueue

`ConcurrentLinkedQueue` 非阻塞队列适合在对性能要求相对较高,同时对队列的读写存在多个线程同时进行的场景,即如果对队列加锁的成本较高则适合使用无锁的 `ConcurrentLinkedQueue` 来替代。

## BlockingQueue 接口

阻塞队列(`BlockingQueue`)被广泛使用在"生产者-消费者"问题中,其原因是 `BlockingQueue` 提供了可阻塞的插入和移除的方法。当队列容器已满,生产者线程会被阻塞,直到队列未满;当队列容器为空时,消费者线程会被阻塞,直至队列非空时为止。

## ArrayBlockingQueue(有界队列)

`ArrayBlockingQueue` 一旦创建,容量不能改变。其并发控制采用可重入锁 `ReentrantLock`,不管是插入操作还是读取操作,都需要获取到锁才能进行操作。当队列容量满时,尝试将元素放入队列将导致操作阻塞;尝试从一个空队列中取一个元素也会同样阻塞。

`ArrayBlockingQueue` 默认情况下不能保证线程访问队列的公平性,如果保证公平性,通常会降低吞吐量。我们可以在构造的时候设置其公平性。

## LinkedBlockingQueue

底层基于单向链表实现的阻塞队列,可以当做无界队列也可以当做有界队列来使用,同样满足 FIFO 的特性,与 `ArrayBlockingQueue` 相比起来具有更高的吞吐量。为了防止 `LinkedBlockingQueue` 容量迅速增,损耗大量内存。通常在创建 `LinkedBlockingQueue` 对象时,会指定其大小,如果未指定,容量等于 `Integer.MAX_VALUE`。

## PriorityBlockingQueue

支持优先级的无界阻塞队列。默认情况下元素采用自然顺序进行排序,也可以通过自定义类实现 `compareTo()` 方法来指定元素排序规则,或者初始化时通过构造器参数 `Comparator` 来指定排序规则。

并发控制采用的是可重入锁 `ReentrantLock`,队列为无界队列。

简单地说,它就是 `PriorityQueue` 的线程安全版本。不可以插入 `null` 值,同时,插入队列的对象必须是可比较大小的(`Comparable`)。它的插入操作 `put` 方法不会 block,因为它是无界队列(`take` 方法在队列为空的时候会阻塞)。

## ConcurrentSkipListMap

跳表的本质是同时维护了多个链表,并且链表是分层的,

![[_assets/JUC-并发容器/JUC-并发容器__09-20-27-2.jpeg]]

从上面很容易看出,跳表是一种利用空间换时间的算法。

使用跳表实现 Map 和使用哈希算法实现 Map 的另外一个不同之处是:哈希并不会保存元素的顺序,而跳表内所有的元素都是排序的。因此在对跳表进行遍历时,你会得到一个有序的结果。