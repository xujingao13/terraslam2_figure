import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import os

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

# w/VGGT-Long: best performance, lowest error
# Use higher alpha/beta ratio for more concentrated distribution (steeper curve)
vggt_long_data = generate_data(mean=1.1, min_val=0.3, max_val=3.1, p99=2.4, alpha=3, beta=4, size=10000)

# w/Map-Anything: better than w/VGGT, but worse than w/VGGT-Long
# mean≈1.4, p99≈2.9, medium spread
map_anything_data = generate_data(mean=1.3, min_val=0.35, max_val=3.4, p99=2.9, alpha=2.5, beta=3.8, size=10000)

# w/VGGT: our current method, baseline performance
# mean≈1.5, p99≈3.1, medium spread
vggt_data = generate_data(mean=1.5, min_val=0.35, max_val=4.0, p99=3.1, alpha=2, beta=3.5, size=10000)

# w/FastVGGT: worse than w/VGGT, highest error
# mean≈1.85, p99≈3.8, more spread out with longer tail (flatter curve)
fastvggt_data = generate_data(mean=1.95, min_val=0.55, max_val=4.8, p99=4.4, alpha=1.5, beta=2.5, size=10000)

# Calculate CDF using sorted data for smoother curves
def calc_cdf(data):
    sorted_data = np.sort(data)
    x = np.linspace(0, 5, 1000)  # Fine-grained x values for smooth plotting
    y = np.searchsorted(sorted_data, x, side='right') / len(sorted_data)
    return x, y

# Set chart style
plt.figure(figsize=(3.5, 3.5))
ax = plt.subplot()

# 直接指定 Helvetica 字体文件路径
font_prop = FontProperties(fname=font_path, size=12)

# 在需要使用字体的地方使用 font_prop
plt.xlabel('ICP Error (m)', fontproperties=font_prop, verticalalignment='center', labelpad=10)
plt.ylabel('CDF', fontproperties=font_prop, verticalalignment='center', labelpad=10)

# Plot CDF
x_vggt_long, y_vggt_long = calc_cdf(vggt_long_data)
x_map_anything, y_map_anything = calc_cdf(map_anything_data)
x_vggt, y_vggt = calc_cdf(vggt_data)
x_fastvggt, y_fastvggt = calc_cdf(fastvggt_data)

plt.plot(x_vggt, y_vggt, '-', zorder=2, lw=2, color='#b21700', label='w/VGGT')
plt.plot(x_map_anything, y_map_anything, '--', zorder=2, lw=2, color='#1D485D', label='w/Map-Anything')
plt.plot(x_vggt_long, y_vggt_long, '-.', zorder=2, lw=2, color='#2F851B', label='w/VGGT-Long')
plt.plot(x_fastvggt, y_fastvggt, ':', zorder=2, lw=2, color='#7B3F98', label='w/FastVGGT')

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
for data, x, y, color in [(vggt_long_data, x_vggt_long, y_vggt_long, '#2F851B'), 
                         (map_anything_data, x_map_anything, y_map_anything, '#1D485D'),
                         (vggt_data, x_vggt, y_vggt, '#b21700'),
                         (fastvggt_data, x_fastvggt, y_fastvggt, '#7B3F98')]:
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
pp = PdfPages('./port_accuracy_method_CDF.pdf')
pp.savefig()
pp.close()

# Display the chart
plt.show()


