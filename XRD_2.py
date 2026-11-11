#!/usr/bin/env -S nix develop ./matplotlib --command python3
import pandas
import matplotlib.pyplot
import matplotlib.ticker
import style


style.apply_style()

# loading
theoretical_diffraction_peaks = pandas.read_csv('theoretical_diffraction_peaks.csv')
experimental_diffraction_peaks = pandas.read_csv('experimental_diffraction_peaks.csv')
labels = [r'', r'', r'', r'ICSD\#']
baseline = experimental_diffraction_peaks[['intensity_1', 'intensity_2', 'intensity_3']].max().max()

# plotting
figure, diffraction_peaks = matplotlib.pyplot.subplots()
diffraction_peaks.set_xlim(left=5, right=80)
diffraction_peaks.set_ylim(bottom=0, top=baseline * 1.5)
diffraction_peaks.spines[['top', 'left', 'right']].set_visible(False)
diffraction_peaks.tick_params(left=False, labelleft=False)
diffraction_peaks.set_xlabel(r'$2\theta$ (\unit{\degree})')
diffraction_peaks.set_ylabel(r'Intensity (\unit{\au})')
diffraction_peaks.plot(experimental_diffraction_peaks['2theta'], experimental_diffraction_peaks['intensity_1'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.blue, label=labels[0])
diffraction_peaks.plot(experimental_diffraction_peaks['2theta'], experimental_diffraction_peaks['intensity_2'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.orange, label=labels[1])
diffraction_peaks.plot(experimental_diffraction_peaks['2theta'], experimental_diffraction_peaks['intensity_3'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.purple, label=labels[2])
diffraction_peaks.vlines(x=theoretical_diffraction_peaks['2theta'], ymin=0, ymax=(theoretical_diffraction_peaks['intensity'] / 100) * (baseline / 10), linestyle='solid', linewidth=1.5, color=style.ColorPalette.black, label=labels[3])
diffraction_peaks.legend(frameon=False)
# diffraction_peaks.axvline(x=0, linestyle='dashed', linewidth=1.2, color=style.ColorPalette.gray)
# diffraction_peaks.axhline(y=0, linestyle='dashed', linewidth=1.2, color=style.ColorPalette.gray)

# annotating
masks = [
    (experimental_diffraction_peaks['2theta'] > 10) & (experimental_diffraction_peaks['2theta'] < 20),
    (experimental_diffraction_peaks['2theta'] > 20) & (experimental_diffraction_peaks['2theta'] < 30),
    (experimental_diffraction_peaks['2theta'] > 30) & (experimental_diffraction_peaks['2theta'] < 40)
]
indices = [
    experimental_diffraction_peaks['intensity_1'][masks[0]].idxmax(),
    experimental_diffraction_peaks['intensity_1'][masks[1]].idxmax(),
    experimental_diffraction_peaks['intensity_1'][masks[2]].idxmax()
]
diffraction_peaks.text(
    x=experimental_diffraction_peaks['2theta'][indices[0]],
    y=0.7,
    s=r'(001)',
    transform=diffraction_peaks.get_xaxis_transform(),
    horizontalalignment='center'
)

# saving
figure.savefig('figure.pdf')
matplotlib.pyplot.show()
