#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyfprint
import os.path
import spidev
import time
from multiprocessing import Pool


def export_pins(pins):
    try:
        f = open("/sys/class/gpio/export", "w")
        f.write(str(pins))	
        f.close()
    except IOError:
        print "GPIO %s already exists, so skipping export gpio" % (str(pins), )


def set_pin_direction(pin_no, pin_direction):
    gpiopin = "PC%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/direction", "w")
    pin.write(pin_direction)
    pin.close()


def write_pins(pin_no, pin_value):
    gpiopin = "PC%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value", "w")
    if pin_value == 1:
        pin.write("1")
    else:
        pin.write("0")
    pin.close()


def read_pins(pin_no):
    gpiopin = "gpio%s" % (str(pin_no), )
    pin = open("/sys/class/gpio/"+gpiopin+"/value", "r")
    value = pin.read()
    print "The value on the PIN %s is : %s" % (str(pin_no), str(value))
    pin.close()
    return int(value)


def timer():
    time.sleep(0.02)


def write_io_module(command, pin, state_verifier):
    while True:
        io_response = []
        write_pins(slave_select, 0)
        for n in command:
            timer()
            r = spi.xfer2([n])
            io_response.append(r[0])
        write_pins(slave_select, 1)
        if not(((io_response[1] >> pin) & 1) ^ state_verifier):
            break


def read_io_module():
    io_response = []
    read_io_pins = [0x00, 0x00]
    write_pins(slave_select, 0)
    for n in read_io_pins:
        timer()
        r = spi.xfer2([n])
        io_response.append(r[0])

    write_pins(slave_select, 1)
    return io_response


def reset_io_module():
    write_pins(reset, 0)
    timer()
    write_pins(reset, 1)
    timer()


def spi_setup():
    spi.max_speed_hz = 300000
    spi.mode = 0b00
    spi.bits_per_word = 8
    export_pins(85)
    export_pins(86)
    set_pin_direction(reset, "out")
    set_pin_direction(slave_select, "out")
    reset_io_module()
    write_pins(slave_select, 1)
    timer()


def flashing_leds():
    print "unplugged"


def acccept():
    print "accept"


def deny():
    print "deny"


def load_fprints():
    file_flag = True
    txt_files = 1
    fingerprints = []
    while file_flag:
        try:
            with open("fingerprints/" + str(txt_files) + ".txt", "r") as myfile:
                data = myfile.read().replace('\n', '')
                fingerprints.append(pyfprint.Fprint(data))
            txt_files += 1
        except IOError:
            file_flag = False
            break
    print "Fprints size:" + str(len(fingerprints))
    return fingerprints


def leds_set(index_io, ports):
    for led in range(len(ports)):
        if ports[led]:
            led0_on = [0x70, led + index_io, 0x01]
            write_io_module(led0_on, led + index_io, 1)
        else:
            led0_off = [0x70, led + index_io, 0x00]
            write_io_module(led0_off, led + index_io, 0)


def makedir():
    if not os.path.exists("fingerprints"):
        os.makedirs("fingerprints")


def init():
    global device_opened, dev
    pyfprint.fp_init()
    devices = pyfprint.discover_devices()
    dev = devices[0]
    dev.open()
    device_opened = True
    return [device_opened, dev]


def add_fingerprint():
    cont = 0
    exist_flag = True
    fn = "fingerprints/1.txt"
    while exist_flag:
        cont += 1
        fn = "fingerprints/" + str(cont) + ".txt"
        exist_flag = os.path.isfile(fn)

    fp, img = dev.enroll_finger()
    print "Enrollment finished"
    f = open(fn, "w+")
    f.write(fp.data())
    print "Writing file /fingerprints/" + str(cont) + ".txt"


spi = spidev.SpiDev()
spi_id = 32766
spi.open(spi_id, 0)
reset = 22
slave_select = 21
spi_setup()

makedir()
device_opened = False
print "Start"
while True:
    try:
        if not device_opened:
            device_opened, dev = init()
    except IndexError:
        print "Plug a supported device"
        time.sleep(3)
    if device_opened:
        response = read_io_module()
        button_pressed = response[1] & 0x02
        if button_pressed:
            print "Enroll finger"
            leds_set(2, [1, 1])
            add_fingerprint()
            leds_set(2, [0, 0])
        else:
            fprints = load_fprints()
            result = dev.identify_finger(fprints)
            if result[0]:
                print "True"
                leds_set(2, [0, 1])
                time.sleep(3)
                leds_set(2, [0, 0])
            else:
                print "False"
                leds_set(2, [1, 0])
                time.sleep(3)
                leds_set(2, [0, 0])
# dev.close()
# pyfprint.fp_exit()
