import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import os
import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Generate approximate data with different distribution shapes
def generate_data(mean, min_val, max_val, p99, alpha, beta, size=10000):
    # Use beta distribution with different parameters to create different shapes
    # Higher alpha/beta ratio = more concentrated (steeper curve)
    # Lower alpha/beta ratio = more spread out (flatter curve with longer tail)
    data = np.random.beta(alpha, beta, size)
    
    # Scale and shift to match desired range and mean
    range_size = max_val - min_val
    data = data * range_size + min_val  # Scale to range
    data = data - np.mean(data) + mean  # Shift to desired mean
    
    # Fine-tune to match p99 more accurately
    for _ in range(10):
        current_p99 = np.percentile(data, 99)
        if abs(current_p99 - p99) < 0.01:
            break
        p99_diff = p99 - current_p99
        # Adjust more for higher values
        adjustment = np.where(data > np.percentile(data, 50),
                             p99_diff * 0.6 * (data - np.percentile(data, 50)) / (current_p99 - np.percentile(data, 50)),
                             0)
        data = data + adjustment
        # Re-center mean
        data = data - np.mean(data) + mean
    
    return data

# Slow speed (<5m/s): best performance, RMSE≈1.5, mean≈1.2, p99≈2.8
# Use higher alpha/beta ratio for more concentrated distribution (steeper curve)
slow_data = generate_data(mean=1.2, min_val=0.3, max_val=3.5, p99=2.8, alpha=3, beta=4, size=10000)

# Medium speed (5-10m/s): moderate performance, worse than slow but better than fast
# mean≈1.8, p99≈3.4, medium spread
medium_data = generate_data(mean=1.5, min_val=0.4, max_val=4.1, p99=3.4, alpha=2, beta=3.5, size=10000)

# Fast speed (>10m/s): worse performance, some degradation
# mean≈2.2, p99≈4.0, more spread out with longer tail (flatter curve)
fast_data = generate_data(mean=2.3, min_val=0.8, max_val=5.1, p99=4.5, alpha=1.5, beta=2.5, size=10000)

# Calculate CDF using sorted data for smoother curves
def calc_cdf(data):
    sorted_data = np.sort(data)
    x = np.linspace(0, 6, 1000)  # Fine-grained x values for smooth plotting
    y = np.searchsorted(sorted_data, x, side='right') / len(sorted_data)
    return x, y

# Set chart style
plt.figure(figsize=(4, 2.5))
ax = plt.subplot()

# 直接指定 Helvetica 字体文件路径
font_prop = FontProperties(fname=font_path, size=12)

# 在需要使用字体的地方使用 font_prop
plt.xlabel('ICP Error (m)', fontproperties=font_prop, verticalalignment='center', labelpad=10)
plt.ylabel('CDF', fontproperties=font_prop, verticalalignment='center', labelpad=10)

# Plot CDF
x_slow, y_slow = calc_cdf(slow_data)
x_medium, y_medium = calc_cdf(medium_data)
x_fast, y_fast = calc_cdf(fast_data)

plt.plot(x_slow, y_slow, '-', zorder=2, lw=2, color='#b21700', label='Corner Points')
plt.plot(x_medium, y_medium, '--', zorder=2, lw=2, color='#1D485D', label='Edge Points')
plt.plot(x_fast, y_fast, '-.', zorder=2, lw=2, color='#2F851B', label='Surface Points')

# Set ticks, grid, and labels
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontproperties(font_prop)
plt.grid(linestyle='--', linewidth=0.5, zorder=1)
plt.ylim(0, 1.02)
plt.xlim(0, 5)
leg = plt.legend(loc='best', prop={'size': 10})
leg.get_frame().set_edgecolor('#000000')
leg.get_frame().set_linewidth(0.5)

# Add mean and 99th percentile markers
for data, x, y, color in [(slow_data, x_slow, y_slow, '#b21700'), 
                         (medium_data, x_medium, y_medium, '#1D485D'),
                         (fast_data, x_fast, y_fast, '#2F851B')]:
    mean = np.mean(data)
    percentile_99 = np.percentile(data, [99])[0]
    
    # Find the y value on CDF curve corresponding to mean
    mean_idx = np.abs(x - mean).argmin()
    mean_y = y[mean_idx]
    
    # Find the y value on CDF curve corresponding to p99
    p99_idx = np.abs(x - percentile_99).argmin()
    p99_y = y[p99_idx]
    
    # Plot mean point with square
    plt.plot(mean, mean_y, color=color, marker='s', markersize=5)
    
    # Plot 99th percentile point with circle
    plt.plot(percentile_99, p99_y, color=color, marker='o', markersize=5)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./rob_accuracy_cat_point_CDF.pdf')
pp.savefig()
pp.close()

# Display the chart
plt.show()

