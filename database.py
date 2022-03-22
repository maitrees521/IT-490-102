import pika, json, sys
import mysql.connector as mysql

#mydb = mysql.connector.connect(
 #   host = '25.2.14.158',
  #  user = 'erik',
   # password = '1234',
    #database = 'test'
#)
HOST = "25.2.14.158" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "users"
# this is the user you create
USER = "erik"
# user password
PASSWORD = "1234"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())

def callback(ch, method, properties, body):
    pull = json.loads(body)
    print(pull)
    if pull.get('purpose') == 'reg':
        mycursor = db_connection.cursor()
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        val = pull.get('values')
        mycursor.execute(sql, val)
        db_connection.commit()
        #insert into table
        #INSERT INTO user (username, password, email) VALUES (%s, %s, %s)
        print('register new user')
    
    
    if pull.get('purpose') == 'login':
        #Select into table
        #SELECT * FROM user WHERE username=%s and pass=%s
        print('Logining in user')
        mycursor = db_connection.cursor()
        sql = 'SELECT * FROM users WHERE username=' + pull['username'] + " AND password=" + pull['password']
        try:
            mycursor.execute(sql)
            myresults = mycursor.fetchall()
        except:
            print('Not there')
            message= "unsucessful"
            push = json.dumps(message)
            channel.basic_publish(exchange='', routing_key='bye' , body=push)
       #Select into table
       #SELECT * FROM user WHERE username=%s and pass=%s
        print('Logining in user')


credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.8.254.80', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.queue_declare(queue='bye')
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
print('Waiting for Information')
channel.start_consuming()
