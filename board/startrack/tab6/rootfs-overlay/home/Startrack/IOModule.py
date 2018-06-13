#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spidev
import time


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
        print "RESPONSE"
        print io_response
        if not(((io_response[1] >> pin) & 1) ^ state_verifier):
            break


def io_read():
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


def io_write(pin_offset, pin_values):
    for pin_index in range(len(pin_values)):
        if pin_values[pin_index]:
            pin_on = [0x70, pin_index + pin_offset, 0x01]
            write_io_module(pin_on, pin_index + pin_offset, 1)
        else:
            pin_off = [0x70, pin_index + pin_offset, 0x00]
            write_io_module(pin_off, pin_index + pin_offset, 0)


spi = spidev.SpiDev()
spi_id = 32766
spi.open(spi_id, 0)
reset = 22
slave_select = 21
spi_setup()

print "Start"
while True:
    pin_array = []
    operation = raw_input("Operation:")
    if operation == "ON":
        pin_array = [0, 0, 0, 0, 1, 1]
        io_write(1, pin_array)
    elif operation == "OFF":
        pin_array = [0, 0, 0, 0, 0, 0]
        io_write(1, pin_array)
    elif operation == "READ":
        print io_read()
