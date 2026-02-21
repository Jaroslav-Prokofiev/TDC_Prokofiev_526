import numpy
import scipy
from scipy import signal, fft
from matplotlib import pyplot as plt

Fs = 1000
n = 500
F_max = 11

random_signal = numpy.random.normal(0,10,n)

time = numpy.arange(n)/Fs

w = F_max/(Fs/2)

lpf = scipy.signal.butter(3,w,'low',output='sos')

filtered = scipy.signal.sosfiltfilt(lpf, random_signal)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(time, filtered, linewidth=1)
ax.set_xlabel("Час (секунди)", fontsize=14)
ax.set_ylabel("Амплітуда", fontsize=14)
title = "signal_Fmax_11Hz"
plt.title("Сигнал з максимальною частотою Fmax = 11 Гц", fontsize=14)
fig.savefig('./figures/' + title + '.png', dpi=600)
plt.grid()
plt.show()

fast_Fourier = scipy.fft.fft(filtered)

fast_Fourier_shifted = numpy.abs(scipy.fft.fftshift(fast_Fourier))

freq_index = scipy.fft.fftfreq(n, 1/n)

freq_index_new = scipy.fft.fftshift(freq_index)

fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
ax.plot(freq_index_new, fast_Fourier_shifted, linewidth=1)
ax.set_xlabel("Частота (Гц)", fontsize=14)
ax.set_ylabel("Амплітуда спектру", fontsize=14)
title = "Fast Fourier transform"
plt.title("Спектр сигналу з максимальною частотою Fmax = 11 Гц", fontsize=14)
fig.savefig('./figures/' + title + '.png', dpi=600)
plt.grid()
plt.show()