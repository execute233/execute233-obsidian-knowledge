**基于****Session****的分离（有状态）**
我们发现，实际上SpringSecurity在登录之后，会利用Session机制记录用户的登录状态，这就要求我们每次请求的时候都需要携带Cookie才可以，因为Cookie中存储了用于识别的JSESSIONID数据。因此，要实现前后端分离，我们只要稍微修改一下可以实现了，这对于小型的单端应用程序非常友好。

登录实现与跨域处理：
首先需要配置相关接口：
@Bean
public SecurityFilterChain filterChain(HttpSecurity httpSecurity) throws Exception {
return httpSecurity.authorizeHttpRequests( conf -\> {
conf.anyRequest().authenticated();
}).formLogin(conf -\> {
conf.loginProcessingUrl("/api/auth/login");
conf.successHandler(this::onAuthenticationSuccess);
conf.failureHandler(this::onAuthenticationFailure);
conf.permitAll();
}).csrf(AbstractHttpConfigurer::disable)
.build();
}
// 自定义成功与失败处理器, 其中RestBean是自定义的响应实体类，用于快速封装响应数据
@SneakyThrows
void onAuthenticationSuccess(HttpServletRequest request,
HttpServletResponse response,
Authentication authentication) {
response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");
response.getWriter().write(RestBean._success_(authentication.getName()).asJsonString());
}
@SneakyThrows
void onAuthenticationFailure(HttpServletRequest request,
HttpServletResponse response,
AuthenticationException exception) {
response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");
response.getWriter().write(RestBean._failure_(exception.getMessage()).asJsonString());
}
然后我们可以在这个地址里使用PST表单请求(username:user,password:生成)来测试登录
由于前后端分离可能是不同的站点，需要允许跨域请求cors，在配置中SercurityFilterChain的返回Bean配置：
.cors( conf -\> {
CorsConfiguration cors = new CorsConfiguration();
// 添加前端站点地址
cors.addAllowedOrigin("http://localhost:8080"); // 其实可以*，但为了安全
cors.setAllowCredentials(true); // 允许带cookie
cors.addAllowedHeader("*");
cors.addAllowedMethod("*");
cors.addExposedHeader("*");
// 注意是org.springframework.web.cors包下的
UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
source.registerCorsConfiguration("/**", cors); // 对所有地址生效
conf.configurationSource(source);
})
为了在不登录情况下访问页面都被跳转登录，我们可以这样处理：
exceptionHandling( conf -\> {
// 授权相关异常处理器
conf.accessDeniedHandler(this::handleProcess);
// 验证相关异常处理器
conf.authenticationEntryPoint(this::handleProcess);
})
因为上面几个方法参数极其相似，我们可以写到同一个方法：
// 授权异常，验证异常，成功与失败处理器
@SneakyThrows
void handleProcess(HttpServletRequest request,
HttpServletResponse response,
Object exceptionOrAuthentication){
response.setContentType("application/json");
response.setCharacterEncoding("UTF-8");
PrintWriter writer = response.getWriter();
if (exceptionOrAuthentication instanceof AccessDeniedException e){
writer.write(RestBean._failure_(403, e.getMessage()).asJsonString());
} else if (exceptionOrAuthentication instanceof Authentication authentication) {
writer.write(RestBean._success_(authentication.getName()).asJsonString());
} else if (exceptionOrAuthentication instanceof Exception e) {
writer.write(RestBean._failure_(401, e.getMessage()).asJsonString());
}
}
对于
**基于****Token****的分离（无状态）**
基于Token的前后端分离主打无状态，无状态服务是指在处理每个请求时，服务本身不会维持任何与请求相关的状态信息。每个请求被视为独立的、自包含的操作，服务只关注处理请求本身，而不关心前后请求之间的状态变化。也就是说，用户在发起请求时，服务器不会记录其信息，而是通过用户携带的Token信息来判断是哪一个用户：

