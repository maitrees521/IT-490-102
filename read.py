import pika, sys, os

def main():
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='test')

	def callback(ch, method, properties, body):
		print(" [x] Received %r" % body)
	channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
	def test(self):
		pass
	
	BlockingChannel.test = test

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('stop')
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)
