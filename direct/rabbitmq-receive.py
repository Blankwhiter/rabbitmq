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