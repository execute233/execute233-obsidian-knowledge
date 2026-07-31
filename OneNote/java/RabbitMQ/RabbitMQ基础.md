**三大功能：**  
流量削峰、应用解耦、异步处理  
**四大核心概念：**

![[RabbitMQ基础__09-21-29-0.png]]

**核心部分**

![[RabbitMQ基础__09-21-31-1.png]] ![[RabbitMQ基础__09-21-34-2.png]]

**Broker****：**接收和分发消息的应用  
**Virtual host****：**出于多租户和安全因素设计的，把AMQP的基本组件划分到一个虚拟的分组中，类似  
于网络中的namesace概念。当多个不同的用户使用同一个RabbitMserver提供的服务时，可以划分出  
多个vhost,每个用户在自己的vhost创建exchange/queue等  
**Connection****：**publisher/consumer和broker之间的TCP连接  
**Channel****：**是在connection内部建立的逻辑连接，如果应用程序支持多线程，通常每个thread创建单独的channel进行通讯，AMQP method包含了channel id帮助客户端和message broker识别channel,所以channel之间是完全隔离的。Channel作为轻量级的Connection极大减少了操作系统建立TCPconnection的开销  
**Exchange****：**message到达broker的第一站，根据分发规则，匹配查询表中的routing key，分发消息到queue中去。常用的类型有：direct(point-to-point),topic(publish-subscribe)和fanout(multicast)  
**安装**  
安装web管理插件  
rabbitmq-plugins enable rabbitmq_management  
访问15672端口即可  
初始账密都为guest  
**添加用户**  
创建账号  
rabbitmqctl add_user \<user_name\> \<password\>  
设置用户角色  
rabbitmqctl set_user_tags \<user_name\> administrator  
设置用户权限  
rabbitmqctl set_permissions [-p \<vhostpath\>] \<user\> \<conf\> \<write\> \<read\>  
比如rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*" 用户admin具有/vhost1这所有的资源配置、读、写  
查询用户和角色  
rabbitmqctl list_users  
**要注意****erlang cookie****不一致问题，一般需要**  
copy "C:\Windows\System32\config\systemprofile\.erlang.cookie" "C:\Users\\<user\>\.erlang.cookie"  
**JAVA****相关使用配置**  
添加相应的maven坐标  
\<dependency\>  
\<groupId\>com.rabbitmq\</groupId\>  
\<artifactId\>amqp-client\</artifactId\>  
\<version\>5.28.0\</version\>  
\</dependency\>