无状态服务的优点包括：
1．服务端无需存储会话信息：传统的会话管理方式需要服务端存储用户的会话信息，包括用户的身份认证信息和会话状态。而使用Token，服务端无需存储任何会话信息，所有的认证信息都包含在Token中，使得服务端变得无状态，减轻了服务器的负担，同时也方
便了服务的水平扩展。
2，减少网络延迟：传统的会话管理方式需要在每次请求中都携带会话标识，即使是无状态的RESTfulAPI也需要携带身份认证信息。而使用Token，身份认证信息已经包含在Token中，只需要在请求的Authorization头部携带Token即可，减少了每次请求的数据量，减少了网络延迟。
3．客户端无需存储会话信息：传统的会话管理方式中，客户端需要存储会话标识，以便在每次请求中携带。而使用Token，客户端只需要保存Token即可，方便了客户端的存储和管理。
4．跨域支持：Token可以在各个不同的域名之间进行传递和使用，因为Token是通过签名来验证和保护数据完整性的，可以防止未经授权的修改。

**JWT****令牌**

![[_assets/SpringBoot-前后端分离/SpringBoot-前后端分离__09-24-16-0.png]]

一个JWT令牌由3部分组成：标头(Header)、有效载荷(Payload)和签名(Signature)。在传输的时候，会将JWT的3部分分别进行Base64编码后用．进行连接形成最终需要传输的字符串。

- 标头：包含一些元数据信息，比如JWT签名所使用的加密算法，还有类型，这里统一都是JWT。
- 有效载荷：包括用户名称、令牌发布时间、过期时间、JWTID等，当然我们也可以自定义添加字段，我们的用户信息一般都在这里存放。
- 签名：首先需要指定一个密钥，该密钥仅仅保存在服务器中，保证不能让其他用户知道。然后亻吏用Header中指定的算法对Header和Payload进行base64加密之后的结果通过密钥计算哈希值，然后就得出一个签名哈希。这个会用于之后验证内容是否被篡改。

于是可以这样设计：

![[_assets/SpringBoot-前后端分离/SpringBoot-前后端分离__09-24-20-1.png]]

在java使用JWT，可以使用第三方库 java-jwt(com.auth0, 4.3.0),用法如：
String jwtKey = "execute233.com:spring-learn:jwt-key"; // jwt-key
Algorithm algorithm = Algorithm._HMAC256_(jwtKey); // 加密算法对象
String sign = JWT._create_()
.withClaim("id", 1)
.withClaim("name", "execute233")
.withClaim("role", "admin")
.withExpiresAt(new Date(2025, Calendar._DECEMBER_, 11)) // 过期时间
.sign(algorithm);// 签名
**Spring-Security整合JWT**
SpringSecurity中并没有为我们提供预设的JWT校验模块（只有OAuth2模块才有）这里我们只能手动进行整合，JWT可以存放在Cookie或是请求头中，不过不管哪种方式，我们都可以通过Request获取到对应的JWT令牌，这里我们使比较常见的请求头携带JWT的方案，客户端发起的请求中会携带这样的的特殊请求头．

![[_assets/SpringBoot-前后端分离/SpringBoot-前后端分离__09-24-22-2.png]]

Basic和Bearer是两种不同的身份验证方式。

- Basic是一种基本的身份验证方式，它将用户名和密码进行base64编码后，放在Authorization请求头中，用于向服务器验证用户身份。这种方式不够安全，因为它将密码以明文的形式传输，容易受到中间人攻击。
- Bearer是一种更安全的身份验证方式，它基于令牌(Token)来验证用户身份。Bearer令牌是由身份验证服务器颁发给客户端的，客户端在每个请求中将令牌放在Authorization请求头的Bearer字段中。服务器会验证令牌的有效性和权限，以确定用户的身份。Bearer令牌通常使用JSONWebToken(JWT)的形式进行传递和验证。

