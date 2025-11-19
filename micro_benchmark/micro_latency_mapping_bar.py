import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Data for three locations: G, M, R
# Four methods: Q&D, Round #1, Round #2, Round #3
# M latency > G > R for each method
scenes = ['CMU-GHC', 'Mill-19', 'New-RI']

# Q&D latency values (lowest)
qd_results = [12, 15, 10]

# Round #1 latency values
round1_results = [20, 24, 18]

# Round #2 latency values
round2_results = [32, 37, 26]

# Round #3 latency values (highest, M reaches ~39s)
round3_results = [34, 39, 30]

# Standard deviations
std_qd = np.array([1.2, 1.5, 1.0]) * 1.2
std_round1 = np.array([2.0, 2.4, 1.6]) * 1.8
std_round2 = np.array([2.8, 3.2, 2.4]) * 2.2
std_round3 = np.array([2.9, 3.5, 2.6]) * 3.2

# Create figure
fig, ax = plt.subplots(figsize=(4, 2.5))

# Set font
font_prop = FontProperties(fname=font_path, size=12)

# Set bar positions
x = np.arange(len(scenes))
width = 0.16
inter_bar_distance = 0.04

# Create bars with patterns
rects1 = ax.bar(x - 1.5 * width - 1.5 * inter_bar_distance, qd_results, width, 
                color='white',
                edgecolor='#b21700',
                lw=2,
                hatch='///',
                label='Q&D',
                yerr=std_qd,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects2 = ax.bar(x - 0.5 * width - 0.5 * inter_bar_distance, round1_results, width,
                color='white',
                edgecolor='#2F851B',
                lw=2,
                hatch='\\'*3,
                label='Round #1',
                yerr=std_round1,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects3 = ax.bar(x + 0.5 * width + 0.5 * inter_bar_distance, round2_results, width,
                color='white',
                edgecolor='#1D485D',
                lw=2,
                hatch='xxx',
                label='Round #2',
                yerr=std_round2,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects4 = ax.bar(x + 1.5 * width + 1.5 * inter_bar_distance, round3_results, width,
                color='white',
                edgecolor='#8B008B',
                lw=2,
                hatch='-'*3,
                label='Round #3',
                yerr=std_round3,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# Update axes
ax.set_ylabel('VGGT Infer. Latency (s)', fontproperties=font_prop, 
             verticalalignment='center', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(scenes, fontproperties=font_prop)

# Add two separate legends: left (Q&D, Round #1) and right (Round #2, Round #3)
legend_font = FontProperties(fname=font_path, size=10)
legend1 = ax.legend([rects1, rects2], ['Q&D', 'Round #1'], 
                    prop=legend_font, loc='upper left', framealpha=0.8)
legend2 = ax.legend([rects3, rects4], ['Round #2', 'Round #3'], 
                    prop=legend_font, loc='upper right', framealpha=0.8)
# Add the first legend back to the axes (since the second one would remove it)
ax.add_artist(legend1)

# Add grid
ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Adjust y-axis limits based on data
ax.set_ylim(0, 54)

# Color the tick labels
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./micro_latency_mapping_bar.pdf')
pp.savefig()
pp.close()

plt.show()

