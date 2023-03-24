import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# 创建一个长度为1000的Hamming窗
window = signal.get_window('hamming', 64)

# 在窗口上应用FFT并计算幅度谱
fft_vals = np.abs(np.fft.fft(window, 2048))

# 创建归一化频率轴
freqs = np.fft.fftfreq(2048, 1/1000)
freqs_norm = freqs[:1024] / 500

# 绘制频域图像
plt.plot(freqs_norm, 20*np.log10(fft_vals[:1024]))
plt.xlim(0, 1)
plt.ylim(-100,50)
plt.xlabel('Normalized Frequency')
plt.ylabel('Magnitude (dB)')
plt.title('Hamming Window Frequency Response')
plt.grid()
plt.show()
