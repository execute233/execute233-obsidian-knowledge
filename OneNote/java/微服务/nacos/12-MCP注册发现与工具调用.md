---
title: MCP 注册发现与工具调用
tags: [java, nacos, MCP, AI]
aliases: [Nacos MCP实操, Java MCP注册发现]
---

# MCP 注册发现与工具调用

本课把一个 Java MCP 工具注册到 Nacos，再由 Java 客户端发现地址并调用，完成不依赖模型 API 的验证闭环。

> [!abstract]
> 本课重点：官方 Java MCP SDK；本机 Streamable HTTP；控制台注册；Nacos 发现与工具调用。

## 实验选择

| 项目 | 本课选择 |
| --- | --- |
| 应用 | 第 4 课的 Boot 4 商品工程 |
| Nacos | <code>3.2.4</code>，默认 <code>all</code> 功能模式 |
| Nacos Client | 由 Alibaba BOM 管理的 <code>3.1.1</code> |
| MCP Java SDK | 官方 <code>2.0.1</code>，Java 17+，默认 Jackson 3 |
| MCP 传输 | 无状态 Streamable HTTP，<code>/mcp</code> |
| 注册方式 | Console 手工登记，便于观察模型与端点 |

这里使用官方 MCP Java SDK 2.0.1 的 Servlet 传输，配合 Boot 4 与 Nacos 3 的资源登记、发现接口。自动注册可在后续核对 Spring AI Alibaba 与当前工程的依赖组合后接入。

## 加入 MCP 依赖

商品工程 POM 的 <code>dependencies</code> 中加入：

```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp</artifactId>
    <version>2.0.1</version>
</dependency>
```

## Java MCP Server

创建 <code>src/main/java/com/example/product/McpConfig.java</code>，由商品应用扫描：

```java
package com.example.product;

import java.util.List;
import java.util.Map;
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.McpStatelessServerFeatures;
import io.modelcontextprotocol.server.McpStatelessSyncServer;
import io.modelcontextprotocol.server.transport.HttpServletStatelessServerTransport;
import io.modelcontextprotocol.spec.McpSchema;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpConfig {
    @Bean
    HttpServletStatelessServerTransport mcpTransport() {
        return HttpServletStatelessServerTransport.builder()
                .messageEndpoint("/mcp").build();
    }

    @Bean
    ServletRegistrationBean<HttpServletStatelessServerTransport> mcpServlet(
            HttpServletStatelessServerTransport transport) {
        var registration = new ServletRegistrationBean<>(transport, "/mcp");
        registration.setLoadOnStartup(1);
        return registration;
    }

    @Bean(destroyMethod = "closeGracefully")
    McpStatelessSyncServer mcpServer(HttpServletStatelessServerTransport transport) {
        Map<String, Object> schema = Map.of(
                "type", "object",
                "properties", Map.of("id", Map.of("type", "integer", "minimum", 1)),
                "required", List.of("id"),
                "additionalProperties", false);
        var tool = McpSchema.Tool.builder("get_product", schema)
                .description("根据商品ID读取演示商品信息").build();
        var specification = McpStatelessServerFeatures.SyncToolSpecification.builder()
                .tool(tool)
                .callHandler((context, request) -> {
                    Number id = (Number) request.arguments().get("id");
                    return McpSchema.CallToolResult.builder()
                            .addTextContent("商品ID=" + id.longValue() + "，名称=演示商品")
                            .isError(false).build();
                }).build();
        return McpServer.sync(transport)
                .serverInfo("product-mcp", "1.0.0")
                .capabilities(McpSchema.ServerCapabilities.builder().tools(true).build())
                .tools(specification).build();
    }
}
```

此处工具只返回演示数据，不写数据库；真实业务在 handler 中调用商品查询服务。参数结构由 schema 描述，SDK 负责相应的协议与输入校验。

重新构建并启动商品应用。浏览器直接 GET <code>/mcp</code> 得到 405 可以是无状态传输的正常行为；MCP Client 会使用协议请求验证功能。

## 在 Nacos 登记

打开 Console 的 AI 管理中心 → MCP 管理，新增远程 MCP Server：

| 项目 | 值 |
| --- | --- |
| Namespace | <code>public</code> |
| 名称 | <code>product-mcp</code> |
| 版本 | <code>1.0.0</code> |
| MCP 协议 | Streamable HTTP / <code>streamable</code> |
| Endpoint 协议 | <code>http</code> |
| Endpoint 地址 / 端口 | <code>&lt;MCP_HOST&gt;</code> / <code>9001</code> |
| Endpoint 路径 | <code>/mcp</code> |
| 工具 | <code>get_product</code>，结构与上面的 schema 一致 |

