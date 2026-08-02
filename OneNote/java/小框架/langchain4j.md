---
title: langchain4j
tags: [java, 小框架]
aliases: [langchain4j]
---

# langchain4j

自己引入 starter 依赖
使用

```java
@Service
@Slf4j
public class AiCodeHelper {

    @Autowired
    private ChatModel chatModel;

    public String chat(String message) {
        UserMessage userMessage = UserMessage.from(message);
        ChatResponse chat = chatModel.chat(userMessage);
        AiMessage aiMessage = chat.aiMessage();
        return aiMessage.text();
    }
}
```

`userMessage` 可以很多,可以是文本、图片、视频、音频等,比如:

```java
UserMessage userMessage = UserMessage.from(
        TextContent.from("描述图片"),
        ImageContent.from("https://www.codefather.cn/logo.png")
);
```

## 系统提示词 SystemMessage

需要在用户对话前带上系统消息。

```java
public String chat(String message) {
    SystemMessage systemMessage = SystemMessage.from(SYSTEM_MESSAGE);
    UserMessage userMessage = UserMessage.from(message);
    ChatResponse chat = chatModel.chat(systemMessage, userMessage);
    AiMessage aiMessage = chat.aiMessage();
    return aiMessage.text();
}
```

## AIService

还有一种方式是 `AiService` 来编写,该方式比较简单。
同时引入 langchain4j 本身的包。

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j</artifactId>
    <version>1.12.2</version>
</dependency>
```

然后就可以:

```java
public interface AiCodeHelperService {
    // 支持本地文件读取,resource 也可以
    // 也可以直接写系统提示词
    @SystemMessage(fromResource = "system-prompt.txt")
    String chat(String userMessage);
}
```

```java
@Configuration
public class AiCodeHelperServiceFactory {

    @Resource
    private ChatModel chatModel;

    @Bean
    public AiCodeHelperService aiCodeHelperService() {
        return AiServices.create(AiCodeHelperService.class, chatModel);
    }
}
```

如果想要知道话费多少 token 等信息,返回值改为 `Result<...>` 即可。

我们还可以使用 starter,打上 `@AiService` 注解来自动生成。

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>${langchain4j.version}</version>
</dependency>
```

```java
@AiService
public interface AiCodeHelperService {
    // 支持本地文件读取,resource 也可以
    // 也可以直接写系统提示词
    @SystemMessage(fromResource = "system-prompt.txt")
    String chat(String userMessage);
}
```

该方式牺牲了些灵活性。

## 会话记忆

一种是存储在内存里的:

```java
@Bean
public AiCodeHelperService aiCodeHelperService() {
    // 会话记忆
    MessageWindowChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);
    // 构造 AIService
    AiCodeHelperService service = AiServices.builder(AiCodeHelperService.class)
            .chatModel(chatModel)
            .chatMemory(chatMemory)
            .build();
    return service;
}
```

还有种是自己实现 `ChatMemoryStore` 接口,实现对话持久化。

```java
public interface ChatMemoryStore {
    List<ChatMessage> getMessages(Object memoryId);
    void updateMessages(Object memoryId, List<ChatMessage> messages);
    void deleteMessages(Object memoryId);
}
```

如果有多个用户,可以给对话方法增加 `memoryId` 参数和注解:

```java
@SystemMessage(fromResource = "system-prompt.txt")
String chat(@MemoryId int memoryId, @UserMessage String userMessage);
```

```java
// 然后这样构造 AIService
AiCodeHelperService service = AiServices.builder(AiCodeHelperService.class)
    .chatModel(chatModel)
    .chatMemory(chatMemory)
    .chatMemoryProvider(memoryId -> MessageWindowChatMemory.withMaxMessages(10))
    .build();
```

## 结构化输出

非常简单,`chat` 方法返回值设置一下就行。

```java
@SystemMessage(fromResource = "system-prompt.txt")
Report chatForReport(String userMessage);

// 学习报告
record Report(String name, List<String> suggestionList) {}
```

就能按指定的结构返回。

有时无法生成准确的 JSON,可以使用 JSON Schema 模式,比如:

```java
ResponseFormat responseFormat = ResponseFormat.builder()
        .type(JSON)
        .jsonSchema(JsonSchema.builder()
                .name("Person")
                .rootElement(JsonObjectSchema.builder()
                        .addStringProperty("name")
                        .addIntegerProperty("age")
                        .addNumberProperty("height")
                        .addBooleanProperty("married")
                        .required("name", "age", "height", "married")
                        .build())
                .build())
        .build();
ChatRequest chatRequest = ChatRequest.builder()
        .responseFormat(responseFormat)
        .messages(userMessage)
        .build();
```

## RAG

RAG(Retrieval-Augmented Generation,基于信息检索技术和 AI 内容生成的混合架构,可解决模型时效性与幻觉问题)流程图:

![[_assets/langchain4j/langchain4j__09-25-46-9.png]]

langchain4j 提供了 3 种 RAG 实现方式。

### 极简版 langchain4j-easy-rag

该版本内嵌了 Embedding 模型。

```java
// RAG
// 1. 加载文档
List<Document> documents = FileSystemDocumentLoader.loadDocuments("src/main/resources/docs");
// 2. 使用内置的 EmbeddingModel 转换文本为向量,然后存储到自动注入的内存 embeddingStore 中
EmbeddingStoreIngestor.ingest(documents, embeddingStore);
// 构造 AI Service
AiCodeHelperService aiCodeHelperService = AiServices.builder(AiCodeHelperService.class)
        .chatModel(qwenChatModel)
        .chatMemory(chatMemory)
        // RAG: 从内存 embeddingStore 中检索匹配的文本片段
        .contentRetriever(EmbeddingStoreContentRetriever.from(embeddingStore))
        .build();
```

### 一般 RAG

```java
@Configuration
public class RagConfig {
    @Autowired
    private EmbeddingModel embeddingModel;
    @Autowired
    private EmbeddingStore<TextSegment> embeddingStore;

    @Bean
    public ContentRetriever contentRetriever() {
        // 加载文档
        Document document = ClassPathDocumentLoader.loadDocument("docs.docx", new ApachePoiDocumentParser());
        // 文档切割:按照段落分割,最大 1000 个字符,最多重叠 200 个字符
        DocumentByParagraphSplitter splitter = new DocumentByParagraphSplitter(1000, 200);
        // 自定义文档加载器,文档转为向量保存在数据库中
        EmbeddingStoreIngestor ingestor = EmbeddingStoreIngestor.builder()
                .documentSplitter(splitter)
                // 为了提高文档的质量,为每个切割后的文档碎片 TextSegment 添加文档名称作为元信息
                .textSegmentTransformer(textSegment ->
                        TextSegment.from(textSegment.metadata().getString("file_name") + "\n" + textSegment.text(),
                                textSegment.metadata()))
                // 指定使用的向量模型
                .embeddingModel(embeddingModel)
                // 向量存储,这里用内存存储
                .embeddingStore(embeddingStore)
                .build();
        // 加载文档
        ingestor.ingest(document);
        // 自定义内容加载器
        EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
                .embeddingStore(embeddingStore)
                .embeddingModel(embeddingModel)
                .maxResults(5) // 最多 5 条结果
                .minScore(0.75) // 过滤分数小于 0.75 的结果
                .build();
        return retriever;
    }
}
```

### 进阶版 RAG

![[_assets/langchain4j/langchain4j__09-25-49-11.png]]

## 工具调用 ToolCalling

我们需要自己定义类,里面打相应的注解:

```java
public class InterviewQuestionTool {

    @Tool(name = "interviewQuestionSearch", value = """
            Retrieves relevant interview questions from mianshiya.com based on a keyword.
            Use this tool when the user asks for interview questions about specific technologies,
            programming concepts, or job-related topics. The input should be a clear search term.
            """)
    public String searchInterviewQuestions(@P(value = "the keyword to search") String keyword) {
        List<String> questions = new ArrayList<>();
        // 构建搜索 URL(编码关键词以支持中文)
        String encodedKeyword = URLEncoder.encode(keyword, StandardCharsets.UTF_8);
        String url = "https://www.mianshiya.com/search/all?searchText=" + encodedKeyword;
        // 发送请求并解析页面
        Document doc;
        try {
            doc = Jsoup.connect(url)
                    .userAgent("Mozilla/5.0")
                    .timeout(5000)
                    .get();
        } catch (IOException e) {
            log.error("get web error", e);
            return e.getMessage();
        }
        // 提取面试题
        Elements questionElements = doc.select(".ant-table-cell > a");
        questionElements.forEach(el -> questions.add(el.text().trim()));
        return String.join("\n", questions);
    }
}
```

