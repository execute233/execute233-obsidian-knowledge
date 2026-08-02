---
title: SpringBoot-前后端分离
tags: [java, Spring框架]
aliases: [SpringBoot-前后端分离]
---

# SpringBoot-前后端分离

## 基于 Session 的分离（有状态）

我们发现，实际上 SpringSecurity 在登录之后，会利用 Session 机制记录用户的登录状态，这就要求我们每次请求的时候都需要携带 Cookie 才可以，因为 Cookie 中存储了用于识别的 JSESSIONID 数据。因此，要实现前后端分离，我们只要稍微修改一下就可以了，这对于小型的单端应用程序非常友好。

### 登录实现与跨域处理

首先需要配置相关接口：

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
    return httpSecurity.authorizeHttpRequests(conf -> {
        conf.anyRequest().authenticated();
    }).formLogin(conf -> {
        conf.loginProcessingUrl("/api/auth/login");
        conf.successHandler(this::onAuthenticationSuccess);
        conf.failureHandler(this::onAuthenticationFailure);
        conf.permitAll();
    }).csrf(AbstractHttpConfigurer::disable)
    .build();
}
```

自定义成功与失败处理器，其中 `RestBean` 是自定义的响应实体类，用于快速封装响应数据：

```java
@SneakyThrows
void onAuthenticationSuccess(HttpServletRequest request,
                             HttpServletResponse response,
                             Authentication authentication) {
    response.setContentType("application/json");
    response.setCharacterEncoding("UTF-8");
    response.getWriter().write(RestBean.success(authentication.getName()).asJsonString());
}

@SneakyThrows
void onAuthenticationFailure(HttpServletRequest request,
                             HttpServletResponse response,
                             AuthenticationException exception) {
    response.setContentType("application/json");
    response.setCharacterEncoding("UTF-8");
    response.getWriter().write(RestBean.failure(exception.getMessage()).asJsonString());
}
```

然后我们可以在这个地址里使用 POST 表单请求（`username: user`、`password: 生成`）来测试登录。

### 跨域处理

由于前后端分离可能是不同的站点，需要允许跨域请求 CORS，在配置中 SecurityFilterChain 的返回 Bean 配置：

```java
.cors(conf -> {
    CorsConfiguration cors = new CorsConfiguration();
    // 添加前端站点地址
    cors.addAllowedOrigin("http://localhost:8080");  // 其实可以 *, 但为了安全
    cors.setAllowCredentials(true);  // 允许带 cookie
    cors.addAllowedHeader("*");
    cors.addAllowedMethod("*");
    cors.addExposedHeader("*");
    // 注意是 org.springframework.web.cors 包下的
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", cors);  // 对所有地址生效
    conf.configurationSource(source);
})
```

### 未登录统一处理

为了在不登录情况下访问页面都被跳转登录，我们可以这样处理：

```java
.exceptionHandling(conf -> {
    // 授权相关异常处理器
    conf.accessDeniedHandler(this::handleProcess);
    // 验证相关异常处理器
    conf.authenticationEntryPoint(this::handleProcess);
})
```

因为上面几个方法参数极其相似，我们可以写到同一个方法：

```java
@SneakyThrows
void handleProcess(HttpServletRequest request,
                   HttpServletResponse response,
                   Object exceptionOrAuthentication) {
    response.setContentType("application/json");
    response.setCharacterEncoding("UTF-8");
    PrintWriter writer = response.getWriter();
    if (exceptionOrAuthentication instanceof AccessDeniedException e) {
        writer.write(RestBean.failure(403, e.getMessage()).asJsonString());
    } else if (exceptionOrAuthentication instanceof Authentication authentication) {
        writer.write(RestBean.success(authentication.getName()).asJsonString());
    } else if (exceptionOrAuthentication instanceof Exception e) {
        writer.write(RestBean.failure(401, e.getMessage()).asJsonString());
    }
}
```

## 基于 Token 的分离（无状态）

基于 Token 的前后端分离主打无状态，无状态服务是指在处理每个请求时，服务本身不会维持任何与请求相关的状态信息。每个请求被视为独立的、自包含的操作，服务只关注处理请求本身，而不关心前后请求之间的状态变化。也就是说，用户在发起请求时，服务器不会记录其信息，而是通过用户携带的 Token 信息来判断是哪一个用户。

无状态服务的优点包括：

1. 服务端无需存储会话信息：传统的会话管理方式需要服务端存储用户的会话信息，包括用户的身份认证信息和会话状态。而使用 Token，服务端无需存储任何会话信息，所有的认证信息都包含在 Token 中，使得服务端变得无状态，减轻了服务器的负担，同时也方便了服务的水平扩展。
2. 减少网络延迟：传统的会话管理方式需要在每次请求中都携带会话标识，即使是无状态的 RESTful API 也需要携带身份认证信息。而使用 Token，身份认证信息已经包含在 Token 中，只需要在请求的 Authorization 头部携带 Token 即可，减少了每次请求的数据量，减少了网络延迟。
3. 客户端无需存储会话信息：传统的会话管理方式中，客户端需要存储会话标识，以便在每次请求中携带。而使用 Token，客户端只需要保存 Token 即可，方便了客户端的存储和管理。
4. 跨域支持：Token 可以在各个不同的域名之间进行传递和使用，因为 Token 是通过签名来验证和保护数据完整性的，可以防止未经授权的修改。

### JWT 令牌

![[_assets/SpringBoot-前后端分离/SpringBoot-前后端分离__09-24-16-0.png]]

一个 JWT 令牌由 3 部分组成：标头（Header）、有效载荷（Payload）和签名（Signature）。在传输的时候，会将 JWT 的 3 部分分别进行 Base64 编码后用 `.` 进行连接形成最终需要传输的字符串。

- **标头**：包含一些元数据信息，比如 JWT 签名所使用的加密算法，还有类型，这里统一都是 JWT。
- **有效载荷**：包括用户名称、令牌发布时间、过期时间、JWT ID 等，当然我们也可以自定义添加字段，我们的用户信息一般都在这里存放。
- **签名**：首先需要指定一个密钥，该密钥仅仅保存在服务器中，保证不能让其他用户知道。然后使用 Header 中指定的算法对 Header 和 Payload 进行 base64 加密之后的结果通过密钥计算哈希值，然后就得出一个签名哈希。这个会用于之后验证内容是否被篡改。

于是可以这样设计：

![[_assets/SpringBoot-前后端分离/SpringBoot-前后端分离__09-24-20-1.png]]

在 Java 使用 JWT，可以使用第三方库 `java-jwt`（`com.auth0`，4.3.0），用法如：

```java
String jwtKey = "execute233.com:spring-learn:jwt-key";  // jwt-key
Algorithm algorithm = Algorithm.HMAC256(jwtKey);  // 加密算法对象

