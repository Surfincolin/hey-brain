import time
import numpy as np

# import threading

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
# from brainflow.data_filter import DataFilter, FilterTypes

# Channel Info
# package ch 0
# eeg chan assoc. ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']
# eeg ch  [1, 2, 3, 4, 5, 6, 7, 8]
# board acc ch [9, 10, 11]
# empty on cyton
# other ch [12, 13, 14, 15, 16, 17, 18] 
# anolog ch [19, 20, 21]

# timestamp ch 22
# marker ch 23

# sample rate 250

class Sampler:
  def __init__(self, port='/dev/cu.usbserial-DM0258I7', debug=False):
    self.streaming = False

    self.data_pool = np.zeros(shape=(24, 1024), dtype=float)

    self.params = BrainFlowInputParams()
    self.params.serial_port = port

    log = debug
    if log:
      BoardShim.enable_dev_board_logger()
    else:
      BoardShim.disable_board_logger()

    self.board = BoardShim(BoardIds.CYTON_BOARD, self.params)


  def start_stream(self):
    self.board.prepare_session()
    self.board.start_stream(5120)
    time.sleep(0.5)
    self.streaming = True
    print('::: Streaming :::')

  def stop_stream(self):
    self.streaming = False
    self.board.stop_stream()
    self.board.release_session()
    print('::: Stream Stopped :::')

  def get_data(self):
    return self.board.get_board_data()

  def mark_event(self, event_id=0):
    self.board.insert_marker(event_id)



# For testing purposes
if __name__ == '__main__':
  sampler = Sampler()
  sampler.start_stream()

  iterations = 0
  while iterations < 20:
    print(sampler.get_data()[8])
    time.sleep(0.1)
    if iterations == 10:
      sampler.mark_event(2)

    iterations += 1

  sampler.stop_stream()

