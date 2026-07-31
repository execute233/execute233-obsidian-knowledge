基于角色授权  
仍然可以在filterChain里配置  
auth.requestMatchers("static/**").permitAll(); // 静态资源全部放行  
auth.requestMatchers("/").hasAnyRole("USER", "ADMIN");  
auth.anyRequest().hasAnyRole("ADMIN"); // 其他请求需要ADMIN角色()  
auth.anyRequest().authenticated(); // 依然所有请求要验证  
同时，实现UserDetailsService的类返回的UserDetail要有.roles  
基于注解授权  
首先要开启方法安全校验@EnableMethodSecurity  
然后就可以在方法打这些注解：  
@PreAuthorize(写SpEL表达式)-方法执行前,详细可在SecurityExpressionRoot查看  
@PostAuthorize-这个是方法执行之后  
@Secured-不支持SpEL，并需要ROLE_前缀  
@PreFilter与@PostFilter-对于集合类型的参数或返回值过滤  
基于权限授权