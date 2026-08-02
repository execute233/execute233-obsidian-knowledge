---
title: AOP与代理
tags: [java, 源码]
aliases: [AOP与代理]
---

# AOP与代理

## ajc 增强

AspectJ 代理并不是很广泛，它通过在编译时修改源代码来实现，不依赖于 Spring。

另见：小框架 → AspectJ

## agent 增强

在类加载时修改字节码实现，也不依赖 Spring。

运行时需要加入 VM Options `-javaagent:aspectjweaver.jar`。

## proxy 增强 — jdk

注意 jdk 代理只能针对接口代理。

```java
interface Foo {
    void foo();
}

class Target implements Foo {
    @Override
    public void foo() {
        IO.println("foo");
    }
}

// 目标对象
Target target = new Target();
ClassLoader classLoader = SpringApplication.class.getClassLoader();
Foo foo = (Foo) Proxy.newProxyInstance(classLoader, new Class[]{Foo.class}, (proxy, method, args1) -> {
    // 传入参数分别是：代理对象自己、执行的方法、方法参数
    IO.println("before foo");
    Object result = method.invoke(target, args1);
    IO.println("after foo");
    return result;
});
foo.foo();
```

## proxy 增强 — cglib

要注意与目标是子父关系（即不能代理 final class）。

```java
Target target = new Target();
// 参 1 为父类型，参 2 是代理方法执行的行为
Target proxy = (Target) Enhancer.create(Target.class, (MethodInterceptor) (obj, method, args1, methodProxy) -> {
    // 代理类自己、当前执行方法、执行参数、可以避免反射调用的代理对象
    IO.println("before");
    Object result = methodProxy.invoke(target, args1); // 没用反射,需要目标(Spring)
    result = methodProxy.invokeSuper(obj, args1); // 也没用反射,用代理自己
    IO.println("after");
    return result;
});
proxy.foo();
```

## 原理 — proxy 增强 jdk

```java
public final class $Proxy2 extends Proxy implements Foo {
    // 一些要用的获取调用的方法保存在这
    private static final Method m0;
    private static final Method m1;
    private static final Method m2;
    private static final Method m3;

    public $Proxy2(InvocationHandler invocationHandler) {super(invocationHandler);}

    // 初始化代理类的方法
    static {
        ClassLoader classLoader = $Proxy2.class.getClassLoader();
        try {
            m0 = Object.class.getMethod("hashCode", new Class[0]);
            m1 = Object.class.getMethod("equals", Object.class);
            m2 = Object.class.getMethod("toString", new Class[0]);
            m3 = Class.forName("com.execute233.springlearn.Application$Foo", false, classLoader)
                    .getMethod("foo", new Class[0]);
            return;
        } catch (NoSuchMethodException noSuchMethodException) {
            throw new NoSuchMethodError(noSuchMethodException.getMessage());
        } catch (ClassNotFoundException classNotFoundException) {
            throw new NoClassDefFoundError(classNotFoundException.getMessage());
        }
    }

    // 下面都是增强代理方法，使用 ASM 生成
    public final void foo() {
        try {
            this.h.invoke(this, m3, null);
            return;
        } catch (Error | RuntimeException throwable) {
            throw throwable;
        } catch (Throwable throwable) {
            throw new UndeclaredThrowableException(throwable);
        }
    }
    // ...
}
```

## 原理 — proxy 增强 cglib

原理与上面类似，该代理是继承了目标类型，还增加了 MethodProxy。

```java
public class $Prox0 extends Target {
    // 一些要用的获取调用的方法保存在这
    private static final Method foo;
    private static final MethodProxy fooProxy;

    // 初始化代理类的方法
    static {
        try {
            foo = Target.class.getMethod("foo");
            // 参数是：目标类、代理类、方法标识符、增强方法名、原始方法名
            fooProxy = MethodProxy.create(Target.class, $Prox0.class, "()V", "fooProxy", "proxy");
        } catch (NoSuchMethodException noSuchMethodException) {
            throw new NoSuchMethodError(noSuchMethodException.getMessage());
        }
    }

    private MethodInterceptor methodInterceptor;

    public void setMethodInterceptor(MethodInterceptor methodInterceptor) {
        this.methodInterceptor = methodInterceptor;
    }

    // 下面都是增强代理方法，使用 ASM 生成
    public final void fooProxy() {
        try {
            methodInterceptor.intercept(this, foo, new Object[0], fooProxy);
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }
}
```

## jdk 与 cglib 的统一

