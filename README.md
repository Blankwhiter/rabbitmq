代码地址：https://github.com/Blankwhiter/rabbitmq

# 一、搭建rabbitmq环境
请参考《springboot简易集成rabbitmq》 的第一步 https://blog.csdn.net/belonghuang157405/article/details/83504207

# 二、python集成rabbitmq
首先python需要安装 **pika** 模块。请读者自行安装。

- 1.**direct**模式 收发消息

发送者 **rabbitmq-send.py**
```python
import pika
#认证 设置账号密码
credentials = pika.PlainCredentials('guest','guest')
#创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.9.219',5672,'/',credentials))
#建立信道
channel = connection.channel()

channel.exchange_declare(exchange='exchange-python-direct',
                         exchange_type='direct')
# 声明queue
#创建一个新队列balance，设置durable=True 队列持久化，注意不要跟已存在的队列重名，否则有报错
channel.queue_declare(queue='direct-queue', durable=True)

#绑定队列与交换器
channel.queue_bind(exchange="exchange-python-direct", queue="direct-queue", routing_key="apple")

#发送消息
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='exchange-python-direct',
                      routing_key='apple',
                      body='exchange-python-direct : apple : Hello World !',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # 使消息或任务也持久化存储
                          ))
print(" [x] Sent 'Hello World!'")
connection.close()
```
接收者 **rabbitmq-receive.py**
```python
import pika
#认证 设置账号密码
credentials = pika.PlainCredentials('guest','guest')
#创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.9.219',5672,'/',credentials))
#建立信道
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
#是为了防止没找到queue队列名称报错
channel.queue_declare(queue='direct-queue', durable=True)

#处理消息
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 接收消息
channel.basic_consume(callback,
                      queue='direct-queue',
                      no_ack=True) #如果接收消息，机器宕机消息就丢了

print(' [*] Waiting for messages. To exit press CTRL+C')
#开始接收
channel.start_consuming()
```


- 2.**fanout**模式 收发消息

发送者 **rabbitmq-send.py**
```python
import pika
#认证 设置账号密码
credentials = pika.PlainCredentials('guest','guest')
#创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.9.219',5672,'/',credentials))
#建立信道
channel = connection.channel()

channel.exchange_declare(exchange="exchange-python-fanout",
                         exchange_type="fanout")
#是为了防止没找到queue队列名称报错
channel.queue_declare(queue='fanout-queue-1', durable=True)
channel.queue_declare(queue='fanout-queue-2', durable=True)
channel.queue_declare(queue='fanout-queue-3', durable=True)
# 绑定队列与交换器
channel.queue_bind(exchange="exchange-python-fanout", queue="fanout-queue-1")
channel.queue_bind(exchange="exchange-python-fanout", queue="fanout-queue-2")
channel.queue_bind(exchange="exchange-python-fanout", queue="fanout-queue-3")
#发送消息
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='exchange-python-fanout',
                      routing_key='',
                      body='exchange-python : Hello World!',
                      properties=pika.BasicProperties(
                          delivery_mode=2  # 使消息或任务也持久化存储
                          ))
print(" [x] Sent 'Hello World!'")
connection.close()
```
接收者 **rabbitmq-receive.py**
```python
import pika
#认证 设置账号密码
credentials = pika.PlainCredentials('guest','guest')
#创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.9.219',5672,'/',credentials))
#建立信道
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
#是为了防止没找到queue队列名称报错
channel.queue_declare(queue='fanout-queue-1', durable=True)

#处理消息
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 接收消息
channel.basic_consume(callback,
                      queue='fanout-queue-1',
                      no_ack=True) #如果接收消息，机器宕机消息就丢了

print(' [*] Waiting for messages. To exit press CTRL+C')
#开始接收
channel.start_consuming()
```
其他模式请读者自行测试。
