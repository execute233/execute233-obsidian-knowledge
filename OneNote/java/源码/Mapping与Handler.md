---
title: Mapping与Handler
tags: [java, 源码]
aliases: [Mapping与Handler]
---

# Mapping与Handler

## 内嵌 Wab 容器的自动配置

```java
AnnotationConfigServletWebServerApplicationContext context
    = new AnnotationConfigServletWebServerApplicationContext(WebConfig.class);
```

```java
@Configuration
@ComponentScan
// 注意这下面是 SpringMVC 的注解，不是 boot
@PropertySource("classpath:application.yml")
@EnableConfigurationProperties({WebMvcProperties.class, ServerProperties.class})
public class WebConfig {

    @Autowired
    WebMvcProperties webMvcProperties;
    @Autowired
    ServerProperties serverProperties;

    @Bean // 内嵌 Web 容器工厂
    public TomcatServletWebServerFactory tomcatServletWebServerFactory() {
        return new TomcatServletWebServerFactory(); // 可以写端口进去
    }

    @Bean // 创建 DispatcherServlet
    public DispatcherServlet dispatcherServlet() {
        return new DispatcherServlet();
    }

    @Bean // 注册 DispatcherServlet，SpringMVC 的入口
    DispatcherServletRegistrationBean dispatcherServletRegistrationBean(DispatcherServlet servlet) {
        // 告诉匹配的路径
        DispatcherServletRegistrationBean registrationBean = new DispatcherServletRegistrationBean(servlet, "/");
        // 设置为大于 0 的值则会在 tomcat 启动时初始化，多个数字小的优先初始化
        registrationBean.setLoadOnStartup(webMvcProperties.getServlet().getLoadOnStartup());
        return registrationBean;
    }

    // 下面是 @EnableWebMvc
}
```

### 在 DispatcherServlet 初始化，会做这些事

```text
initMultipartResolver(context); // 文件上传解析器
initLocaleResolver(context); // 本地化
initThemeResolver(context); // 网页主题
initHandlerMappings(context); // 路径映射
initHandlerAdapters(context); // 执行请求处理适配
initHandlerExceptionResolvers(context); // 异常解析处理
// 用于在未明确提供视图名称时将输入 HttpServletRequest 转换为逻辑视图名称
initRequestToViewNameTranslator(context);
initViewResolvers(context); // 视图解析器
initFlashMapManager(context); // 用于重定向
```

DispatcherServlet 是 SpringMVC 请求处理入口，完整的请求链路见 [[SpringMVC-Controller]]。

## RequestMappingHandlerMapping

```java
// 用于解析 @RequestMapping 以及派生注解，生成路径与控制器方法的映射关系，初始化时生成
RequestMappingHandlerMapping mapping = context.getBean(RequestMappingHandlerMapping.class);
// 获取映射结果
Map<RequestMappingInfo, HandlerMethod> handlerMethods = mapping.getHandlerMethods();

// 假设请求来了，获得请求方法 返回处理器执行链对象
HandlerExecutionChain handlerExecutionChain // 模拟一个请求
    = mapping.getHandler(new MockHttpServletRequest("GET", "/test"));
```

## RequestMappingHandlerAdapter

作用就是调用控制器方法（被 `@RequestMapping` 标注）。

```java
// 接上
RequestMappingHandlerAdapter adapter = context.getBean(RequestMappingHandlerAdapter.class);
// 这是受保护的核心方法
adapter.invokeHandlerMethod(request, response, (HandlerMethod) handlerExecutionChain.getHandler());

// 参数解析器，解析 @RequestParam、@PathVariable、@CookieValue、@RequestHeader、@RequestBody 等等
adapter.getArgumentResolvers();
// 返回值解析器，比如 ModelAndView、String 等等
adapter.getReturnValueHandlers();
```

### 自定义参数解析器

参数解析器的组合与解析过程见 [[参数解析器]]。

```java
class TokenArgumentResolver implements HandlerMethodArgumentResolver {
    @Override // 是否支持某个参数
    public boolean supportsParameter(MethodParameter parameter) {
        Token token = parameter.getParameterAnnotation(Token.class);
        return token != null;
    }

    @Nullable
    @Override // 解析参数
    public Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer,
                                   NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception {
        return webRequest.getHeader("token");
    }
}

@Bean
RequestMappingHandlerAdapter requestMappingHandlerAdapter() {
    TokenArgumentResolver resolver = new TokenArgumentResolver();
    RequestMappingHandlerAdapter handlerAdapter = new RequestMappingHandlerAdapter();
    handlerAdapter.setCustomArgumentResolvers(List.of(resolver));
    return handlerAdapter;
}
```

### 自定义返回值处理器

```java
class YmlReturnValueHandler implements HandlerMethodReturnValueHandler {
    @Override // 是否支持这种返回值
    public boolean supportsReturnType(MethodParameter returnType) {
        Annotation yml = returnType.getMethodAnnotation(Yml.class);
        return yml != null;
    }

    @Override
    public void handleReturnValue(@Nullable Object returnValue, MethodParameter returnType,
                                  ModelAndViewContainer mavContainer, NativeWebRequest webRequest) throws Exception {
        // 返回结果转为 yaml
        String dumped = new Yaml().dump(returnType);
        HttpServletResponse response = webRequest.getNativeResponse(HttpServletResponse.class);
        // 写入响应
        response.setContentType("text/plain;charset=utf-8");
        response.getWriter().print(dumped);
        // 后面还有 SpringMvc 视图解析，我们要设置请求处理完毕
        mavContainer.setRequestHandled(true);
    }
}

@Bean
RequestMappingHandlerAdapter requestMappingHandlerAdapter() {
    YmlReturnValueHandler returnValueHandler = new YmlReturnValueHandler();
    RequestMappingHandlerAdapter handlerAdapter = new RequestMappingHandlerAdapter();
    handlerAdapter.setCustomReturnValueHandlers(List.of(returnValueHandler));
    return handlerAdapter;
}
```
