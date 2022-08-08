import RPi.GPIO as GPIO
from time import sleep

ledpin = 24
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)
pi_pwm_24 = GPIO.PWM(24, 100)
pi_pwm_24.start(100)

GPIO.setup(25, GPIO.OUT)
pi_pwm_25 = GPIO.PWM(25, 100)
pi_pwm_25.start(100)

GPIO.setup(23, GPIO.OUT)
pi_pwm_23 = GPIO.PWM(23, 100)
pi_pwm_23.start(100)

GPIO.setup(22, GPIO.OUT)
pi_pwm_22 = GPIO.PWM(22, 100)
pi_pwm_22.start(100)

GPIO.setup(27, GPIO.OUT)
pi_pwm_27 = GPIO.PWM(27, 100)
pi_pwm_27.start(100)

while True:
	for i in range(100,-1,-1):
		pi_pwm_22.ChangeDutyCycle(100-i)
		pi_pwm_23.ChangeDutyCycle(100-i)
		pi_pwm_24.ChangeDutyCycle(100-i)
		pi_pwm_25.ChangeDutyCycle(100-i)
		pi_pwm_27.ChangeDutyCycle(100-i)
		sleep(0.02)
	print('Ciclo completo')
