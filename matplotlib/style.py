import matplotlib


def apply_style():
    matplotlib.rcParams.update({
        'figure.figsize': [4, 3],
        'figure.autolayout': True,
        'axes.linewidth': 1,
        'axes.edgecolor': '#aaaaaa',
        'xtick.major.width': 1,
        'xtick.major.size': 5,
        'xtick.color': '#aaaaaa',
        'xtick.labelsize': 10,
        'xtick.labelcolor': '#000000',
        'ytick.major.width': 1,
        'ytick.major.size': 5,
        'ytick.color': '#aaaaaa',
        'ytick.labelsize': 10,
        'ytick.labelcolor': '#000000',
        'figure.dpi': 100,
        'savefig.dpi': 600,
        'text.usetex': True,
        'font.size': 12,
        'font.family': 'sans-serif',
        'text.latex.preamble': r'''
            \renewcommand{\familydefault}{\sfdefault}
            \usepackage[T1]{fontenc}
            \usepackage[scaled]{helvet}
            \usepackage{amsmath}
            \usepackage{newtxsf}
            \usepackage{bm}
            \usepackage[version=4]{mhchem}
            \usepackage{siunitx}
            \sisetup{detect-all, range-phrase=--, range-units=single, group-separator={,}}
            \DeclareSIUnit\au{a.u.}
            \DeclareSIUnit{\atom}{atom}
            \DeclareSIUnit\hartree{\ensuremath{\mathit{E}_{\mathrm{h}}}}
            \DeclareSIUnit\bohr{\ensuremath{\mathit{a}_0}}
            \DeclareSIUnit\angstrom{\text{Å}}
            \DeclareSIUnit\molar{M}
            \DeclareSIUnit\gforce{\ensuremath{\mathit{g}}}
            \DeclareSIUnit\USD{USD}
            \newcommand{\Vthree}{\ce{V^{III}}}
            \newcommand{\Vfour}{\ce{V^{IV}}}
            \newcommand{\Vfive}{\ce{V^{V}}}
            \newcommand{\ZnSO}{\qty{2}{\molar}~\ce{ZnSO4}}
            \newcommand{\ZnOTf}{\qty{2}{\molar}~\ce{Zn(OTf)2}}
            \newcommand{\CCVOH}{\ce{CC{@}VOH}}
        '''
    })

class ColorPalette:
    black = '#000000'
    white = '#ffffff'
    gray = '#aaaaaa'
    green = '#5fb236'
    green_dark = '#35691e'
    blue = '#2ea8e5'
    blue_dark = '#126194'
    orange = '#f19837'
    orange_dark = '#e66b27'
    purple = '#a28ae5'
    purple_bright = '#e56eee'