```java
// 1、准备切点
AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
pointcut.setExpression("execution(* foo())");

// 2、准备通知
MethodInterceptor advice = invocation -> {
    IO.println("before");
    Object result = invocation.proceed();
    IO.println("after");
    return result;
};

// 3、准备切面
DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(pointcut, advice);

// 4、创建代理，会根据情况使用 jdk 或者 cglib 代理
// proxyTargetClass = false 时，目标实现了接口，则使用 jdk 实现，否则 cglib
// proxyTargetClass = true 时，总是使用 cglib 实现
ProxyFactory factory = new ProxyFactory();
factory.setTarget(new Target());
factory.addAdvisor(advisor);
Target proxy = (Target) factory.getProxy();
proxy.foo();
```

## 切点匹配

```java
AspectJExpressionPointcut pointcut1 = new AspectJExpressionPointcut();
pointcut1.setExpression("execution(* foo())");
boolean flag1 = pointcut1.matches(Target.class.getMethod("foo"), Target.class); // 看下指定的方法是否匹配表达式

AspectJExpressionPointcut pointcut2 = new AspectJExpressionPointcut();
pointcut2.setExpression("@annotation(org.springframework.transaction.annotation.Transactional)"); // 匹配注解方法,但是 Spring 没用这种
boolean flag2 = pointcut2.matches(Target.class.getMethod("foo"), Target.class);

// Spring 的 @Transactional 可以加载方法、类、接口，所以 AspectJ 不能这样实现，类似于下面的步骤
StaticMethodMatcherPointcut pointcut3 = new StaticMethodMatcherPointcut() {
    @Override
    public boolean matches(Method method, Class<?> aClass) {
        // 检查方法是否加了 @Transactional
        MergedAnnotations annotations = MergedAnnotations.from(method);
        if (annotations.isPresent(Transactional.class)) {
            return true;
        }
        // 检查类是否加了 @Transactional，会在本类、父类、接口上找
        annotations = MergedAnnotations.from(aClass, MergedAnnotations.SearchStrategy.TYPE_HIERARCHY);
        if (annotations.isPresent(Transactional.class)) {
            return true;
        }
        return false;
    }
};
```

## 从 @Aspect 到 Advisor

```java
@Aspect // 高级切面类
static class Aspect1 {
    @Before("execution(* foo())")
    public void before() {
        IO.println("before");
    }

    @After("execution(* foo())")
    public void after() {
        IO.println("after");
    }
}

@Configuration
static class Config {
    @Bean // 低级切面类
    public Advisor advisor() {
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        pointcut.setExpression("execution(* foo())");
        return new DefaultPointcutAdvisor(pointcut, (MethodInterceptor) invocation -> {
            IO.println("before");
            Object result = invocation.proceed();
            IO.println("after");
            return result;
        });
    }
}

public static void main(String[] args) {
    GenericApplicationContext context = new GenericApplicationContext();
    context.registerBean("aspect", Aspect1.class);
    context.registerBean("context", Config.class);
    context.registerBean(ConfigurationClassPostProcessor.class);
    // 用于切点解析的 BeanPostProcessor，在 Bean 的依赖注入前和初始化后做了增强
    context.registerBean(AnnotationAwareAspectJAutoProxyCreator.class);
    AnnotationAwareAspectJAutoProxyCreator creator = context.getBean(AnnotationAwareAspectJAutoProxyCreator.class);

    // AnnotationAwareAspectJAutoProxyCreator 做了以下事情
    // 第一种重要方法：收集可以应用指定类的有资格的 Advisor，参 1 是指定类，参 2 是 bean 名
    // 一种是自己写的 Advisor，另一种则是 @Aspect 转为 Advisor
    List<Advisor> advisors = creator.findEligibleAdvisors(Target.class, "");

    // 第二种重要方法：内部调用了 findEligibleAdvisors，只要返回的集合不为空就表示需要创建代理
    // 分别为：要代理的对象，bean 名、cacheKey，这里返回得是得你对象或者原始对象
    Object object = creator.wrapIfNecessary(new Target(), "target1", "taget1");
}
```

## 代理的创建时机

- 初始化之后（无循环依赖）
- 实例创建之后，依赖注入前（有循环依赖时），并暂存在二级缓存

依赖注入与初始化不应该被增强，仍被施加于原始对象。

## 切面顺序控制

对于切面，一般是低级切面在外面先被执行，然后高级切面在里面后被执行。

我们可以自己控制执行顺序（高级切面）。

```java
@Aspect // 高级切面类
@Order(1) // 定义切面顺序，越小越优先，不能用在方法
static class Aspect1 {
}
```

在低级切面可以：

```java
DefaultPointcutAdvisor pointcutAdvisor = new DefaultPointcutAdvisor(pointcut, (MethodInterceptor) invocation -> {
    IO.println("before");
    Object result = invocation.proceed();
    IO.println("after");
    return result;
});
pointcutAdvisor.setOrder(2);
```

## 将高级切面转换为低级切面

