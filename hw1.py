import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# 維基百科公式
def myNormal(mu, variance, x):
    return (1 / (variance * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / variance) ** 2)

def myCDF(mu, variance, x):
    return 0.5 * (1 + erf((x - mu) / (variance * np.sqrt(2))))

def plot_pdf(mu, variance, x_value, color, ax,i):
    x = np.linspace(mu - 4 * variance, mu + 4 * variance, 1000)
    y_pdf = myNormal(mu, variance, x)
    ax.plot(x, y_pdf, label=f'PDF {i+1}(mu={mu}, var={variance})', color=color) # 給予圖上LABEL

def plot_cdf(mu, variance, x_value, color, ax,i):
    x = np.linspace(mu - 4 * variance, mu + 4 * variance, 1000)
    y_cdf = myCDF(mu, variance, x)
    ax.plot(x, y_cdf, label=f'CDF {i+1}(mu={mu}, var={variance})', color=color) # 給予圖上LABEL

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 輸入轉換浮點數
x = float(input('輸入 x 的值: '))

# 參數
mu_list = [0, 0, 0, -2]
variance_list = [0.2, 1.0, 5.0, 0.5]
colors_pdf = ['blue', 'green', 'purple', 'orange']
colors_cdf = ['blue', 'green', 'purple', 'orange']


fig, (ax_pdf, ax_cdf) = plt.subplots(1, 2, figsize=(14, 6))

# 繪製PDF CDF
for i in range(4):
    plot_pdf(mu_list[i], variance_list[i], x, colors_pdf[i], ax_pdf,i)
    plot_cdf(mu_list[i], variance_list[i], x, colors_cdf[i], ax_cdf,i)

# PDF圖表
ax_pdf.set_title('概率密度函數 (PDF)')
ax_pdf.set_xlabel('x')
ax_pdf.set_ylabel('密度')
ax_pdf.legend()

# CDF圖表
ax_cdf.set_title('累積分布函數 (CDF)')
ax_cdf.set_xlabel('x')
ax_cdf.set_ylabel('累積機率')
ax_cdf.legend()

plt.tight_layout()
plt.show()
