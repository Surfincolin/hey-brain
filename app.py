

import tkinter as tk
from tkinter import ttk

import pickle
import os

import pygame
import webbrowser
from pyautogui import keyDown, keyUp, click

import time
from datetime import datetime

# import warnings
from heybrain.LiveView import *

from sklearn.metrics import classification_report

class Application(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()
    self.main_window()
    # self.master.option_add('*tearOff', FALSE)

  def main_window(self):
    win = self.winfo_toplevel()
    win.title('Hey Brain')
    window_width = 1280
    window_height = 720
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_pos = int(screen_width/2 - window_width/2)
    y_pos = int(screen_height/2 - window_height/2)
    win.geometry('{}x{}+{}+{}'.format(window_width, window_height, x_pos, y_pos))
    self.master.protocol('WM_DELETE_WINDOW', self.close)

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand = True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    self.main_container = container    

    self.frames = {}

    self.start = tk.Button(self, text='Start', fg='green', command=self.open_live_view)
    self.start.pack(side='top')

    self.quit = tk.Button(self, text='QUIT', fg='red', command=self.close)
    self.quit.pack(side='bottom')

  def open_live_view(self):
    frame = LiveView(self.main_container, self)
    frame.grid(row=0, column=0, sticky='nsew')
    self.frames['LiveView'] = frame
    frame.tkraise()
    frame.show()

  def close(self):
    print('closing the app')
    for key, frame in self.frames.items():
      frame.kill()
      frame.destroy()
      frame = None

    self.master.destroy()

  def start_record(self):
    print('Begin Recording')

def main():
  print('Lets read some minds!')
  root = tk.Tk()
  app = Application(master=root)
  app.mainloop()

if __name__ == "__main__":
  main()