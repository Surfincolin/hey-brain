import time
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


# Brainflow Channel Info
# ======================
# Cyton Channel Info
# package ch 0
 
# eeg chan assoc. ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2'] # Default
# channels = np.array(['F9', 'F7', 'Fp1', 'Fp2', 'F8', 'F4', 'F3', 'Fz']) # Data set 2
channels = np.array(['T3', 'F7', 'Fp1', 'Fp2', 'F8', 'F4', 'F3', 'T4']) # Data set 3
# eeg ch  [1, 2, 3, 4, 5, 6, 7, 8]
 
# board accelerometer ch [9, 10, 11]

# empty on cyton
# other ch [12, 13, 14, 15, 16, 17, 18]
#  
# analog ch [19, 20, 21]

# timestamp ch 22
# marker ch 23

# sample rate 250
# Scale Factor      microVolts/gain/24bit 2'sC => 0.02235
SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) # uV/count

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

    ring_buffer_size = 5120
    self.board.start_stream(ring_buffer_size)

    # Let the stream run for 1/2 a second
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

  sampler = Sampler()
  # sampler = Sampler(port='/dev/cu.usbserial-4')
  sampler.start_stream()

  NUM_RUNS = 35
  SAMPLE_TIME = 3.5 # seconds
  AVG_BREAK_TIME = 3 # +~2 seconds randomly

  data = []

  events = [(1, 'Say Hey Brain'),
            (2, 'Think Hey Brain'),
            (3, 'Visualize talking to the computer'),
            (4, 'Talk out loud')]

  blink_event = (5, 'Blink Twice')
  stop_event = (9, 'Stop')


  print('prepare yourself')
  time.sleep(5)
  # clear buffer
  sampler.get_data()
  # record eye blink event
  print(blink_event[1])
  sampler.mark_event(blink_event[0])
  time.sleep(SAMPLE_TIME)
  data.append(sampler.get_data())
  print('...\n...\n...\n...\n...\n...\n...')
  time.sleep(5)

  # begin actual runs
  for i in range(NUM_RUNS):
    random.shuffle(events)
    for ev in events:
      print(ev[1])
      sampler.mark_event(ev[0])
      time.sleep(SAMPLE_TIME)
      print('...\n...\n...\n...\n...\n...\n...')
      print(stop_event[1])
      time.sleep(AVG_BREAK_TIME + random.uniform(0,2))
      data.append(sampler.get_data())
      print('...\n...\n...\n...\n...\n...\n...')

  # record eye blink event
  print(blink_event[1])
  sampler.mark_event(blink_event[0])
  time.sleep(SAMPLE_TIME)
  data.append(sampler.get_data())
  print('...\n...\n...\n...\n...\n...\n...')
  time.sleep(5)

  print('done!')

  sampler.stop_stream()

  pickle_file = '/Users/colinwageman/Desktop/School/Cogs189/hey-brain/data/raw_data_recording-8ch-3.pkl'
  with open(pickle_file, 'wb') as file:  
    pickle.dump(data, file)
