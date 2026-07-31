实现了基于注解的缓存功能，底层可以切换不同缓存实现（EHCache, Caffeine, Redis）  
\<dependency\>  
\<groupId\>org.springframework.boot\</groupId\>  
\<artifactId\>spring-boot-starter-cache\</artifactId\>  
\</dependency\>  
配置  
spring:  
data:  
redis:  
##redis 单机环境配置  
host: 192.168.200.157  
port: 6370  
password: xxxx  
database: 0  
cache:  
type: redis  
redis:  
# 设置缓存项的过期时间（以毫秒为单位）。  
time-to-live: 3600000  
# 设置缓存键的前缀。  
key-prefix: CACHE_  
# 指定是否使用缓存键前缀。  
use-key-prefix: true  
# 指定是否缓存空值。  
cache-null-values: true  
有以下常用注解

|   |   |
|---|---|
|@EnableCaching|开启注解功能，在启动类上|
|@Cacheable|方法执行前先查询缓存是否有数据，有就用缓存否则直接调方法|
|@CachePut|将方法的返回值放到缓存中|
|@CacheEvict|将一条或多条数据从缓存删除|
|@CacheConfig|用于类级别的缓存配置，可指定默认的缓存名称，键生成器等|
 
@CachePut(cacheNames="key前缀"， key="#user.id") // 前缀::id, key是spEL表达式  
@CacheEvict 可以使用allEntries属性将cacheNames::***的所有键删除