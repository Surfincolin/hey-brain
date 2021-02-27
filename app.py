import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation

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
    window_width = 300
    window_height = 200
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_pos = int(screen_width/2 - window_width/2)
    y_pos = int(screen_height/2 - window_height/2)
    win.geometry('{}x{}+{}+{}'.format(window_width, window_height, x_pos, y_pos))
    self.master.protocol('WM_DELETE_WINDOW', self.close)

    self.record = tk.Button(self)
    self.record['text'] = "Record"
    self.record['command'] = self.start_record
    self.record.pack(side='top')

    self.quit = tk.Button(self, text='QUIT', fg='red',
                          command=self.close)
    self.quit.pack(side='bottom')

  def close(self):
    print('closing the app')
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