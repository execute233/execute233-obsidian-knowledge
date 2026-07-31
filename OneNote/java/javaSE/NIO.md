# NIO

Buffer类及其实现
Buffer类是缓冲区的实现，类似于Java中的数组，也是用于存放和获取数据的。但是Buffer相比Java中的数组，功能就非常强大了，它包含一系列对于数组的快捷操作
```csharp
public abstract class Buffer {
// 这四个变量的关系: mark <= position <= limit <= capacity
private int mark = -1;
private int position = 0;
private int limit;
private int capacity;
```
// 直接缓冲区实现子类的数据内存地址（之后会讲解）
long address;}
Buffer类的子类包含很多基本类型，以XXXBuffer(除了Boolean)命名，但这些也是抽象类，但可以通过静态方法获取对象
allocate() 申请固定大小的缓冲区，或者通过warp把数组变为缓冲区
**缓冲区读写操作**
存数据的有以下四种方法：
```java
public abstract IntBuffer put(int i); - 在当前position位置插入数据，由具体子类实现
public abstract IntBuffer put(int index, int i); - 在指定位置存放数据，也是由具体子类实现
public final IntBuffer put(int[] src); - 直接存放所有数组中的内容（数组长度不能超出缓冲区大小）
public IntBuffer put(int[] src, int offset, int length); - 直接存放数组中的内容，同上，但是可以指定存放一段范围
public IntBuffer put(IntBuffer src); - 直接存放另一个缓冲区中的内容
```
读操作也有四个方法：
```java
public abstract int get(); - 直接获取当前position位置的数据，由子类实现
public abstract int get(int index); - 获取指定位置的数据，也是子类实现
public IntBuffer get(int[] dst) - 将数据读取到给定的数组中
public IntBuffer get(int[] dst, int offset, int length) - 同上，加了个范围
```
**缓冲区的其它操作**
```java
public abstract IntBuffer compact() - 压缩缓冲区，由具体实现类实现
public IntBuffer duplicate() - 复制缓冲区，会直接创建一个新的数据相同的缓冲区
public abstract IntBuffer slice() - 划分缓冲区，会将原本的容量大小的缓冲区划分为更小的出来进行操作
public final Buffer rewind() - 重绕缓冲区，其实就是把position归零，然后mark变回-1
public final Buffer clear() - 将缓冲区清空，所有的变量变回最初的状态
```
**通道接口层次**

![[_assets/NIO/NIO__09-20-40-0.png]]

```java
除了读写之外，Channel还可以具有响应中断的能力：
public interface InterruptibleChannel extends Channel {
  	//当其他线程调用此方法时，在此通道上处于阻塞状态的线程会直接抛出 AsynchronousCloseException 异常
    public void close() throws IOException;
}
//这是InterruptibleChannel的抽象实现，完成了一部分功能
public abstract class AbstractInterruptibleChannel implements Channel, InterruptibleChannel {
//加锁关闭操作用到
    private final Object closeLock = new Object();
  //当前Channel的开启状态
    private volatile boolean open = true;
    protected AbstractInterruptibleChannel() { }
    //关闭操作实现
    public final void close() throws IOException {
        synchronized (closeLock) {   //同时只能有一个线程进行此操作，加锁
            if (!open)   //如果已经关闭了，那么就不用继续了
                return;
            open = false;   //开启状态变成false
            implCloseChannel();   //开始关闭通道
        }
    }
    //该方法由 close 方法调用，以执行关闭通道的具体操作，仅当通道尚未关闭时才调用此方法，不会多次调用。
    protected abstract void implCloseChannel() throws IOException;
```

```java
    public final boolean isOpen() {
        return open;
    }
```

```java
    //开始阻塞（有可能一直阻塞下去）操作之前，需要调用此方法进行标记，
    protected final void begin() {
        ...
    }
```

```java
  	//阻塞操作结束之后，也需要需要调用此方法，为了防止异常情况导致此方法没有被调用，建议放在finally中
    protected final void end(boolean completed)
...
    }
...
    }
而之后的一些实现类，都是基于这些接口定义的方法去进行实现的，比如FileChannel：
```

![[_assets/NIO/NIO__09-20-42-1.png]]

