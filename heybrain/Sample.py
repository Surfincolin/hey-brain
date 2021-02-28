import time
import numpy as np

import threading
import struct

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes

def main():

  params = BrainFlowInputParams()
  params.serial_port = '/dev/cu.usbserial-DM0258I7'

  log = False
  if log:
    BoardShim.enable_dev_board_logger()
  else:
    BoardShim.disable_board_logger()


  board = BoardShim(BoardIds.CYTON_BOARD, params)
  board.prepare_session()
  board.start_stream(48000)
  print('sleep...')
  time.sleep(1)
  data = board.get_board_data()  # get all data and remove it from internal buffer
  

# eeg chan ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']
# eeg ch   [1, 2, 3, 4, 5, 6, 7, 8]
# board acc ch [9, 10, 11]
# other ch [12, 13, 14, 15, 16, 17, 18]
# anolog ch [19, 20, 21]
# sample rate 250
# package ch 0
# timestamp ch 22
# marker ch 23
interations = 0
while interations < 10:
  print(data.shape)
  time.sleep(0.1)
  data = board.get_board_data()
  interations += 1
  
  board.stop_stream()
  board.release_session()


import sys
import glob
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

if __name__ == '__main__':
  # print(serial_ports())
  main()


# print('connecting') 
# ser = serial.Serial(port='/dev/cu.usbserial-DM0258I7', baudrate=115200, timeout=None)
# time.sleep(2)
# ser.write(b'v')
# print('Connected')
# time.sleep(1)
# print('stream')
# ser.write(b'b')
# time.sleep(0.5)

# START_BYTE = 0xA0
# END_BYTE = 0xC0
# TEST_BYTE = 0xCE

# count = 0
# while count < 50:

#   b = ser.read(1)
#   print('packet:', b)


#   b = ser.read(1)

#   channels_data = []
#   for c in range(8):
#     bb = ser.read(3)

#     unpacked = struct.unpack('3B', bb)

#     if unpacked[0] > 127:
#       pre_fix = bytes(bytearray.fromhex('FF'))
#     else:
#       pre_fix = bytes(bytearray.fromhex('00'))

#     bb = pre_fix + bb

#     myInt = struct.unpack('>i', bb)[0]

#     channels_data.append(myInt)

#   for a in range(3):
#     b = ser.read(2)

#   b = ser.read(1)
#   # val = struct.unpack('B', b)[0]
#   print(b)

#   print(channels_data)
#   count += 1

# print('disconnect')
# ser.write(b's')

# print(TEST_BYTE == END_BYTE)
