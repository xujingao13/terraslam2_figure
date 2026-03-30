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
# Three point types: Corner Points, Edge Points, Surface Points
scenes = ['CMU-GHC', 'Mill-19', 'CMU-RIC']

# Corner Points completeness rate (highest, ~98%)
corner_results = np.array([97.2, 98.8, 99.1])

# Edge Points completeness rate (medium, ~95%)
edge_results = np.array([94.3, 95.9, 96.1])

# Surface Points completeness rate (lowest, 89-92%)
surface_results = np.array([90.2, 92.5, 93.8])

# Standard deviations (smaller for higher completeness)
std_corner = np.array([0.8, 0.9, 0.7]) * 0.3
std_edge = np.array([1.1, 1.2, 1.0]) * 0.5
std_surface = np.array([1.5, 1.8, 1.4]) * 0.9

# Create figure
fig, ax = plt.subplots(figsize=(4, 2.5))

# Set font
font_prop = FontProperties(fname=font_path, size=12)

# Set bar positions
x = np.arange(len(scenes))
width = 0.16
inter_bar_distance = 0.04

# Create bars with patterns
rects1 = ax.bar(x - (width + inter_bar_distance), corner_results, width, 
                color='white',
                edgecolor='#b21700',
                lw=2,
                hatch='///',
                label='Corner Points',
                yerr=std_corner,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects2 = ax.bar(x, edge_results, width,
                color='white',
                edgecolor='#1D485D',
                lw=2,
                hatch='\\'*3,
                label='Edge Points',
                yerr=std_edge,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects3 = ax.bar(x + (width + inter_bar_distance), surface_results, width,
                color='white',
                edgecolor='#2F851B',
                lw=2,
                hatch='xxx',
                label='Surface Points',
                yerr=std_surface,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# Update axes
ax.set_ylabel('Completeness Rate (%)', fontproperties=font_prop, 
             verticalalignment='center', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(scenes, fontproperties=font_prop)

# Add legend - left side with two items, right side with one item
legend_font = FontProperties(fname=font_path, size=10)
legend1 = ax.legend([rects1, rects2], ['Corner Points', 'Edge Points'], 
                    prop=legend_font, loc='upper left', framealpha=0.8)
legend2 = ax.legend([rects3], ['Surface Points'], 
                    prop=legend_font, loc='upper right', framealpha=0.8)
# Add the first legend back to the axes (since second legend removes it)
ax.add_artist(legend1)

# Add grid
ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Adjust y-axis limits based on data (percentage from 85 to 100)
ax.set_ylim(85, 103)

# Set y-axis ticks every 5
ax.set_yticks(np.arange(85, 101, 5))

# Color the tick labels
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./rob_completeness_cat_point_bar.pdf')
pp.savefig()
pp.close()

plt.show()

