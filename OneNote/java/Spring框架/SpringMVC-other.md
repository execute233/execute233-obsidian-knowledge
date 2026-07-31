**RestFul**  
一种设计风格。它的主要作用是充分并正确利用HTTP协议的特性，规范资源获取的URI路径。RESTful风格的设计允许将数通过URL拼接传到服务端，目的是让URL看起来更简洁实用，  
并且我们可以充分使用多种HTTPP请求方式(POST/GET/PUT/DELETE)，来执行相同请求地址的不同类型操作。
   

我们可以直接将inde×的下一级路径作为请求参数进行处理，也就是说现在的请求参数包含在了请求路径中：  
@RequestMapping("/index/{str}")  
public String testIndex(@PathVariable String str) {  
System._out_.println(str);  
return "index";  
}  
**拦截器**  
拦截器是整个SpringMVC的一个重要内容，拦截器与过滤器类似，都是用于拦截一些非法请求，但是我们之前讲解的过滤器是作用于Serviet之前，只有经过层层的拦截器才可以成功到达Servlet，而拦截器并不是在Servlet之前，它在Servlet与RequestMapping之间，相当于DispatcherServlet在将请求交给对应Controller中的方法之前进行拦截处理，它只会拦截所有Controller中定义的请求映射对应的请求（不会拦截静态资源），这里一定要区分两者的不同。

![[SpringMVC-other__09-23-55-0.png]]  

创建拦截器  
需要实现HandlerIntercepter接口  
// 请求处理之前，只有返回true才会继续，否则直接结束  
boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler);  
// 请求处理之后  
void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView);  
// 请求完成之后,不管处理请求期间是否发生异常  
void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex);  
接着需要在配置类注册（实现WebMvcConfigurer的配置类）  
@Override  
public void addInterceptors(InterceptorRegistry registry) {  
registry.addInterceptor(new MainInterceptor())  
.addPathPatterns("/**") // 拦截器匹配路径  
.excludePathPatterns("/home"); // 拦截器不进行拦截的路径  
}  
可以添加多个拦截器，链式调用拦截器order方法设置优先级（按顺序注册则按顺序优先级），如：  
1号拦截器：处理前  
2号拦截器：处理前  
Controller处理  
2号拦截器：处理后  
1号拦截器：处理后  
2号拦截器：完成后  
1号拦截器：完成后  
**异常处理**  
我们可以专门写一个异常处理的Controller，出现指定异常可以转接到此控制器执行  
@ControllerAdvice  
public class ErrorController {  
@ExceptionHandler  
public ModelAndView handleException(Exception e, Model model) {  
model.addAttribute("e", e);  
return new ModelAndView("error");  
}  
}  
**文件上传与下载**  
需要在ServletInitializer中注册  
@Override  
protected void customizeRegistration(ServletRegistration.Dynamic registration) {  
// 直接通过registration配置Multipart，必须设置临时上传路径  
// 同时可以设置其他属性  
registration.setMultipartConfig(new MultipartConfigElement("xxx"));  
}  
然后就可以写在Controller了  
@PostMapping("/upload")  
@ResponseBody  
public String upload(@RequestParam("file") MultipartFile file) throws IOException {  
File fileObj = new File("test.txt");  
file.transferTo(fileObj);  
return "success";  
}  
下载可以直接用HttpServletRespone了  
@GetMapping("/download")  
@ResponseBody  
public void download(HttpServletResponse response) throws IOException {  
response.setContentType("multipart/form-data");  
try (OutputStream out = response.getOutputStream();  
InputStream in = Files._newInputStream_(Paths._get_("test.txt"))) {  
IOUtils._copy_(in, out);  
} catch (Exception e) {  
e.printStackTrace();  
}  
}