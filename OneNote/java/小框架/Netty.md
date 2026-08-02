---
title: Netty
tags: [java, 小框架]
aliases: [Netty]
---

# Netty

导入只需导入 `netty-all` 与 `io.netty`。

### ByteBuf

Netty 并没有使用 NIO 中提供的 ByteBuffer 来进行数据装载,而是自行定义了一个 ByteBuf 类。
与 ByteBuffer 不同之处:

- 写操作完成后无需进行 `flip()` 翻转。
- 具有比 ByteBuffer 更快的响应速度。
- 动态扩容。

内部结构:

```java
public abstract class AbstractByteBuf extends ByteBuf {
    // ...
    int readerIndex;       // index 被分为了读和写,是两个指针在同时工作
    int writerIndex;
    private int markedReaderIndex;   // mark 操作也分两种
    private int markedWriterIndex;
    private int maxCapacity;         // 最大容量,没错,这玩意能动态扩容
}
```

可以看到,读操作和写操作分别由两个指针在进行维护,每写入一次,writerIndex 向后移动一位,每读取一次,也是 readerIndex 向后移动一位,当然 readerIndex 不能大于 writerIndex,这样就不会像 NIO 中的 ByteBuffer 那样还需要进行翻转了。

![[_assets/Netty/Netty__09-24-55-0.png]]

可以在 `Unpooled` 类的静态方法获取实例。
缓冲区的三种实现模式:堆缓冲区模式、直接缓冲区模式、复合缓冲区模式:
前两个都知道,这些缓冲区可以从 `Unpooled` 的 `buffer`、`directBuffer`、`compositeBuffer` 等方法获得。
复合模式可以任意地拼凑组合其他缓冲区,比如我们可以:

![[_assets/Netty/Netty__09-24-56-1.png]]

`Unpooled` 使用 `ByteBufAllocator` 来获取 Buffer,它有两个具体实现类:
`UnpooledByteBufAllocator` 和 `PooledByteBufAllocator`,一个是非池化缓冲区生成器,还有一个是池化缓冲区生成器。

### 零拷贝

零拷贝是一种 I/O 操作优化技术,可以快速高效地将数据从文件系统移动到网络接口,而不需要将其从内核空间复制到用户空间,有三种实现方法:

- 使用虚拟内存
- 使用 mmap/write 内存映射
- 使用 sendfile 方式

现在的操作系统基本都是支持虚拟内存的,我们可以让内核空间和用户空间的虚拟地址指向同一个物理地址,这样就相当于是直接共用了这一块区域,也就谈不上拷贝操作了:

![[_assets/Netty/Netty__09-24-58-2.png]]

实际上这种方式就是将内核空间中的缓存直接映射到用户空间缓存,比如我们之前在学习 NIO 中使用的 `MappedByteBuffer`,就是直接作为映射存在,当我们需要将数据发送到 Socket 缓冲区时,直接在内核空间中进行操作就行了:

![[_assets/Netty/Netty__09-25-00-3.png]]

在 Linux 2.1 开始,引入了 sendfile 方式来简化操作,我们可以直接告诉内核要把哪个文件数据拷贝到 Socket 上,直接在内核空间中一步到位:

![[_assets/Netty/Netty__09-25-02-4.png]]

比如我们之前在 NIO 中使用的 `transferTo()` 方法,就是利用了这种机制来实现零拷贝的。

### Netty 工作模型

Netty 以主从 Reactor 多线程模型为基础,构建出了一套高效的工作模型:

![[_assets/Netty/Netty__09-25-07-5.png]]

- Netty 抽象出两组线程池 BossGroup 和 WorkerGroup,BossGroup 专门负责接受客户端的连接,WorkerGroup 专门负责读写,就像我们前面说的主从 Reactor 一样。
- 无论是 BossGroup 还是 WorkerGroup,都是使用 EventLoop 来进行事件监听的,整个 Netty 也是使用事件驱动来运作的,比如当客户端已经准备好读写、连接建立时,都会进行事件通知,说白了就像我们之前写 NIO 多路复用那样,只不过这里换成 EventLoop 了而已,它已经帮助我们封装好了一些常用操作,而且我们可以自己添加一些额外的任务,如果有多个 EventLoop,会存放在 EventLoopGroup 中,EventLoopGroup 就是 BossGroup 和 WorkerGroup 的具体实现。
- 在 BossGroup 之后,会正常将 SocketChannel 绑定到 WorkerGroup 中的其中一个 EventLoop 上,进行后续的读写操作监听。

下面演示下:

```java
// 这里我们使用 NioEventLoopGroup 实现类即可,创建 BossGroup 和 WorkerGroup
// 当然还有 EpollEventLoopGroup,但是仅支持 Linux,这是 Netty 基于 Linux 底层 Epoll 单独编写的一套本地实现,没有使用 NIO 那套
EventLoopGroup bossGroup = new NioEventLoopGroup(), workerGroup = new NioEventLoopGroup();

// 创建服务端启动引导类
ServerBootstrap bootstrap = new ServerBootstrap();

// 可链式,就很棒
bootstrap
    .group(bossGroup, workerGroup)          // 指定事件循环组
    .channel(NioServerSocketChannel.class)  // 指定为 NIO 的 ServerSocketChannel
    .childHandler(new ChannelInitializer<SocketChannel>() {  // 注意,这里的 SocketChannel 不是我们 NIO 里面的,是 Netty 的
        @Override
        protected void initChannel(SocketChannel channel) {
            // 获取流水线,当我们需要处理客户端的数据时,实际上是像流水线一样在处理,这个流水线上可以有很多 Handler
            channel.pipeline().addLast(new ChannelInboundHandlerAdapter() {
                // 添加一个 Handler,这里使用 ChannelInboundHandlerAdapter
                @Override
                public void channelRead(ChannelHandlerContext ctx, Object msg) {
                    // ctx 是上下文,msg 是收到的消息,默认以 ByteBuf 形式(也可以是其他形式,后面再说)
                    ByteBuf buf = (ByteBuf) msg;    // 类型转换一下
                    System.out.println(Thread.currentThread().getName()
                        + " >> data:" + buf.toString(StandardCharsets.UTF_8));

                    // 通过上下文可以直接发送数据回去,注意要 writeAndFlush 才能让客户端立即收到
                    ctx.writeAndFlush(Unpooled.wrappedBuffer("已收到!".getBytes()));
                }
            });
        }
    });

// 最后绑定端口,启动
bootstrap.bind(8080);
```

