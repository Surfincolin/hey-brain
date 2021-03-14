#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 12:36:31 2021

@author: colinwageman
"""

from openal import *
import time

source_1 = oalOpen("computer_bop.wav")
source_2 = oalOpen("cowbell.wav")

source_1.play()

while source_1.get_state() == AL_PLAYING:
    time.sleep(1)

source_2.play()
    
while source_2.get_state() == AL_PLAYING:
    time.sleep(1)
    

source_1.destroy()
source_2.destroy()

oalQuit()