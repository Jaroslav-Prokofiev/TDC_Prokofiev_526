import soundfile as sf
from math import gcd
from scipy.signal import resample_poly, butter, sosfiltfilt, convolve, resample
import numpy as np
import matplotlib.pyplot as plt
from skimage.restoration import denoise_wavelet, denoise_invariant, denoise_tv_chambolle, denoise_bilateral, cycle_spin
import pywt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import glob

SAMPLE_RATE = 44100
NAME_ORIGINAL_WAV = "./Sounds/Sound_44100[Hz]_2[byte].wav"

def wavelet_denoiser(signal, level=5, mode='hard', wavelet='db4'):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    threshold = sigma * np.sqrt(2 * np.log(signal.size))

    denoised_coeffs = [coeffs[0]] + [
        pywt.threshold(c, threshold, mode=mode) for c in coeffs[1:]
    ]

    denoised_signal = pywt.waverec(denoised_coeffs, wavelet)
    return denoised_signal[:len(signal)]

def gaussian_kernel(size, sigma):
    x = np.linspace(-(size // 2), size // 2, size)
    kernel = np.exp(-0.5 * (x / sigma) ** 2)
    return kernel / kernel.sum()

def wavelet_shifted_filter():
    data, fs_original = sf.read(NAME_ORIGINAL_WAV)
    time = np.arange(len(data)) / fs_original

    max_shifts = [0, 1, 3, 5]
    signals = []
    for n, s in enumerate(max_shifts):
        sig_filtered = cycle_spin(
            data,
            func=wavelet_denoiser,
            max_shifts=s,
            shift_steps=5
        )
        sf.write(f"./Sounds/Filtered_Shifted_Wavelet_{n}.wav",
                 sig_filtered, SAMPLE_RATE)
        signals.append(sig_filtered)

    kernel = gaussian_kernel(size=11, sigma=2)
    filtered_signal = convolve(data, kernel, mode='same')
    sf.write("./Sounds/Filtered_Gaussian_Filter.wav", filtered_signal, SAMPLE_RATE)

    plt.figure(figsize=(12, 6))
    plt.plot(time, data, label=f"Оригінал (fs={SAMPLE_RATE} Гц)")
    plt.plot(time, signals[0], label=f"Wavelet Shifted: no shift")
    plt.plot(time, signals[1], label=f"Wavelet Shifted: 1x2")
    plt.plot(time, signals[2], label=f"Wavelet Shifted: 1x4")
    plt.plot(time, signals[3], label=f"Wavelet Shifted: 1x6")
    plt.title("Порівняння сигналів у часовій області, вейвлет-фільтр, модифікований")
    plt.xlabel("Час (мс)")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./Sounds/wavelet_shifted.png")
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(time, data, label=f"Оригінал (fs={SAMPLE_RATE} Гц)")
    plt.plot(time, filtered_signal, label=f"Gaussian Filter")
    plt.title("Порівняння сигналів у часовій області, фільтр Гаусса")
    plt.xlabel("Час (мс)")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./Sounds/gaussian.png")
    plt.show()

def filtration_efficiency():
    data, fs_original = sf.read(NAME_ORIGINAL_WAV)

    signal_power = np.mean(data ** 2)
    max_shifts = 5
    mse_wt_mean = []
    mse_wt_list = []
    mse_g_mean = []
    mse_g_list = []
    mae_wt_mean = []
    mae_wt_list = []
    mae_g_mean = []
    mae_g_list = []
    rmse_wt_mean = []
    rmse_wt_list = []
    rmse_g_mean = []
    rmse_g_list = []
    r2_wt_mean = []
    r2_wt_list = []
    r2_g_mean = []
    r2_g_list = []
    d_wt_mean = []
    d_wt_list = []
    d_g_mean = []
    d_g_list = []
    snr_values = []

    for SNR_dB in np.arange(-10, 21, 0.5):
        mse_wt = []
        mse_g = []
        mae_wt = []
        mae_g = []
        rmse_wt = []
        rmse_g = []
        r2_wt = []
        r2_g = []
        d_wt = []
        d_g = []

        for i in range(0, 10):
            noise_power = signal_power / (10 ** (SNR_dB / 10))

            noise = np.random.normal(
                0,
                np.sqrt(noise_power),
                size=data.shape
            )
            noisy_signal = data + noise
            sig_filtered_wavelet = cycle_spin(
                noisy_signal,
                func=wavelet_denoiser,
                max_shifts=max_shifts,
                shift_steps=5,
                num_workers=1
            )

            kernel = gaussian_kernel(size=11, sigma=2)
            sig_filtered_gaussian = convolve(
                noisy_signal,
                kernel,
                mode='same'
            )

            mse_wavelet = mean_squared_error(
                data,
                sig_filtered_wavelet
            )

            mse_gaussian = mean_squared_error(
                data,
                sig_filtered_gaussian
            )

            mae_wavelet = mean_absolute_error(data, sig_filtered_wavelet)
            mae_gaussian = mean_absolute_error(data, sig_filtered_gaussian)

            rmse_wavelet = np.sqrt(mse_wavelet)
            rmse_gaussian = np.sqrt(mse_gaussian)

            r2_wavelet = r2_score(data, sig_filtered_wavelet)
            r2_gaussian = r2_score(data, sig_filtered_gaussian)

            d_wavelet = np.var(data - sig_filtered_wavelet)
            d_gaussian = np.var(data - sig_filtered_gaussian)

            mse_wt.append(mse_wavelet)
            mse_g.append(mse_gaussian)
            mae_wt.append(mae_wavelet)
            mae_g.append(mae_gaussian)
            rmse_wt.append(rmse_wavelet)
            rmse_g.append(rmse_gaussian)
            r2_wt.append(r2_wavelet)
            r2_g.append(r2_gaussian)
            d_wt.append(d_wavelet)
            d_g.append(d_gaussian)

        mse_wt_mean.append(np.mean(mse_wt))
        mse_wt_list.append(list(mse_wt))
        mse_g_mean.append(np.mean(mse_g))
        mse_g_list.append(list(mse_g))

        mae_wt_mean.append(np.mean(mae_wt))
        mae_wt_list.append(list(mae_wt))
        mae_g_mean.append(np.mean(mae_g))
        mae_g_list.append(list(mae_g))

        rmse_wt_mean.append(np.mean(rmse_wt))
        rmse_wt_list.append(list(rmse_wt))
        rmse_g_mean.append(np.mean(rmse_g))
        rmse_g_list.append(list(rmse_g))

        r2_wt_mean.append(np.mean(r2_wt))
        r2_wt_list.append(list(r2_wt))
        r2_g_mean.append(np.mean(r2_g))
        r2_g_list.append(list(r2_g))

        d_wt_mean.append(np.mean(d_wt))
        d_wt_list.append(list(d_wt))
        d_g_mean.append(np.mean(d_g))
        d_g_list.append(list(d_g))
        snr_values.append(SNR_dB)

    snr_scatter_wt = []
    mse_scatter_wt = []
    snr_scatter_g = []
    mse_scatter_g = []

    for snr, mse_list in zip(snr_values, mse_wt_list):
        snr_scatter_wt.extend([snr] * len(mse_list))
        mse_scatter_wt.extend(mse_list)

    for snr, mse_list in zip(snr_values, mse_g_list):
        snr_scatter_g.extend([snr] * len(mse_list))
        mse_scatter_g.extend(mse_list)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(snr_scatter_wt, mse_scatter_wt, color='red', alpha=0.05, label="Окремі значення MSE")
    axes[0].plot(snr_values, mse_wt_mean, linewidth=2, label="Середнє MSE WT")
    axes[0].scatter(snr_scatter_g, mse_scatter_g, color='green', alpha=0.05, label="Окремі значення MSE")
    axes[0].plot(snr_values, mse_g_mean, linewidth=2, label="Середнє MSE GF")
    axes[0].set_xticks(np.arange(-10, 21, 2))
    axes[0].set_xlabel("SNR (дБ)")
    axes[0].set_ylabel("MSE")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_title("Лінійний масштаб")
    axes[1].scatter(snr_scatter_wt, mse_scatter_wt, color='red', alpha=0.05, label="Окремі значення MSE")
    axes[1].plot(snr_values, mse_wt_mean, linewidth=2, label="Середнє MSE WT")
    axes[1].scatter(snr_scatter_g, mse_scatter_g, color='green', alpha=0.05, label="Окремі значення MSE")
    axes[1].plot(snr_values, mse_g_mean, linewidth=2, label="Середнє MSE GF")
    axes[1].set_xticks(np.arange(-10, 21, 1))
    axes[1].set_xlabel("SNR (дБ)")
    axes[1].set_ylabel("MSE")
    axes[1].grid(True)
    axes[1].set_yscale('log')
    axes[1].legend()
    axes[1].set_title("Логарифмічний масштаб")
    plt.tight_layout()
    plt.savefig("MSE-SNR.png", dpi=600)
    plt.show()

    snr_scatter_wt_mae = []
    mae_scatter_wt = []
    snr_scatter_g_mae = []
    mae_scatter_g = []

    for snr, mae_list in zip(snr_values, mae_wt_list):
        snr_scatter_wt_mae.extend([snr] * len(mae_list))
        mae_scatter_wt.extend(mae_list)

    for snr, mae_list in zip(snr_values, mae_g_list):
        snr_scatter_g_mae.extend([snr] * len(mae_list))
        mae_scatter_g.extend(mae_list)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(snr_scatter_wt_mae, mae_scatter_wt, color='red', alpha=0.05, label="Окремі значення MAE")
    axes[0].plot(snr_values, mae_wt_mean, linewidth=2, label="Середнє MAE WT")
    axes[0].scatter(snr_scatter_g_mae, mae_scatter_g, color='green', alpha=0.05, label="Окремі значення MAE")
    axes[0].plot(snr_values, mae_g_mean, linewidth=2, label="Середнє MAE GF")
    axes[0].set_xticks(np.arange(-10, 21, 2))
    axes[0].set_xlabel("SNR (дБ)")
    axes[0].set_ylabel("MAE")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_title("Лінійний масштаб")
    axes[1].scatter(snr_scatter_wt_mae, mae_scatter_wt, color='red', alpha=0.05, label="Окремі значення MAE")
    axes[1].plot(snr_values, mae_wt_mean, linewidth=2, label="Середнє MAE WT")
    axes[1].scatter(snr_scatter_g_mae, mae_scatter_g, color='green', alpha=0.05, label="Окремі значення MAE")
    axes[1].plot(snr_values, mae_g_mean, linewidth=2, label="Середнє MAE GF")
    axes[1].set_xticks(np.arange(-10, 21, 1))
    axes[1].set_xlabel("SNR (дБ)")
    axes[1].set_ylabel("MAE")
    axes[1].grid(True)
    axes[1].set_yscale('log')
    axes[1].legend()
    axes[1].set_title("Логарифмічний масштаб")
    plt.tight_layout()
    plt.savefig("MAE-SNR.png", dpi=600)
    plt.show()

    snr_scatter_wt_rmse = []
    rmse_scatter_wt = []
    snr_scatter_g_rmse = []
    rmse_scatter_g = []

    for snr, rmse_list in zip(snr_values, rmse_wt_list):
        snr_scatter_wt_rmse.extend([snr] * len(rmse_list))
        rmse_scatter_wt.extend(rmse_list)

    for snr, rmse_list in zip(snr_values, rmse_g_list):
        snr_scatter_g_rmse.extend([snr] * len(rmse_list))
        rmse_scatter_g.extend(rmse_list)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(snr_scatter_wt_rmse, rmse_scatter_wt, color='red', alpha=0.05, label="Окремі значення RMSE")
    axes[0].plot(snr_values, rmse_wt_mean, linewidth=2, label="Середнє RMSE WT")
    axes[0].scatter(snr_scatter_g_rmse, rmse_scatter_g, color='green', alpha=0.05, label="Окремі значення RMSE")
    axes[0].plot(snr_values, rmse_g_mean, linewidth=2, label="Середнє RMSE GF")
    axes[0].set_xticks(np.arange(-10, 21, 2))
    axes[0].set_xlabel("SNR (дБ)")
    axes[0].set_ylabel("RMSE")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_title("Лінійний масштаб")
    axes[1].scatter(snr_scatter_wt_rmse, rmse_scatter_wt, color='red', alpha=0.05, label="Окремі значення RMSE")
    axes[1].plot(snr_values, rmse_wt_mean, linewidth=2, label="Середнє RMSE WT")
    axes[1].scatter(snr_scatter_g_rmse, rmse_scatter_g, color='green', alpha=0.05, label="Окремі значення RMSE")
    axes[1].plot(snr_values, rmse_g_mean, linewidth=2, label="Середнє RMSE GF")
    axes[1].set_xticks(np.arange(-10, 21, 1))
    axes[1].set_xlabel("SNR (дБ)")
    axes[1].set_ylabel("RMSE")
    axes[1].grid(True)
    axes[1].set_yscale('log')
    axes[1].legend()
    axes[1].set_title("Логарифмічний масштаб")
    plt.tight_layout()
    plt.savefig("RMSE-SNR.png", dpi=600)
    plt.show()

    snr_scatter_wt_r2 = []
    r2_scatter_wt = []
    snr_scatter_g_r2 = []
    r2_scatter_g = []

    for snr, r2_list in zip(snr_values, r2_wt_list):
        snr_scatter_wt_r2.extend([snr] * len(r2_list))
        r2_scatter_wt.extend(r2_list)

    for snr, r2_list in zip(snr_values, r2_g_list):
        snr_scatter_g_r2.extend([snr] * len(r2_list))
        r2_scatter_g.extend(r2_list)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(snr_scatter_wt_r2, r2_scatter_wt, color='red', alpha=0.05, label="Окремі значення R2")
    axes[0].plot(snr_values, r2_wt_mean, linewidth=2, label="Середнє R2 WT")
    axes[0].scatter(snr_scatter_g_r2, r2_scatter_g, color='green', alpha=0.05, label="Окремі значення R2")
    axes[0].plot(snr_values, r2_g_mean, linewidth=2, label="Середнє R2 GF")
    axes[0].set_xticks(np.arange(-10, 21, 2))
    axes[0].set_xlabel("SNR (дБ)")
    axes[0].set_ylabel("R2")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_title("Лінійний масштаб")
    axes[1].scatter(snr_scatter_wt_r2, r2_scatter_wt, color='red', alpha=0.05, label="Окремі значення R2")
    axes[1].plot(snr_values, r2_wt_mean, linewidth=2, label="Середнє R2 WT")
    axes[1].scatter(snr_scatter_g_r2, r2_scatter_g, color='green', alpha=0.05, label="Окремі значення R2")
    axes[1].plot(snr_values, r2_g_mean, linewidth=2, label="Середнє R2 GF")
    axes[1].set_xticks(np.arange(-10, 21, 1))
    axes[1].set_xlabel("SNR (дБ)")
    axes[1].set_ylabel("R2")
    axes[1].grid(True)
    axes[1].legend()
    axes[1].set_title("Логарифмічний масштаб")
    plt.tight_layout()
    plt.savefig("R2-SNR.png", dpi=600)
    plt.show()

    snr_scatter_wt_d = []
    d_scatter_wt = []
    snr_scatter_g_d = []
    d_scatter_g = []

    for snr, d_list in zip(snr_values, d_wt_list):
        snr_scatter_wt_d.extend([snr] * len(d_list))
        d_scatter_wt.extend(d_list)

    for snr, d_list in zip(snr_values, d_g_list):
        snr_scatter_g_d.extend([snr] * len(d_list))
        d_scatter_g.extend(d_list)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(snr_scatter_wt_d, d_scatter_wt, color='red', alpha=0.05, label="Окремі значення D")
    axes[0].plot(snr_values, d_wt_mean, linewidth=2, label="Середнє D WT")
    axes[0].scatter(snr_scatter_g_d, d_scatter_g, color='green', alpha=0.05, label="Окремі значення D")
    axes[0].plot(snr_values, d_g_mean, linewidth=2, label="Середнє D GF")
    axes[0].set_xticks(np.arange(-10, 21, 2))
    axes[0].set_xlabel("SNR (дБ)")
    axes[0].set_ylabel("D (дисперсія похибки)")
    axes[0].grid(True)
    axes[0].legend()
    axes[0].set_title("Лінійний масштаб")
    axes[1].scatter(snr_scatter_wt_d, d_scatter_wt, color='red', alpha=0.05, label="Окремі значення D")
    axes[1].plot(snr_values, d_wt_mean, linewidth=2, label="Середнє D WT")
    axes[1].scatter(snr_scatter_g_d, d_scatter_g, color='green', alpha=0.05, label="Окремі значення D")
    axes[1].plot(snr_values, d_g_mean, linewidth=2, label="Середнє D GF")
    axes[1].set_xticks(np.arange(-10, 21, 1))
    axes[1].set_xlabel("SNR (дБ)")
    axes[1].set_ylabel("D (дисперсія похибки)")
    axes[1].grid(True)
    axes[1].set_yscale('log')
    axes[1].legend()
    axes[1].set_title("Логарифмічний масштаб")
    plt.tight_layout()
    plt.savefig("D-SNR.png", dpi=600)
    plt.show()


if __name__ == "__main__":
    filtration_efficiency()

    # wavelet_shifted_filter()
    '''results = []
    row = []
    headers = ['MSE', 'MAE', 'RMSE', 'R2', 'D']

    data_original, fs_original = sf.read(NAME_ORIGINAL_WAV)
    wav_files = glob.glob("./Sounds/*.wav")

    for sounds in wav_files:
        sounds = sounds.replace("\\", "/")
        if sounds == NAME_ORIGINAL_WAV:
            continue
        elif sounds == NAME_RESAMPLED_WAV:
            row.append('Ресемпл 4КГц')
            data, fs = sf.read(sounds)
            data = resample(data, len(data_original))
        else:
            type_filter = sounds.replace('./Sounds/Filtered_', '')
            type_filter = type_filter.replace('.wav', '')
            type_filter = type_filter.replace('_', ' ')
            if type_filter == '4000[Hz] 2[byte]':
                type_filter = 'Лінійний фільтр 4 КГц'
            row.append(type_filter)
            data, fs = sf.read(sounds)
            if len(data) != len(data_original):
                data = resample(data, len(data_original))

        mse = mean_squared_error(data_original, data)
        mae = mean_absolute_error(data_original, data)
        rmse = np.sqrt(mse)
        r2 = r2_score(data_original, data)
        D = np.var(data_original - data)

        results.append([
            to_scientific_pretty(mse),
            to_scientific_pretty(mae),
            to_scientific_pretty(rmse),
            round(r2, 2),
            to_scientific_pretty(D)
        ])

    n_rows = len(row)
    n_cols = len(headers)

    fig, ax = plt.subplots(figsize=(n_cols * 2.8, n_rows * 0.4))

    table = ax.table(
        cellText=results,
        rowLabels=row,
        colLabels=headers,
        loc='center',
        bbox=[0.08, 0, 1, 1]
    )

    ax.axis('off')
    plt.savefig("results.png", dpi=600)
    plt.show()'''