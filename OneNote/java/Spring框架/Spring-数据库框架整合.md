1. **整合****Mybatis****框架**：将数据源交给IoC容器管理
2. HikariCP连接池
3. MyBatis事务管理
4. Spring事务管理
5. JUnit整合

首先导入mybatis-spring, ver:3.0.5, spring-jdbc
然后在Spring配置类sqlSessionTemple()方法打@Bean,一般是
SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(Resources._getResourceAsReader_("mybatis-config.xml"));
return new SqlSessionTemplate(sqlSessionFactory);
或者自己单独创建DataSource(方便后续更换)，然后返回SqlSessionFactoryBean,如
@Bean
public DataSource dataSource() {
return new PooledDataSource(…);
}
@Bean
public SqlSessionTemplate sqlSessionTemplate(DataSource source) throws Exception {
SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
bean.setDataSource(source);
return new SqlSessionTemplate(bean.getObject());
}
后面就可以getBean(SqlSessionTemple)
POM导入HikariCP, ver:5.01, gropuId: com.zoxxer
将前面的dataSource换为HikariDataSource即可

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-23-0.png]]

来看看存在的问题：
读未提交：最后事务B出现问题发生回滚，但这时事务A获取的是未更新的数据（毫无意义的数据），即是脏读

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-25-1.png]]

读已提交：如果事件B修改并提交了数据，那么实际上事务A之前读取到的数据依然不是最新的数据，直接导致两次读取的数据不一致，这种现象称为**虚读**或**不可重复读**

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-27-2.png]]

可重复读（MySQL默认）：这里仅仅是禁止了事务执行过程中的UPDATE操作，但是它并没有禁止INSERT这类操作，因此，如果事务A执行过程中事务B插入了新的数据，那么A这时是毫不知情的，这就是**幻读**比如：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-32-3.png]]

总结就是：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-34-4.png]]

\<environment\>下的\<transaction\>即是管理事务,分为两种：
JDBC：使用JDBC的事务管理机制：即利用对应数据库的驱动生成的Connection对象完成事务操作
MANAGED：让程序容器来实现对事务的管理
在配置类打上@EnableTransactionManagement启用
写上
@Bean
pubilc TransactionManager transactionManager(DataSource dataSource) {
return new DataSourceTransactionManager(dataSource)
}
便可以使用了

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-36-5.png]]

详细看下@Transactional

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-37-6.png]]

如果这个事务方法调用了另一个事务方法，此时事务传播规则生效
事务的传播规则如下：

![[_assets/Spring-数据库框架整合/Spring-数据库框架整合__09-23-39-7.png]]

Spring提供了Test模块，会自动集成JUnit进行测试，导入：
\<dependency\>
\<groupId\>org.junit.jupiter\</groupId\>
\<artifactId\>junit-jupiter\</artifactId\>
\<version\>5.9.0\</version\>
\<scope\>test\</scope\>
\</dependency\>
\<dependency\>
\<groupId\>org.springframework\</groupId\>
\<artifactId\>spring-test\</artifactId\>
\<version\>6.2.11\</version\>
\</dependency\>
然后测试类打上
@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = 配置类)
然后这个类就可以直接@Test运行，使用自动装配