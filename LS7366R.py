#!/usr/bin/python

#Python library to interface with the chip LS7366R for the Raspberry Pi
#Written by Federico Bolanos
#Source: https://github.com/fbolanos/LS7366R
#Last Edit: February 8th 2016
#Reason: Refactoring some names
#Update: November 4th 2017 by Thilo Brueckner & Sirius3 from 
#Forum: https://www.python-forum.de/viewtopic.php?f=31&t=41495#p316868
#!/usr/bin/python3

import struct
import spidev
import sys
from time import sleep
from functools import reduce

class LS7366R:

    # Commands
    CLEAR_COUNTER = 0x20
    CLEAR_STATUS  = 0x30
    READ_COUNTER  = 0x60
    READ_STATUS   = 0x70
    WRITE_DTR     = 0x98
    LOAD_COUNTER  = 0xE0
    LOAD_OTR      = 0xE4
    WRITE_MODE0   = 0x88
    WRITE_MODE1   = 0x90

    # Mode settings
    FOURX_COUNT = 0x03

    FOURBYTE_COUNTER  = 0x00
    THREEBYTE_COUNTER = 0x01
    TWOBYTE_COUNTER   = 0x02
    ONEBYTE_COUNTER   = 0x03

    EN_CNTR  = 0x00
    DIS_CNTR = 0x04

    BYTE_MODE = [ONEBYTE_COUNTER, TWOBYTE_COUNTER, THREEBYTE_COUNTER, FOURBYTE_COUNTER]

    def __init__(self, cs_line, max_speed_hz, byte_mode):
        self.byte_mode = byte_mode
        self.spi = spidev.SpiDev()
        self.spi.open(0, cs_line)
        self.spi.max_speed_hz = max_speed_hz

        # Initialize LS7366R
        self.clear_counter()
        self.clear_status()
        self.spi.xfer2([self.WRITE_MODE0, self.FOURX_COUNT])
        sleep(0.1)
        self.spi.xfer2([self.WRITE_MODE1, self.BYTE_MODE[self.byte_mode - 1]])

    def close(self):
        self.spi.close()

    def clear_counter(self):
        self.spi.xfer2([self.CLEAR_COUNTER])

    def clear_status(self):
        self.spi.xfer2([self.CLEAR_STATUS])

    def load_counter(self, enc_val):
        data = struct.pack(">I", enc_val)[-self.byte_mode:]
        self.spi.xfer2([self.WRITE_DTR] + list(data))
        self.spi.xfer2([self.LOAD_COUNTER])

    def read_counter(self):
        data = [self.READ_COUNTER] + [0] * self.byte_mode
        data = self.spi.xfer2(data)
        return reduce(lambda a, b: (a << 8) + b, data[1:], 0)

    def read_status(self):
        data = self.spi.xfer2([self.READ_STATUS, 0xFF])
        return data[1]

if __name__ == "__main__":
    encoder = LS7366R(0, 1000000, 4)  # CE0, 1 MHz, 4-byte counter
    try:
        while True:
            sys.stdout.write('\rEncoder count: %11i  (CTRL+C to exit)' % encoder.read_counter())
            sys.stdout.flush()
            sleep(0.2)
    except KeyboardInterrupt:
        encoder.close()
        print("\nAll done, bye bye.")

