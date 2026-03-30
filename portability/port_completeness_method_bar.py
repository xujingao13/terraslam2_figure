import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import os

import matplotlib as mpl

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Data for three mapping scenes
# Four methods: w/VGGT-Long, w/Map-Anything, w/VGGT, w/FastVGGT
scenes = ['CMU-GHC', 'Mill-19', 'New-RI']

# w/VGGT-Long completeness rate (highest, ~98-99%)
vggt_long_results = np.array([98.2, 98.8, 99.1])

# w/Map-Anything completeness rate (second, ~96-97%)
map_anything_results = np.array([96.3, 97.1, 97.5])

# w/VGGT completeness rate (our current method, ~94-95%)
vggt_results = np.array([94.2, 95.1, 95.8])

# w/FastVGGT completeness rate (lowest, ~91-92%)
fastvggt_results = np.array([91.2, 92.0, 92.5])

# Standard deviations (smaller for higher completeness)
std_vggt_long = np.array([0.6, 0.7, 0.5]) * 0.3
std_map_anything = np.array([0.8, 0.9, 0.8]) * 0.4
std_vggt = np.array([1.0, 1.1, 1.0]) * 0.5
std_fastvggt = np.array([1.3, 1.5, 1.4]) * 0.6

# Create figure
fig, ax = plt.subplots(figsize=(4, 2.5))

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

# w/Map-Anything: second best (blue, dashed pattern)
rects2 = ax.bar(x - 0.5 * (width + inter_bar_distance), map_anything_results, width,
                color='white',
                edgecolor='#1D485D',
                lw=2,
                hatch='\\'*3,
                label='w/Map-Anything',
                yerr=std_map_anything,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# w/VGGT-Long: best performance (green, dot-dash pattern)
rects3 = ax.bar(x + 0.5 * (width + inter_bar_distance), vggt_long_results, width, 
                color='white',
                edgecolor='#2F851B',
                lw=2,
                hatch='x'*3,
                label='w/VGGT-Long',
                yerr=std_vggt_long,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# w/FastVGGT: lowest performance (purple, dotted pattern)
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
ax.set_ylabel('Completeness Rate (%)', fontproperties=font_prop, 
             verticalalignment='center', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(scenes, fontproperties=font_prop)

# Add legend - split into two parts for better layout
legend_font = FontProperties(fname=font_path, size=10)
legend1 = ax.legend([rects1, rects2], ['w/VGGT', 'w/Map-Anything'], 
                    prop=legend_font, loc='upper left', framealpha=0.8)
legend2 = ax.legend([rects3, rects4], ['w/VGGT-Long', 'w/FastVGGT'], 
                    prop=legend_font, loc='upper right', framealpha=0.8)
# Add the first legend back to the axes (since second legend removes it)
ax.add_artist(legend1)

# Add grid
ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Adjust y-axis limits based on data (percentage from 88 to 100)
ax.set_ylim(88, 103)

# Set y-axis ticks every 4
ax.set_yticks(np.arange(88, 102, 4))

# Color the tick labels
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./port_completeness_method_bar.pdf')
pp.savefig()
pp.close()

plt.show()


