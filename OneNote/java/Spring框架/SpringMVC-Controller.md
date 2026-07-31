1. **Controller****控制器**

有了SpringMVC之后，我们不必再像之前那样一个请求地址创建一个Servlet了，它使用DispatcherServlet替代Tomcat为我们提供的默认的静态资源Servlet，也就是说，现在所有的请求（除了jsp,因为Tomcat还提供了一个jsp的Servlet)都会经过DispatcherServlet进行处理。

- 根据图片我们可以了解，我们的请求到达Tomcat服务器之后，会交给当前的Web应用程序进行处理，而SpringMVC用DispatcherServlet来处理所有的请求，也就是说它被作为一个统一的访问点，所有的请求全部由它来进行调度。
- 当一个请求经过DispatcherServlet之后，会先走HandlerMapping，它会将请求映射为HandlerExecutionChain，依次经过Handlerlnterceptor有点类似于之前我们所学的过滤器，不过在SpringMVC中我们使用的是拦截器，然后再交给HandlerAdapter，根据请求的路径选择合适的控制器进行处理，控制器处理完成之后，会返回一个ModelAndView对象，包括数据模型和视图，通俗的讲就是页面中数据和页面本身（只包含视图名称即可）
- 返回ModelAndView之后，会交给ViewResolver〈视图解析器）进行处理，视图解析器会对整个视图页面进行解析，SpringMVC自带了一些视图解析器，但是只适用于JSP页面，我们也可以像之前一样使用Thymeleaf作为视图解析器，这样我们就可以根据给定的视图名称，直接读取HTML编写的页面，解析为一个真正的View。
- 解析完成后，就需要将页面中的数据全部渲染到View中，最后返回给DispatcherServlet一个包含所有数据的成形页面，再响应给浏览器，完成整个过程。
- 因此，实际上整个过程我们只需要编写对应请求路径的的Contrer以及配置好我们需要的ViewReso|ver即可，之后还可以继续补充添加拦截器，而其他的流程已经由SpringMVC帮助我们完成了。

4. **配置视图解析器和控制器**
5. **RequestMapping****注解**
    - value：指定路径还可以进行模式匹配
    - method：请求方法的类型，是RequestMethod中的枚举,其实可以@XXXMapping实现等价效果
    - params：指定请求必须带哪些参数，是一个数组。甚至可以在参数前加!表示不允许带这个参数
    - header：请求头参数，跟params用法一样
    - consumes：指定处理请求的提交内容类型（Content-Type）
    - produces：指定返回的内容类型，仅当request中（Accept）包含该指定类型才返回
    
    如果映射的多个前缀相同，可以加在类上作为前缀，如  
    @Controller  
    public class TestController {  
    @ResponseBody  
    @RequestMapping("/test/a")  
    String testA() {  
    return "a";  
    }  
    @ResponseBody  
    @RequestMapping("/test/b")  
    String testB() {  
    return "b";  
    }  
    }  
    可转变为  
    @Controller  
    @RequestMapping("/test")  
    public class TestController {  
    @ResponseBody  
    @RequestMapping("/a")  
    String testA() {  
    return "a";  
    }  
    @ResponseBody  
    @RequestMapping("/b")  
    String testB() {  
    return "b";  
    }  
    }
    

![Exported image](Exported%20image%2020260731092351-0.png)

这里使用Thymeleaf为我们提供的视图解析器，直接maven导入thymeleaf-spring6  
配置视图解析器也很简单，只要将对应的ViewResolver注册为Bean即可  
// 需要用ThymeleafViewResolver作为视图解析器，并解析html页面  
@Bean  
public ThymeleafViewResolver thymeleafViewResolver(SpringTemplateEngine engine) {  
ThymeleafViewResolver resolver = new ThymeleafViewResolver();  
resolver.setOrder(1); // 可以存在多个视图解析器，并且可以为他们设定解析程序  
resolver.setCharacterEncoding("UTF-8");  
resolver.setTemplateEngine(engine); // 设置模版引擎  
return resolver;  
}  
// 配置模版解析器  
@Bean  
public SpringResourceTemplateResolver templateResolver() {  
SpringResourceTemplateResolver resolver = new SpringResourceTemplateResolver();  
resolver.setSuffix(".html"); // 需要解析的后缀名称  
resolver.setPrefix("/"); // 需要解析的HTML页面文件存放位置，默认是webapp下，如果是类路径需要加classpath:前缀  
return resolver;  
}  
// 配置模版引擎Bean  
@Bean  
public SpringTemplateEngine SpringTemplateEngine(ITemplateResolver resolver) {  
SpringTemplateEngine engine = new SpringTemplateEngine();  
engine.setTemplateResolver(resolver); // 模版解析器，默认即可  
return engine;  
}  
然后就可以在Controller里使用ModelAndView了  
@RequestMapping("/")  
ModelAndView hello() {  
return new ModelAndView("index"); // 这里写视图名称，返回后会经过视图解析器处理  
}  
由前面的配置可知，这里映射的是web目录下的index.html  
为了使用css js等静态资源，让静态资源通过Tomcat默认的Servelet进行解析，需要让Web配置类实现WebMvcConfiguration接口，会根据重写的方法进一步配置  
@Override  
public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {  
configurer.enable(); // 开启默认的Servlet  
}
 
@Override  
public void addResourceHandlers(ResourceHandlerRegistry registry) {  
// 配置静态资访问路径  
registry.addResourceHandler("/static/**").addResourceLocations("/static/");  
}  
?： 表示任意一个字符  
*：表示任意0~n个字符  
**：表示当前目录的多级目录  
**@RequestParam与@RequestHeader**  
@RequestParam 用于修饰参数列表，用于请求参数到方法参数的映射  
其实不加这个也会默认传到方法参数列表里，加了相当于强制要求  
required - 可以指定该参数是否必须  
defaultValue - 设定默认值，当请求参数缺失时  
如果要用Servlet原本的一些类，可以直接在参数列表写HttpServletRquest，甚至还有HttpServletRespone和HttpSession  
还可以在参数列表使用实体类来封装  
@RequestHeader 用法和上面的一样，不再阐述  
**@CookieValue****和****SessionAttrbutie**  
都是只能修饰参数列表，来快速拿到东西，用法和上面差不多  
**重定向与请求转发**  
重定向只要返回的视图名前加上 redirect:即可  
请求转发只要返回的视图名前加上 forward:即可  
**Bean****的****Web****作用域**  
包含以下作用域：

- request：对于每个请求，使用request作用域定义deBean都产生一个新的实例，请求结束后Bean消失
- session：对于每个会话，使用session作用域定义deBean都产生一个新的实例，请求结束后Bean消失
- global session：不常用，不做阐述

可以在使用@Bean的地方打上@XXXScope来指定BEan的生命周期  
文件的上传与下载