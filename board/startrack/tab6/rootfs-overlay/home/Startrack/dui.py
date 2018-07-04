#!/usr/bin/env python

import os
from time import time
from PIL import Image
import numpy as np
import cv2
import time
import spidev
import serial


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
    # print "The value on the PIN %s is : %s" % (str(pin_no), str(value))
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


def io_write(pin_offset, pin_values):
    for pin_index in range(len(pin_values)):
        if pin_values[pin_index]:
            pin_on = [0x70, pin_index + pin_offset, 0x01]
            write_io_module(pin_on, pin_index + pin_offset, 1)
        else:
            pin_off = [0x70, pin_index + pin_offset, 0x00]
            write_io_module(pin_off, pin_index + pin_offset, 0)


def sort_contours(x_positions, contours):
    for iter_num in range(len(x_positions) - 1, 0, -1):
        for idx in range(iter_num):
            if x_positions[idx] > x_positions[idx + 1]:
                temp = x_positions[idx]
                temp2 = contours[idx]
                x_positions[idx] = x_positions[idx + 1]
                contours[idx] = contours[idx + 1]
                x_positions[idx + 1] = temp
                contours[idx + 1] = temp2
    return contours


def load_font():
    contours_font = []
    font_image = cv2.imread("/home/Startrack/font.jpg")
    if font_image is None:
        print "Font: Image not found"
        return 0
    font_image_grayscale = cv2.cvtColor(font_image, cv2.COLOR_BGR2GRAY)

    font_image_binary = cv2.threshold(font_image_grayscale, 10, 255, cv2.THRESH_BINARY_INV)[1]

    font_contours = cv2.findContours(font_image_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    font_contours = font_contours[1]

    # draw_image_contours = cv2.drawContours(font_image.copy(), font_contours, -1, (0, 255, 0), 1)
    # cv2.imwrite("/mnt/usb4GB/draw_font_contours.jpg", draw_image_contours)

    index = 0
    for contour in font_contours:
        index = index + 1
        (x, y, w, h) = cv2.boundingRect(contour)
        letter_font = font_image[y:y + h, x:x + w]
        letter_font = cv2.resize(letter_font, (16, 25))
        contours_font.append(letter_font)
    return contours_font


def process_image(frame):
    cropped_img = frame
    x_positions = []
    gray_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    # threshold = 80, 113 on oddice in front of power supply,
    image_binary = cv2.threshold(gray_image, 113, 255, cv2.THRESH_BINARY_INV)[1]

    # cv2.imwrite("/mnt/usb4GB/image_binary.jpg", image_binary)

    image_contours = cv2.findContours(image_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_contours = image_contours[1]

    # draw_image_contours = cv2.drawContours(frame.copy(), image_contours, -1, (0, 255, 0), 1)
    # cv2.imwrite("/mnt/usb4GB/draw_image_contours.jpg", draw_image_contours)

    contours_image = []

    for index, contour in enumerate(image_contours):
        area = cv2.contourArea(contour)
        #50
        if area > 40:
            (x, y, w, h) = cv2.boundingRect(contour)
            letter_image = cropped_img[y:y + h, x:x + w]
            # cv2.imwrite("/mnt/usb4GB/Images/" + str(index) + ".jpg", letter_image)
            letter_image = cv2.resize(letter_image, (16, 25))
            x_positions.append(x)
            contours_image.append(letter_image)

    sorted_contours = sort_contours(x_positions, contours_image)

    # for (index, n) in enumerate(sorted_contours):
    #    cv2.imwrite("/mnt/usb4GB/Images/" + str(index) + ".jpg", n)

    return sorted_contours


def match_characters(dictionary, characters):
    scores = []
    code = []
    for character in characters:
        for letter in dictionary:
            result = cv2.matchTemplate(letter, character, cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)
        code.append(np.argmax(scores))
        scores = []
    return code


def print_characters(letters):
    resulting_text = ""
    font_template = [">", "<", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C",
                     "B", "A", "Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q", "P",
                     "O", "7", "6", "5", "4", "3", "1", "9", "8", "2", "0"]
    for index in letters:
        if font_template[index] == "O":
            resulting_text = resulting_text + "0"
        else:
            resulting_text = resulting_text + font_template[index]
    print text
    return resulting_text


# IDGTM = Guatemala, IDSLV = El Salvador, I<PER
def check_text(first_line_mrz):
    if first_line_mrz == "":
        return 0
    elif "IDGTM" in first_line_mrz:
        number = first_line_mrz[5:14] + first_line_mrz[15:19]
    elif "IDSLV" in first_line_mrz:
        number = first_line_mrz[5:13] + first_line_mrz[15:16]
    elif "I<PER" in first_line_mrz:
        number = first_line_mrz[5:13]
    else:
        return 0
    try:
        return int(number)
    except ValueError:
        return 2


def calibrate_focus():
    response = ""
    while response != (focus + "\n"):
        stream = os.popen("uvcdynctrl -g 'Focus'")
        response = stream.readline()
        # print "response " + response
        if response == "ERROR: Unknown control specified.\n":
            os.popen("uvcdynctrl -i /usr/share/uvcdynctrl/data/046d/logitech.xml")
        elif response == "ERROR: Unable to open device.\n":
            print "Attach a camera."
            time.sleep(1)
        elif response != (focus + "\n"):
            # print "Setting Focus to " + focus
            os.popen("uvcdynctrl -s 'Focus' " + focus)


def open_camera():
    capture = cv2.VideoCapture(0)
    while not capture.isOpened():
        capture = cv2.VideoCapture(0)
        print "Attach a camera"
        time.sleep(1)
    return capture


def camera_setup(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


def get_mrz(frame):
    # cv2.imwrite("/mnt/usb4GB/Original.jpg", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("/mnt/usb4GB/Gray.jpg", gray)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    # cv2.imwrite("/mnt/usb4GB/Blackhat.jpg", blackhat)

    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
    # cv2.imwrite("/mnt/usb4GB/Scharr.jpg", gradX)

    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, second_rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imwrite("/mnt/usb4GB/Threshold.jpg", thresh)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=1)
    # cv2.imwrite("/mnt/usb4GB/Erode.jpg", thresh)

    p = int(frame.shape[1] * 0.03)
    thresh[:, 0:p] = 0
    thresh[:, frame.shape[1] - p:] = 0

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    roi = frame
    # loop over the contours
    height, width = 0, 0
    point_x, point_y = 0, 0

    # start = time.time()
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w > width and h > height:
            height = h
            width = w
            point_x = x
            point_y = y
    roi = frame[point_y:point_y + (height - 60), point_x:point_x + width].copy()
    # cv2.imwrite("/mnt/usb4GB/MRZ.jpg", cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
    # end = time.time()

    # print "Time in for loop mrz: " + str(end - start)
    return roi


def send_dui(numero):
    VRBL = [0, 0, 0, 0, 0]
    numero_binario = bin(numero)
    numero_binario = numero_binario[2:]
    size = len(numero_binario)
    if size <= 16:
        VRBL[4] = numero_binario
        VRBL[4] = int(VRBL[4], 2)
    elif size <= 32:
        VRBL[4] = numero_binario[size - 16:size]
        VRBL[3] = numero_binario[0:size - 16]
        VRBL[4] = int(VRBL[4], 2)
        VRBL[3] = int(VRBL[3], 2)
    elif size <= 48:
        VRBL[4] = numero_binario[size - 16:size]
        VRBL[3] = numero_binario[size - 32:size - 16]
        VRBL[2] = numero_binario[0:size - 32]
        VRBL[4] = int(VRBL[4], 2)
        VRBL[3] = int(VRBL[3], 2)
        VRBL[2] = int(VRBL[2], 2)
    elif size <= 64:
        VRBL[4] = numero_binario[size - 16:size]
        VRBL[3] = numero_binario[size - 32:size - 16]
        VRBL[2] = numero_binario[size - 48:size - 32]
        VRBL[1] = numero_binario[0:size - 48]
        VRBL[4] = int(VRBL[4], 2)
        VRBL[3] = int(VRBL[3], 2)
        VRBL[2] = int(VRBL[2], 2)
        VRBL[1] = int(VRBL[1], 2)
    elif size <= 80:
        VRBL[4] = numero_binario[size - 16:size]
        VRBL[3] = numero_binario[size - 32:size - 16]
        VRBL[2] = numero_binario[size - 48:size - 32]
        VRBL[1] = numero_binario[size - 64:size - 48]
        VRBL[0] = numero_binario[0:size - 64]
        VRBL[4] = int(VRBL[4], 2)
        VRBL[3] = int(VRBL[3], 2)
        VRBL[2] = int(VRBL[2], 2)
        VRBL[1] = int(VRBL[1], 2)
        VRBL[0] = int(VRBL[0], 2)

    mensaje = 'AT$FUNC="VRBL",0,91' + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$FUNC="VRBL",5,' + str(VRBL[4]) + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$FUNC="VRBL",4,' + str(VRBL[3]) + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$FUNC="VRBL",3,' + str(VRBL[2]) + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$FUNC="VRBL",2,' + str(VRBL[1]) + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$FUNC="VRBL",1,' + str(VRBL[0]) + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    mensaje = 'AT$GPOS=2,0' + '\r\n'
    ser.write(mensaje.encode('utf-8'))
    print 'AT$FUNC="VRBL",0,91'.encode('utf-8')
    print 'AT$FUNC="VRBL",5,' + str(VRBL[4]).encode('utf-8')
    print 'AT$FUNC="VRBL",4,' + str(VRBL[3]).encode('utf-8')
    print 'AT$FUNC="VRBL",3,' + str(VRBL[2]).encode('utf-8')
    print 'AT$FUNC="VRBL",2,' + str(VRBL[1]).encode('utf-8')
    print 'AT$FUNC="VRBL",1,' + str(VRBL[0]).encode('utf-8')
    print 'AT$GPOS=2,0'.encode('utf-8')


def get_image():
    start = time.time()
    cap = open_camera()
    camera_setup(cap)
    time.sleep(0.1)
    _, frame = cap.read()
    if frame is None:
        print "No frame"
        return 1
    time.sleep(0.1)
    cap.release()
    end = time.time()
    print "Time taking image: " + str(end - start)
    return frame[300:600, 0:800]


def make_kernels():
    return cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5)), \
           cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21)), \
           cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))


ser = serial.Serial('/dev/ttyS0', 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    xonxoff=False, rtscts=False)
spi = spidev.SpiDev()
spi_id = 32766
spi.open(spi_id, 0)
reset = 22
slave_select = 21
spi_setup()
# 126 prototipo 1
# 167 a 8.5cm del lente de la camara
focus = "167"
calibrate_focus()
earlier_dui = 0
rectKernel, sqKernel, second_rectKernel = make_kernels()
font = load_font()
while True:
    start = time.time()
    text = ""
    mrz = get_mrz(get_image())
    try:
        if mrz == 1:
            continue
    except ValueError:
        pass
    dui_int = check_text(print_characters(match_characters(font, process_image(mrz))))
    print dui_int
    if dui_int != earlier_dui and dui_int != 2 and dui_int != 0:
        # print "Sending dui"
        send_dui(dui_int)
        earlier_dui = dui_int
        io_write(1, [1, 0])
        time.sleep(0.5)
        io_write(1, [0, 0])
    else:
        print "Not a valid number"
        io_write(1, [0, 1])
        time.sleep(0.5)
        io_write(1, [0, 0])
    end = time.time()
    print "Time processing: " + str(end - start)