首先完成JWT的相关工具类：
import org.springframework.security.core.userdetails.UserDetails;
public class JwtUtils {
private static final String _key_ = "execute233.com:spring-learn:jwt-key";
// 根据用户信息创建令牌
public static String createJwt(UserDetails detail) {
Algorithm algorithm = Algorithm._HMAC256_(_key_);
Calendar calendar = Calendar._getInstance_();
Date now = calendar.getTime();
calendar.add(Calendar._HOUR_, 24); // 令牌有效期24小时
return JWT._create_()
.withClaim("name", detail.getUsername())
.withClaim("authorities", detail.getAuthorities().stream().map(GrantedAuthority::getAuthority).toList())
.withExpiresAt(calendar.getTime()) // 过期时间
.withIssuedAt(now) // 签发时间
.sign(algorithm); // 签名
}
// 根据jwt验证并解析信息
public static UserDetails resolveJwt(String token) {
Algorithm algorithm = Algorithm._HMAC256_(_key_);
JWTVerifier verifier = JWT._require_(algorithm).build();
try {
DecodedJWT verified = verifier.verify(token); // 验证令牌
Map\<String, Claim\> claims = verified.getClaims(); // 获取令牌中的内容
if (new Date().after(claims.get("exp").asDate())) { // 如果是过期令牌返回null
return null;
} else { // 重组装为USerDetails对象
return User._withUsername_(claims.get("name").asString())
.password("") // 不需要密码
.authorities(claims.get("authorities").asArray(String.class))
.build();
}
} catch (JWTVerificationException e) {
return null;
}
}
}
然后我们要自己写一个JWTAuthenticationFilter加入到Spring默认提供的过滤器链
public class JWTAuthenticationFilter extends OncePerRequestFilter {
// 继承自OncePerRequestFilter，保证每次请求只经过一次过滤器
@Override
protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
throws ServletException, IOException {
String authorizationString = request.getHeader("Authorization");// 从请求头中获取Authorization字段
// 判断是否包含JWT并正确
if (authorizationString != null && authorizationString.startsWith("Bearer ")) {
String token = authorizationString.substring(7);
// 开始解析成USerDetails对象，得到null说明解析失败，JWT有问题
UserDetails userDetails = JwtUtils._resolveJwt_(token);
if (userDetails != null) {
// 验证没有问题，那么就可以开始创建Authentication了，这里我们跟默认情况保持一致
// 使用UsernamePasswordAuthenticationToken作为实体，填写相关用户信息进去
UsernamePasswordAuthenticationToken authentication =
new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
// 把设置好的Authentication塞入SecurityContext表示完成认证
SecurityContextHolder._getContext_().setAuthentication(authentication);
}
}
// 最后放行，下一个过滤器
// 没有给到SecurityContextHolder设置Authentication，后面直接拦截掉了，况且还有用户密码登录请求
filterChain.doFilter(request,response);
}
}
然后配置：
http.sessionManagement( conf -\> {
conf.sessionCreationPolicy(SessionCreationPolicy._STATELESS_); // Session管理策略设置为无状态
}).addFilterBefore( // 添加自己写的JWT过滤器到Security链中，要放在UserPasswordAuthenticationFilter之前
new JWTAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class
).build();
记得登录处理时返回token，同时跨域也可以不带Cookie：
writer.write(RestBean._success_(JwtUtils._createJwt_((User) authentication.getPrincipal())).asJsonString());
**JWT****退出登录处理**
一种黑名单机制，另一种白名单机制，目前我们以黑名单机制为例：
我们可以在创建JWT的时候额外创建一个UUID用于记录黑名单，作为JWT的ID属性jti：
.withJWTId(UUID._randomUUID_().toString())
然后创建个集合来放黑名单的UUID，一般是放在redis(方便过期)的，这里省略
同时在验证token的时候也要验证它是否过期
自动续签JWT令牌
前端发现时间不足时自动向后端申请一个新的token即可