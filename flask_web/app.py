import pika, sys, os 
import json
from flask_rabmq import RabbitMQ
from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

global PassFail
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('25.8.254.80', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
	pull = json.loads(body)
	if pull.get('purpose') == 'results': #Recieve Login information
		PassFail = 1


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	try:
		NPass = str(request.form['password'])
		Nuser = str(request.form['username'])
		NEmail = str(request.form['Email'])
		message = {
			"purpose": "login",
			"username": Nuser,
			"password": NPass,
			"Email": NEmail
		}
		push = json.dumps(message)
		print(push)
		print('trying to reg')
		channel.basic_publish(exchange='', routing_key='hello', body=push)
		return render_template('landing.html')
	except KeyError:
		return render_template('register.html', message='')

#THIS IS GETTING THE REGISTRATION FROM THE USER AND SENDING IT TO BE PUSHED TO RABBIT
#BACKEND WILL TAKE THIS AND SEND IT TO DATABASE
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	try:
		Pass = str(request.form['password'])
		user = str(request.form['username'])
		message = {
			"purpose": "login",
			"username": user,
			"password": Pass
		}
		push = json.dumps(message)
		print(push)
		print('trying to login')
		channel.basic_publish(exchange='', routing_key='hello', body=push)
		return render_template('landing.html')
	except KeyError:
		return render_template('login.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

