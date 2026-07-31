导入只需导入netty-all与io.netty  
**ByteBuf**  
Netty并没有使用NIO中提供的ByteBuffer来进行数据装载，而是自行定义了一个ByteBuf类。  
与ByteBuffer不同之处：

- 写操作完成后无需进行flip()翻转。
- 具有比ByteBuffer更快的响应速度。
- 动态扩容。

内部结构：  
public abstract class AbstractByteBuf extends ByteBuf {  
...  
int readerIndex; //index被分为了读和写，是两个指针在同时工作  
int writerIndex;  
private int markedReaderIndex; //mark操作也分两种  
private int markedWriterIndex;  
private int maxCapacity; //最大容量，没错，这玩意能动态扩容  
可以看到，读操作和写操作分别由两个指针在进行维护，每写入一次，writerIndex向后移动一位，每读取一次，也是readerIndex向后移动一位，当然readerIndex不能大于writerIndex，这样就不会像NIO中的ByteBuffer那样还需要进行翻转了。

![[.attachments/Netty/Netty__09-24-55-0.png]]

可以在Unpooled类的静态方法获取实例  
缓冲区的三种实现模式：堆缓冲区模式、直接缓冲区模式、复合缓冲区模式：  
前两个都知道，这些缓冲区可以从Unpooled的buffer, directBuffer, compositeBuffer等方法获得  
复合模式可以任意地拼凑组合其他缓冲区，比如我们可以：

![[.attachments/Netty/Netty__09-24-56-1.png]]

Unpooled使用ByteBufAllocator来获取Buffer，它有两个具体实现类：  
UnpooledByteBufAllocator和PooledByteBufAllocator，一个是非池化缓冲区生成器，还有一个是池化缓冲区生成器  
**零拷贝**  
零拷贝是一种I/O操作优化技术，可以快速高效地将数据从文件系统移动到网络接口，而不需要将其从内核空间复制到用户空间，有三种实现方法：

- 使用虚拟内存
- 使用mmap/write内存映射
- 使用sendfile方式

现在的操作系统基本都是支持虚拟内存的，我们可以让内核空间和用户空间的虚拟地址指向同一个物理地址，这样就相当于是直接共用了这一块区域，也就谈不上拷贝操作了：

![[.attachments/Netty/Netty__09-24-58-2.png]]

实际上这种方式就是将内核空间中的缓存直接映射到用户空间缓存，比如我们之前在学习NIO中使用的MappedByteBuffer，就是直接作为映射存在，当我们需要将数据发送到Socket缓冲区时，直接在内核空间中进行操作就行了：

![[.attachments/Netty/Netty__09-25-00-3.png]]

在Linux2.1开始，引入了sendfile方式来简化操作，我们可以直接告诉内核要把哪个文件数据拷贝拷贝到Socket上，直接在内核空间中一步到位：

![[.attachments/Netty/Netty__09-25-02-4.png]]

比如我们之前在NIO中使用的transferTo()方法，就是利用了这种机制来实现零拷贝的。  
**Netty****工作模型**  
Netty以主从Reactor多线程模型为基础，构建出了一套高效的工作模型

![[.attachments/Netty/Netty__09-25-07-5.png]]

- Netty 抽象出两组线程池BossGroup和WorkerGroup，BossGroup专门负责接受客户端的连接, WorkerGroup专门负读写，就像我们前面说的主从Reactor一样。
- 无论是BossGroup还是WorkerGroup，都是使用EventLoop来进行事件监听的，整个Netty也是使用事件驱动来运作的，比如当客户端已经准备好读写、连接建立时，都会进行事件通知，说白了就像我们之前写NIO多路复用那样，只不过这里换成EventLoop了而已，它已经帮助我们封装好了一些常用操作，而且我们可以自己添加一些额外的任务，如果有多个EventLoop，会存放在EventLoopGroup中，EventLoopGroup就是BossGroup和WorkerGroup的具体实现。
- 在BossGroup之后，会正常将SocketChannel绑定到WorkerGroup中的其中一个EventLoop上，进行后续的读写操作监听。

下面演示下：  
//这里我们使用NioEventLoopGroup实现类即可，创建BossGroup和WorkerGroup  
//当然还有EpollEventLoopGroup，但是仅支持Linux，这是Netty基于Linux底层Epoll单独编写的一套本地实现，没有使用NIO那套  
EventLoopGroup bossGroup = new NioEventLoopGroup(), workerGroup = new NioEventLoopGroup();  
//创建服务端启动引导类  
ServerBootstrap bootstrap = new ServerBootstrap();  
//可链式，就很棒  
bootstrap  
.group(bossGroup, workerGroup) //指定事件循环组  
.channel(NioServerSocketChannel.class) //指定为NIO的ServerSocketChannel  
.childHandler(new ChannelInitializer\<SocketChannel\>() { //注意，这里的SocketChannel不是我们NIO里面的，是Netty的  
@Override  
protected void initChannel(SocketChannel channel) {  
//获取流水线，当我们需要处理客户端的数据时，实际上是像流水线一样在处理，这个流水线上可以有很多Handler  
channel.pipeline().addLast(new ChannelInboundHandlerAdapter(){ //添加一个Handler，这里使用ChannelInboundHandlerAdapter  
@Override  
public void channelRead(ChannelHandlerContext ctx, Object msg) { //ctx是上下文，msg是收到的消息，默认以ByteBuf形式（也可以是其他形式，后面再说）  
ByteBuf buf = (ByteBuf) msg; //类型转换一下  
System._out_.println(Thread._currentThread_().getName()+" \>\> data："+buf.toString(StandardCharsets._UTF_8_));  
//通过上下文可以直接发送数据回去，注意要writeAndFlush才能让客户端立即收到  
ctx.writeAndFlush(Unpooled._wrappedBuffer_("已收到！".getBytes()));  
}  
});  
}  
});  
//最后绑定端口，启动  
bootstrap.bind(8080);  
**Channel****详解**  
Netty中也有自己对应的Channel类型  
public interface Channel extends AttributeMap, ChannelOutboundInvoker, Comparable\<Channel\> {  
ChannelId id(); //通道ID  
EventLoop eventLoop(); //获取此通道所属的EventLoop，因为一个Channel在它的生命周期内只能注册到一个EventLoop中  
Channel parent(); //Channel是具有层级关系的，这里是返回父Channel  
ChannelConfig config();  
boolean isOpen(); //通道当前的相关状态  
boolean isRegistered();  
boolean isActive();  
ChannelMetadata metadata(); //通道相关信息  
SocketAddress localAddress();  
SocketAddress remoteAddress();  
ChannelFuture closeFuture(); //关闭通道，但是会用到ChannelFuture，后面说  
boolean isWritable();  
long bytesBeforeUnwritable();  
long bytesBeforeWritable();  
Unsafe unsafe();  
ChannelPipeline pipeline(); //流水线，之后也会说  
ByteBufAllocator alloc(); //可以直接从Channel拿到ByteBufAllocator的实例，来分配ByteBuf  
Channel read();  
Channel flush(); //刷新，基操  
}  
Netty中的Channel相比NIO功能就多得多了。Netty中的Channel主要特点如下：  
所有的IO操作都是异步的，并不是在当前线程同步运行，方法调用之后就直接返回了，那怎么获取操作的结果呢？还记得我们在前面JUC篇教程中学习的Future吗，没错，这里的ChannelFuture也是干这事的。  
我们可以将需要处理的事情放在ChannelHandler中，ChannelHandler充当了所有入站和出站数据的应用程序逻辑的容器，实际上就是我们之前Reactor模式中的Handler，全靠它来处理读写操作  
先从顶层接口开始看起：  
public interface ChannelHandler {  
//当ChannelHandler被添加到流水线中时调用  
void handlerAdded(ChannelHandlerContext var1) throws Exception;  
//当ChannelHandler从流水线中移除时调用  
void handlerRemoved(ChannelHandlerContext var1) throws Exception;  
}  
顶层接口的定义比较简单，就只有一些流水线相关的回调方法，我们接着来看下一级：  
//ChannelInboundHandler用于处理入站相关事件  
public interface ChannelInboundHandler extends ChannelHandler {  
//当Channel已经注册到自己的EventLoop上时调用，前面我们说了，一个Channel只会注册到一个EventLoop上，注册到EventLoop后，这样才会在发生对应事件时被通知。  
void channelRegistered(ChannelHandlerContext var1) throws Exception;  
//从EventLoop上取消注册时  
void channelUnregistered(ChannelHandlerContext var1) throws Exception;  
//当Channel已经处于活跃状态时被调用，此时Channel已经连接/绑定，并且已经就绪  
void channelActive(ChannelHandlerContext var1) throws Exception;  
//跟上面相反，不再活跃了，并且不在连接它的远程节点  
void channelInactive(ChannelHandlerContext var1) throws Exception;  
//当从Channel读取数据时被调用，可以看到数据被自动包装成了一个Object（默认是ByteBuf）  
void channelRead(ChannelHandlerContext var1, Object var2) throws Exception;  
//上一个读取操作完成后调用  
void channelReadComplete(ChannelHandlerContext var1) throws Exception;  
//暂时不介绍  
void userEventTriggered(ChannelHandlerContext var1, Object var2) throws Exception;  
//当Channel的可写状态发生改变时被调用  
void channelWritabilityChanged(ChannelHandlerContext var1) throws Exception;  
//出现异常时被调用  
void exceptionCaught(ChannelHandlerContext var1, Throwable var2) throws Exception;  
}  
与ChannelInboundHandler对应的还有ChannelOutboundHandler用于处理出站相关的操作，这里就不进行演示了。  
我们接着来看看ChannelPipeline，每一个Channel都对应一个ChannelPipeline（在Channel初始化时就被创建了）

![[.attachments/Netty/Netty__09-25-09-6.png]]

```
它就像是一条流水线一样，整条流水线上可能会有很多个Handler（包括入站和出站），整条流水线上的两端还有两个默认的处理器（用于一些预置操作和后续操作，比如释放资源等），我们只需要关心如何安排这些自定义的Handler即可  
但要注意，出站操作在流水线上是反着来的，整个流水线操作大概流程如下:
```

![[.attachments/Netty/Netty__09-25-11-7.png]]

**EventLoop****和任务调度**