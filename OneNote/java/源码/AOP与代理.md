# AOP与代理

ajc增强
AspectJ代理并不是很广泛，它通过在编译时修改源代码来实现，不依赖于Spring
另见：小框架 -> AspectJ
agent增强
在类加载时修改字节码实现，也不依赖Spring
运行时需要加入VM Options -javaagent:aspectjweaver.jar
proxy增强-jdk
注意jdk代理只能针对接口代理
```csharp
interface Foo {
void foo();
```
}
```python
class Target implements Foo {
public void foo() {
IO._println_("foo");
```
}
}
// 目标对象
```text
Target target = new Target();
ClassLoader classLoader = SpringApplication.class.getClassLoader();
Foo foo = (Foo) Proxy._newProxyInstance_(classLoader, new Class[]{Foo.class}, (proxy, method, args1) -> {
```
// 传入参数分别是：代理对象自己、执行的方法、方法参数
```python
IO._println_("before foo");
Object result = method.invoke(target, args1);
IO._println_("after foo");
return result;
```
});
foo.foo();
proxy增强-cglib
要注意与目标是子父关系（即不能代理final class）
Target target = new Target();
// 参1为父类型，参2是代理方法执行的行为
Target proxy = (Target) Enhancer._create_(Target.class, (MethodInterceptor) (obj, method, args1, methodProxy) -> {
// 代理类自己、当前执行方法、执行参数、可以避免反射调用的代理对象
```python
IO._println_("before");
Object result = methodProxy.invoke(target, args1); // 没用反射，需要目标(Spring)
result = methodProxy.invokeSuper(obj, args1); // 也没用反射，用代理自己
IO._println_("after");
return result;
```
});
proxy.foo();
}
原理-proxy增强-jdk
public final class $Proxy2 extends Proxy implements Foo {
// 一些要用的获取调用的方法保存在这
```csharp
private static final Method _m0_;
private static final Method _m1_;
private static final Method _m2_;
private static final Method _m3_;
public $Proxy2(InvocationHandler invocationHandler) {super(invocationHandler);}
```
// 初始化代理类的方法
```python
static {
ClassLoader classLoader = $Proxy2.class.getClassLoader();
try {
_m0_ = Object.class.getMethod("hashCode", new Class[0]);
_m1_ = Object.class.getMethod("equals", Object.class);
_m2_ = Object.class.getMethod("toString", new Class[0]);
_m3_ = Class._forName_("com.execute233.springlearn.Application$Foo", false, classLoader).getMethod("foo", new Class[0]);
return;
```
}
```csharp
catch (NoSuchMethodException noSuchMethodException) {
throw new NoSuchMethodError(noSuchMethodException.getMessage());
```
}
```csharp
catch (ClassNotFoundException classNotFoundException) {
throw new NoClassDefFoundError(classNotFoundException.getMessage());
```
}
}
// 下面都是增强代理方法，使用ASM生成
```python
public final void foo() {
try {
this.h.invoke(this, _m3_, null);
return;
```
}
```csharp
catch (Error | RuntimeException throwable) {
throw throwable;
```
}
```csharp
catch (Throwable throwable) {
throw new UndeclaredThrowableException(throwable);
```
}
}
…
}
原理-proxy增强-cglib
原理与上面类似，该代理是继承了目标类型，还增加了MethodProxy
public class $Prox0 extends Target {
// 一些要用的获取调用的方法保存在这
```csharp
private static final Method _foo_;
private static final MethodProxy _fooProxy_;
```
// 初始化代理类的方法
```csharp
static {
try {
_foo_ = Target.class.getMethod("foo");
```
// 参数是：目标类、代理类、方法标识符、增强方法名、原始方法名
_fooProxy_ = MethodProxy._create_(Target.class, $Prox0.class, "()V", "fooProxy", "proxy");
}
```csharp
catch (NoSuchMethodException noSuchMethodException) {
throw new NoSuchMethodError(noSuchMethodException.getMessage());
```
}
}
private MethodInterceptor methodInterceptor;

```java
public void setMethodInterceptor(MethodInterceptor methodInterceptor) {
this.methodInterceptor = methodInterceptor;
```
}

