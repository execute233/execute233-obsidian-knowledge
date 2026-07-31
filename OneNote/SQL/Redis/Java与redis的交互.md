Java交互
<dependency>
<groupId>redis.clients</groupId>
<artifactId>jedis</artifactId>
<version>7.1.0</version>
</dependency>
代码如下
// 创建Jedis对象
Jedis jedis = new Jedis("localhost", 6379);
// 创建之后就可以通过同名方法来执行redis命令
jedis.set("a", "2222"); // set a 2222
jedis.hset("test", "key", "value"); // hset test key value
jedis.lpush("mylist", "1", "2", "3"); // lpush mylist 1 2 3
// lrange mylist 0 -1
jedis.lrange("mylist", 0, -1).forEach(System._out_::println);
// 使用后关闭连接
jedis.close();
SpringBoot交互
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
默认配置使用本地redis，0号数据库，可配置：
spring:
data:
redis:
host: localhost
port: 6379
database: 0
提供了一下Bean可使用：
@AutoConfiguration
@ConditionalOnClass({RedisOperations.class})
@EnableConfigurationProperties({RedisProperties.class})
@Import({LettuceConnectionConfiguration.class, JedisConnectionConfiguration.class})
public class RedisAutoConfiguration {
@Bean
@ConditionalOnMissingBean({RedisConnectionDetails.class})
PropertiesRedisConnectionDetails redisConnectionDetails(RedisProperties properties, ObjectProvider<SslBundles> sslBundles) {
return new PropertiesRedisConnectionDetails(properties, (SslBundles)sslBundles.getIfAvailable());
}

@Bean
@ConditionalOnMissingBean(
name = {"redisTemplate"}
)
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
可通过opsFor…获取对应类型(String List Hash…)操作
// 获取要对应进行操作的值，以StringRedisTemplate为例，操作都是String类型
// 大多情况下哎跟jedis使用一样
ValueOperations<String, String> ops = template.opsForValue();
也可以是使用RedisTemplate<Object, Object>，设置对应的json序列化器，将POJO转为JSON、存储，同时可以开始事务（需要jdbc），如下：
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
// 这里可以传入对象，会交给序列化器转为json
template.opsForValue().set("d", new Object());
template.exec();
}
}