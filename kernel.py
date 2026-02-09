import numpy as np
import matplotlib.pyplot as plt

# --- Definição dos Kernels ---


def hat(t, center, width):
    return np.maximum(0, 1 - np.abs(t - center) / width)


def box(t, start, end):
    return np.where((t >= start) & (t <= end), 1, 0)


def gaussian(t, center, sigma):
    return np.exp(-0.5 * ((t - center) / sigma) ** 2)


fs = 100.0
T = 10.0
N = int(T * fs)

t = np.linspace(-T / 2, T / 2, N)


freqs = np.fft.fftfreq(N, d=1 / fs)
freqs = np.fft.fftshift(freqs)


def plot_kernel_fft(ax_time, ax_freq, sinal, titulo):

    ax_time.plot(t, sinal, lw=2)
    ax_time.set_title(f"{titulo} (Tempo)")
    ax_time.set_xlabel("Tempo (s)")
    ax_time.grid(True, alpha=0.3)
    ax_time.set_xlim(-3, 3)

    transformada = np.fft.fft(sinal)

    transformada_shift = np.fft.fftshift(transformada)

    magnitude = np.abs(transformada_shift) / N

    ax_freq.plot(freqs, magnitude, color="red", lw=2)
    ax_freq.set_title(f"FFT de {titulo} (Frequência)")
    ax_freq.set_xlabel("Frequência (Hz)")
    ax_freq.grid(True, alpha=0.3)
    ax_freq.set_xlim(-5, 5)


sinal_box = box(t, -1, 1)
sinal_hat = hat(t, 0, 1)
sinal_gauss = gaussian(t, 0, 0.5)

fig, axs = plt.subplots(3, 2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.4)

plot_kernel_fft(axs[0, 0], axs[0, 1], sinal_box, "Box (Retângulo)")

plot_kernel_fft(axs[1, 0], axs[1, 1], sinal_hat, "Hat (Triângulo)")

plot_kernel_fft(axs[2, 0], axs[2, 1], sinal_gauss, "Gaussiana")

plt.show()
