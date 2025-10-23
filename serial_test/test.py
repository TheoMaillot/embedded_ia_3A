import serial
import numpy as np

PORT = "COM6" 

if __name__ == '__main__':
    ser = serial.Serial(PORT, 115200, timeout=1)
    while (1):
            ser.write(b"\xAB\x00")
            ret = ser.read(1)
            print(ret)