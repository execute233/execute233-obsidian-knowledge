**基于内存验证**  
在Sercurity配置类中注册一个Bean即可  
@Bean  
public UserDetailsService userDetailsService() {  
UserDetails user = User._withDefaultPasswordEncoder_()  
.username("user")  
.password("password")  
.roles("USER")  
.build();  
UserDetails admin = User._withDefaultPasswordEncoder_()  
.username("admin")  
.password("password")  
.roles("ADMIN", "USER")  
.build();  
return new InMemoryUserDetailsManager(user, admin);  
}  
我们发现，withDefaultPasswordEncoder()这种方法已经被弃用  
（谁教你明文存密码的？）  
我们可以使用官方提供的BCrypt工具，将PasswordEncoder在Sercurity配置中注册为Bean即可,于是可把上面修改为  
@Bean  
public UserDetailsService userDetailsService(PasswordEncoder encoder) {  
UserDetails user = User  
._withUsername_("user")  
.password(encoder.encode("password"))  
.roles("USER")  
.build();  
UserDetails admin = User  
._withUsername_("admin")  
.password(encoder.encode("password"))  
.roles("ADMIN", "USER")  
.build();  
return new InMemoryUserDetailsManager(user, admin);  
}  
这个BCrypt工具生成的格式：

![[.attachments/SpringSecurity-认证/SpringSecurity-认证__09-24-00-0.png]]

但发现，所有的POST请求都被拦截，返回403  
因为SpringSecurity自带了csrf防护，任何的POST请求都需要带_csrf才行  
关闭可参考自定义登录界面实现  
**基于数据库的验证**  
官方提供了可以直接使用的用户和权限表设计  
create table users(username varchar(50) not null primary key, password varchar(500) not null, enabled boolean not null);  
create table authorities(username varchar(50) not null, authority varchar(50) not null, constraint fk_authorities_users foreign key(username) references users(username));  
create unique index ix_auth_username on authorities(username, authority);  
然后添加Mybatis和MySQL的依赖  
注意要额外使用spring-jdbc和mybatis-spring  
然后就可以了  
@Bean  
public UserDetailsService userDetailsService(DataSource source, PasswordEncoder encoder) {  
JdbcUserDetailsManager manager = new JdbcUserDetailsManager(source);  
// 仅首次启动时创建新用户用于测试，后续无需创建，记得删去  
manager.createUser(User._withUsername_("user")  
.password(encoder.encode("password"))  
.roles("USER").build());  
return manager;  
}  
无论是InMemoryUserDetailsManager还是现在的JdbcUserDetaiIsManager,他们都是实现自UserDetaiIsManager接囗，这个接囗中有着一套完整的增删改查操作，方便我们直接对用户进行处理：  
public interface UserDetailsManager extends UserDetailsService {  
void createUser(UserDetails user);  
void updateUser(UserDetails user);  
void deleteUser(String username);  
void changePassword(String oldPassword, String newPassword);  
boolean userExists(String username);  
}  
通过使用UserDetailsManager对象，我们就能快速执行用户相关的管理操作，比如我们可以直接在网站上 添加一个快速重置密码的接囗，首先需要配置一下JdbcUserDetaiIsManager,为其添加一个AuthenticationManager用于原密码的校验：  
private AuthenticationManager authenticationManager(UserDetailsManager manager, PasswordEncoder encoder) {  
DaoAuthenticationProvider provider = new DaoAuthenticationProvider();  
provider.setUserDetailsService(manager);  
provider.setPasswordEncoder(encoder);  
return new ProviderManager(provider);  
}  
@Bean  
public UserDetailsManager userDetailsManager(DataSource source, PasswordEncoder encoder, DataSource dataSource) throws Exception {  
JdbcUserDetailsManager manager = new JdbcUserDetailsManager(dataSource);  
// 为UserDetailsManager设置AuthenticationManager即可开启重置密码的校验  
manager.setAuthenticationManager(authenticationManager(manager, encoder));  
return manager;  
}  
**自定义验证**  
只需要自定义实现UserDetailService或UserDetailManager，添加到Bean当中并重写其中的方法即可  
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
return User._withUsername_(account.getUsername())  
.password(account.getPassword())  
.roles("USER").build();  
}  
}  
**自定义登录界面**  
过滤请求  
@Bean  
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {  
return http.authorizeHttpRequests(auth -\> {  
auth.requestMatchers("static/**").permitAll(); // 静态资源全部放行  
auth.anyRequest().authenticated(); // 依然所有请求要验证  
}).formLogin( conf -\> {  
// 下面是表单登录配置  
conf.loginPage("/login"); // 登录页  
conf.loginProcessingUrl("/api/auth/login"); // 登录表单提交地址  
conf.defaultSuccessUrl("/index"); // 登录成功后跳转页面  
conf.permitAll(); // 将登录相关的地址放行  
// 用户名和密码的表单名称，不过默认就是这个，除非有特殊需求  
conf.usernameParameter("username");  
conf.passwordParameter("password");  
}).logout( conf -\> {  
conf.logoutUrl("/doLogout"); // 退出登录地址  
conf.logoutSuccessUrl("/login"); // 退出登录成功后跳转页面  
conf.permitAll();  
})  
.csrf(AbstractHttpConfigurer::disable).build();  
}  
**记住我功能**  
使用本地Cookie存储的方式实现了记住我功能，但是这种方式并不安全，我们可以使用SpringSecurity实现，它提供了携带Token的Cookie，默认保留14天，只需配置SercurityFilterChain的Bean即可  
……  
.rememberMe( conf -\> {  
conf.alwaysRemember(false); // 不开启始终记住，需要配置为用户自行勾选  
conf.rememberMeParameter("remember-me"); // 记住我表单字段，默认就是这个，可以不配置  
conf.rememberMeCookieName("token"); // 记住我cookie名称  
}).build();  
但注意，这个信息是存在服务器内存中的，如果要保存在数据库中可以实现PersistentTokenRepository接口  
@Bean  
public PersistentTokenRepository tokenRepository(DataSource source) {  
JdbcTokenRepositoryImpl repository = new JdbcTokenRepositoryImpl();  
// 启动时自动创建记住我的表，仅第一次需要，后续不需要  
repository.setCreateTableOnStartup(true);  
repository.setDataSource(source);  
return repository;  
}  
记得最后要在rememberMe()里设置tokenRepository并设置有效期