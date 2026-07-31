# SpringMVC-配置

**MVC****的三层架构**

![[_assets/SpringMVC-配置/SpringMVC-配置__09-23-42-0.png]]

MVC详细解释如下：

- M是指业务模型(Model)：通俗的讲就是我们之前用于圭寸装数据传递的实类。
- V是指用户界面(View)：一般指的是前端页面。
- C则是控制器(Controller)：控制器就相当于Servlet的基本功能，处理请求，返回响应。
![[_assets/SpringMVC-配置/SpringMVC-配置__09-23-44-1.png]]

**传统****XML****配置**

1. POM添加依赖spring-webmvc
2. 配置spring的Servlet
3. 配置Spring上下文,比如spring.xml

```yaml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:context="http://www.springframework.org/schema/context"
xsi:schemaLocation="http://www.springframework.org/schema/beans
```
[http://www.springframework.org/schema/beans/spring-beans.xsd](http://www.springframework.org/schema/beans/spring-beans.xsd) [http://www.springframework.org/schema/context](http://www.springframework.org/schema/context) [https://www.springframework.org/schema/context/spring-context.xsd](https://www.springframework.org/schema/context/spring-context.xsd)">
```xml
<!-- 需要引入context命名空间，配置base-package -->
<context:component-scan base-package="" />
</beans>
```
 6. 为DispatcherServlet配置初始化参数,配置spring bean配置文件路径

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee [https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd](https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd)"
version="6.0">
<servlet>
<servlet-name>mvc</servlet-name>
<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
</servlet>
<servlet-mapping>
<servlet-name>mvc</servlet-name>
<url-pattern>/</url-pattern>
</servlet-mapping>
</web-app>
```

在步骤2里，<servlet>标签里写
```xml
<init-param>
<param-name>contextConfigLocation</param-name>
<param-value>classpath:spring.xml</param-value>
</init-param>
```
**注解配置**

1. Tomcat会在类路径中查找实现ServietContainerlnitializer接囗的类，如果发现的话，就用它来配置Servlet容器，Spring提供了这个接囗的实现类SpringServletContainerlnitializer，通过@HandIesTypes(WebAppIicationlnitializer.class)来设置，这个类反过来会查找实现WebAppIicationInitiaIizer的类，并将配置的任务交给他们来完成，因此直接实现接囗即可：
```python
public class WebInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
@Override
protected Class<?>[] getRootConfigClasses() {
return new Class[]{WebInitializer.class}; // 基本的Spring配置类，一般用于业务配置
```
}
```python
@Override
protected Class<?>[] getServletConfigClasses() {
return new Class[0]; // DispatcherServlet的配置类，用于Controller等配置
```
}
```python
@Override
protected String[] getServletMappings() {
return new String[]{"/"}; // 匹配路径
```
}
}