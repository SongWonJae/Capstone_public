import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2E = 32
LED1A = 26
LED1B = 24

confirm_M1 = 0
confirm_M2 = 0
confirm_L1 = 0
confirm_L2 = 0

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(LED1A,GPIO.OUT)
GPIO.setup(LED1B,GPIO.OUT)

Door = GPIO.PWM(Motor2E, 50)
Door.start(2.5)

def on_connect(client, userdata, flags, rc):
	print('connected with result code '+str(rc))
	client.subscribe(in_topic)

def on_message(client, userdata, msg):
	global confirm_M1
	global confirm_M2
	global confirm_L1
	global confirm_L2

	print(msg.payload)
	value = str(msg.payload.decode("utf-8"))
	if value  == '1':
		if confirm_L1 == 0:
			confirm_L1 = 1
			GPIO.output(LED1A, GPIO.HIGH)
			print('Action 1 detected')
			print('turn on the white LED\n')			
		elif confirm_L1 == 1:
			confirm_L1 = 0
			GPIO.output(LED1A, GPIO.LOW)
			print('Action1 detected again')
			print('turn off the white LED\n')
	elif value == '3':
		if confirm_M1 == 0:
			confirm_M1 = 1
			GPIO.output(Motor1A,GPIO.HIGH)
			GPIO.output(Motor1B,GPIO.LOW)
			GPIO.output(Motor1E,GPIO.HIGH)
			print('Action3 detected')
			print('turn on the Fan\n')
		elif confirm_M1 == 1:
			confirm_M1 = 0
			GPIO.output(Motor1E,GPIO.LOW)
			print('Action3 detected again')
			print('turn off the Fan\n')
	elif value == '5':
		if confirm_M2 == 0:
			confirm_M2 = 1
			Door.ChangeDutyCycle(6.5)
			print('Action4 detected')
			print('open the Door')
		elif confirm_M2 == 1:
			confirm_M2 = 0
			Door.ChangeDutyCycle(2.5)
			print('Action4 detected again')
			print('close the Door')
	elif value == '4':
		print('Action5 detected')
		print('This is no Action')
		print('Do Nothing')
	elif value == '2':
		if confirm_L2 == 0:
			confirm_L2 = 1
			GPIO.output(LED1B, GPIO.HIGH)
			print('Action 5 detected')
			print('turn on the yellow LED')
		elif confirm_L2 == 1:
			confirm_L2 = 0
			GPIO.output(LED1B, GPIO.LOW)
			print('Action 5 detected again')
			print('turn off the yellow LED')
	else :
			print('Action detecting failed')
			print('Please do again')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

in_topic = 'abc'
out_topic = 'abc'

client.connect("52.78.240.59",1883,60)

client.loop_forever()
