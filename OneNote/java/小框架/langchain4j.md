# langchain4j

自己引入starter依赖
使用

![[_assets/langchain4j/langchain4j__09-25-24-0.png]]

userMessage可以很多，可以是文本，图片，视频，音频等，比如

![[_assets/langchain4j/langchain4j__09-25-27-1.png]]

系统提示词SystemMessage
需要在用户对话前带上系统消息

![[_assets/langchain4j/langchain4j__09-25-32-2.png]]

AIService
还有一种方式是AiService来编写，该方式比较简单
同时引入langchain4j本身的包
```xml
<dependency>
<groupId>dev.langchain4j</groupId>
<artifactId>langchain4j</artifactId>
<version>1.12.2</version>
</dependency>
```
然后就可以

![[_assets/langchain4j/langchain4j__09-25-33-3.png]] ![[_assets/langchain4j/langchain4j__09-25-34-4.png]]

如果想要知道话费多少token等信息，返回值改为Result<…>即可
我们还可以使用starter，打上@AiService注解来自动生成
```xml
<dependency>
<groupId>dev.langchain4j</groupId>
<artifactId>langchain4j-spring-boot-starter</artifactId>
<version>${langchain4j.version}</version>
</dependency>
```

![[_assets/langchain4j/langchain4j__09-25-36-5.png]]

该方式牺牲了些灵活性
会话记忆
一种是存储在内存里的

![[_assets/langchain4j/langchain4j__09-25-38-6.png]]

还有种是自己实现ChatMemoryStore接口，实现对话持久化
```csharp
public interface ChatMemoryStore {
List<ChatMessage> getMessages(Object memoryId);
void updateMessages(Object memoryId, List<ChatMessage> messages);
void deleteMessages(Object memoryId);
```
}
如果有多个用户，可以给对话方法增加memoryId参数和注解
```python
@SystemMessage(fromResource = "system-prompt.txt")
String chat(@MemoryId int memoryId,@UserMessage String userMessage);
```

// 然后这样构造AIService
AiCodeHelperService service = AiServices._builder_(AiCodeHelperService.class)
.chatModel(chatModel)
.chatMemory(chatMemory)
.chatMemoryProvider(memoryId -> MessageWindowChatMemory._withMaxMessages_(10))
.build();
结构化输出
非常简单，chat方法返回值设置一下就行

![[_assets/langchain4j/langchain4j__09-25-39-7.png]]

就能按指定的结构返回
有时无法生成准确的JSON，可以使用JSON Schema模式，比如

![[_assets/langchain4j/langchain4j__09-25-41-8.png]]

RAG（基于信息检索技术和AI内容生成的混合架构，可解决模型时效性与幻觉问题）

![[_assets/langchain4j/langchain4j__09-25-46-9.png]]

langchain4j提供了3中RAG实现方式
极简版langchain4j-easy-rag
该版本内嵌了Embedding模型

![[_assets/langchain4j/langchain4j__09-25-48-10.png]]

一般RAG
// 加载RAG
```python
@Configuration
public class RagConfig {
@Autowired
private EmbeddingModel embeddingModel;
@Autowired
private EmbeddingStore<TextSegment> embeddingStore;
@Bean
public ContentRetriever contentRetriever() {
```
// 加载文档
Document document = ClassPathDocumentLoader._loadDocument_("docs.docx", new ApachePoiDocumentParser());
// 文档切割：按照段落分割，最大1000个字符，最多重叠200个字符
DocumentByParagraphSplitter splitter = new DocumentByParagraphSplitter(1000, 200);
// 自定义文档加载器，文档转为向量保存在数据库中
EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor._builder_()
.documentSplitter(splitter)
// 为了提高文档的质量，为每个切割后的文档碎片 TextSegment 添加文档名称作为元信息
.textSegmentTransformer(textSegment ->
```text
TextSegment._from_(textSegment.metadata().getString("file_name") + "\n" + textSegment.text(),
textSegment.metadata()))
```
// 指定使用的向量模型
.embeddingModel(embeddingModel)
// 向量存储，这里用内存存储
.embeddingStore(embeddingStore)
.build();
// 加载文档
ingestor.ingest(document);
// 自定义内容加载器
EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever._builder_()
.embeddingStore(embeddingStore)
.embeddingModel(embeddingModel)
```text
.maxResults(5) // 最多5条结果
.minScore(0.75) // 过滤分数小于0.75的结果
```
.build();
return retriever;
}
}
进阶版RAG

![[_assets/langchain4j/langchain4j__09-25-49-11.png]]

工具调用ToolCalling
我们需要自己定义类，里面打相应的注解

![[_assets/langchain4j/langchain4j__09-25-51-12.png]]

构造的时候就可以指定tool

![[_assets/langchain4j/langchain4j__09-25-52-13.png]]

MCP
项目中引入langchain4j-mcp
langchain4j使用的是MCP Server
我们需要这样的

![[_assets/langchain4j/langchain4j__09-25-53-14.png]]

拦截器(护轨 Guardrail)
在请求AI前和收到AI响应后执行一些额外的操作
下面是一个输入拦截器的例子

![[_assets/langchain4j/langchain4j__09-25-58-15.png]]

然后我们在AiService接口打上@InputGuardrails注解，指定该类即可
可观测性
类似于日志，能够帮我们更好的看到langchain4j执行的细节
在构造大模型时使用listeners方法绑定一个监听器，里面会传入相关信息
AI服务化
SSE流式接口开发

![[_assets/langchain4j/langchain4j__09-26-03-16.png]]

还有另一种方法，使用Flux代替tokenStream
引入langchain4j-reactor
直接让chat方法返回Flex<String>
构造AiService时调用streamingChatModel
给前端接口可以

![[_assets/langchain4j/langchain4j__09-26-06-17.png]]