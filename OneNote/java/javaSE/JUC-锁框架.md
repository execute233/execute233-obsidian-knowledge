---
title: JUC-锁框架
tags: [java, javaSE]
aliases: [JUC-锁框架]
---

# JUC-锁框架

在 JDK 5 之后,并发包中新增了 `Lock` 接口(以及相关实现类)用来实现锁功能,`Lock` 接口提供了与 `synchronized` 关键字类似的同步功能,但需要在使用时手动获取锁和释放锁。`ReentrantLock` 的内部实现是基于 [[JUC-AQS]] 队列同步器的。

## Lock 与 Condition 接口

```java
public interface Lock {
    // 获取锁,拿不到锁会阻塞,等待其他线程释放锁,获取到锁后返回
    void lock();

    // 同上,但是等待过程中会响应中断
    void lockInterruptibly() throws InterruptedException;

    // 尝试获取锁,但是不会阻塞,如果能获取到会返回 true,不能返回 false
    boolean tryLock();

    // 尝试获取锁,但是可以限定超时时间,如果超出时间还没拿到锁返回 false,否则返回 true,可以响应中断
    boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

    // 释放锁
    void unlock();

    // 暂时可以理解为替代传统的 Object 的 wait()、notify() 等操作的工具
    Condition newCondition();
}
```

那么,我们如何像传统的加锁那样,调用对象的 `wait()` 和 `notify()` 方法呢,并发包提供了 `Condition` 接口:

```java
public interface Condition {
    // 与调用锁对象的 wait 方法一样,会进入到等待状态,但是这里需要调用 Condition 的 signal 或 signalAll 方法进行唤醒
    // (感觉就是和普通对象的 wait 和 notify 是对应的)同时,等待状态下是可以响应中断的
    void await() throws InterruptedException;

    // 同上,但不响应中断
    void awaitUninterruptibly();

    // 等待指定时间,如果在指定时间(纳秒)内被唤醒,会返回剩余时间,如果超时,会返回 0 或负数,可以响应中断
    long awaitNanos(long nanosTimeout) throws InterruptedException;

    // 等待指定时间(可以指定时间单位),如果等待时间内被唤醒,返回 true,否则返回 false,可以响应中断
    boolean await(long time, TimeUnit unit) throws InterruptedException;

    // 可以指定一个明确的时间点,如果在时间点之前被唤醒,返回 true,否则返回 false,可以响应中断
    boolean awaitUntil(Date deadline) throws InterruptedException;

    // 唤醒一个处于等待状态的线程,注意还得获得锁才能接着运行
    void signal();

    // 同上,但是是唤醒所有等待线程
    void signalAll();
}
```

## 可重入锁 ReentrantLock

简单来说,就是同一个线程,可以反复进行加锁操作:假设连续加了 n 次该锁,其他线程只有当前线程连续释放了 n 次该锁才能拿到锁。

有几个特有的方法(同样的,`Condition` 也有类似的方法):

- `getHoldCount()`:查看当前线程的加锁次数。
- `getQueueLength()`:获取等待中线程数量的预估值。
- `hasQueueThread(Thread)`:指定线程是否在等待队列中。

## 公平锁与非公平锁(如何去拿到锁)

- **公平锁**:多个线程按照申请锁的顺序去获得锁,线程会直接进入队列去排队,永远都是队列的第一位才能得到锁。
- **非公平锁**:多个线程去获取锁的时候,会直接去尝试获取,获取不到,再去进入等待队列,如果能获取到,就直接获取到锁。

简单来说,公平锁不让插队,都老老实实排着;非公平锁让插队,但是排队的人让不让你插队就是另一回事了。

## 读写锁

可重入锁是一种排他锁,当一个线程得到锁之后,另一个线程必须等待其释放锁,否则一律不允许获取到锁。而读写锁在同一时间,是可以让多个线程获取到锁的,它其实就是针对于读写场景而出现的。

读写锁维护了一个读锁和一个写锁,这两个锁的机制是不同的:

- **读锁**:在没有任何线程占用写锁的情况下,同一时间可以有多个线程加读锁。
- **写锁**:在没有任何线程占用读锁的情况下,同一时间只能有一个线程加写锁。

读写锁有个专门的接口:

```java
public interface ReadWriteLock {
    Lock readLock();   // 获取读锁
    Lock writeLock();  // 获取写锁
}
```

有一个实现类 `ReentrantReadWriteLock`(非 `Lock` 接口),需要主动获取读锁还是写锁。

多个线程可以同时对读锁加锁,但有读锁状态下不能加写锁,反之亦然。

并且,`ReentrantReadWriteLock` 不仅具有读写锁的功能,还保留了可重入锁和公平 / 非公平机制,比如同一个线程可以重复为写锁加锁,并且必须全部解锁才真正释放锁。

## 锁降级与锁升级

**锁降级**指的是持有写锁时再加读锁。当一个线程持有写锁的情况下,虽然其他线程不能加读锁,但是线程自己是可以加读锁的。

注意可以写锁 → 读锁,但不能读锁 → 写锁。

**锁升级**指的是持有读锁时再加写锁,`ReentrantReadWriteLock` 是不支持的。