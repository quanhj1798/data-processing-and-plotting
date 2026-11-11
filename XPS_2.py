#!/usr/bin/env -S nix develop ./matplotlib --command python3
import pandas
import matplotlib.pyplot
import matplotlib.ticker
import style


style.apply_style()

# loading
data_C1s = pandas.read_csv('data_C1s.csv')
data_V2p = pandas.read_csv('data_V2p.csv')
labels = pandas.read_csv('centers.csv')

# plotting_C1s
figure_C1s, (fitting_C1s, residual_C1s) = matplotlib.pyplot.subplots(nrows=2, gridspec_kw={'height_ratios': [5, 1], 'hspace': 0}, sharex=True)
fitting_C1s.set_xlim(left=300, right=280)
fitting_C1s.set_ylim(bottom=0, top=data_C1s['intensity'].max() * 1.5)
residual_C1s.set_ylim(bottom=-data_C1s['residual'].max() * 1.2, top=data_C1s['residual'].max() * 1.2)
fitting_C1s.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
residual_C1s.tick_params(left=False, labelleft=False)
fitting_C1s.set_ylabel(r'Intensity (\unit{\au})')
residual_C1s.set_xlabel(r'Binding energy (\unit{\electronvolt})')
residual_C1s.set_ylabel(r'Residual', fontsize=10)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['intensity'], marker='o', linestyle='none', markersize=3, markeredgewidth=0.3, markerfacecolor='none', markeredgecolor=style.ColorPalette.black)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['result'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.black)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['component_background'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.black)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['component_C1C'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.black)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['component_C1O'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.black)
fitting_C1s.plot(data_C1s['binding_energy'], data_C1s['component_C3O'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.black)
residual_C1s.plot(data_C1s['binding_energy'], data_C1s['residual'], linestyle='solid', linewidth=0.9, color=style.ColorPalette.black)
residual_C1s.axhline(y=0, linestyle='dashed', linewidth=1.2, color=style.ColorPalette.gray)
fitting_C1s.text(
    x=labels['center_peak_C1C'][0], 
    y=0.7,
    s=r'\ce{C-C}' + '\n' + rf'\qty{{{labels['center_peak_C1C'][0]:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_C1s.get_xaxis_transform(),
    horizontalalignment='center'
)
fitting_C1s.text(
    x=labels['center_peak_C1O'][0],
    y=0.4,
    s=r'\ce{C-O}' + '\n' + rf'\qty{{{labels['center_peak_C1O'][0]:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_C1s.get_xaxis_transform(),
    horizontalalignment='center'
)

fitting_C1s.text(
    x=labels['center_peak_C3O'][0],
    y=0.25,
    s=r'\ce{O-C=O}' + '\n' + rf'\qty{{{labels['center_peak_C3O'][0]:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_C1s.get_xaxis_transform(),
    horizontalalignment='center'
)

# plotting_V2p
figure_V2p, (fitting_V2p, residual_V2p) = matplotlib.pyplot.subplots(nrows=2, gridspec_kw={'height_ratios': [5, 1], 'hspace': 0}, sharex=True)
fitting_V2p.set_xlim(left=540, right=510)
fitting_V2p.set_ylim(bottom=0, top=data_V2p['intensity'].max() * 1.5)
residual_V2p.set_ylim(bottom=-data_V2p['residual'].max() * 1.2, top=data_V2p['residual'].max() * 1.2)
fitting_V2p.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
residual_V2p.tick_params(left=False, labelleft=False)
fitting_V2p.set_ylabel(r'Intensity (\unit{\au})')
residual_V2p.set_xlabel(r'Binding energy (\unit{\electronvolt})')
residual_V2p.set_ylabel(r'Residual', fontsize=10)
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['intensity'], marker='o', linestyle='none', markersize=3, markeredgewidth=0.3, markerfacecolor='none', markeredgecolor=style.ColorPalette.black)
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['result'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.black)
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['component_background'], linestyle='solid', linewidth=1.5, color=style.ColorPalette.black)
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['component_OV'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.black)
fitting_V2p.fill_between(data_V2p['binding_energy'], data_V2p['component_background'], data_V2p['component_V4'], where=(data_V2p['component_V4'] > data_V2p['component_background']), color=style.ColorPalette.blue, alpha=0.3, edgecolor='none')
fitting_V2p.fill_between(data_V2p['binding_energy'], data_V2p['component_background'], data_V2p['component_V5'], where=(data_V2p['component_V5'] > data_V2p['component_background']), color=style.ColorPalette.orange, alpha=0.3, edgecolor='none')
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['component_V5_satellite'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.orange)
fitting_V2p.plot(data_V2p['binding_energy'], data_V2p['component_OC'], linestyle='solid', linewidth=1.2, color=style.ColorPalette.black)
residual_V2p.plot(data_V2p['binding_energy'], data_V2p['residual'], linestyle='solid', linewidth=0.9, color=style.ColorPalette.black)
residual_V2p.axhline(y=0, linestyle='dashed', linewidth=1.6, color=style.ColorPalette.gray)
fitting_V2p.text(
    x=labels['center_peak_OV'][0], 
    y=0.7,
    s=r'\ce{O-V-O}' + '\n' + rf'\qty{{{labels['center_peak_OV'][0]:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_V2p.get_xaxis_transform(),
    horizontalalignment='center'
)
fitting_V2p.text(
    x=labels['center_peak_V4'][0], 
    y=0.4,
    s=r'\Vfour~$2\mathrm{p}_{3/2}$' + '\n' + rf'\qty{{{labels['center_peak_V4'][0]:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_V2p.get_xaxis_transform(),
    horizontalalignment='center',
    color=style.ColorPalette.blue
)
fitting_V2p.text(
    x=labels['center_peak_V5'][0] + 7.33, 
    y=0.3,
    s=r'\Vfive~$2\mathrm{p}_{1/2}$' + '\n' + rf'\qty{{{labels['center_peak_V5'][0] + 7.33:.2f}}}{{\electronvolt}}',
    fontsize=8,
    transform=fitting_V2p.get_xaxis_transform(),
    horizontalalignment='center',
    color=style.ColorPalette.orange
)

# saving
figure_C1s.savefig('figure_C1s.pdf')
figure_V2p.savefig('figure_V2p.pdf')
matplotlib.pyplot.show()
