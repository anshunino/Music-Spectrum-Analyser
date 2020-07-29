import matplotlib.pyplot as plt
import numpy as np
import pyaudio
#from pyqtgraph.Qt import QtGui, QtCore
#import pyqtgraph as pg
import struct
import scipy
from scipy.fftpack import fft
import sys
import time
import serial
ardS= serial.Serial('COM12',19200, serial.EIGHTBITS, serial.PARITY_NONE)
FRAME_SIZE = 2048
x = np.arange(0,8)
p = pyaudio.PyAudio()
def callback(in_data, frame_count, time_info, status):
    nextTime = time.time()
    newSamples = np.fromstring(in_data,dtype=np.int16)
    newdata = np.column_stack((newSamples[::2],newSamples[1::2])) # converting it to a 2D array, with each channel corresponding to a column
    #print(newdata.shape)
    frame = (newdata[:,0]+newdata[:,1])/2.0 #coverting stereo array to mono array
    fourier_t = np.fft.fft(frame*np.hamming(FRAME_SIZE), FRAME_SIZE)
    mag_fourier = np.abs(fourier_t)
    arr=np.zeros(8)
    #y = np.zeros(8)
    y= np.zeros(9,dtype=np.uint8)
    #################################
    #put graphing code here
    #################################.....22222222
    
    for j in range(0,8):
        arr[j]=np.sum(mag_fourier[8*j:8*(j+1)])/100000
        if arr[j]>80:
                    y[j] = 31
        elif arr[j]>50:
                    y[j] = 15
        elif arr[j]>35:
                    y[j] = 7
        elif arr[j]>10:
                    y[j] = 3
        else:
                    y[j] = 1
                    
        y[8] = 85
        
        bit2 = np.zeros([8,8],dtype=np.uint8)
        '''
        for j in range(7,-1, -1):
                for k in range(0,8):
                    if(j<3):
                        if(k==7):
                           bit2[j][k]=1
                        else:
                            bit2[j][k]=0
                    else:
                       if(4-j<y[k]):
                           bit2[j][k] = 1
        bit = np.transpose(bit2)
        '''
        '''
        b=np.packbits(bit)
        b1=np.array(b,dtype=np.uint8)
        b1 = np.concatenate((b1,[85]))
        b1 = np.array(b1,dtype=np.uint8)
        #for i in range(0,5):
         #   for j in range(0,8):
          #      b[i]+=2**bit[i][j]
        print(arr)
        #print(b1)
        #..for i in range(0,5):'''
        ardS.write(y)
        #ardS.write(0x55)
        #if(Serial.inWaiting()>0):
         #   print("////")
          #  print(ardS.readline())
        #print(i)
    startTime = nextTime
    return (in_data,pyaudio.paContinue)
#print('Run')

startTime = time.time()
stream = p.open(channels=2,
                format=pyaudio.paInt16,
                frames_per_buffer=FRAME_SIZE,
                rate=44100,
                input=True,
                input_device_index=6, #change input_device_index depending on the sound card
                stream_callback=callback,
                )
stream.start_stream()
while stream.is_active():
    time.sleep(0.005)
stream.close()
p.terminate()