// 下面都是增强代理方法，使用ASM生成
```java
public final void fooProxy() {
try {
methodInterceptor.intercept(this, _foo_, new Object[0], _fooProxy_);
} catch (Throwable e) {
throw new RuntimeException(e);
```
}
}
}
jdk与cglib的统一
// 1、准备切点
```text
AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
pointcut.setExpression("execution(* foo())");
```
// 2、准备通知
```python
MethodInterceptor advice = invocation -> {
IO._println_("before");
Object result = invocation.proceed();
IO._println_("after");
return result;
```
};
// 3、准备切面
DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(pointcut, advice);
// 4、创建代理，会根据情况使用jdk或者cglib代理
// proxyTargetClass = false时,目标实现了接口，则使用jdk实现，否则cglib
// proxyTargetClass = true时，总是使用cglib实现
```text
ProxyFactory factory = new ProxyFactory();
factory.setTarget(new Target());
```
factory.addAdvisor(advisor);
Target proxy = (Target) factory.getProxy();
proxy.foo();
切点匹配
```text
AspectJExpressionPointcut pointcut1 = new AspectJExpressionPointcut();
pointcut1.setExpression("execution(* foo())");
boolean flag1 = pointcut1.matches(Target.class.getMethod("foo"), Target.class);// 看下指定的方法是否匹配表达式
AspectJExpressionPointcut pointcut2 = new AspectJExpressionPointcut();
pointcut2.setExpression("@annotation(org.springframework.transaction.annotation.Transactional)"); // 匹配注解方法，但是Spring没用这种
boolean flag2 = pointcut2.matches(Target.class.getMethod("foo"), Target.class);
```
// Spring的@Transactional可以加载方法、类、接口，所以AspectJ不能这样实现，类似于下面的步骤
```python
StaticMethodMatcherPointcut pointcut3 = new StaticMethodMatcherPointcut() {
@Override
public boolean matches(Method method, Class<?> aClass) {
```
// 检查方法是否加了@Transactional
```python
MergedAnnotations annotations = MergedAnnotations._from_(method);
if (annotations.isPresent(Transactional.class)) {
return true;
```
}
// 检查类是否加了@Transactional，会在本类、父类、接口上找
```python
annotations = MergedAnnotations._from_(aClass, MergedAnnotations.SearchStrategy._TYPE_HIERARCHY_);
if (annotations.isPresent(Transactional.class)) {
return true;
```
}
return false;
}
};
从@Aspect到Advisor
```python
@Aspect // 高级切面类
static class Aspect1 {
@Before("==execution(* foo())==")
public void before() {
IO._println_("before");
```
}
```python
@After("==execution(* foo()==")
public void after() {
IO._println_("after");
```
}
}
```python
@Configuration
static class Config {
@Bean // 低级切面类
public Advisor advisor() {
AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
pointcut.setExpression("execution(* foo())");
return new DefaultPointcutAdvisor(pointcut, (MethodInterceptor) invocation -> {
IO._println_("before");
Object result = invocation.proceed();
IO._println_("after");
return result;
```
});
}
}
main
```text
GenericApplicationContext context = new GenericApplicationContext();
context.registerBean("aspect", Aspect1.class);
context.registerBean("context", Config.class);
```
context.registerBean(ConfigurationClassPostProcessor.class);
// 用于切点解析的BeanPostProcessor，在Bean的依赖注入前和初始化后做了增强
context.registerBean(AnnotationAwareAspectJAutoProxyCreator.class);
AnnotationAwareAspectJAutoProxyCreator做了以下事情
AnnotationAwareAspectJAutoProxyCreator creator = context.getBean(AnnotationAwareAspectJAutoProxyCreator.class);
// AnnotationAwareAspectJAutoProxyCreator做了以下事情
// 第一种重要方法：收集可以应用指定类的有资格的Advisor,参1是指定类，参2是bean名
// 一种是自己写的Advisor，另一种则是@Aspect转为Advisor
List<Advisor> advisors = creator.findEligibleAdvisors(Target.class, "");
// 第二种重要方法：内部调用了findEligibleAdvisors，只要返回的集合不为空就表示需要创建代理
// 分别为：要代理的对象，bean名、cacheKey，这里返回得是得你对象或者原始对象
Object object = creator.wrapIfNecessary(new Target(), "target1", "taget1");
代理的创建时机
初始化之后（无循环依赖）
实例创建之后，依赖注入前（有循环依赖时），并暂存在二级缓存
依赖注入与初始化不应该被增强，仍被施加于原始对象
切面顺序控制
对于切面，一般是低级切面在外面先被执行，然后高级切面在里面后被执行
我们可以自己控制执行顺序（高级切面）
@Aspect // 高级切面类
@Order(1) // 定义切面顺序，越小越优先，不能用在方法
static class Aspect1
在低级切面可以
```python
DefaultPointcutAdvisor pointcutAdvisor = new DefaultPointcutAdvisor(pointcut, (MethodInterceptor) invocation -> {
IO._println_("before");
Object result = invocation.proceed();
IO._println_("after");
return result;
```
});
pointcutAdvisor.setOrder(2);
将高级切面转换为低级切面
// 要代理对象的实例工厂
```text
AspectInstanceFactory factory = new SingletonAspectInstanceFactory(new Aspect1());
ArrayList<Advisor> list = new ArrayList<>();
```
_/**_
_*_ **@Before** _会被转换为__AspectJMethodBeforeAdvice__的形式，保存了：_
_*_ _通知代码从哪来、切点是什么，通知对象如何被创建_
_*_ _类似的还有__AspectJAroundAdvice(__环绕通知__)__、__AspectJAfterReturningAdvice(__后置通知__)__、__AspectJAfterThrowingAdvice(__环绕通知__)__、__AspectJAfterAdvice(__环绕通知__)_
_* **/_
// 这里假定Aspect1是高级切面对象
```python
for (Method method : Aspect1.class.getDeclaredMethods()) {
if (method.isAnnotationPresent(Before.class)) {
```
// 切点解析
```text
String expression = method.getAnnotation(Before.class).value();
AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
```
pointcut.setExpression(expression);
// 前置通知，参3是对应的对象实例工厂
AspectJMethodBeforeAdvice advice = new AspectJMethodBeforeAdvice(method, pointcut, factory);
// 切面
DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(pointcut, advice);
list.add(advisor);
}
// ... @After、@Around、@AfterReturning、@AfterThrowing类似
}
然后将通知统一转换为MethodInterceptor（适配器模式）

