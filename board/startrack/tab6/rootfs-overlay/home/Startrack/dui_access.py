import struct
import time
import sys
import serial


def check_text(mrz):
    if "IDGTM" in mrz:
        number = mrz[5:14] + mrz[15:19]
    elif "IDSLV" in mrz:
        number = mrz[5:13] + mrz[15:16]
    elif "I<PER" in mrz:
        number = mrz[5:13]
    else:
        return 0
    return int(number)


def decode_key(keycode):
    key = ''
    if keycode == 16:
        key = "Q"
    elif keycode == 17:
        key = "W"
    elif keycode == 18:
        key = "E"
    elif keycode == 19:
        key = "R"
    elif keycode == 20:
        key = "T"
    elif keycode == 21:
        key = "Y"
    elif keycode == 22:
        key = "U"
    elif keycode == 23:
        key = "I"
    elif keycode == 24:
        key = "O"
    elif keycode == 25:
        key = "P"
    elif keycode == 30:
        key = "A"
    elif keycode == 31:
        key = "S"
    elif keycode == 32:
        key = "D"
    elif keycode == 33:
        key = "F"
    elif keycode == 34:
        key = "G"
    elif keycode == 35:
        key = "H"
    elif keycode == 36:
        key = "J"
    elif keycode == 37:
        key = "K"
    elif keycode == 38:
        key = "L"
    elif keycode == 44:
        key = "Z"
    elif keycode == 45:
        key = "X"
    elif keycode == 46:
        key = "C"
    elif keycode == 47:
        key = "V"
    elif keycode == 48:
        key = "B"
    elif keycode == 49:
        key = "N"
    elif keycode == 50:
        key = "M"
    return key


infile_path = "/dev/input/event0"
#  long int, long int, unsigned short, unsigned short, unsigned int
#  Structure input event:time seconds(timeval),time micro seconds(timeval),type(short),code(short),value(int)
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
#  open file in binary mode
in_file = open(infile_path, "rb")

ser = serial.Serial('/dev/ttyS0', 9600, timeout=0, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    xonxoff=False, rtscts=False)
event = in_file.read(EVENT_SIZE)
number = ''
while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
    if type == 1 and value == 1:
        #  Keyboard Event - Type = 1, Value = 1 porque es keypress
        # Numbers are not aligned, code 11 = 0
        if code == 11:
            code = 0
            number = str(number) + str(code)
        elif code in range(2, 11):
            code = code - 1
            number = str(number) + str(code)
        elif code in range(16, 26) or code in range(30, 39) or code in range(44, 51):
            code = decode_key(code)
            number = str(number) + str(code)
        #  27 means Enter, end of line
        elif code == 28 and check_text(number):
            number = check_text(number)
            VRBL = [0, 0, 0, 0, 0]
            copied_number = int(number)
            binary_number = bin(copied_number)
            binary_number = binary_number[2:]
            Size = len(binary_number)
            if Size <= 16:
                # No changes made
                VRBL[4] = binary_number
                VRBL[4] = int(VRBL[4], 2)
            elif Size <= 32:
                VRBL[4] = binary_number[Size - 16:Size]
                VRBL[3] = binary_number[0:Size - 16]
                VRBL[4] = int(VRBL[4], 2)
                VRBL[3] = int(VRBL[3], 2)
            elif Size <= 48:
                VRBL[4] = binary_number[Size - 16:Size]
                VRBL[3] = binary_number[Size - 32:Size - 16]
                VRBL[2] = binary_number[0:Size - 32]
                VRBL[4] = int(VRBL[4], 2)
                VRBL[3] = int(VRBL[3], 2)
                VRBL[2] = int(VRBL[2], 2)
            elif Size <= 64:
                VRBL[4] = binary_number[Size - 16:Size]
                VRBL[3] = binary_number[Size - 32:Size - 16]
                VRBL[2] = binary_number[Size - 48:Size - 32]
                VRBL[1] = binary_number[0:Size - 48]
                VRBL[4] = int(VRBL[4], 2)
                VRBL[3] = int(VRBL[3], 2)
                VRBL[2] = int(VRBL[2], 2)
                VRBL[1] = int(VRBL[1], 2)
            elif Size <= 80:
                VRBL[4] = binary_number[Size - 16:Size]
                VRBL[3] = binary_number[Size - 32:Size - 16]
                VRBL[2] = binary_number[Size - 48:Size - 32]
                VRBL[1] = binary_number[Size - 64:Size - 48]
                VRBL[0] = binary_number[0:Size - 64]
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

            print('AT$FUNC="VRBL",0,91\r\n')
            print('AT$FUNC="VRBL",5,' + str(VRBL[4]) + '\r\n')
            print('AT$FUNC="VRBL",4,' + str(VRBL[3]) + '\r\n')
            print('AT$FUNC="VRBL",3,' + str(VRBL[2]) + '\r\n')
            print('AT$FUNC="VRBL",2,' + str(VRBL[1]) + '\r\n')
            print('AT$FUNC="VRBL",1,' + str(VRBL[0]) + '\r\n')
            print('AT$GPOS=2,0' + '\r\n')
            number = ''
        elif code == 28:
            number = ''
    event = in_file.read(EVENT_SIZE)

in_file.close()
