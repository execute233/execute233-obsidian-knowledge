BeanFactory与ApplicationContext
我们从SpringApplication.run返回ConfigurableApplicationContext的开始研究接口关系

![[_assets/Spring-Start/Spring-Start__09-26-15-0.png]]

BeanFactory是ApplicationContext的父接口，是Spring的核心容器，主要的ApplicationContext实现了组合它的功能
Spring中BeanFactory默认实现是用DefaultListableBeanFactory

![[_assets/Spring-Start/Spring-Start__09-26-17-1.png]]

可以通过反射拿到里面的BeanFactory字段
ConfigurableApplicationContext context = SpringApplication._run_(SpringLearnApplication.class);
Field singletonObjects = DefaultSingletonBeanRegistry.class.getDeclaredField("singletonObjects");
singletonObjects.setAccessible(true);
ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
Map<String, Object> map = (Map<String, Object>) singletonObjects.get(beanFactory);
map.forEach( (k, v) -> {
_log_.info(k + ": " + v);
});
ApplicationContext比BeanFactory多的功能主要体现在以下接口
MessageSource（国际化资源处理）
通用的翻译在messages.properties中，国家翻译以messages_en.properties为文件存储键值对
当对应的键不存在对应的语言环境时，会去默认语言找
IDEA在resources目录下创建资源包即可，添加语言文件
可以注入MessageSource该Bean在任何地方用
// 里面的文本可以嵌入{0}类似的，使用args传参
r = context.getMessage("key", null, Locale._CHINA_);
// 找不到就用默认的消息
r = context.getMessage("key", null, "defaultMessage", Locale._CHINA_);
ResourcePatternResolver（通过通配符匹配资源）
// 返回资源路径下的文件，有多个则返回第一个找到的
context.getResource("classpath:application.yml");
// 返回在jar包中的资源路径下的所有文件
context.getResources("classpath*:META_INF/spring.factories");
EnvironmentCapable（处理环境信息）
// 获取环境变量
ConfigurableEnvironment environment = context.getEnvironment();
// 获取的是系统环境变量，不区分大小写
environment.getProperty("java_home");
// Spring中的配置文件的环境变量
environment.getProperty("server.port");
ApplicationEventPublish（发布事件对象）
// 发送事件
context.publishEvent(new ApplicationEvent("test") {});
我们可以在任意一个Bean中的方法打上@EventListener注解来监听事件
@EventListener
public void test(ApplicationEvent event) {
Object source = event.getSource();
}
BeanFactory的实现
// 创建BeanFactory
DefaultListableBeanFactory beanFactory = new DefaultListableBeanFactory();
// 得到Bean的定义(class, scope, 初始化, 销毁)
AbstractBeanDefinition beanDefinition =
BeanDefinitionBuilder._genericBeanDefinition_(Config.class).setScope("singleton").getBeanDefinition();
// 添加到BeanFactory
beanFactory.registerBeanDefinition("config", beanDefinition);
// 给BeanFactory添加常用的后处理器，包括注解处理以及事件处理
AnnotationConfigUtils._registerAnnotationConfigProcessors_(beanFactory);
// 拿到该BeanFactory里面的所有BeanFactory后处理器
Collection<BeanFactoryPostProcessor> postProcessors = beanFactory.getBeansOfType(BeanFactoryPostProcessor.class).values();
// 让每个BeanFactory后处理器去处理这个BeanFactory
for (BeanFactoryPostProcessor beanFactoryPostProcessor : postProcessors) {
beanFactoryPostProcessor.postProcessBeanFactory(beanFactory);
}
// 还有Bean的后处理器，针对Bean的各个阶段提供扩展，比如@Autowired
beanFactory.getBeansOfType(BeanPostProcessor.class).values().forEach(beanFactory::addBeanPostProcessor);
// beanFactory默认是lazy-init,可以调用下面方法来预先实例化所有的单例Bean
beanFactory.preInstantiateSingletons();
// 获取所有bean的名字
for (String name : beanFactory.getBeanDefinitionNames()) {
_log_.info(name);
}
_/**_
_* beanFactory__不会自动：_
_*_ _主动调用__BeanFactory__后处理器_
_*_ _主动添加__Bean__后处理器_
_*_ _主动初始化单例__Bean_
_*_ _解析__beanFactory__、__${}__和__#{}_
_* bean__的后处理器有排序的逻辑_
_* **/_
ApplicationContext的实现
它主要实现了类似于上面代码的功能，扩展BeanFactory
主要是这种
ClassPathXmlApplicationContext - 基于classpath下xml格式的配置文件来创建
FileSystemXmlApplicationContext - 基于磁盘路径下xml格式配置文件来创建
AnnotationApplicationContext - 基于java注解配置来创建
AnnotationConfigServletWebServerApplicationContext - 基于java注解来创建，用于web环境
基于xml格式的配置文件原理
// 一样创建个BeanFactory
DefaultListableBeanFactory beanFactory = new DefaultListableBeanFactory();
// 得到BeanDefinition读取器
XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(beanFactory);
// 加载配置文件，把Bean添加到BeanFactory里
reader.loadBeanDefinitions(new ClassPathResource("application.xml"));
基于注解的配置
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(Config.class);
基于注解+Web的配置
AnnotationConfigServletWebServerApplicationContext context =
new AnnotationConfigServletWebServerApplicationContext(WebConfig.class);
@Configuration
static class WebConfig {
@Bean
public ServletWebServerFactory servletWebServerFactory() {
return new TomcatServletWebServerFactory(); // tomcat
}
@Bean
public DispatcherServlet dispatcherServlet() {
return new DispatcherServlet(); // dispatcherServlet
}
@Bean
public DispatcherServletRegistrationBean registrationBean(DispatcherServlet servlet) {
return new DispatcherServletRegistrationBean(servlet, "/"); // 绑定
}
@Bean("/") // 另类的Controller配置方法，Bean名字就是Web路径
public Controller controller1() {
return (Controller) (request, response) -> {
response.getWriter().print("helloWorld");
return null;
};
}
}