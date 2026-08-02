---
title: Java 与 redis 的交互
tags: [SQL, Redis]
aliases: [Java与redis的交互]
---

# Java与redis的交互

## Jedis 交互

```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>7.1.0</version>
</dependency>
```

代码如下:

```java
// 创建 Jedis 对象
Jedis jedis = new Jedis("localhost", 6379);
// 创建之后就可以通过同名方法来执行 redis 命令
jedis.set("a", "2222");             // set a 2222
jedis.hset("test", "key", "value"); // hset test key value
jedis.lpush("mylist", "1", "2", "3"); // lpush mylist 1 2 3

// lrange mylist 0 -1
jedis.lrange("mylist", 0, -1).forEach(System.out::println);
// 使用后关闭连接
jedis.close();
```

## SpringBoot 交互

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

默认配置使用本地 redis,0 号数据库,可配置:

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
      database: 0
```

提供了以下 Bean 可使用:

```java
@AutoConfiguration
@ConditionalOnClass({RedisOperations.class})
@EnableConfigurationProperties({RedisProperties.class})
@Import({LettuceConnectionConfiguration.class, JedisConnectionConfiguration.class})
public class RedisAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean({RedisConnectionDetails.class})
    PropertiesRedisConnectionDetails redisConnectionDetails(RedisProperties properties, ObjectProvider<SslBundles> sslBundles) {
        return new PropertiesRedisConnectionDetails(properties, (SslBundles) sslBundles.getIfAvailable());
    }

    @Bean
    @ConditionalOnMissingBean(name = {"redisTemplate"})
    @ConditionalOnSingleCandidate(RedisConnectionFactory.class)
    public RedisTemplate<Object, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {
        RedisTemplate<Object, Object> template = new RedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnSingleCandidate(RedisConnectionFactory.class)
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory redisConnectionFactory) {
        return new StringRedisTemplate(redisConnectionFactory);
    }
}
```

可通过 `opsFor…` 获取对应类型(String / List / Hash / …)操作:

```java
// 获取要对应进行操作的值,以 StringRedisTemplate 为例,操作都是 String 类型
// 大多情况下跟 jedis 使用一样
ValueOperations<String, String> ops = template.opsForValue();
```

也可以使用 `RedisTemplate<Object, Object>`,设置对应的 JSON 序列化器,将 POJO 转为 JSON、存储,同时可以开启事务(需要 jdbc),如下:

```java
@Service
public class RedisTestService {
    @Resource
    RedisTemplate<Object, Object> template;

    @PostConstruct
    public void init() {
        template.setEnableTransactionSupport(true);
        // 可以配置序列化器
        template.setValueSerializer(new Jackson2JsonRedisSerializer<Object>(Object.class));
    }

    @Transactional
    public void test() {
        template.multi();
        // 这里可以传入对象,会交给序列化器转为 JSON
        template.opsForValue().set("d", new Object());
        template.exec();
    }
}
```