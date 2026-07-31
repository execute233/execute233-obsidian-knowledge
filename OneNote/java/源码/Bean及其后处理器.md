Bean的生命周期  
以下面为例  
ConfigurableApplicationContext context = SpringApplication._run_(SpringLearnApplication.class, args);  
context.close();  
@Slf4j  
@Component  
class LifeCleanBean {  
public LifeCleanBean() {  
_log_.info("constructor");  
}  
// 该方法会寻找bean进行注入，默认不注入字符串，如果使用@Value则会进行值注入  
@Autowired // 是在构造方法完成后注入  
public void autowire(@Value("${JAVA_HOME}") String home) {  
_log_.info("autowire: {}", home);  
}  
@PostConstruct // 在构造方法后，也在注入完成后  
public void postConstruct() {  
_log_.info("postConstruct");  
}  
@PreDestroy // 仅在单例bean被销毁时调用，其他类型的销毁时机不同  
public void preDestroy() {  
_log_.info("preDestroy");  
}  
}  
扩展Bean处理器  
public class MyBeanPostProcessor // 这届接口都实现了BeanPostProcessor  
implements InstantiationAwareBeanPostProcessor, DestructionAwareBeanPostProcessor {  
@Nullable  
@Override  
public Object postProcessBeforeInstantiation(Class\<?\> beanClass, String beanName) throws BeansException {  
// 实例化之前执行，这里返回的对象会替换原本的bean  
return null;  
}  
@Override  
public boolean postProcessAfterInstantiation(Object bean, String beanName) throws BeansException {  
// 实例化之后执行，这里返回false会跳过依赖注入阶段  
return true;  
}
 
@Nullable  
@Override  
public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {  
// 初始化之前执行，返回的对象会替换原本的bean，如@PostConstruct、@ConfigurationProperties就是在这一步解析  
return null;  
}  
@Nullable  
@Override  
public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {  
// 初始化之后执行，返回的对象会替换原本的bean，如代理增强  
return true;  
}
 
@Override  
public void postProcessBeforeDestruction(Object bean, String beanName) throws BeansException {  
// bean销毁之前执行  
}  
@Override  
public boolean requiresDestruction(Object bean) {  
// 是否需要执行销毁方法  
return true;  
}  
@Nullable  
@Override  
public PropertyValues postProcessProperties(PropertyValues pvs, Object bean, String beanName) throws BeansException {  
// 依赖注入阶段执行, 返回null会跳过属性注入阶段  
return pvs;  
}  
}  
执行顺序就是：  
postProcessBeforeInstantiation  
constructor()  
@PostConstructor  
InitializingBean.afterPropertiesSet  
@Bean(initMethod=)  
postProcessAfterInstantiation  
postProcessProperties  
@Autowired  
postProcessBeforeInitialization  
@PostConstruct  
postProcessAfterInitialization  
postProcessBeforeDestruction  
requiresDestruction  
@PreDestroy  
DisposableBean.destroy()  
@Bean(destroyMethod=)  
常见的Bean后处理器  
// 干净的容器，没有自己添加后处理器  
GenericApplicationContext context = new GenericApplicationContext();  
// 设置BeanFactory的@Autowired的参数解析器，这里添加了就可以解析参数里的@Value值注入  
context.getDefaultListableBeanFactory().setAutowireCandidateResolver(new ContextAnnotationAutowireCandidateResolver());  
// 解析@Autowired、@Value的Bean处理器  
context.registerBean(AutowiredAnnotationBeanPostProcessor.class);  
// @Resource、@PostConstruct、@PreDestroy的Bean处理器  
context.registerBean(CommonAnnotationBeanPostProcessor.class);  
// @ConfigurationProperties的Bean处理器，要绑定  
ConfigurationPropertiesBindingPostProcessor._register_(context.getDefaultListableBeanFactory());  
context.refresh(); // 执行BeanFactory后处理器，添加Bean后处理器，初始化说有单例  
@Autowired Bean后处理器解析  
// 1、查看哪些属性、方法添加了@Autowired、称为InjectionMetadata  
AutowiredAnnotationBeanPostProcessor processor = new AutowiredAnnotationBeanPostProcessor();  
processor.setBeanFactory(beanFactory);  
// 执行依赖注入，指定属性对（没有就找默认的），指定的Bean类型，指定的Bean名字  
processor.postProcessProperties(null, Bean1.class, "bean1");  
postProcessProperties的方法具体做了下面的事  
// findAutowiringMetadata方法是私有的，这里通过反射来执行该方法  
InjectionMetadata metadata = (InjectionMetadata) findAutowiringMetadata.invoke(processor, "bean1", Bean1.class, null);  
// 返回的InjectionMetadata调用inject来进行注入，注入时按类型查找值  
metadata.inject(bean1, "bean1", null);  
inject方法里如何注入值  
Field bean2 = Bean1.class.getDeclaredField("bean2"); // 首先获取要注入的字段  
DependencyDescriptor descriptor = new DependencyDescriptor(bean2, false);// 包装字段，并且指示依赖是否必要，否则报错  
// 根据成员变量找要注入谁，给指定的beanName, autowiredBeanName, typeConverter  
// 因为是根据类型来找值的，后面3个参数都可以为null  
beanFactory.doResolveDependency(descriptor, null, null, null);  
inject方法里如何注入方法  
Method setBean2 = Bean1.class.getDeclaredMethod("setBean2", Bean2.class); // 首先获取注入的方法  
DependencyDescriptor descriptor = new DependencyDescriptor(new MethodParameter(setBean2, 0), false);  
beanFactory.doResolveDependency(descriptor, null, null, null);  
总的来说

![[.attachments/Bean及其后处理器/Bean及其后处理器__09-26-21-0.png]]