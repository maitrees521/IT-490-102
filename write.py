import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='25.8.254.80'))
channel = connection.channel()

channel.queue_declare(queue='test')

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)

channel.basic_consume(queue ='', on_message_callback=callback, auto_ack=True)
print(" [x] Sent 'Hello World!'")
connection.close