```java
我们可以使用通道代替传统读取：
//缓冲区创建好，一会就靠它来传输数据
    ByteBuffer buffer = ByteBuffer.allocate(10);
    //将System.in作为输入源，一会Channel就可以从这里读取数据，然后通过缓冲区装载一次性传递数据
    ReadableByteChannel readChannel = Channels.newChannel(System.in);
    while (true) {
        //将通道中的数据写到缓冲区中，缓冲区最多一次装10个
        readChannel.read(buffer);
        //写入操作结束之后，需要进行翻转，以便接下来的读取操作
        buffer.flip();
        //最后转换成String打印出来康康
        System.out.println("读取到一批数据："+new String(buffer.array(), 0, buffer.remaining()));
        //回到最开始的状态
        buffer.clear();
    }
**文件传输****FileChannel**
//RandomAccessFile能够支持文件的随机访问，并且实现了数据流
public class RandomAccessFile implements DataOutput, DataInput, Closeable
可以使用RandomAccessFile创建
```

```java
r  以只读的方式使用
```

- rw 读操作和写操作都可以
- rws 每当进行写操作，同步的刷新到磁盘，刷新内容和元数据
- rwd 每当进行写操作，同步的刷新到磁盘，刷新内容

```java
try(RandomAccessFile f = new RandomAccessFile("test.txt", "rw");
        FileChannel channel = f.getChannel()){   //通过RandomAccessFile创建一个通道
        channel.write(ByteBuffer.wrap("伞兵二号马飞飞准备就绪！".getBytes()));
        System.out.println("写操作完成之后文件访问位置："+channel.position());  //注意读取也是从现在的位置开始
        channel.position(0);  //需要将位置变回到最前面，这样下面才能从文件的最开始进行读取
        ByteBuffer buffer = ByteBuffer.allocate(128);
        channel.read(buffer);
        buffer.flip();
        System.out.println(new String(buffer.array(), 0, buffer.remaining()));
    }
```

```java
使用filp方法来反转读写
也可以使用truncate对文件进行截断
文件拷贝可以使用transferTo/From方法
当我们要编辑某个文件时，通过使用MappedByteBuffer类，可以将其映射到内存中进行编辑，编辑的内容会同步更新到文件中：
//注意一定要是可写的，不然无法进行修改操作
try(RandomAccessFile f = new RandomAccessFile("test.txt", "rw");
    FileChannel channel = f.getChannel()){
    //通过map方法映射文件的某一段内容，创建MappedByteBuffer对象
    //比如这里就是从第四个字节开始，映射10字节内容到内存中
 //注意这里需要使用MapMode.READ_WRITE模式，其他模式无法保存数据到文件
    MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ_WRITE, 4, 10);
    //我们可以直接对在内存中的数据进行编辑，也就是编辑Buffer中的内容
  //注意这里写入也是从pos位置开始的，默认是从0开始，相对于文件就是从第四个字节开始写
  //注意我们只映射了10个字节，也就是写的内容不能超出10字节了
    buffer.put("yyds".getBytes());
    //编辑完成后，通过force方法将数据写回文件的映射区域
    buffer.force();
}
**文件锁FileLock**
可以创建一个跨进程文件锁来防止多个进程之间的文件争抢操作
有关共享锁和独占锁：
```

- 进程对文件加独占锁后，当前进程对文件可读可写，独占此文件，其它进程是不能读该文件进行读写操作的。
- 进程对文件加共享锁后，进程可以对文件进行读操作，但是无法进行写操作，共享锁可以被多个进程添加，但是只要存在共享锁，就不能添加独占锁。

通过Channel获取FileLock
多路复用网络通信
比如以下代码使用了Channel方式实现了网络通信：
//创建一个新的SocketChannel，一会通过通道进行通信
```java
try (SocketChannel channel = SocketChannel.open(new InetSocketAddress("localhost", 8080));
Scanner scanner = new Scanner(System.in)){
System.out.println("已连接到服务端！");
System.out.println("请输入要发送给服务端的内容：");
String text = scanner.nextLine();
```
//直接向通道中写入数据，真舒服
channel.write(ByteBuffer.wrap(text.getBytes()));

```java
        ByteBuffer buffer = ByteBuffer.allocate(128);
        channel.read(buffer);   //直接从通道中读取数据
        buffer.flip();
        System.out.println("收到服务器返回："+new String(buffer.array(), 0, buffer.remaining()));
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
选择器与IO多路复用
NIO为我们提供的网络IO模型：
```

