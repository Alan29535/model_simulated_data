# -*- coding: utf-8 -*-
"""signal_representation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pn9pvXLux8tQC71-CunZSEsrD2sOkPlg
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.signal import stft
import os
import pywt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft, periodogram

class SpectrogramPlotter:
    def __init__(self, signals, fs, nperseg):
        self.signals = signals
        self.fs = fs
        self.nperseg = nperseg

    def plot_spectrogram(self):
        f, t, Zxx = stft(self.signals, fs=self.fs, nperseg=self.nperseg, window = ('hann'))
        
        fig, axs = plt.subplots(2, 5, figsize=(15, 6))
        axs = axs.ravel()
        for i in range(self.signals.shape[0]):
            axs[i].pcolormesh(t, f, np.abs(Zxx[i, :, :]))
            axs[i].set_title('Signal {}'.format(i))
            axs[i].set_xlabel('Time [s]')
            axs[i].set_ylabel('Frequency [Hz]')
            axs[i].set_ylim(0, 4)

        plt.tight_layout()
        plt.show()

    def plot_power_spectrum(self):
        fig, axs = plt.subplots(2, 5, figsize=(15, 6))
        axs = axs.ravel()
        for i in range(self.signals.shape[0]):
            f, Pxx = periodogram(self.signals[i, :], fs=self.fs)
            axs[i].plot(f, Pxx)
            axs[i].set_title('Signal {}'.format(i))
            axs[i].set_xlabel('Frequency [Hz]')
            axs[i].set_ylabel('Power Spectral Density [V^2/Hz]')

        plt.tight_layout()
        plt.show()

class ScalogramPlotter:
    def __init__(self, signals, wavelet='morl', widths=np.arange(1, 31)):
        self.signals = signals
        self.wavelet = wavelet
        self.widths = widths
        self.num_signals, self.num_samples = signals.shape
        
    def compute_cwt(self):
        cwtmatrs = []
        for signal in self.signals:
            cwtmatr, freqs = pywt.cwt(signal, self.widths, self.wavelet)
            cwtmatrs.append(cwtmatr)
        self.cwtmatrs = cwtmatrs
        self.freqs = freqs
        
    def plot_scalograms(self):
        fig, axs = plt.subplots(nrows=self.num_signals, figsize=(20, 40), sharex=True, sharey=True)
        for i in range(self.num_signals):
            axs[i].imshow(self.cwtmatrs[i], extent=[0, 1000, self.freqs[0], self.freqs[-1]], cmap='bone', aspect='auto', vmax=abs(self.cwtmatrs[i]).max(), vmin=-abs(self.cwtmatrs[i]).max())
            axs[i].set_title(f'Scalogram of signal {i+1}')
            axs[i].set_ylabel('Frequency (Hz)')
        axs[-1].set_xlabel('Time (s)')
        plt.show()

    def save_scalograms(self, folder_path):
        for i in range(self.num_signals):
            fig, ax = plt.subplots(figsize=(20, 10))
            ax.imshow(self.cwtmatrs[i], extent=[0, 1000, self.freqs[0], self.freqs[-1]], cmap='bone', aspect='auto', vmax=abs(self.cwtmatrs[i]).max(), vmin=-abs(self.cwtmatrs[i]).max())
            ax.set_title(f'Scalogram of signal {i+1}')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_xlabel('Time (s)')
            file_name = folder_path + '/scalogram_of_signal_' + str(i+1) + '.png'
            plt.savefig(file_name)
            plt.close(fig)

class SynchrosqueezedTransform:
    def __init__(self, flow, wavelet='db1', level=3):
        self.flow = np.array(flow)
        self.num_signals, self.num_samples = self.flow.shape
        self.wavelet = wavelet
        self.level = level
        
    def perform_sst(self):
        ss_coeffs = []
        for signal in self.flow:
            coeffs = pywt.swt(signal, self.wavelet, level=self.level)
            ss_coeff = np.zeros_like(coeffs[0][0])
            for i in range(self.level):
                (cA, cD) = coeffs[i]
                ss_coeff += np.abs(cD)
            ss_coeffs.append(np.expand_dims(ss_coeff, axis=0))
        self.ss_coeffs = ss_coeffs
        
    def plot_sst(self):
        fig, axs = plt.subplots(nrows=self.num_signals, figsize=(20,40), sharex=True, sharey=True)
        for i in range(self.num_signals):
            axs[i].imshow(self.ss_coeffs[i], extent=[0,1000, 0, self.level], cmap='bone', aspect='auto', vmax=abs(self.ss_coeffs[i]).max(), vmin=-abs(self.ss_coeffs[i]).max())
            axs[i].set_title(f'Synchrosqueezed Transform of signal {i+1}')
            axs[i].set_ylabel('Frequency')
        axs[-1].set_xlabel('Time (s)')
        plt.show()