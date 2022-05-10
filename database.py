
import pika, json, sys
import mysql.connector as mysql
# or "domain.com"
HOST = "localhost"

# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "users"
# this is the user you create
USER = "?"
# user password
PASSWORD = "?"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="test",
#  password="test",
#  database= "users"
#)

#This document is for putting the new user into the system and also checking for users when login in. 
def callback(ch, method, properties, body):
    pull = json.loads(body)
    print(pull)
    if pull.get('purpose') == 'reg':
        mycursor = db_connection.cursor(buffered=True)
        sql = pull.get('query')
        val = pull.get('values')
        mycursor.execute(sql, val)
        db_connection.commit()
        print('register new user')

    if pull.get('purpose') == 'login':
        mycursor = db_connection.cursor(buffered=True)
        sql = pull.get('query')
        val = pull.get('values')
        #mycursor.execute(sql,val)

       # myresult = mycursor.fetchall()
        try:
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            message= "sucessful"
        except:
            message= "unsucessful"
        push = json.dumps(message) 
        print(message)
        channel.basic_publish(exchange='', routing_key='front' , body=push)
    

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.8.254.80', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='front')
channel.queue_declare(queue='database')
channel.queue_declare(queue='backend')
channel.basic_consume(queue='database', on_message_callback=callback, auto_ack=True)
print('Waiting for Information')
channel.start_consuming()