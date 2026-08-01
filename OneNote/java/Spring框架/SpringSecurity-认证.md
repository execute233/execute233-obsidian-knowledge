---
title: SpringSecurity-认证
tags: [java, Spring框架]
aliases: [SpringSecurity-认证]
---

# SpringSecurity-认证

## 基于内存验证

在 Security 配置类中注册一个 Bean 即可：

```java
@Bean
public UserDetailsService userDetailsService() {
    UserDetails user = User.withDefaultPasswordEncoder()
        .username("user")
        .password("password")
        .roles("USER")
        .build();
    UserDetails admin = User.withDefaultPasswordEncoder()
        .username("admin")
        .password("password")
        .roles("ADMIN", "USER")
        .build();
    return new InMemoryUserDetailsManager(user, admin);
}
```

我们发现，`withDefaultPasswordEncoder()` 这种方法已经被弃用（谁教你明文存密码的？）。

我们可以使用官方提供的 BCrypt 工具，将 `PasswordEncoder` 在 Security 配置中注册为 Bean 即可，于是可把上面修改为：

```java
@Bean
public UserDetailsService userDetailsService(PasswordEncoder encoder) {
    UserDetails user = User
        .withUsername("user")
        .password(encoder.encode("password"))
        .roles("USER")
        .build();
    UserDetails admin = User
        .withUsername("admin")
        .password(encoder.encode("password"))
        .roles("ADMIN", "USER")
        .build();
    return new InMemoryUserDetailsManager(user, admin);
}
```

这个 BCrypt 工具生成的格式：

![[_assets/SpringSecurity-认证/SpringSecurity-认证__09-24-00-0.png]]

但发现，所有的 POST 请求都被拦截，返回 403。

因为 SpringSecurity 自带了 CSRF 防护，任何的 POST 请求都需要带 `_csrf` 才行。关闭可参考自定义登录界面实现。

## 基于数据库的验证

官方提供了可以直接使用的用户和权限表设计：

```sql
create table users(username varchar(50) not null primary key, password varchar(500) not null, enabled boolean not null);
create table authorities(username varchar(50) not null, authority varchar(50) not null,
    constraint fk_authorities_users foreign key(username) references users(username));
create unique index ix_auth_username on authorities(username, authority);
```

然后添加 Mybatis 和 MySQL 的依赖。

注意要额外使用 `spring-jdbc` 和 `mybatis-spring`。

然后就可以了：

```java
@Bean
public UserDetailsService userDetailsService(DataSource source, PasswordEncoder encoder) {
    JdbcUserDetailsManager manager = new JdbcUserDetailsManager(source);
    // 仅首次启动时创建新用户用于测试，后续无需创建，记得删去
    manager.createUser(User.withUsername("user")
        .password(encoder.encode("password"))
        .roles("USER").build());
    return manager;
}
```

无论是 `InMemoryUserDetailsManager` 还是现在的 `JdbcUserDetailsManager`，他们都是实现自 `UserDetailsManager` 接口，这个接口中有着一套完整的增删改查操作，方便我们直接对用户进行处理：

```java
public interface UserDetailsManager extends UserDetailsService {
    void createUser(UserDetails user);
    void updateUser(UserDetails user);
    void deleteUser(String username);
    void changePassword(String oldPassword, String newPassword);
    boolean userExists(String username);
}
```

通过使用 `UserDetailsManager` 对象，我们就能快速执行用户相关的管理操作，比如我们可以直接在网站上添加一个快速重置密码的接口，首先需要配置一下 `JdbcUserDetailsManager`，为其添加一个 `AuthenticationManager` 用于原密码的校验：

```java
private AuthenticationManager authenticationManager(UserDetailsManager manager, PasswordEncoder encoder) {
    DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
    provider.setUserDetailsService(manager);
    provider.setPasswordEncoder(encoder);
    return new ProviderManager(provider);
}

@Bean
public UserDetailsManager userDetailsManager(DataSource source, PasswordEncoder encoder, DataSource dataSource) throws Exception {
    JdbcUserDetailsManager manager = new JdbcUserDetailsManager(dataSource);
    // 为 UserDetailsManager 设置 AuthenticationManager 即可开启重置密码的校验
    manager.setAuthenticationManager(authenticationManager(manager, encoder));
    return manager;
}
```

## 自定义验证

只需要自定义实现 `UserDetailService` 或 `UserDetailManager`，添加到 Bean 当中并重写其中的方法即可：

```java
@Service
public class AuthorizeService implements UserDetailsService {
    @Autowired
    UserMapper userMapper;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        Account account = userMapper.selectAccountByName(username);
        if (account == null) {
            throw new UsernameNotFoundException(username);
        }
        return User.withUsername(account.getUsername())
            .password(account.getPassword())
            .roles("USER").build();
    }
}
```

## 自定义登录界面

过滤请求：

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http.authorizeHttpRequests(auth -> {
        auth.requestMatchers("static/**").permitAll();  // 静态资源全部放行
        auth.anyRequest().authenticated();  // 依然所有请求要验证
    }).formLogin(conf -> {
        // 下面是表单登录配置
        conf.loginPage("/login");  // 登录页
        conf.loginProcessingUrl("/api/auth/login");  // 登录表单提交地址
        conf.defaultSuccessUrl("/index");  // 登录成功后跳转页面
        conf.permitAll();  // 将登录相关的地址放行
        // 用户名和密码的表单名称，不过默认就是这个，除非有特殊需求
        conf.usernameParameter("username");
        conf.passwordParameter("password");
    }).logout(conf -> {
        conf.logoutUrl("/doLogout");  // 退出登录地址
        conf.logoutSuccessUrl("/login");  // 退出登录成功后跳转页面
        conf.permitAll();
    })
    .csrf(AbstractHttpConfigurer::disable).build();
}
```

## 记住我功能

使用本地 Cookie 存储的方式实现了记住我功能，但是这种方式并不安全，我们可以使用 SpringSecurity 实现，它提供了携带 Token 的 Cookie，默认保留 14 天，只需配置 SecurityFilterChain 的 Bean 即可：

```java
.rememberMe(conf -> {
    conf.alwaysRemember(false);  // 不开启始终记住，需要配置为用户自行勾选
    conf.rememberMeParameter("remember-me");  // 记住我表单字段，默认就是这个，可以不配置
    conf.rememberMeCookieName("token");  // 记住我 cookie 名称
}).build();
```

但注意，这个信息是存在服务器内存中的，如果要保存在数据库中可以实现 `PersistentTokenRepository` 接口：

```java
@Bean
public PersistentTokenRepository tokenRepository(DataSource source) {
    JdbcTokenRepositoryImpl repository = new JdbcTokenRepositoryImpl();
    // 启动时自动创建记住我的表，仅第一次需要，后续不需要
    repository.setCreateTableOnStartup(true);
    repository.setDataSource(source);
    return repository;
}
```

记得最后要在 `rememberMe()` 里设置 `tokenRepository` 并设置有效期。