String sign = JWT.create()
    .withClaim("id", 1)
    .withClaim("name", "execute233")
    .withClaim("role", "admin")
    .withExpiresAt(new Date(2025, Calendar.DECEMBER, 11))  // 过期时间
    .sign(algorithm);  // 签名
```

### Spring-Security 整合 JWT

SpringSecurity 中并没有为我们提供预设的 JWT 校验模块（只有 OAuth2 模块才有），这里我们只能手动进行整合。JWT 可以存放在 Cookie 或是请求头中，不过不管哪种方式，我们都可以通过 Request 获取到对应的 JWT 令牌，这里我们使用比较常见的请求头携带 JWT 的方案，客户端发起的请求中会携带这样的特殊请求头：

一个典型的 `Authorization` 请求头看起来像这样：

```text
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJzZWxmIiwic3ViIjoiZXh...
```

其中 `Bearer` 是认证方案名称，后面紧跟一个空格，再后面是 JWT 令牌本身（即 base64 编码的 header.payload.signature 三段式字符串）。

Basic 和 Bearer 是两种不同的身份验证方式：

- **Basic** 是一种基本的身份验证方式，它将用户名和密码进行 base64 编码后，放在 Authorization 请求头中，用于向服务器验证用户身份。这种方式不够安全，因为它将密码以明文的形式传输，容易受到中间人攻击。
- **Bearer** 是一种更安全的身份验证方式，它基于令牌（Token）来验证用户身份。Bearer 令牌是由身份验证服务器颁发给客户端的，客户端在每个请求中将令牌放在 Authorization 请求头的 Bearer 字段中。服务器会验证令牌的有效性和权限，以确定用户的身份。Bearer 令牌通常使用 JSON Web Token（JWT）的形式进行传递和验证。

首先完成 JWT 的相关工具类：

```java
import org.springframework.security.core.userdetails.UserDetails;

