
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk

import numpy as np

from heybrain.Sampler import *

class LiveView(tk.Frame):

  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    print('Live View Open')
    # self.controller = controller

    label = tk.Label(self, text='Live View', font=("Verdana", 12, 'bold'))
    label.pack(pady=10, padx=10)

    # Initialize figures and timepoints xvals array
    self.num_seconds_to_display = 5
    self.x_values = np.linspace(0, self.num_seconds_to_display, 250 * self.num_seconds_to_display) # replace this in real test

    self.fig = Figure(figsize=(5,5), dpi=100)

    self.average_pred_plot = self.fig.add_subplot(2, 1, 1)
    self.average_pred_plot.set_ylim(0, 1)
    self.average_pred_plot.set_xlim(0, self.num_seconds_to_display) # replace this in real test
    self.average_pred_plot.set_title("Prediction Value")
    self.average_pred_plot.set_ylabel("Probability Left")
    self.average_pred_plot.set_xticklabels([])
    self.eeg_plot = self.fig.add_subplot(2, 1, 2)
    self.eeg_plot.set_ylim(-400, 400)
    self.eeg_plot.set_xlim(0, self.num_seconds_to_display) # replace this in real test

    self.eeg_plot.set_title("EEG Data")
    self.eeg_plot.set_xlabel("Time (s)")
    self.eeg_plot.set_ylabel("Voltage (uV)")

    # Create canvas for figures 
    self.canvas = FigureCanvasTkAgg(self.fig, self)
    self.canvas.draw()
    self.canvas_tk_wid = self.canvas.get_tk_widget()
    self.canvas_tk_wid.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    self.board = Sampler()

    self.in_session = False
    self.pool = np.zeros(shape=(4,1250), dtype=float)

  def show(self):
    print('show live view')
    

    if not self.in_session:
      self.in_session = True
      self.board.start_stream()
      self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100)
      self.canvas.draw()

  def __plotMultilines(self, ax, xvals, yvals): 
    '''
      xvals should be 1d with length of the timepoints 
      yvals can be multiple lines each with same length as xvals
    '''
    if ax.lines: 
      for i, line in enumerate(ax.lines):
          line.set_ydata(yvals[i])
    else:
      for i, ys in enumerate(yvals): 
          ax.plot(xvals, ys)

  def animate(self,i):     
    '''
      The animate function for FuncAnimate 
    '''
    # print('animate')
    data = self.board.get_data()
    chop = data.shape[1]
    self.pool = np.concatenate((data[5:9], self.pool[:,:-chop]), axis=1)

    xList = self.x_values
    # yList = self.eeg_sampler.getBuffer()[200:len(xList) + 200, :4].T # Offset by 100 to reduce the visibility of the filter lag
    yList = self.pool # Offset by 100 to reduce the visibility of the filter lag
    yFlipped = []
    for elem in yList:
      yFlipped.append(np.flip(elem))
    self.__plotMultilines(self.eeg_plot, xList, yFlipped)

    # xList = self.x_values
    # yList = np.flip(self.eeg_sampler.getPredictionValues().T[100:len(xList) + 100])
    # self.__plotMultilines(self.average_pred_plot, xList, [yList])

  def kill(self):
    self.board.stop_stream()
    self.ani = None