#!/usr/bin/env -S nix develop ./data_processing --command python3
import sys
import numpy
import pandas
import pymatgen.io.cif
import pymatgen.analysis.diffraction.xrd


# loading
structure = pymatgen.io.cif.CifParser(sys.argv[1]).parse_structures(primitive=True)[0]
pattern = pymatgen.analysis.diffraction.xrd.XRDCalculator(wavelength='CuKa').get_pattern(structure)
filenames = [sys.argv[2], sys.argv[2], sys.argv[2]]
ndarrays = []
for filename in filenames:
    data_frame = pandas.read_csv(filename, header=None, skiprows=2, sep=r'\s+')
    ndarrays.append(data_frame.to_numpy())
    
# saving
theoretical_diffraction_peaks = {
    '2theta': pattern.x,
    'intensity': pattern.y
}
data_frame_theoretical_diffraction_peaks = pandas.DataFrame(theoretical_diffraction_peaks)
data_frame_theoretical_diffraction_peaks.to_csv('theoretical_diffraction_peaks.csv', index=False)
experimental_diffraction_peaks = {
    '2theta': ndarrays[0][:, 0],
    'intensity_1': ndarrays[0][:, 1],
    'intensity_2': ndarrays[1][:, 1],
    'intensity_3': ndarrays[2][:, 1]
}
data_frame_experimental_diffraction_peaks = pandas.DataFrame(experimental_diffraction_peaks)
data_frame_experimental_diffraction_peaks.to_csv('experimental_diffraction_peaks.csv', index=False)
