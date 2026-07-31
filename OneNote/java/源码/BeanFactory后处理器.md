BeanFactoryPostProcessor
BeanFactory扫描Bean注解的后处理器
GenericApplicationContext context = new GenericApplicationContext();
// 注册BeanFactory后处理器, 用于解析@Configuration
// 可以处理@ComponentScan、@Bean、@Import、@ImportResource
context.registerBean(ConfigurationClassPostProcessor.class);
ConfigurationClassPostProcessor中组件扫描原理
// 工具类，查找某个类上面是否有某个注解，这里以Config类上是否有@ComponentScan为例
ComponentScan componentScan = AnnotationUtils._findAnnotation_(Config.class, ComponentScan.class);
if (componentScan != null) {
// 获取包名属性
for (String basePackage : componentScan.basePackages()) {
// 拿到要扫描的包，转换为路径，比如
// com.execute233.springlearn.controller -> classpath*:com/execute233/springlearn/controller/**/*.class
String path = "classpath:" + basePackage.replace('.', '/') + "/**/*.class";
// 用于缓存类信息的工厂
CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();
// 通过注解构建bean名器
AnnotationBeanNameGenerator generator = new AnnotationBeanNameGenerator();
Resource[] resources = context.getResources(path);
// 拿到所有要扫描的类的路径
for (Resource resource : resources) {
// 得到每个类的元信息，检查是否加了@Component
MetadataReader reader = factory.getMetadataReader(resource);
AnnotationMetadata annotationMetadata = reader.getAnnotationMetadata();
// 如果该类添加了@Component或其派生
if (annotationMetadata.hasAnnotation(Component.class.getName())
|| annotationMetadata.hasMetaAnnotation(Component.class.getName())) {
// 构建BeanDefinition并注册到BeanFactory中
AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder
._genericBeanDefinition_(reader.getClassMetadata().getClassName()).getBeanDefinition();
DefaultListableBeanFactory beanFactory = context.getDefaultListableBeanFactory();
String beanName = generator.generateBeanName(beanDefinition, beanFactory);
beanFactory.registerBeanDefinition(beanName, beanDefinition);
}
}
}
}
ConfigurationClassPostProcessor中@Bean扫描原理
// 用于缓存类信息的工厂
CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();
MetadataReader reader = factory.getMetadataReader(Config.class.getName());
// 拿到被@Bean修饰的方法
Set<MethodMetadata> methods = reader.getAnnotationMetadata().getAnnotatedMethods(Bean.class.getName());
for (MethodMetadata method : methods) {
// 这里是工厂方法得到的Bean，就不用指定类名了
BeanDefinitionBuilder builder = BeanDefinitionBuilder._genericBeanDefinition_();
// 你要拿到方法的bean肯定要一个实例化的对象给它访问，这里指定工厂方法名称与工厂Bean名称
builder.setFactoryMethodOnBean(method.getMethodName(), Config.class.getName());
// 我们还要定义工厂方法参数的装配形式
builder.setAutowireMode(AbstractBeanDefinition._AUTOWIRE_CONSTRUCTOR_ );
// 这样就拿到BeanDefinition
AbstractBeanDefinition beanDefinition = builder.getBeanDefinition();
context.getDefaultListableBeanFactory().registerBeanDefinition(method.getMethodName(), beanDefinition);
}
Mapper接口的管理
单个Mapper可以如此管理
// 返回的是工厂对象，但最后还是Mapper1的Bean
@Bean
public MapperFactoryBean<Mapper1> mapper1(SqlSessionFactory sqlSessionFactory) {
MapperFactoryBean<Mapper1> factory = new MapperFactoryBean<>(Mapper1.class);
factory.setSqlSessionFactory(sqlSessionFactory);
return factory;
}
多个 Mapper可以模拟ComponentScan做的事
class MapperPostProcessor implements BeanDefinitionRegistryPostProcessor {
@Override
public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry beanfactory) throws BeansException {
PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
AnnotationBeanNameGenerator generator = new AnnotationBeanNameGenerator();
// 拿到Mapper路径下的所有资源
Resource[] resources = resolver.getResources(path);
CachingMetadataReaderFactory factory = new CachingMetadataReaderFactory();
for (Resource resource : resources) {
MetadataReader reader = factory.getMetadataReader(resource);
ClassMetadata metadata = reader.getClassMetadata();
if (metadata.isInterface()) {
// 拿到接口
AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder._genericBeanDefinition_(MapperFactoryBean.class)
.addConstructorArgValue(metadata.getClassName())
.setAutowireMode(AbstractBeanDefinition._AUTOWIRE_BY_TYPE_)
.getBeanDefinition();
// 这里bean名字是个问题，直接丢给生成器是拿到MapperFactoryBean的名字，会覆盖容器已有的东西
// Spring源码里是另起一个beanDefinition来生成名字的
AbstractBeanDefinition beanNameDefinition = BeanDefinitionBuilder
._genericBeanDefinition_(metadata.getClassName()).getBeanDefinition();
String beanName = generator.generateBeanName(beanNameDefinition, beanfactory);
beanfactory.registerBeanDefinition(beanName, beanDefinition);
}
}
}
}