![[_assets/NIO/NIO__09-20-44-2.png]]

服务端不再是一个单纯通过accept()方法来创建连接的机制了，而是根据客户端不同的状态，Selector会不断轮询，只有客户端在对应的状态时，比如真正开始读写操作时，才会创建线程或进行处理（这样就不会一直阻塞等待某个客户端的IO操作了），而不是创建之后需要一直保持连接，即使没有任何的读写操作。这样就不会因为占着茅坑不拉屎导致线程无限制地创建下去了。
有多种状态：

- select：当这些连接出现具体的某个状态时，只是知道已经就绪了，但是不知道详具体是哪一个连接已经就绪，每次调用都进行线性遍历所有连接，时间复杂度为O(n)，并且存在最大连接数限制。
- poll：同上，但是由于底层采用链表，所以没有最大连接数限制。
- epoll：采用事件通知方式，当某个连接就绪，能够直接进行精准通知（这是因为在内核实现中epoll是根据每个fd上面的callback函数实现的，只要就绪会会直接回调callback函数，实现精准通知，但是只有Linux支持这种方式），时间复杂度O(1)，Java在Linux环境下正是采用的这种模式进行实现的。

示例如下：
```python
try (ServerSocketChannel serverChannel = ServerSocketChannel.open();
Selector selector = Selector.open()){ //开启一个新的Selector，这玩意也是要关闭释放资源的
serverChannel.bind(new InetSocketAddress(8080));
```
//要使用选择器进行操作，必须使用非阻塞的方式，这样才不会像阻塞IO那样卡在accept()，而是直接通过，让选择器去进行下一步操作
serverChannel.configureBlocking(false);
//将选择器注册到ServerSocketChannel中，后面是选择需要监听的时间，只有发生对应事件时才会进行选择，多个事件用 | 连接，注意，并不是所有的Channel都支持以下全部四个事件，可能只支持部分
//因为是ServerSocketChannel这里我们就监听accept就可以了，等待客户端连接
```text
//SelectionKey.OP_CONNECT --- 连接就绪事件，表示客户端与服务器的连接已经建立成功
//SelectionKey.OP_ACCEPT --- 接收连接事件，表示服务器监听到了客户连接，服务器可以接收这个连接了
//SelectionKey.OP_READ --- 读 就绪事件，表示通道中已经有了可读的数据，可以执行读操作了
```
//SelectionKey.OP_WRITE --- 写 就绪事件，表示已经可以向通道写数据了（这玩意比较特殊，一般情况下因为都是可以写入的，所以可能会无限循环）
serverChannel.register(selector, SelectionKey.OP_ACCEPT);
while (true) { //无限循环等待新的用户网络操作
//每次选择都可能会选出多个已经就绪的网络操作，没有操作时会暂时阻塞
```cpp
int count = selector.select();
System.out.println("监听到 "+count+" 个事件");
Set<SelectionKey> selectionKeys = selector.selectedKeys();
Iterator<SelectionKey> iterator = selectionKeys.iterator();
while (iterator.hasNext()) {
SelectionKey key = iterator.next();
```
//根据不同的事件类型，执行不同的操作即可
```python
if(key.isAcceptable()) { //如果当前ServerSocketChannel已经做好准备处理Accept
SocketChannel channel = serverChannel.accept();
System.out.println("客户端已连接，IP地址为："+channel.getRemoteAddress());
```
//现在连接就建立好了，接着我们需要将连接也注册选择器，比如我们需要当这个连接有内容可读时就进行处理
channel.configureBlocking(false);
channel.register(selector, SelectionKey.OP_READ);
//这样就在连接建立时完成了注册
```text
} else if(key.isReadable()) { //如果当前连接有可读的数据并且可以写，那么就开始处理
SocketChannel channel = (SocketChannel) key.channel();
ByteBuffer buffer = ByteBuffer.allocate(128);
```
channel.read(buffer);
buffer.flip();
System.out.println("接收到客户端数据："+new String(buffer.array(), 0, buffer.remaining()));

```java
                    //直接向通道中写入数据就行
                    channel.write(ByteBuffer.wrap("已收到！".getBytes()));
                    //别关，说不定用户还要继续通信呢
                }
                //处理完成后，一定记得移出迭代器，不然下次还有
                iterator.remove();
            }
        }
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
```