import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, 'Helvetica.ttf')

# Data for three locations: G, M, R
# Three methods: Q&D, Round #1, Round #2
# M latency > G > R for each method
scenes = ['CMU-GHC', 'Mill-19', 'New-RI']

# Q&D latency values (lowest)
qd_results = np.array([7, 9, 6]) * 1

# Round #1 latency values
round1_results = np.array([12, 14, 11]) * 1.3

# Round #2 latency values
round2_results = np.array([18, 20, 15]) * 1.9

# Standard deviations (proportional to mapping latency)
std_qd = np.array([0.7, 0.9, 0.6]) * 1.2
std_round1 = np.array([1.2, 1.4, 1.1]) * 1.4
std_round2 = np.array([1.7, 1.9, 1.4]) * 2.5

# Create figure
fig, ax = plt.subplots(figsize=(4, 2.5))

# Set font
font_prop = FontProperties(fname=font_path, size=12)

# Set bar positions
x = np.arange(len(scenes))
width = 0.16
inter_bar_distance = 0.04

# Create bars with patterns
rects1 = ax.bar(x - (width + inter_bar_distance), qd_results, width, 
                color='white',
                edgecolor='#b21700',
                lw=2,
                hatch='///',
                label='Q&D',
                yerr=std_qd,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects2 = ax.bar(x, round1_results, width,
                color='white',
                edgecolor='#2F851B',
                lw=2,
                hatch='\\'*3,
                label='Round #1',
                yerr=std_round1,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

rects3 = ax.bar(x + (width + inter_bar_distance), round2_results, width,
                color='white',
                edgecolor='#1D485D',
                lw=2,
                hatch='xxx',
                label='Round #2',
                yerr=std_round2,
                capsize=3,
                error_kw=dict(ecolor='#2F2F2F', capthick=1, alpha=0.6))

# Update axes
ax.set_ylabel('Map Eval. Latency (s)', fontproperties=font_prop, 
             verticalalignment='center', labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(scenes, fontproperties=font_prop)

# Add legend
legend_font = FontProperties(fname=font_path, size=10)
ax.legend([rects1, rects2, rects3], ['Q&D', 'Round #1', 'Round #2'], 
          prop=legend_font, loc='upper right', framealpha=0.8)

# Add grid
ax.grid(linestyle='--', linewidth=0.5, alpha=0.3)

# Adjust y-axis limits based on data
ax.set_ylim(0, 45)

# Set y-axis ticks every 10
ax.set_yticks(np.arange(0, 45, 10))

# Color the tick labels
for label in ax.get_yticklabels():
    label.set_fontproperties(font_prop)

plt.tight_layout()

# Save as PDF
pp = PdfPages('./micro_latency_evaluation_bar.pdf')
pp.savefig()
pp.close()

plt.show()

