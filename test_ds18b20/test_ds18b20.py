import os
import glob
import time
from datetime import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

fname = 'log.txt'

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equal_pos = lines[1].find('t=')
	if equal_pos != -1:
		temp_string = lines[1][equal_pos+2:]
		temp_c = float(temp_string)/1000.0
		# temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c # , temp_f

while True:
	temp_c = read_temp()
	new_line = datetime.today().strftime('%d/%m/%Y,%H:%M:%S')+',T={0:0.1f}°C\n'.format(temp_c)
	file = open(fname, 'a')
	file.write(new_line)
	print(new_line)
	time.sleep(1)
