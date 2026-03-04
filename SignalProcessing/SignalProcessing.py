import numpy
import scipy
from scipy import signal, fft
from matplotlib import pyplot as plt

Fs = 1000
n = 500
F_max = 11
F_filter = 18

random_signal = numpy.random.normal(0,10,n)

time = numpy.arange(n)/Fs

w = F_max/(Fs/2)

lpf = scipy.signal.butter(3,w,'low',output='sos')

filtered = scipy.signal.sosfiltfilt(lpf, random_signal)

def plot(x, y, x_label, y_label, title):

    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))

    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(x_label, fontsize=14)
    ax.set_ylabel(y_label, fontsize=14)
    plt.title(title, fontsize=14)
    fig.savefig('./figures/' + title + '.png', dpi=600)
    plt.show()

def plot_2x2(x, y_list, x_label, y_label, title):

    fig, ax = plt.subplots(2, 2, figsize=(21/2.54, 14/2.54))

    line_width = 1
    font_size = 14

    s = 0
    for i in range(0, 2):
        for j in range(0, 2):
            ax[i][j].plot(x, y_list[s], linewidth=line_width)
            s += 1

    fig.supxlabel(x_label, fontsize=font_size)
    fig.supylabel(y_label, fontsize=font_size)
    fig.suptitle(title, fontsize=font_size)

    fig.savefig('./figures/' + title + '.png', dpi=600)
    plt.show()

#plot(time, filtered,"Час (секунди)","Амплітуда","signal_Fmax_11Hz")

fast_Fourier = scipy.fft.fft(filtered)

fast_Fourier_shifted = numpy.abs(scipy.fft.fftshift(fast_Fourier))

freq_index = scipy.fft.fftfreq(n, 1/n)

freq_index_new = scipy.fft.fftshift(freq_index)

#plot(freq_index_new, fast_Fourier_shifted,"Час (секунди)","Амплітуда","Fast Fourier transform")

'''discrete_signals = []
discrete_spectrum = []
restored_signals = []
E1_list  = []
signal_to_noise_list = []

for Dt in [2, 4, 8, 16]:

    discrete_signal = numpy.zeros(n)

    for i in range(0, round(n/Dt)):
        discrete_signal[i * Dt] = filtered[i * Dt]

    discrete_signals += [list(discrete_signal)]

    spectrum = scipy.fft.fft(discrete_signal)
    spectrum_shifted = numpy.abs(scipy.fft.fftshift(spectrum))

    discrete_spectrum += [list(spectrum_shifted)]

    w = F_filter/(Fs/2)

    kef = scipy.signal.butter(3, w, 'low', output='sos')
    restored = scipy.signal.sosfiltfilt(kef, discrete_signal)
    restored_signals.append(restored)

    E1 = restored-filtered

    var_signal = numpy.var(filtered)
    var_error = numpy.var(E1)

    E1_list.append(var_error)
    signal_to_noise_list.append(var_signal/var_error)

plot_2x2(time, discrete_signals, "Час (секунди)", "Амплітуда","Сигнал з кроком дискретизації Dt = (2,4,8,16)")
plot_2x2(freq_index_new, discrete_spectrum, "Частота (Гц)", "Амплітуда спектру", "Спектри сигналів з кроком дискретизації Dt = (2,4,8,16)")
plot_2x2(time, restored_signals,"Час (секунди)", "Амплітуда сигнал", "Відновлені аналогові сигнали з кроком дискретизації Dt = (2,4,8,16)")

Dt_val = [2, 4, 8, 16]

plot(Dt_val, E1_list, "Крок дискретизації", "Дисперсія","Залежність дисперсії від кроку дискретизації")
plot(Dt_val, signal_to_noise_list,"Крок дискретизації", "Сигнал/шум", "Залежність співвідношення сигнал-шум від кроку дискретизації")'''

quantized_signals = []
var_list  = []
signal_to_noise_list = []

for M in [4, 16, 64, 256]:

    bits = []
    signal_from_bits = []

    delta = (numpy.max(filtered) - numpy.min(filtered))/(M-1)
    quantized_signal = delta * numpy.round(filtered / delta)
    quantized_signals.append(quantized_signal)
    quantize_levels = numpy.arange(numpy.min(quantized_signal), numpy.max(quantized_signal) + 1, delta)

    quantize_bit = numpy.arange(0, M)
    quantize_bit = [format(bits, '0' + str(int(numpy.log(M) / numpy.log(2))) + 'b') for bits in quantize_bit]
    quantize_table = numpy.c_[quantize_levels[:M], quantize_bit[:M]]

    fig, ax = plt.subplots(figsize=(14/2.54, M/2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    plt.close()
    fig.savefig(f'./figures/Таблиця квантування_M_{M}.png', dpi=600)

    for signal_value in quantized_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if numpy.round(numpy.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    bits = [int(item) for item in list(''.join(bits))]

    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.step(numpy.arange(0, len(bits)), bits, linewidth=0.1)
    ax.set_xlabel("Біти")
    ax.set_ylabel("Амплітуда сигнала")
    ax.set_title(f"Кодова послідовність сигналу при кількості рівнів квантування = {M}")
    fig.savefig(f'./figures/Кодова послідовність M = {M}.png', dpi=600)
    plt.close()

    E1 = filtered - quantized_signal

    var_signal = numpy.var(filtered)
    var_error = numpy.var(E1)

    var_list.append(var_error)
    signal_to_noise_list.append(var_signal/var_error)

M_values = [4, 16, 64, 256]

plot_2x2(time, quantized_signals,"Час (секунди)","Амплітуда сигналу","Цифрові сигнали з рівнями квантування (4,16,64,256)")
plot(M_values, var_list,"Кількість рівнів квантування","Дисперсія","Залежність дисперсії від кількості рівнів квантування")
plot(M_values, signal_to_noise_list, "Кількість рівнів квантування", "Сигнал/шум", "Залежність співвідношення сигнал-шум від кількості рівнів квантування")


