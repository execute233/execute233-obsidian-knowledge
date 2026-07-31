# SpringBoot-接口规则校验

导入依赖
spring-boot-starter-validation
使用
@Validated打在Controller上启用验证，我们可以使用以下注解来对参数校验

|   |   |   |
|---|---|---|
|验证注解|验证的数据类型|说明|
|@AssertFalse|boolean/装箱|值必须是false|
|@AssertTrue|boolean/装箱|值必须是true|
|@NotNull|Any|不能是null|
|@Null|Any|必须是null|
|@Min|Number或CharSequence|大于等于指定值|
|@Max|Number或CharSequence|小于等于指定值|
|@DecimalMax/Min|同上|同上(高精度)|
|@Size|字符串,Collectiopn,Map,数组|长度在指定区间内|
|@Past|Date,Calender|值比当前时间早|
|@Future|同上|值比当前时间晚|
|@NotBlank|CharSequence|值不为空，比较时会去除字符串的首位空格|
|@Length|CharSequence|长度在指定区间内|
|@NotEmpty|CharSequence,Collection,Map,数组|值不为null且长度不为空|
|@Range|BigDecimal,BigInteger,CharSequence等数值|值在指定区间内|
|@Email|CharSequence|值必须是邮件格式|
|@Pattern|CharSequence|必须匹配正则表达式|
|@Valid|非原子类型|验证对象属性|

对于异常不是很友好，可以单独使用@ControllerAdvice打上类，给方法打@ExceptionHandler(要处理的Controller.class)即可，方法参数是Exception
如果方法传入的参数是自定义对象需要验证，可以给参数打@Valid，在自定义对象的类中的属性打注解即可