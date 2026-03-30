import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import PercentFormatter
import os

import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Generate data for Content-level Selection
np.random.seed(42)  # For reproducibility
size = 1000
mean_content = 13.0  # 平均值12-14ms，取中间值
std_content = 2.5  # 标准差，使得p99约18ms

# Generate Content-level Selection data with normal distribution
data_content = np.clip(np.random.normal(mean_content, std_content, size), 5, 20)

# Generate data for Token-level Selection
# 工作原理：随着frame数量增加latency逐步增加，在30ms左右出现高峰，之后是拖尾
mean_token = 25.0  # 平均值25ms左右
p99_token = 35.0  # p99 35ms左右

# 创建混合分布：
# 1. 15-25ms: 逐步增加的部分（40%的数据）
# 2. 28-32ms: 高峰区域（25%的数据，更分散）
# 3. 30ms之后: 拖尾分布（35%的数据，指数衰减）

# 逐步增加的部分
part1 = np.random.normal(18, 2.5, int(size * 0.20))  # 15-20ms
part2 = np.random.normal(22.5, 2.5, int(size * 0.20))  # 20-25ms

# 30ms附近的高峰（更分散，不那么像正态分布）
# 使用更宽泛的分布，在28-32ms范围内
peak_center = 30
peak_std = 3.0  # 增加标准差，让分布更分散
part3 = np.random.normal(peak_center, peak_std, int(size * 0.25))  # 降低比例，增加分散度

# 30ms之后的拖尾（使用指数分布模拟拖尾）
# 从30开始，使用指数分布生成拖尾数据
tail_start = 30
tail_scale = 3.0  # 指数分布的尺度参数
tail_data = tail_start + np.random.exponential(tail_scale, int(size * 0.35))
tail_data = np.clip(tail_data, 30, 40)  # 限制在30-40ms

# 合并所有部分
data_token = np.concatenate([part1, part2, part3, tail_data])
np.random.shuffle(data_token)  # 打乱顺序

# 限制在合理范围
data_token = np.clip(data_token, 12, 40)

# 微调以确保均值约25ms，p99约35ms
current_mean = np.mean(data_token)
current_p99 = np.percentile(data_token, 99)

# 如果均值偏离，进行微调
if current_mean < mean_token - 0.5:
    # 如果均值偏小，增加一些较大的值（在30ms高峰附近）
    adjustment = np.random.normal(30, 2, int(size * 0.05))
    data_token = np.concatenate([data_token, adjustment])
elif current_mean > mean_token + 0.5:
    # 如果均值偏大，增加一些较小的值
    adjustment = np.random.normal(20, 2, int(size * 0.05))
    data_token = np.concatenate([data_token, adjustment])

# 如果p99偏离，进行微调
if current_p99 < p99_token - 1:
    # 增加一些35ms附近的值
    adjustment = np.random.normal(35, 1.5, int(size * 0.03))
    data_token = np.concatenate([data_token, adjustment])
elif current_p99 > p99_token + 1:
    # 移除一些过大的值
    data_token = data_token[data_token < 38]

data_token = np.clip(data_token, 12, 40)  # 最终限制在合理范围

# Create figure
plt.figure(figsize=(4, 2.5))
ax = plt.subplot()

# Set font
font_prop = FontProperties(fname=font_path, size=12)

# Calculate mean and 99th percentile
mean_content = np.mean(data_content)
percentile_99_content = np.percentile(data_content, 99)
mean_token = np.mean(data_token)
percentile_99_token = np.percentile(data_token, 99)

# Calculate common bin edges for both histograms
min_x = min(data_content.min(), data_token.min())
max_x = max(data_content.max(), data_token.max())
bins = np.linspace(min_x, max_x, 41)  # 40 bins需要41个边界点

# Create histogram for Content-level Selection
n, bins, patches = plt.hist(data_content, bins=bins, density=False, weights=np.ones(len(data_content))/len(data_content)*100, 
                          color='#2F851B', alpha=0.7, rwidth=0.9, label='Content-level Selection', zorder=1)

# Create histogram for Token-level Selection
n2, bins2, patches2 = plt.hist(data_token, bins=bins, density=False, weights=np.ones(len(data_token))/len(data_token)*100,
                             color='#1D485D', alpha=0.7, rwidth=0.9, label='Token-level Selection', zorder=2)

# Highlight bars containing mean and 99th percentile
def highlight_bars(patches, mean_val, percentile_val, bins):
    for patch, left, right in zip(patches, bins[:-1], bins[1:]):
        if left <= mean_val <= right:
            patch.set_hatch('/' * 5)      # 添加斜线纹理
            patch.set_edgecolor('darkred')  # 纹理的颜色
            patch.set_zorder(10)      # 确保在最上层
        if left <= percentile_val <= right:
            # patch.set_hatch('\\' * 10)      # 添加斜线纹理
            patch.set_facecolor('darkred')  # 纹理的颜色
            patch.set_zorder(10)      # 确保在最上层

highlight_bars(patches, mean_content, percentile_99_content, bins)
highlight_bars(patches2, mean_token, percentile_99_token, bins2)

# Add legend
plt.legend(loc='upper right', prop={'size': 10})

# Add labels and title
plt.xlabel('KF Selection Latency Distribution (ms)', fontproperties=font_prop, verticalalignment='center', labelpad=10)
plt.ylabel('Percentage', fontproperties=font_prop, verticalalignment='center', labelpad=10)

# Customize ticks and format y-axis as percentage
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))  # 设置decimals=0去掉小数部分
plt.yticks(np.arange(0, 16, 5))  # 每5%一个刻度：0%, 5%, 10%, 15%

# Add grid
plt.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Set axis limits
min_x = min(data_content.min(), data_token.min())
max_x = max(data_content.max(), data_token.max())
# 添加一些边距（比如5%）使图表更美观
margin = (max_x - min_x) * 0.05
x_min = min_x - margin
x_max = max_x + margin
plt.xlim(x_min, x_max)
plt.ylim(0, 15)  # 设置y轴上限为15%

# 设置x轴刻度，每5ms一个刻度
x_ticks = np.arange(np.ceil(x_min / 5) * 5, np.floor(x_max / 5) * 5 + 1, 5)
plt.xticks(x_ticks)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./micro_latency_selection_histogram.pdf')
pp.savefig()
pp.close()

# Display the plot
plt.show()

