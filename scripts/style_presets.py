#!/usr/bin/env python3
"""
Matplotlib style presets for autoresearch-skill visualizations.
Embedded from /scientific-visualization skill for cross-platform portability.

Usage in any visualize.py:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
    from style_presets import rcparams
    rcparams()  # MUST be called before any plt.subplots()
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
from matplotlib import font_manager

# Okabe-Ito colorblind-friendly palette
OKABE_ITO = [
    '#E69F00',  # Orange
    '#56B4E9',  # Sky Blue
    '#009E73',  # Bluish Green
    '#F0E442',  # Yellow
    '#0072B2',  # Blue
    '#D55E00',  # Vermillion
    '#CC79A7',  # Reddish Purple
    '#000000',  # Black
]


def rcparams():
    """Apply publication-ready style. Call before any figure creation."""
    # Font: Pretendard > Arial > system default
    rcParams['font.family'] = 'sans-serif'
    available = {f.name for f in font_manager.fontManager.ttflist}
    if 'Pretendard' in available:
        rcParams['font.sans-serif'] = ['Pretendard']
    elif 'Arial' in available:
        rcParams['font.sans-serif'] = ['Arial']

    # Font sizes
    rcParams['font.size'] = 14
    rcParams['axes.titlesize'] = 18
    rcParams['axes.titleweight'] = 'normal'
    rcParams['axes.titlepad'] = 10
    rcParams['axes.labelsize'] = 16
    rcParams['axes.labelweight'] = 'normal'
    rcParams['axes.labelpad'] = 8
    rcParams['xtick.labelsize'] = 12
    rcParams['ytick.labelsize'] = 12

    # Ticks: inward, minor visible
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'
    rcParams['xtick.minor.visible'] = True
    rcParams['ytick.minor.visible'] = True
    rcParams['xtick.major.width'] = 1
    rcParams['ytick.major.width'] = 1
    rcParams['xtick.minor.width'] = 0.5
    rcParams['ytick.minor.width'] = 0.5
    rcParams['xtick.major.size'] = 5
    rcParams['ytick.major.size'] = 5
    rcParams['xtick.minor.size'] = 3
    rcParams['ytick.minor.size'] = 3
    rcParams['xtick.major.pad'] = 7
    rcParams['ytick.major.pad'] = 7
    rcParams['xtick.color'] = 'black'
    rcParams['ytick.color'] = 'black'

    # Axes
    rcParams['axes.linewidth'] = 1
    rcParams['axes.edgecolor'] = 'black'
    rcParams['axes.labelcolor'] = 'black'
    rcParams['axes.axisbelow'] = True
    rcParams['axes.grid'] = False
    rcParams['axes.prop_cycle'] = mpl.cycler(color=OKABE_ITO)

    # Figure: WHITE background
    rcParams['figure.figsize'] = (5, 4)
    rcParams['figure.dpi'] = 100
    rcParams['figure.facecolor'] = 'white'
    rcParams['figure.autolayout'] = False

    # Lines
    rcParams['lines.linewidth'] = 1.5
    rcParams['lines.markersize'] = 5
    rcParams['lines.markeredgewidth'] = 0.5

    # Legend: black border, fully opaque
    rcParams['legend.fontsize'] = 12
    rcParams['legend.frameon'] = True
    rcParams['legend.edgecolor'] = 'black'
    rcParams['legend.framealpha'] = 1
    rcParams['legend.loc'] = 'best'

    # Save: DPI > 500
    rcParams['savefig.dpi'] = 600
    rcParams['savefig.bbox'] = 'tight'
    rcParams['savefig.pad_inches'] = 0.05
    rcParams['savefig.transparent'] = False
    rcParams['savefig.facecolor'] = 'white'

    # Colormap
    rcParams['image.cmap'] = 'viridis'