```java
// 要代理对象的实例工厂
AspectInstanceFactory factory = new SingletonAspectInstanceFactory(new Aspect1());
ArrayList<Advisor> list = new ArrayList<>();

/**
 * @Before 会被转换为 AspectJMethodBeforeAdvice 的形式，保存了：
 *   通知代码从哪来、切点是什么，通知对象如何被创建
 *   类似的还有 AspectJAroundAdvice（环绕通知）、
 *              AspectJAfterReturningAdvice（后置通知）、
 *              AspectJAfterThrowingAdvice（环绕通知）、
 *              AspectJAfterAdvice（环绕通知）
 */
// 这里假定 Aspect1 是高级切面对象
for (Method method : Aspect1.class.getDeclaredMethods()) {
    if (method.isAnnotationPresent(Before.class)) {
        // 切点解析
        String expression = method.getAnnotation(Before.class).value();
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        pointcut.setExpression(expression);
        // 前置通知，参 3 是对应的对象实例工厂
        AspectJMethodBeforeAdvice advice = new AspectJMethodBeforeAdvice(method, pointcut, factory);
        // 切面
        DefaultPointcutAdvisor advisor = new DefaultPointcutAdvisor(pointcut, advice);
        list.add(advisor);
    }
    // ... @After、@Around、@AfterReturning、@AfterThrowing 类似
}
```

然后将通知统一转换为 MethodInterceptor（适配器模式）。

其实无论 `ProxyFactory` 基于哪种方式创建代理，最后干活(调用 advice)的是一个 `MethodInvocation` 对象。

- 因为 advisor 有多个，且一个套一个调用，因此需要一个调用链对象，即 `MethodInvocation`
- `MethodInvocation` 要知道 advice 有哪些，还要知道目标，调用次序如下

```text
|-> before1 ----------------------------------
|                                            |
|    |-> before2 ----------------------------|
|    |                                       |
|    |    |-> target ------- 目标   advice2  advice1
|    |    |                                 |
|    |    |                                 |
|    |-> after2 ----------------------------|
|    |                                       |
|-> after1 -----------------------------------
```

- 从上图看出，**环绕通知**才适合作 advice，因此其他 before、afterReturning、afterThrowing 都会被转换成环绕通知。
- 统一转换为环绕通知，体现的是设计模式中的**适配器模式**：
  - 对外是为了方便使用要区分 before、afterReturning、afterThrowing
  - 对内统一都是环绕通知，统一用 `MethodInterceptor` 表示

## 创建并执行调用链

```java
// 获取代理工厂
Target target = new Target();
ProxyFactory proxyFactory = new ProxyFactory();
proxyFactory.setTarget(target);
proxyFactory.addAdvisors(list);
// 将说有通知转换为环绕通知
List<Object> methodInterceptorslist = proxyFactory.getInterceptorsAndDynamicInterceptionAdvice(
        Target.class.getMethod("foo"), Target.class);

// 参数分别为：代理、目标、方法、方法参数、目标类型、转换好的环绕通知
MethodInvocation methodInvocation = new ReflectiveMethodInvocation(
        null, target, Target.class.getMethod("foo"), new Object[0], Target.class, methodInterceptorslist);

// 执行过程里面的通知要拿到当前的调用链，放在了当前线程里
// 方调用链操作也是环绕通知，由最外层通知执行，比如
// proxyFactory.addAdvisor(ExposeInvocationInterceptor.INSTANCE);
methodInvocation.proceed(); // 调用所有的环绕通知
```

## 调用链调用演示

```java
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
    }

    @Override
    public Method getMethod() {return method;}

    @Override
    public Object[] getArguments() {return args;}

    @Override
    public Object proceed() throws Throwable {
        // 职责是调用每个环绕通知（没有就调用目标）
        if (count > methodInterceptorList.size()) {
            // 调用目标结束递归
            return method.invoke(target, args);
        }
        // 逐一调用通知
        MethodInterceptor interceptor = methodInterceptorList.get(count++ - 1);
        // 传入本调用链对象，注意里面还会调用 proceed 方法，从而进入下一个通知
        return interceptor.invoke(this);
    }

    @Override
    public Object getThis() {return target;}

    @Override
    public AccessibleObject getStaticPart() {return method;}
}
```

## 动态通知调用

下面这种需要参数的就是动态通知调用，静态执行不需要切点，但这个要。

```java
@Before("execution(* foo()) && args(x)")
public void before(int x) {
    IO.println("before: " + x);
}
```

对于这种动态通知，它使用的不是环绕通知，而是：

```java
record InterceptorAndDynamicMethodMatcher(
    MethodInterceptor interceptor, MethodMatcher matcher) {
}
```

多出了切点就可以解析参数调用了。

```java
MethodInvocation methodInvocation = new ReflectiveMethodInvocation(
    null, target, Target.class.getMethod("foo", int.class),
    new Object[]{100}, Target.class, methodInterceptorslist) {};

methodInvocation.proceed();
```