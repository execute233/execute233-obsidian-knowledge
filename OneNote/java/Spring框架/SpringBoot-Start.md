**常用模块快速整合**  
导入SpringBoot直接写  
\<dependency\>  
\<groupId\>org.springframework.boot\</groupId\>  
\<artifactId\>spring-boot-starter\</artifactId\>  
\<version\>3.5.7\</version\>  
\</dependency\>  
所有的Spring依赖都是以starter的形式命名的，类似于spring-boot-starter-xxx  
比如一些常见的：  
web：内置Tomcat的SpringMVC模块  
包含starter，json，tomcat，spring-web，spring-webmvc  
要注意的是：  
不需要手动添加包扫描，会自动扫描  
Controller返回的对象可以直接变为JSON文本返回（需要Resful风格）  
可以添加下面这些依赖：  
spring-boot-starter-security  
mybatis-spring-boot-start (注意还是得要数据库相关依赖,配置数据源)  
**自定义运行器**  
只需要实现ApplicationRunner并注册为Bean即可，在SpringBoot启动完后自动调用其中的run  
也可以使用CommandLineRunner，支持@Oreder或实现Ordered接口设置优先级  
配置文件  
在resource文件夹中的application.properties(或者application.yml)  
打包运行

- 导出jar包：
- 导出war包：

maven package  
\<dependency\>  
\<groupId\>org.springframework.boot\</groupId\>  
\<artifactId\>spring-boot-starter-web\</artifactId\>  
\<!-- 排除内嵌tomcat --\>  
\<exclusions\>  
\<exclusion\>  
\<groupId\>org.springframework.boot\</groupId\>  
\<artifactId\>spring-boot-starter-tomcat\</artifactId\>  
\</exclusion\>  
\</exclusions\>  
\</dependency\>  
\<!-- 添加Servlet依赖 --\>  
\<dependency\>  
\<groupId\>jakarta.servlet\</groupId\>  
\<artifactId\>jakarta.servlet-api\</artifactId\>  
\<scope\>provided\</scope\>  
\</dependency\>  
记得在\<project\>里设置\<packaging\>为war包  
运行主类继承SpringBootServletInitializer，实现方法返回参数调用builder使用主类class