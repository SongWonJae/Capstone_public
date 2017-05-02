import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
door_speed = 20

class Door :
	def __init__(self, doorOpen, doorClose, pinControl):

		self.doorOpen = doorOpen
		self.doorClose = doorClose
		self.pinControl = pinControl
		GPIO.setup(self.doorOpen,GPIO.OUT)
		GPIO.setup(self.doorClose,GPIO.OUT)
		GPIO.setup(self.pinControl,GPIO.OUT)
		self.pwm_forward = GPIO.PWM(self.doorOpen, 100)
		self.pwm_backward = GPIO.PWM(self.doorClose, 100)
		self.pwm_forward.start(0)
		self.pwm_backward.start(0)
		GPIO.output(self.pinControl, GPIO.HIGH)

	def forward(self,speed):

		self.pwm_backward.ChangeDutyCycle(0)
		self.pwm_forward.ChangeDutyCycle(speed)

	def backward(self,speed):

		self.pwm_forward.ChangeDutyCycle(0)
		self.pwm_backward.ChangeDutyCycle(speed)

	def stop(self):

		self.pwm_forward.ChangeDutyCycle(0)
		self.pwm_backward.ChangeDutyCycle(0)

door = Door(16,18,22)
LED1A = 26

confirm_M = 0
confirm_L = 0

GPIO.setup(LED1A,GPIO.OUT)

def on_connect(client, userdata, flags, rc):
	print('connected with result code '+str(rc))
	client.subscribe(in_topic)

def on_message(client, userdata, msg):
	global confirm_M
	global confirm_L

	#print(msg.payload)
	value = str(msg.payload.decode("utf-8"))

	if value  == '0':
		if confirm_M == 0:
			confirm_M = 1
			door.forward(door_speed)
			print('Action 1 detected')
			print('turn on the motor\n')
		elif confirm_M == 1:
			confirm_M = 0
			door.backward(door_speed)
			print('Action 1 detected again')
			print('turn off the motor\n')
	elif value == '1':
		if confirm_L == 0:
			confirm_L = 1
			GPIO.output(LED1A, GPIO.HIGH)
			print('Action 2 detected')
			print('turn on the Light\n')
		elif confirm_L == 1:
			confirm_L = 0
			GPIO.output(LED1A, GPIO.LOW)
			print('Action 2 detected again')
			print('turn off the Light\n')
	elif value == '2':
		
		print('Action 3 detected\n')
	elif value == '3':

		print('Action 4 detected\n')
	else:
		print('undefined Action detected.')
		print('Do nothing\n')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

in_topic = 'abc'
out_topic = 'abc'

client.connect("52.78.240.59",1883,60)

client.loop_forever()
