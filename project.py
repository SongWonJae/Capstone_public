import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22
LED1A = 26

confirm_M = 0;
confirm_L = 0;

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(LED1A,GPIO.OUT)

def on_connect(client, userdata, flags, rc):
	print('connected with result code '+str(rc))
	client.subscribe(in_topic)

def on_message(client, userdata, msg):
	print(msg.payload)
	value = str(msg.payload.decode("utf-8"))
	if value  == '0':
		GPIO.output(Motor1A,GPIO.HIGH)
		GPIO.output(Motor1B,GPIO.LOW)
		GPIO.output(Motor1E,GPIO.HIGH)
		print('this is turn on the motor')
	elif value == '1':
		GPIO.output(Motor1E,GPIO.LOW)
		print('this is turn off the motor')
	elif value == '2':
		GPIO.output(LED1A,GPIO.HIGH)
		print('this is turn on the LED')
	elif value == '3':
		GPIO.output(LED1A,GPIO.LOW)
		print('this is turn off the LED')
	else:
		GPIO.output(Motor1E,GPIO.LOW)
		print('this is else')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

in_topic = 'abc'
out_topic = 'abc'

client.connect("52.78.240.59",1883,60)

client.loop_forever()