![[_assets/AOP与代理/AOP与代理__09-26-31-0.png]]

// 获取代理工厂
```text
Target target = new Target();
ProxyFactory proxyFactory = new ProxyFactory();
```
proxyFactory.setTarget(target);
proxyFactory.addAdvisors(list);
// 将说有通知转换为环绕通知
List<Object> methodInterceptorslist =
proxyFactory.getInterceptorsAndDynamicInterceptionAdvice(Target.class.getMethod("foo"), Target.class);
创建并执行调用链
// 参数分别为:代理、目标、方法、方法参数、目标类型、转换好的环绕通知
MethodInvocation methodInvocation = new ReflectiveMethodInvocation(
null, target, Target.class.getMethod("foo"), new Object[0], Target.class, methodInterceptorslist);
// 执行过程里面的通知要拿到当前的调用链，放在了当前线程里
// 方调用链操作也是环绕通知，由最外层通知执行，比如
```text
// proxyFactory.addAdvisor(ExposeInvocationInterceptor.INSTANCE);
methodInvocation.proceed(); // 调用所有的环绕通知
```
调用链调用演示
```csharp
class MyInvocation implements MethodInvocation {
private final Object target;
private final Method method;
private final Object[] args;
private final List<MethodInterceptor> methodInterceptorList;
private int count = 1; // 调用次数
public MyInvocation(Object target, Method method, Object[] args, List<MethodInterceptor> methodInterceptorList) {
this.target = target;
this.method = method;
this.args = args;
this.methodInterceptorList = methodInterceptorList;
```
}
```python
@Override
public Method getMethod() {return method;}
@Override
public Object[] getArguments() {return args;}
@Override
public Object proceed() throws Throwable {
```
// 职责是调用每个环绕通知（没有就调用目标）
if (count > methodInterceptorList.size()) {
// 调用目标结束递归
return method.invoke(target, args);
}
// 逐一调用通知
MethodInterceptor interceptor = methodInterceptorList.get(count++ - 1);
// 传入本调用链对象，注意里面还会调用proceed方法，从而进入下一个通知
return interceptor.invoke(this);
}
```python
@Override
public Object getThis() {return target;}
@Override
public AccessibleObject getStaticPart() {return method;}
```
}
动态通知调用
下面这种需要参数的就是动态通知调用，静态执行不需要切点，但这个要
```python
@Before("==execution(* foo()) && args(x)==")
public void before(int x) {
IO._println_("before: " + x);
```
}
对于这种动态通知，它使用的不是环绕通知，而是
record InterceptorAndDynamicMethodMatcher(
MethodInterceptor interceptor, MethodMatcher matcher) {}
多出了切点就可以解析参数调用了
MethodInvocation methodInvocation = new ReflectiveMethodInvocation(
```sql
null, target, Target.class.getMethod("foo", int.class)
, new Object[]{100}, Target.class, methodInterceptorslist) {};
```
methodInvocation.proceed();