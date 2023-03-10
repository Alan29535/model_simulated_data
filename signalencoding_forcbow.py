# -*- coding: utf-8 -*-
"""SignalEncoding_forCBOW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VnN37o1QQ4SsdtueffkKBUF0ztoJsaKy
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.signal import stft
import os

import numpy as np


class SignalEncoding:
    def __init__(self, sampling_rate, num_levels):
        self.sampling_rate = sampling_rate
        self.num_levels = num_levels
        self.time_interval = 1 / self.sampling_rate # Calculate the time interval between samples
        self.time_steps_between_samples = int(1 / self.time_interval) # Calculate the number of time steps between samples
        self.step_size = None


    def sample_signal(self, signal):
        sampled_signal = signal[:, ::self.time_steps_between_samples] # Select every time_steps_between_samples time step from the original signal
        min_value = np.min(sampled_signal)
        max_value = np.max(sampled_signal)
        self.step_size = (max_value - min_value) / self.num_levels # Calculate the step size for quantization
        quantized_signal = np.round((sampled_signal - min_value) / self.step_size) * self.step_size + min_value # Map each sample of the signal to one of the quantization levels
        return quantized_signal


class DeltaEncoding:
    def delta_encode(self, signal):
      for i in range(signal.shape[0]):
          for j in range(1, signal.shape[1]):
              signal[i, j] = signal[i, j] - signal[i, j-1]
      return signal

