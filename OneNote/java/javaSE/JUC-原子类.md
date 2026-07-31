前面我们说到，如果要保证i++的原子性，那么我们的唯一选择就是加锁，那么，除了加锁之外，还有没有其他更好的解决方法呢？JUC为我们提供了原子类，底层采用CAS算法，它是一种用法简单、性能高效、线程安全地更新变量的方式。

所有的原子类都位于java.util.concurrent.atomic包下。

**原子类介绍**
常用基本数据类，有对应的原子类封装：
AtomicInteger：原子更新int
AtomicLong：原子更新long
AtomicBoolean：原子更新boolean
AtomicIntegerArray：原子更新int数组
AtomicLongArray：原子更新long数组
AtomicBooleanArray：原子更新boolean数组
ABA类问题可以使用版本号来解决，java提供了这个类来提供带版本的支持
AtomicStampedReference\<T \>