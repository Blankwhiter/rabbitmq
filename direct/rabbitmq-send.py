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