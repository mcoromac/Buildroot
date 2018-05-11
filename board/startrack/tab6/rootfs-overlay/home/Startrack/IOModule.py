import spidev
import time
spi = spidev.SpiDev()
spi.open(32766,0)
CMD_DUMMY = [0x00,0x00,0x00,0x00,0x00,0x00]
CMD_ON = [0x70,0x01,0x01]
CMD_READ = [0x00,0x00,0x00]
CMD_OFF = [0x70,0x01,0x00]

#ALl this values comes from the IOModule with the 10k resistor modifications
ACC_ON1 = [[0x81],[0x02],[0x00]]
ACC_ON2 = [0x81,0x04,0x00]
ACC_ON3 = [0x81,0x08,0x00]
ACC_ON4 = [0x81,0x10,0x00]
ACC_ON5 = [0x81,0x32,0x00]

#Always returns 0, no way of knowing the real state of this pin
ACC_ON6 = [0x81,0x00,0x00] 

ACC_OFF = [[0x81],[0x00],[0x00]]

spi.max_speed_hz=227451
spi.mode=0b00
spi.bits_per_word=8

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

Reset = 22
CS = 21
export_pins(85)
export_pins(86)
setpindirection(Reset, "out")
setpindirection(CS, "out")
writepins(Reset,0)
writepins(CS,1)
time.sleep(0.1)
writepins(Reset,1)
time.sleep(0.1)
while True:
	RESPONSE = [0,0,0]
	operacion = raw_input("Ingrese la operacion: ")
	if operacion == "ON":
		while RESPONSE != ACC_ON1:
			writepins(CS,0);
			time.sleep(0.1)
			RESPONSE[0] = spi.xfer2([CMD_ON[0]],227451,1000,8)
			time.sleep(0.1)
			RESPONSE[1] = spi.xfer2([CMD_ON[1]],227451,1000,8)
			time.sleep(0.1)
			RESPONSE[2] = spi.xfer2([CMD_ON[2]],227451,1000,8)
			time.sleep(0.1)
			writepins(CS,1)
			time.sleep(0.1)
			print "Response[0]: " + str(RESPONSE[0])
			print "Response[1]: " + str(RESPONSE[1])
			print "Response[2]: " + str(RESPONSE[2])
	elif operacion == "OFF":
		while RESPONSE != ACC_OFF:
			writepins(CS,0);
			time.sleep(0.1)
			RESPONSE[0] = spi.xfer2([CMD_OFF[0]],227451,1000,8)
			time.sleep(0.1)
			RESPONSE[1] = spi.xfer2([CMD_OFF[1]],227451,1000,8)
			time.sleep(0.1)
			RESPONSE[2] = spi.xfer2([CMD_OFF[2]],227451,1000,8)
			time.sleep(0.1)
			writepins(CS,1)
			time.sleep(0.1)
			print "Response[0]: " + str(RESPONSE[0])
			print "Response[1]: " + str(RESPONSE[1])
			print "Response[2]: " + str(RESPONSE[2])
	elif operacion == "READ":
			writepins(CS,0)
			RESPONSE = spi.xfer2(CMD_READ,227451,1000,8)
			time.sleep(0.1)
			writepins(CS,1)
			time.sleep(0.1)
			print "Response[0]: " + str(RESPONSE[0])
			print "Response[1]: " + str(RESPONSE[1])
			print "Response[2]: " + str(RESPONSE[2])
	elif operacion == "EXIT":
		unexport_pins(85)
		unexport_pins(86)
		break
