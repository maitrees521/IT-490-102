import pika, sys, os
def main():
	connection = pika.BlockingConnection()
	channel = connection.channel()
	channel.queue_declare(queue='test')

	def callback(ch, method, properties, body):
		print('read')
	channel.basic_consume(queue='test' , on_message_callback=callback, auto_ack=True)
	print('testing')
	channel.start_consuming()

if__name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('stop')
	try:
		sys.exit(0)
	except SystemExit:
		os._exit(0)
