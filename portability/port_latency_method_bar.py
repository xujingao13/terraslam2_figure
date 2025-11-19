import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Data for three mapping scenes
# Four methods: w/VGGT-Long, w/Map-Anything, w/VGGT, w/FastVGGT
scenes = ['CMU-GHC', 'Mill-19', 'New-RI']

# w/FastVGGT latency (lowest, fastest)
fastvggt_results = np.array([18.5, 19.2, 15.1])

# w/VGGT latency (our current method, medium)
vggt_results = np.array([34.5, 39.1, 30.8])

# w/Map-Anything latency (slower)
map_anything_results = np.array([45.6, 46.4, 45.8])

# w/VGGT-Long latency (highest, slowest)
vggt_long_results = np.array([58.2, 59.1, 57.5])

# Standard deviations (proportional to latency)
std_fastvggt = np.array([1.8, 1.9, 1.7]) * 2
std_vggt = np.array([2.9, 3.5, 2.6]) * 3.2
std_map_anything = np.array([1.2, 1.3, 1.1]) * 7.6
std_vggt_long = np.array([1.4, 1.5, 1.3]) * 10.8

# Create figure
fig, ax = plt.subplots(figsize=(3.5, 3.5))

# Set font
font_prop = FontProperties(fname=font_path, size=12)

# Set bar positions
x = np.arange(len(scenes))
width = 0.16
inter_bar_distance = 0.04

# Create bars with patterns
# w/VGGT: our current method (red, solid pattern)
rects1 = ax.bar(x - 1.5 * (width + inter_bar_distance), vggt_results, width,
                color='white',
                edgecolor='#b21700',
                lw=2,
                hatch='/'*3,
                label='w/VGGT',
                yerr=std_vggt,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# w/Map-Anything: slower (blue, dashed pattern)
rects2 = ax.bar(x - 0.5 * (width + inter_bar_distance), map_anything_results, width,
                color='white',
                edgecolor='#1D485D',
                lw=2,
                hatch='\\'*3,
                label='w/Map-Anything',
                yerr=std_map_anything,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# w/VGGT-Long: slowest (green, dot-dash pattern)
rects3 = ax.bar(x + 0.5 * (width + inter_bar_distance), vggt_long_results, width, 
                color='white',
                edgecolor='#2F851B',
                lw=2,
                hatch='x'*3,
                label='w/VGGT-Long',
                yerr=std_vggt_long,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# w/FastVGGT: fastest (purple, dotted pattern)
rects4 = ax.bar(x + 1.5 * (width + inter_bar_distance), fastvggt_results, width,
                color='white',
                edgecolor='#7B3F98',
                lw=2,
                hatch='-'*3,
                label='w/FastVGGT',
                yerr=std_fastvggt,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# Update axes
ax.set_ylabel('Latency (s)', fontproperties=font_prop, 
             verticalalignment='center', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(scenes, fontproperties=font_prop)

# Add legend
legend_font = FontProperties(fname=font_path, size=9)
ax.legend(prop=legend_font, loc='best', framealpha=0.6)

# Add grid
ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Adjust y-axis limits based on data
ax.set_ylim(10, 79)

# Set y-axis ticks
# ax.set_yticks(np.arange(0, 24, 4))

# Color the tick labels
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./port_latency_method_bar.pdf')
pp.savefig()
pp.close()

plt.show()

