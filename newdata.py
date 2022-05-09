import pika, json, sys

def callback(ch, method, properties, body):
    pull = json.loads(body)
    print(pull)
    if pull.get('purpose') == 'reg':
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        message= {'purpose': 'reg', 'query':sql, 'values':(pull['username'], pull['password'], pull['Email'])}
        print('sending registeration to database')
        push = json.dumps(message) 
        print(message)
        channel.basic_publish(exchange='', routing_key='database' , body=push)
    
    if pull.get('purpose') == 'login':
        #Select into table
        #SELECT * FROM user WHERE username=%s and pass=%s
        sql = "SELECT * FROM users WHERE username =%s AND password =%s"
        message= {'purpose': 'login', 'query':sql, 'values':(pull['username'], pull['password'])}
        push = json.dumps(message)
        channel.basic_publish(exchange='', routing_key='database' , body=push)
        print('pushing login to database')


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.8.254.80', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='front')
channel.queue_declare(queue='database')
channel.queue_declare(queue='backend')
channel.basic_consume(queue='backend', on_message_callback=callback, auto_ack=True)
print('Waiting for Information')
channel.start_consuming()