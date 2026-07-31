Aware  
Aware接口用于注入与容器相关的信息，例如  
BeanNameAware 注入Bean的名字  
BeanFactoryAware 注入BeanFactory容器  
ApplicationContextAware 注入ApplicationContext容器  
EmbeddedValueResolverAware 注入${}  
举例  
class MyBean implements BeanNameAware, ApplicationContextAware, InitializingBean {  
/*  
这些功能用@Autowired也可以实现，但与Aware接口还有区别  
@Autowired的解析需要bean后处理器，属于扩展功能  
Aware是内置功能，不添加扩展，Spring就能识别  
在一些情况下会用到Aware，比如bean加载顺序是：Configuration -\> beanFactoryPostProcessor  
-\> beanPostProcessor -\> bean  
这种情况下Configuration里面的注解便会  
*/  
@Override  
public void setBeanName(String name) {  
_log_.info("setBeanName"); // Bean名称设置后  
}  
@Override  
public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {  
_log_.info("setApplicationContext"); // 设置ApplicationContext后  
}  
@Override  
public void afterPropertiesSet() throws Exception {  
_log_.info("afterPropertiesSet"); // Bean初始化后  
}  
}  
Scope  
目前有以下Scope  
singleton、prototype、request、session、application  
单例注入多例失效  
对于单例对象来讲，依赖注入仅发生了一次，后续没有用到多例，因此使用的始终是第一次依赖注入的多例  
解决办法是使用@Lazy生成代理，每次使用单例方法都由代理生成新的多例对象  
另一种方法是指定@Scope(proxyMode = ScopedProxyMode._TARGET_CLASS_)  
还有种方法是注入ObjectFactory\<Object\>对象，每次使用都利用工厂对象拿到Object的多例