按页面要求登记地址与工具定义后发布。<code>service-product</code> 的普通 Naming 注册不会自动生成这份 MCP 资源。

<code>&lt;MCP_HOST&gt;</code> 由读者填写为 Console 与 MCP Client 都能访问的地址。多机部署不能用调用方自己的回环地址代替远程服务地址；Console 的回环地址指向 Console 自己。

如果使用页面的“从 MCP 获取工具”能力，3.2.4 默认限制本机 / 内网目标。在 Console 所用配置中明确允许本次目标，并重启：

```properties
nacos.console.ai.mcp.import.allowed-private-addresses=<MCP_TARGET_IP_OR_CIDR>
```

允许列表填写目标 IP 或 CIDR，不能填写完整 URL；只放行本次需要的目标。也可手工填写工具定义完成登记。工具定义保存在 Nacos，不代表普通直连 MCP Server 会自动执行 Nacos 上的所有工具开关；这种动态治理需要相应 Wrapper、集成或 Router。

## Java 发现并调用

创建 <code>src/main/java/com/example/mcp/McpDiscoveryDemo.java</code>。它是独立 main，不需要被商品应用组件扫描；在 IDE 中运行，环境变量配置与第 4 课相同。

```java
package com.example.mcp;

import java.util.Map;
import java.util.Properties;
import com.alibaba.nacos.api.PropertyKeyConst;
import com.alibaba.nacos.api.ai.AiFactory;
import io.modelcontextprotocol.client.McpClient;
import io.modelcontextprotocol.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema;

public class McpDiscoveryDemo {
    public static void main(String[] args) throws Exception {
        Properties p = new Properties();
        p.setProperty(PropertyKeyConst.SERVER_ADDR, System.getenv("NACOS_SERVER_ADDR"));
        p.setProperty(PropertyKeyConst.NAMESPACE, "public");
        p.setProperty(PropertyKeyConst.USERNAME, System.getenv("NACOS_USERNAME"));
        p.setProperty(PropertyKeyConst.PASSWORD, System.getenv("NACOS_PASSWORD"));
        var ai = AiFactory.createAiService(p);
        try {
            var detail = ai.getMcpServer("product-mcp", "1.0.0");
            var endpoint = detail.getBackendEndpoints().stream().findFirst()
                    .orElseThrow(() -> new IllegalStateException("没有可用MCP端点"));
            String baseUrl = "%s://%s:%d".formatted(
                    endpoint.getProtocol(), endpoint.getAddress(), endpoint.getPort());
            var transport = HttpClientStreamableHttpTransport.builder(baseUrl)
                    .endpoint(endpoint.getPath()).build();
            try (var client = McpClient.sync(transport).build()) {
                client.initialize();
                System.out.println(client.listTools().tools());
                var result = client.callTool(McpSchema.CallToolRequest.builder("get_product")
                        .arguments(Map.of("id", 1)).build());
                System.out.println(result.content());
            }
        } finally {
            ai.shutdown();
        }
    }
}
```

预期能发现 <code>get_product</code> 并得到“商品ID=1，名称=演示商品”。这验证了 **Nacos 资源发现 → MCP 协议通信 → 工具执行**，没有调用模型。

加入多个 main 后，在 Boot Maven 插件中指定商品应用的入口，避免重新打包时无法选择启动类：

```xml
<configuration>
    <mainClass>com.example.product.ProductApplication</mainClass>
</configuration>
```

## 三层鉴权

| 层次 | 凭据与作用 |
| --- | --- |
| Client → Nacos | Nacos 账号、资源读取权限、可见性 |
| Console → MCP 导入目标 | 出站允许列表；只约束相应导入行为 |
| MCP Client → MCP Server | MCP Server 自己的身份校验，与 Nacos Token 分开 |

本地演示工具没有单独接入 MCP 业务鉴权；如果扩展到共享环境，按 MCP Server 的协议与部署方式添加认证、授权和来源约束。不要把 Nacos 管理员 Token 发给工具服务。

详见 [[11-Nacos3AI管理中心|AI 管理中心]]、[[13-Prompt版本发布与读取实操|Prompt 实操]]、[[官方资料索引|官方 MCP 与 Nacos 资料]]。
