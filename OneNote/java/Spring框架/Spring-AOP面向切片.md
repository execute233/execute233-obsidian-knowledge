首先要导入pom，一般是  
\<dependency\>  
\<groupId\>org.springframework\</groupId\>  
\<artifactId\>spring-aspects\</artifactId\>  
\<version\>6.2.11\</version\>  
\</dependency\>
 
1. XML配置AOP
2. 接口实现AOP
3. 注解实现AOP

XML文件应该是这样  
\<?xml version="1.0" encoding="UTF-8"?\>  
\<beans xmlns="http://www.springframework.org/schema/beans"  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
xmlns:aop="http://www.springframework.org/schema/aop"  
xsi:schemaLocation="http://www.springframework.org/schema/beans  
http://www.springframework.org/schema/beans/spring-beans.xsd  
http://www.springframework.org/schema/aop  
http://www.springframework.org/schema/aop/spring-aop.xsd"\>  
\<!-- 1. 配置目标对象 --\>  
\<bean id="userService" class="com.example.service.UserServiceImpl"/\>   \<!-- 2. 配置切面 --\>  
\<bean id="loggingAspect" class="com.example.aspect.LoggingAspect"/\>  
\<aop:config\>  
\<!-- 定义切点，指定要切的方法 --\>  
\<aop:pointcut id="serviceMethods"  
expression="execution(* com.example.service.*.*(..))"/\>  
\<!-- 配置切面,引用切面bean id --\>  
\<aop:aspect ref="loggingAspect"\>  
切片方法标签  
\</aop:aspect\>  
\</aop:config\>  
\</beans\>
 
1. \<aop:pointcut/\>

id - 指定的id

3. \<aop:aspect\> \<aop:aspect/\>

ref - 指定那个类提供了切片的方法的bean id
 
expression - 选择切入的方法，有很多种可以选择

![[.attachments/Spring-AOP面向切片/Spring-AOP面向切片__09-23-19-0.png]]

以execution为例，它填写的格式(可以使用*匹配任意)是  
修饰符 包名.类名.方法名(参数)
 
这里面有好几个内部标签使用，如  
\<aop:after-returning/\>  
\<aop:after-throwing/\>  
\<aop:after method="afterAdvice" pointcut-ref="serviceMethods"/\>  
\<aop:around/\>  
他们有些共同的属性  
method - 提供了切片方法类里的方法名  
pointcut-ref - 切点id  
如果我们想在切片方法中拿到方法的一些信息，可以在参数列表添加JoinPoint，Spring会自动传入该对象  
还能\<around/\>完全包围方法,切面方法需要ProceedingJoinPoint参数，并要调用proceed()手动执行方法  
实现切片方法的类需要实现XXXAdvice接口  
只需要在\<aop:aspect\>标签内使用\<aop:advisor advice-ref="实现切面的Bean", pointcut-ref="切点"\>  
有这些接口可以使用：  
MethodInterceptor(环绕方法),MethodBeforeAdvice,AfterReturningAdvice,ThrowsAdvice  
首先在@Configuration修饰的类启用注解AOP支持，打上@EnableAspectJAutoProxy  
然后在实现切面的类打上@Bean和@Aspect注解（注意Configuration要打上@Component）  
最后就能在实现切面的类的成员方法上打上相关注解，即是前面的expression字段  
@Before - JoinPoint参数  
@After - 执行后，不管成功还是异常，JoinPoint参数  
@AfterReturning  
@AfterThrowing  
@Around - 环绕通知，有ProceedingJoinPoint参数  
当然，这些注解写expression可能会有性能损失，其实可以直接写切点名的  
可以在@Aspect里面的方法用@Pointcut(expression),创建的切点名就是方法名()  
例（给指定包下指定注解添加Before方法来修改传入参数）：  
_/**_  
_*_ _公共字段自动填充_  
_* **/_  
@Aspect  
@Component  
@Slf4j  
public class AutoFillAspect {  
_/**_  
_*_ _切入点_  
_* **/_  
@Pointcut("==execution(* com.sky.mapper.*.*(..)) && @annotation(com.sky.annotation.AutoFill)==")  
public void autoFillPointCut() {}  
@Before("==autoFillPointCut()==")  
public void autoFill(JoinPoint joinPoint) {  
// 获取AutoFill注解传入的enum  
MethodSignature signature = (MethodSignature) joinPoint.getSignature();  
AutoFill autoFill = signature.getMethod().getAnnotation(AutoFill.class);  
OperationType value = autoFill.value();  
// 获取方法传入参数  
Object[] args = joinPoint.getArgs();  
if (args == null || args.length == 0) return;  
Object entity = args[0];  
Class\<?\> clazz = entity.getClass();  
// 准备数据  
……  
// 根据注解传参不同赋值  
……  
}  
}