构造的时候就可以指定 tool:

```java
// 构造 AI Service
AiCodeHelperService aiCodeHelperService = AiServices.builder(AiCodeHelperService.class)
        .chatModel(qwenChatModel)
        .chatMemory(chatMemory) // 会话记忆
        .contentRetriever(contentRetriever) // RAG 检索增强生成
        .tools(new InterviewQuestionTool()) // 工具调用
        .build();
return aiCodeHelperService;
```

## MCP

项目中引入 `langchain4j-mcp`。langchain4j 使用的是 MCP Server。
我们需要这样的:

```java
@Bean
public McpToolProvider mcpToolProvider() {
    // 和 MCP 服务通信
    McpTransport transport = new HttpMcpTransport.Builder()
            .sseUrl("https://open.bigmodel.cn/api/mcp/web_search")
            .logRequests(true) // 开启日志,查看更多信息
            .logResponses(true)
            .build();
    // 创建 MCP 客户端
    McpClient mcpClient = new DefaultMcpClient.Builder()
            .key("yupiMcpClient")
            .transport(transport)
            .build();
    // 从 MCP 客户端获取工具
    McpToolProvider toolProvider = McpToolProvider.builder()
            .mcpClients(mcpClient)
            .build();
    return toolProvider;
}
```

## 拦截器(护轨 Guardrail)

在请求 AI 前和收到 AI 响应后执行一些额外的操作。
下面是一个输入拦截器的例子:

```java
public class SafeInputGuardrail implements InputGuardrail {

    // 敏感词集合
    private static final Set<String> sensitiveWords = Set.of("kill", "evil");

    /**
     * 检测用户输入是否安全
     */
    @Override
    public InputGuardrailResult validate(UserMessage userMessage) {
        // 获取用户输入并转换为小写以确保大小写不敏感
        String inputText = userMessage.singleText().toLowerCase();
        // 使用正则表达式分割输入文本为单词
        String[] words = inputText.split("\\W+");
        // 遍历所有单词,检查是否存在敏感词
        for (String word : words) {
            if (sensitiveWords.contains(word)) {
                return fatal("Sensitive word detected: " + word);
            }
        }
        return success();
    }
}
```

然后我们在 `AiService` 接口打上 `@InputGuardrails` 注解,指定该类即可。

## 可观测性

类似于日志,能够帮我们更好的看到 langchain4j 执行的细节。
在构造大模型时使用 `listeners` 方法绑定一个监听器,里面会传入相关信息。

## AI 服务化

### SSE 流式接口开发

```java
interface Assistant {
    TokenStream chat(String message);
}

StreamingChatModel model = OpenAiStreamingChatModel.builder()
        .apiKey(System.getenv("OPENAI_API_KEY"))
        .modelName(GPT_4_O_MINI)
        .build();

Assistant assistant = AiServices.create(Assistant.class, model);

TokenStream tokenStream = assistant.chat("Tell me a joke");

tokenStream.onPartialResponse((String partialResponse) -> System.out.println(partialResponse))
        .onRetrieved((List<Content> contents) -> System.out.println(contents))
        .onToolExecuted((ToolExecution toolExecution) -> System.out.println(toolExecution))
        .onCompleteResponse((ChatResponse response) -> System.out.println(response))
        .onError((Throwable error) -> error.printStackTrace())
        .start();
```

还有另一种方法,使用 `Flux` 代替 `tokenStream`。
引入 `langchain4j-reactor`,直接让 `chat` 方法返回 `Flux<String>`,构造 `AiService` 时调用 `streamingChatModel`,给前端接口可以:

```java
@RestController
@RequestMapping("/ai")
public class AiController {

    @Resource
    private AiCodeHelperService aiCodeHelperService;

    @GetMapping("/chat")
    public Flux<ServerSentEvent<String>> chat(int memoryId, String message) {
        return aiCodeHelperService.chatStream(memoryId, message)
                .map(chunk -> ServerSentEvent.<String>builder()
                        .data(chunk)
                        .build());
    }
}
```