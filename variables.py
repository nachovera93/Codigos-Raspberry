import subprocess
import os
import json
import requests
import RPi.GPIO as GPIO
import time
from time import sleep
import signal
import psutil
import sys
import datetime
from datetime import timedelta
import socket

pin = 14 # The pin ID, edit here to change it
maxTMP = 45 # The maximum temperature in Celsius after which we trigger the fan

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    return()

def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return(ip_address)

def cpu_temp():
	thermal_zone = subprocess.Popen(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE)
	out, err = thermal_zone.communicate()
	cpu_temp = int(out.decode())/1000
	return cpu_temp


def check_temp():
	cpu = cpu_temp()
	print ("CPU: "+str(cpu)+"º")
	if(float(cpu) > 45):
	     GPIO.output(14, True)#Ventilador on
          
	elif(float(cpu) <= 40):
		 GPIO.output(14, False) #Ventilador off
         

def get_cpuload():
    cpuload = psutil.cpu_percent(interval=1, percpu=False)
    return str(cpuload)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
     uptime_seconds = float(f.readline().split()[0])
     uptime = (timedelta(seconds = uptime_seconds))
     return str(uptime)
    
def setPin(mode): # A little redundant function but useful if you want to add logging
    GPIO.output(pin, mode)
    return()

try:
    print("Direccion IP : {0}".format(get_ip_address()))
    setup()
    while True:
        check_temp()
        #print(get_cpuload())
        print("Uso cpu : {0}".format(get_cpuload())+"%")
        print("Uptime : {0}".format(get_uptime()))
        sleep(5) # Read the temperature every 5 sec, increase or decrease this limit if you want
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    GPIO.cleanup() # resets all GPIO ports used by this program
