import pika

connection = pika.BlockingConnection()
channel = connection.channel()

channel.queue_declare(queue='test')
channel.basic_public(exchange='', routing='test', body='testing')
print('writing to queue')
connection.close
