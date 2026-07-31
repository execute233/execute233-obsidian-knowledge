![[_assets/SpringBoot-Log/SpringBoot-Log__09-24-09-0.png]]

所以，SpringBoot为了统一日志框架的使用，做了这些事情：

- 直接将其他依赖以前的日志框架剔除
- 导入对应日志框架的SIf4j中间包
- 导入自己官方指定的日志实现，并作为Slf4j的日志实现层

打印项目日志信息
SpringBoot使用的是Sif4j作为日志门面，Logback作为日志现，对应的依赖为：
spring-boot-starter-logging // 此依赖项已经被包含了
然后就可以LoggerFactory.getLogger()了，也可以lombok
配置logback日志
SpringBoot推荐其配置文件名称命名为logback-spring.xml，可以使用高级Profile功能
我们可使用默认配置的文件中已有的东西自己配置，如
<?xml version="1.0" encoding="utf-8" ?>
<!-- 该标签会覆盖spring的默认配置 -->
<configuration>
<include resource="org/springframework/boot/logging/logback/defaults.xml"/>
<!-- ch.qos.logback.core.ConsoleAppender 是专用于控制台的Appender -->
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
<encoder>
<pattern>${CONSOLE_LOG_PATTERN}</pattern>
<pattern>${CONSOLE_LOG_CHARSET}</pattern>
</encoder>
</appender>
<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
<encoder>
<pattern>${CONSOLE_LOG_PATTERN}</pattern>
<pattern>${CONSOLE_LOG_CHARSET}</pattern>
</encoder>
<rollingPolicy class="cn.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
<!-- 日志文件输出路径，以及命名规则 -->
<fileNamePattern>logs/app-log-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
<!-- 单个日志文件大小上限 -->
<maxFileSize>10MB</maxFileSize>
<!-- 到期自动清理日志文件 -->
<cleanHistoryOnStart>true</cleanHistoryOnStart>
<!-- 保留最近30天的日志文件 -->
<maxHistory>30</maxHistory>
<!-- 总日志文件大小上限 -->
<totalSizeCap>50MB</totalSizeCap>
</rollingPolicy>
</appender>
<!-- 指定日志输出级别，和启用的Appender -->
<root level="INFO">
<appender-ref ref="CONSOLE"/>
<appender-ref ref="FILE"/>
</root>
</configuration>
Logback内置的日志字段还是比较少，可以使用其MDC机制获取日志打印上下文
这个在org.sl4f.MDC中，需要自定义丢key-value（基于ThreadLocal），然后在配置文件中写%X{key}占位符
自定义Banner
在resource文件夹下使用banner.txt即可自定义，替换掉SpringBoot原来的Banner
可以在里面使用颜色，比如：
${AnsiColor}设置后面输出颜色，当然也是spring占位