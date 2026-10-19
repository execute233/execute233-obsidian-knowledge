---
title: Prompt 版本发布与读取实操
tags: [java, nacos, Prompt, AI]
aliases: [Nacos Prompt实操, Nacos提示词管理]
---

# Prompt 版本发布与读取实操

Nacos Prompt 管理把提示词模板变成有版本、标签和发布状态的资源，应用查询后再填充变量并调用模型。

## 创建第一版

在 Nacos 3.2.4 Console 的 AI 管理中心 → Prompt 管理中，选择 <code>public</code>，创建资源：

| 项目 | 值 |
| --- | --- |
| Prompt Key | <code>order-summary</code> |
| 版本 | <code>1.0.0</code> |
| 变量 | <code>orderText</code> |
| 用途 | 生成简短订单摘要 |

模板内容：

```text
请用中文概括下面的订单，最多两句话。
订单内容：{{orderText}}
```

本课约定 <code>{{orderText}}</code> 为**应用侧的替换语法**，并在页面登记同名变量。Nacos 保存模板和变量信息，不自动替所有语言应用渲染模板。

创建草稿后提交并发布，上线并确认可读，再按页面能力把 <code>latest</code> 标签指向 <code>1.0.0</code>。启用发布 Pipeline 的环境要先完成相应审核；不要为学习步骤直接强制发布绕过团队流程。

## 按版本查询

先使用 [[07-JavaSDK与v3OpenAPI|API 课]] 的登录方法得到 <code>nacosApi</code> 与访问 Token。账号需对目标 Prompt 有读取权限和可见性。

```bash
curl -sS "$nacosApi/v3/client/ai/prompt?namespaceId=public&promptKey=order-summary&version=1.0.0" \
    -H 'accessToken: <NACOS_ACCESS_TOKEN>'
```

运行时查询返回 <code>promptKey</code>、<code>version</code>、<code>template</code>、<code>variables</code>、<code>md5</code> 等字段。先判断请求成功，再读取内容。

## 按标签查询

```bash
curl -sS "$nacosApi/v3/client/ai/prompt?namespaceId=public&promptKey=order-summary&label=latest" \
    -H 'accessToken: <NACOS_ACCESS_TOKEN>'
```

| 读取方式 | 适合场景 | 变化来源 |
| --- | --- | --- |
| <code>version=1.0.0</code> | 验证、回放、固定行为 | 显式修改读取版本 |
| <code>label=latest</code> | 跟随发布指针 | 管理端切换标签 |
| 不指定版本或标签 | 使用默认最新选择逻辑 | 以当前发布与 latest 语义为准 |

接口选择优先级为 version > label > latest；应用最好明确选一种，不同时传多个选择字段。

## Java 查询与渲染

沿用商品工程的 WebMVC 依赖，创建 <code>src/main/java/com/example/prompt/PromptDemo.java</code>，在 IDE 中独立运行。

```java
package com.example.prompt;

import java.util.Map;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.web.client.RestClient;

public class PromptDemo {
    public static void main(String[] args) {
        var client = RestClient.builder()
                .baseUrl("<NACOS_HTTP_BASE_URL>")
                .defaultHeader("accessToken", "<NACOS_ACCESS_TOKEN>")
                .build();
        Map<String, Object> response = client.get()
                .uri("/v3/client/ai/prompt?namespaceId=public&promptKey=order-summary&label=latest")
                .retrieve().body(new ParameterizedTypeReference<Map<String, Object>>() {});
        if (response == null || !(response.get("code") instanceof Number code)
                || code.intValue() != 0) {
            throw new IllegalStateException("Prompt查询失败");
        }
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) response.get("data");
        String template = (String) data.get("template");
        String rendered = template.replace("{{orderText}}", "订单A001：两件商品，实付99元");
        System.out.println("版本=" + data.get("version"));
        System.out.println(rendered);
    }
}
```

这里仅对一个约定变量做字符串替换；复杂模板使用应用选定的模板引擎，并校验必填变量。真实业务还需处理 Token 到期、网络超时、解析错误和可用版本缓存。

<code>3.1.1</code> Client 未涵盖所有 3.2 新增 AI SDK 能力，因此本课用 Server 的 **v3 HTTP Prompt 接口**，不为这次实验强行覆盖 Alibaba BOM 的客户端版本。

## 发布第二版与回退

1. 新建 <code>1.1.0</code> 草稿，在模板中增加“同时提取订单号”。
2. 发布并上线，用固定版本查询验证 <code>1.1.0</code>。
3. 确认后把 <code>latest</code> 切到 <code>1.1.0</code>，再次运行查询，检查返回版本和内容。
4. 如果验证失败，把标签指回已发布可用的 <code>1.0.0</code>，再次查询验证。

回退标签不会修改目标版本内容，也不会保证应用已立即重新读取。应用启动时读取一次就固定在内存中；需要跟随标签时设计明确的重新查询或刷新策略。

## MD5 与模板评估

| 机制 | 解决的问题 | 不能证明什么 |
| --- | --- | --- |
| MD5 条件查询 | 内容不变时返回 304，复用缓存 | 模板语义是否正确 |
| 历史版本 | 审计和回退 | 模型输出必然稳定 |
| 变量定义 | 应用清楚需要填哪些输入 | 外部输入没有提示词注入风险 |
| 业务样例评估 | 比较模板对真实输入的效果 | 对所有模型与输入绝对有效 |

模板查询验证与模型输出评估分开做：本课闭环到模板读取和渲染，后续接入模型时再用固定样例评估改版效果。

详见 [[11-Nacos3AI管理中心|AI 资源生命周期]]、[[12-MCP注册发现与工具调用|MCP 工具实操]]、[[06-环境隔离与配置治理|环境和权限治理]]。