public class JwtUtils {
    private static final String key = "execute233.com:spring-learn:jwt-key";

    // 根据用户信息创建令牌
    public static String createJwt(UserDetails detail) {
        Algorithm algorithm = Algorithm.HMAC256(key);
        Calendar calendar = Calendar.getInstance();
        Date now = calendar.getTime();
        calendar.add(Calendar.HOUR, 24);  // 令牌有效期 24 小时
        return JWT.create()
            .withClaim("name", detail.getUsername())
            .withClaim("authorities", detail.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority).toList())
            .withExpiresAt(calendar.getTime())  // 过期时间
            .withIssuedAt(now)  // 签发时间
            .sign(algorithm);  // 签名
    }

    // 根据 jwt 验证并解析信息
    public static UserDetails resolveJwt(String token) {
        Algorithm algorithm = Algorithm.HMAC256(key);
        JWTVerifier verifier = JWT.require(algorithm).build();
        try {
            DecodedJWT verified = verifier.verify(token);  // 验证令牌
            Map<String, Claim> claims = verified.getClaims();  // 获取令牌中的内容
            if (new Date().after(claims.get("exp").asDate())) {  // 如果是过期令牌返回 null
                return null;
            } else {  // 重组装为 UserDetails 对象
                return User.withUsername(claims.get("name").asString())
                    .password("")  // 不需要密码
                    .authorities(claims.get("authorities").asArray(String.class))
                    .build();
            }
        } catch (JWTVerificationException e) {
            return null;
        }
    }
}
```

然后我们要自己写一个 `JWTAuthenticationFilter` 加入到 Spring 默认提供的过滤器链：

```java
public class JWTAuthenticationFilter extends OncePerRequestFilter {
    // 继承自 OncePerRequestFilter，保证每次请求只经过一次过滤器

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        String authorizationString = request.getHeader("Authorization");  // 从请求头中获取 Authorization 字段
        // 判断是否包含 JWT 并正确
        if (authorizationString != null && authorizationString.startsWith("Bearer ")) {
            String token = authorizationString.substring(7);
            // 开始解析成 UserDetails 对象，得到 null 说明解析失败，JWT 有问题
            UserDetails userDetails = JwtUtils.resolveJwt(token);
            if (userDetails != null) {
                // 验证没有问题，那么就可以开始创建 Authentication 了，这里我们跟默认情况保持一致
                // 使用 UsernamePasswordAuthenticationToken 作为实体，填写相关用户信息进去
                UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                // 把设置好的 Authentication 塞入 SecurityContext 表示完成认证
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        }
        // 最后放行，下一个过滤器
        // 没有给到 SecurityContextHolder 设置 Authentication，后面直接拦截掉了，况且还有用户密码登录请求
        filterChain.doFilter(request, response);
    }
}
```

然后配置：

```java
http.sessionManagement(conf -> {
    conf.sessionCreationPolicy(SessionCreationPolicy.STATELESS);  // Session 管理策略设置为无状态
}).addFilterBefore(  // 添加自己写的 JWT 过滤器到 Security 链中，要放在 UserPasswordAuthenticationFilter 之前
    new JWTAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class
).build();
```

记得登录处理时返回 token，同时跨域也可以不带 Cookie：

```java
writer.write(RestBean.success(JwtUtils.createJwt((User) authentication.getPrincipal())).asJsonString());
```

### JWT 退出登录处理

一种黑名单机制，另一种白名单机制，目前我们以黑名单机制为例：

我们可以在创建 JWT 的时候额外创建一个 UUID 用于记录黑名单，作为 JWT 的 ID 属性 `jti`：

```java
.withJWTId(UUID.randomUUID().toString())
```

然后创建个集合来放黑名单的 UUID，一般是放在 Redis（方便过期）的，这里省略。

同时在验证 token 的时候也要验证它是否过期。

### 自动续签 JWT 令牌

前端发现时间不足时自动向后端申请一个新的 token 即可。