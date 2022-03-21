import pika, sys, os 
import json
from flask_rabmq import RabbitMQ
from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

global PassFail
app.config['DATABASE'] = ''
try:
	credentials = pika.PlainCredentials('admin', 'admin')
	connection = pika.BlockingConnection(pika.ConnectionParameters('25.8.254.80', 5672, '/', credentials))
	channel = connection.channel()
	channel.queue_declare(queue='hello')
except:
	print('rabbit not online')

def callback(ch, method, properties, body):
	pull = json.loads(body)
	if pull.get('purpose') == 'results': #Recieve Login information
		PassFail = 1


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('landing.html')

@app.route('/register', methods=['GET',' POST'])
def register():
	return render_template('register.html')
#THIS IS GETTING THE REGISTRATION FROM THE USER AND SENDING IT TO BE PUSHED TO RABBIT
#BACKEND WILL TAKE THIS AND SEND IT TO DATABASE

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

