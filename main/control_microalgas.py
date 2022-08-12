import io
import sys
import fcntl
import time
import copy
import string
import os
import glob
import time
from datetime import datetime
import RPi.GPIO as GPIO
from AtlasI2C import (
	 AtlasI2C
)

def str_to_time(m_str):
	return datetime.strptime(m_str, "%H:%M:%S").time()

def time_to_int(m_time):
	dt = datetime.strptime(m_time, "%H:%M:%S").time().second + m_time.minute*60 + m_time.hour*3600
	return dt.second + dt.minute*60 + dt.hour*3600

class Luz():
    self.estado = REPOSO
    self.pi_pwm = None
    self.gpio_num = 0
    self.subida_inicio = 0
    self.subida_fin = 0
    self.bajada_inicio = 0
    self.bajada_fin = 0
    self.intensidad_maxima = 100
    self.intensidad_minima = 0
    self.intensidad_actual = 0

    def __init__(self, gpio_num, subida_inicio, subida_fin, bajada_inicio, bajada_fin, intensidad_maxima, intensidad_minima, hora_actual):
        self.gpio_num = gpio_num
        self.pin_electrovalvula = pin_electrovalvula
        self.subida_inicio = time_to_int(subida_inicio)
        self.subida_fin = time_to_int(subida_fin)
        self.bajada_inicio = time_to_int(bajada_inicio)
        self.bajada_fin = time_to_int(bajada_fin)
        self.intensidad_maxima = intensidad_maxima
        self.intensidad_minima = intensidad_minima

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_num, GPIO.OUT)
        self.pi_pwm = GPIO.PWM(gpio_num, 100)
        self.pi_pwm.start(100)

		# Esto es por si al arrancar caigo en un periodo de reposo, que arranque con la intensidad correcta
		if time_to_int(str_to_time(hora_actual)) > bajada_fin or time_to_int(hora_actual) < subida_inicio: # REPOSO (intensidad_minima)
			self.intensidad_actual = intensidad_minima
            self.pi_pwm.ChangeDutyCycle(intensidad_minima)
		elif time_to_int(hora_actual) > subida_fin and time_to_int(hora_actual) < bajada_inicio: # REPOSO (intensidad maxima)
			self.intensidad_actual = intensidad_maxima
			self.pi_pwm.ChangeDutyCycle(intensidad_maxima)

		# https://stackoverflow.com/questions/15105112/compare-only-time-part-in-datetime-python
		# Este lin es para quedarme solo con las hora y los minutos de una fecha y comparar a partir de esto
		# https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds
		# Este link es para poder pasar la hora a cantidad de segundos (int) de esta forma voy a poder
		# usar en la funcion remap 2 valores enteros y no los datetime que iban a hacer un lio barbaro en el calculo

    def update(self, hora_actual):
		hora_actual = time_to_int(hora_actual)
        if hora_actual > self.bajada_fin or hora_actual < self.subida_inicio: # REPOSO (intensidad minima)
            print("LEDS EN REPOSO (minima intensidad) - PWM:", self.intensidad_actual)
        elif hora_actual > self.subida_inicio and hora_actual < self.subida_fin: # SUBIENDO
            print("LEDS SUBIENDO - PWM:", self.intensidad_actual)
            self.intensidad_actual = remap(hora_actual, self.subida_inicio, self.subida_fin, self.intensidad_minima, self.intensidad_maxima)
            self.pi_pwm.ChangeDutyCycle(self.intensidad_actual)
        elif hora_actual > self.subida_fin and hora_actual < self.bajada_inicio: # REPOSO
            print("LEDS EN REPOSO (maxima intensidad) - PWM:", self.intensidad_actual)
        elif hora_actual > self.bajada_inicio and hora_actual < self.bajada_fin: # BAJANDO
            print("LEDS BAJANDO - PWM:", self.intensidad_actual)
            self.intensidad_actual = remap(hora_actual, self.bajada_inicio, self.bajada_fin, self.intensidad_maxima, self.intensidad_minima)
            self.pi_pwm.ChangeDutyCycle(self.intensidad_actual)

# Constantes para el sensor DS18B20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Funcion utilitaria para el sensor DS18B20
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Medicion en grados Celsius de temperatura del sensor DS18B20
def read_ds18b20():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equal_pos = lines[1].find('t=')
	if equal_pos != -1:
		temp_string = lines[1][equal_pos+2:]
		temp_c = float(temp_string)/1000.0
		return temp_c

def remap(old_value, old_min, old_max, new_min, new_max):
    return (((old_value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

def print_devices(device_list, device):
    for i in device_list:
        if(i == device):
            print("--> " + i.get_device_info())
        else:
            print(" - " + i.get_device_info())

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1]
            response = device.query("name,?").split(",")[1]
        except:
            continue
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list

def mde():
    if state == READ_PH:
        print("READ_PH")
        sensor_ph.write("R")
        time.sleep(sensor_ph.long_timeout)
        print(sensor_ph.read())
        state = READ_DO
    elif state == READ_DO:
        print("READ_DO")
        sensor_do.write("R")
        time.sleep(sensor_do.long_timeout)
        print(sensor_do.read())
        state = READ_TEMP
    elif state == READ_TEMP:
        print("READ_TEMP")
        print(read_ds18b20())
        state = SET_LEDS
    elif state == SET_LEDS:
        for led in leds:
            led.update()
        state = READ_PH

def main():
    ezo_device_list = get_devices()

    device = ezo_device_list[0]
    print_devices(ezo_device_list, device)

    for dev in ezo_device_list:
        if dev.get_device_info().upper().startswith("DO"):
            sensor_do = dev
        elif dev.get_device_info().upper().startswith("PH"):
            sensor_ph = dev

    led_1 = Luz(22, "08:00", "12:00", "14:00", "18:00", 90, 10)
    led_2 = Luz(23, "08:00", "12:00", "14:00", "18:00", 90, 10)
    led_3 = Luz(24, "08:00", "12:00", "14:00", "18:00", 90, 10)
    led_4 = Luz(25, "08:00", "12:00", "14:00", "18:00", 90, 10)
    led_5 = Luz(27, "08:00", "12:00", "14:00", "18:00", 90, 10)

    leds = []
    leds.append(led_1)
    leds.append(led_2)
    leds.append(led_3)
    leds.append(led_4)
    leds.append(led_5)

    while True:
        mde()

if __name__ == '__main__':
    main()