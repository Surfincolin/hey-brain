import time
import numpy as np

import threading

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, LogLevels
from brainflow.data_filter import DataFilter, FilterTypes

# Channel Info
# eeg chan ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']
# eeg ch   [1, 2, 3, 4, 5, 6, 7, 8]
# board acc ch [9, 10, 11]
# other ch [12, 13, 14, 15, 16, 17, 18]
# anolog ch [19, 20, 21]
# sample rate 250
# package ch 0
# timestamp ch 22
# marker ch 23

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
  
interations = 0
while interations < 10:
  print(data.shape)
  time.sleep(0.1)
  data = board.get_board_data()
  interations += 1
  
  board.stop_stream()
  board.release_session()

if __name__ == '__main__':
  main()
