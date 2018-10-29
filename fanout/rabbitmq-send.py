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