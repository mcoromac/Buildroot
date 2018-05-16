#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Python 2.7.14
import pyfprint
import os.path
import spidev
import time
import signal
class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raiseTimeout.Timeout()

def export_pins(pins):
    try:
        f = open("/sys/class/gpio/export","w")
        f.write(str(pins))
        f.close()
    except IOError:
        print "GPIO %s already exists, so skipping export gpio" % (str(pins), )

def unexport_pins(pins):
    try:
        f = open("/sys/class/gpio/unexport","w")
        f.write(str(pins))
        f.close()
    except IOError:
        print "GPIO %s is not found, so skipping unexport gpio" % (str(pins), )

def setpindirection(pin_no, pin_direction):
    gpiopin = "PC%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/direction","w")
    pin.write(pin_direction)
    pin.close()

def writepins(pin_no, pin_value):
    gpiopin = "PC%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value","w")
    if pin_value == 1:
      pin.write("1")
    else:
      pin.write("0")
    pin.close()

def readpins(pin_no):
    gpiopin = "gpio%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value","r")
    value = pin.read()
    print "The value on the PIN %s is : %s" % (str(pin_no), str(value))
    pin.close()
    return int(value)
def timer():
	time.sleep(0.02)
def writeSpi(CMD,CS,spi):
	RESPONSE = [0]
	writepins(CS,0)
	for n in CMD:
		timer()
		RESPONSE.extend(spi.xfer2([n]))
	
	writepins(CS,1)
	return RESPONSE[1:(len(CMD)+1)]

def resetSpi(Reset):
	writepins(Reset,0)
	timer()
	writepins(Reset,1)
	timer()

def setup(CS,Reset,spi):
	spi.max_speed_hz=300000
	spi.mode=0b00
	spi.bits_per_word=8
	export_pins(85)
	export_pins(86)
	setpindirection(Reset, "out")
	setpindirection(CS, "out")
	writepins(Reset,0)
	writepins(CS,1)
	timer()
	writepins(Reset,1)
	timer()

def unplugged(CS,spi):
	print "unplugged"
def flashing(CS,spi):
	print "flashing"
def acccept(CS,spi):
	print "accept"
def deny(CS,spi):
	print "deny"
spi = spidev.SpiDev()
spi.open(32766,0)
Reset = 22
CS = 21
cont = 0
setup(CS,Reset,spi)

CMD_READ = [0x00,0x00]
#Command to turn on the IO pins
CMD_ON2 = [0x70,0x02,0x01]
CMD_ON3 = [0x70,0x03,0x01]
#This is the off command
CMD_OFF2 = [0x70,0x02,0x00]
CMD_OFF3 = [0x70,0x03,0x00]
#SPI response when IO is on.
ACC_ON2 = [0x81,0x04,0x00]
ACC_ON3 = [0x81,0x08,0x00]
#All IO offs
ACC_OFF = [0x81,0x00,0x00]
if not os.path.exists("fingerprints"):
	os.makedirs("fingerprints")
#Variable for "I opened the device already"
once = False
while True: 
	try:
		if not once:
			pyfprint.fp_init()
			devs = pyfprint.discover_devices()
			dev = devs[0]
			dev.open()
			once = True
	except IndexError:
		flag = True 
		print "Plug a supported device"
		time.sleep(3)
		#unplugged(CS,spi)
	if once: 
		#Is button pressed? -> Enroll fingerprint
		RESPONSE = writeSpi(CMD_READ,CS,spi)
		#Input is pin 1
		if RESPONSE[1] and 0x01:
			print "Enroll finger"
			#Turn on both leds
			RESPONSE = [0,0,0]
			while not ((RESPONSE[1] >> 2) and (RESPONSE[1] >> 3) and 0x01):
				writeSpi(CMD_ON2,CS,spi)
				RESPONSE = writeSpi(CMD_ON3,CS,spi)
				print "Response"
				print RESPONSE
			#Can be blocking function
			fp, img = dev.enroll_finger()

			while ((RESPONSE[1] >> 2) and (RESPONSE[1] >> 3) and 0x01):
				writeSpi(CMD_OFF2,CS,spi)
				RESPONSE = writeSpi(CMD_OFF3,CS,spi)
				print "Response"
				print RESPONSE

			exist_flag = True
			while exist_flag:
				cont+=1
				fn = "fingerprints/" + str(cont) + ".txt"
				exist_flag = os.path.isfile(fn)

			print "Enrollment finished"
			#If power is removed check if there is already fingerprints logs
			f = open(fn,"w+")
			f.write(fp.data())
			print "Writing file /fingerprints/" + str(cont) + ".txt"
		else: 
			#Variable for "I'm reading all the files"
			file_flag = True
			contf = 1
			while file_flag:
				try:
					data = ''
					with open("fingerprints/" + str(contf) + ".txt","r") as myfile:
    						data = myfile.read().replace('\n', '')
					contf+=1
				except IOError:
					file_flag = False
					break
				print "Checking /fingerprints/" + str(contf - 1) + ".txt"
				fp2 = pyfprint.Fprint(data)
				print "Verifying, finger please" 
				try:
					with Timeout(5):
						res = dev.verify_finger(fp2)
				except Timeout.Timeout:
					print "Too much data"
					break
				RESPONSE = [0,0,0]
				if res[0]:
					print res[0]
					while not ((RESPONSE[1] >> 2) and 0x01):
						RESPONSE = writeSpi(CMD_ON2,CS,spi)
						print "Response"
						print RESPONSE
					time.sleep(3)
					while ((RESPONSE[1] >> 2) and 0x01):
						RESPONSE = writeSpi(CMD_OFF2,CS,spi)
						print "Response"
						print RESPONSE
				else:
					print res[0]
					while not ((RESPONSE[1] >> 3) and 0x01):
						RESPONSE = writeSpi(CMD_ON3,CS,spi)
						print "Response"
						print RESPONSE
					time.sleep(3)
					while ((RESPONSE[1] >> 2) and 0x01):
						RESPONSE = writeSpi(CMD_OFF3,CS,spi)
						print "Response"
						print RESPONSE
dev.close()
pyfprint.fp_exit()
