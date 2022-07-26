import RPi.GPIO as GPIO
from time import sleep

ledpin = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledpin, GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin, 100)
pi_pwm.start(100)

while True:
	for i in range(100,-1,-1):
		pi_pwm.ChangeDutyCycle(100-i)
		sleep(0.02)
	print('Ciclo completo')