### Channel 详解

Netty 中也有自己对应的 Channel 类型:

```java
public interface Channel extends AttributeMap, ChannelOutboundInvoker, Comparable<Channel> {
    ChannelId id();                // 通道 ID
    EventLoop eventLoop();        // 获取此通道所属的 EventLoop,因为一个 Channel 在它的生命周期内只能注册到一个 EventLoop 中
    Channel parent();             // Channel 是具有层级关系的,这里是返回父 Channel
    ChannelConfig config();
    boolean isOpen();             // 通道当前的相关状态
    boolean isRegistered();
    boolean isActive();
    ChannelMetadata metadata();   // 通道相关信息
    SocketAddress localAddress();
    SocketAddress remoteAddress();
    ChannelFuture closeFuture();  // 关闭通道,但是会用到 ChannelFuture,后面说
    boolean isWritable();
    long bytesBeforeUnwritable();
    long bytesBeforeWritable();
    Unsafe unsafe();
    ChannelPipeline pipeline();   // 流水线,之后也会说
    ByteBufAllocator alloc();     // 可以直接从 Channel 拿到 ByteBufAllocator 的实例,来分配 ByteBuf
    Channel read();
    Channel flush();              // 刷新,基操
}
```

Netty 中的 Channel 相比 NIO 功能就多得多了。Netty 中的 Channel 主要特点如下:

- 所有的 I/O 操作都是异步的,并不是在当前线程同步运行,方法调用之后就直接返回了,那怎么获取操作的结果呢?还记得我们在前面 JUC 篇教程中学习的 Future 吗,没错,这里的 `ChannelFuture` 也是干这事的。
- 我们可以将需要处理的事情放在 `ChannelHandler` 中,`ChannelHandler` 充当了所有入站和出站数据的应用程序逻辑的容器,实际上就是我们之前 Reactor 模式中的 Handler,全靠它来处理读写操作。

先从顶层接口开始看起:

```java
public interface ChannelHandler {
    // 当 ChannelHandler 被添加到流水线中时调用
    void handlerAdded(ChannelHandlerContext ctx) throws Exception;
    // 当 ChannelHandler 从流水线中移除时调用
    void handlerRemoved(ChannelHandlerContext ctx) throws Exception;
}
```

顶层接口的定义比较简单,就只有一些流水线相关的回调方法,我们接着来看下一级:

```java
// ChannelInboundHandler 用于处理入站相关事件
public interface ChannelInboundHandler extends ChannelHandler {
    // 当 Channel 已经注册到自己的 EventLoop 上时调用,前面我们说了,一个 Channel 只会注册到一个 EventLoop 上,注册到 EventLoop 后,这样才会在发生对应事件时被通知。
    void channelRegistered(ChannelHandlerContext ctx) throws Exception;
    // 从 EventLoop 上取消注册时
    void channelUnregistered(ChannelHandlerContext ctx) throws Exception;
    // 当 Channel 已经处于活跃状态时被调用,此时 Channel 已经连接/绑定,并且已经就绪
    void channelActive(ChannelHandlerContext ctx) throws Exception;
    // 跟上面相反,不再活跃了,并且不在连接它的远程节点
    void channelInactive(ChannelHandlerContext ctx) throws Exception;
    // 当从 Channel 读取数据时被调用,可以看到数据被自动包装成了一个 Object(默认是 ByteBuf)
    void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception;
    // 上一个读取操作完成后调用
    void channelReadComplete(ChannelHandlerContext ctx) throws Exception;
    // 暂时不介绍
    void userEventTriggered(ChannelHandlerContext ctx, Object evt) throws Exception;
    // 当 Channel 的可写状态发生改变时被调用
    void channelWritabilityChanged(ChannelHandlerContext ctx) throws Exception;
    // 出现异常时被调用
    void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception;
}
```

与 `ChannelInboundHandler` 对应的还有 `ChannelOutboundHandler` 用于处理出站相关的操作,这里就不进行演示了。

我们接着来看看 `ChannelPipeline`,每一个 Channel 都对应一个 `ChannelPipeline`(在 Channel 初始化时就被创建了):

![[_assets/Netty/Netty__09-25-09-6.png]]

它就像是一条流水线一样,整条流水线上可能会有很多个 Handler(包括入站和出站),整条流水线上的两端还有两个默认的处理器(用于一些预置操作和后续操作,比如释放资源等),我们只需要关心如何安排这些自定义的 Handler 即可。但要注意,出站操作在流水线上是反着来的,整个流水线操作大概流程如下:

![[_assets/Netty/Netty__09-25-11-7.png]]

## EventLoop 和任务调度
