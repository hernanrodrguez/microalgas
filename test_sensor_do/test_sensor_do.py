#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)

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
       
def main():
    ezo_device_list = get_devices()        
    device = ezo_device_list[0]    
    print_devices(ezo_device_list, device)
    
    while True:
        for dev in ezo_device_list:
            dev.write("R")
        time.sleep(device.long_timeout)
        for dev in ezo_device_list:
            print(dev.read())
                    
if __name__ == '__main__':
    main()
