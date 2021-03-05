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
SCALE_FACTOR_EEG = (4500000)/24/100/(2**23-1) # uV/count

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
    # self.board.config_board('1234')
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
    if self.streaming:
      return self.board.get_board_data()
    else:
      print('not streaming')
      return np.zeros(shape=(24, 25), dtype=float)

  def mark_event(self, event_id=0):
    if self.streaming:
      self.board.insert_marker(event_id)
    else:
      print('event not saved, not streaming')



# For testing purposes
if __name__ == '__main__':
  import random

  import pickle

  sampler = Sampler(port='/dev/cu.usbserial-4')
  sampler.start_stream()

  data = []

  events = [(1, 'Say Hey Brain'),
            (2, 'Think Hey Brain'),
            (3, 'Visualize talking to the computer'),
            (4, 'Type this sentence out on the computer')]

  stop_event = (9, 'Stop')


  print('prepare yourself')
  time.sleep(3)
  data.append(sampler.get_data())
  for i in range(20):
    ev = random.choice(events)
    sampler.mark_event(ev[0])
    print(ev[1])
    time.sleep(3)
    sampler.mark_event(stop_event[0])
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')
    print(stop_event[1])
    time.sleep(3 + random.randint(0,2))
    data.append(sampler.get_data())
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')
    print('...')

  print('done!')


  # iterations = 0
  # while iterations < 20:
  #   # print(sampler.get_data()[0])
  #   data.append(sampler.get_data())
  #   time.sleep(0.1)
  #   if iterations == 10:
  #     sampler.mark_event(2)

  #   iterations += 1

  sampler.stop_stream()

  pickle_file = './Cogs189/hey-brain/data/raw_data_recording-8ch-2.pkl'
  with open(pickle_file, 'wb') as file:  
    pickle.dump(data, file)
  # # print(len(data))
  # for i in range(10):
  #   print(random.choice(events)[1])


    # Record and segment data
    # Convert data from uV to V
    # Bandpass Filter: (1-51 Hz, 3rd order)
    # Bandstop Filter: (59.5-60.5 Hz, 4th order)
    # Denoising (Undecided method)
    # Convert to RMS value (What sized window is uses in the GUI?)
