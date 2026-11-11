#!/usr/bin/env -S nix develop ./data_processing --command python3
import sys
import numpy
import pandas
import lmfit
import lmfitxps.models


# loading
data_frames = pandas.read_excel(sys.argv[1], sheet_name=['C1s Scan', 'V2p Scan'], header=None, skiprows=16)
data_frame_C1s = data_frames['C1s Scan']
data_frame_V2p = data_frames['V2p Scan']
ndarray_C1s = data_frame_C1s.iloc[:, [0, 2]].to_numpy()
ndarray_V2p = data_frame_V2p.iloc[:, [0, 2]].to_numpy()
binding_energy_C1s = ndarray_C1s[:, 0]
binding_energy_V2p = ndarray_V2p[:, 0]
intensity_C1s = ndarray_C1s[:, 1]
intensity_V2p = ndarray_V2p[:, 1]

# fitting_C1s
model_C1s = (
    lmfitxps.models.ShirleyBG(prefix='background_C1s_', independent_vars=['y']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_C1C_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_C1O_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_C3O_', independent_vars=['x'])
)
parameters_C1s = lmfit.Parameters()
parameters_C1s.add('background_C1s_k', value=0.002)
parameters_C1s.add('background_C1s_const', value=numpy.min(intensity_C1s) * 0.8, min=0)
parameters_C1s.add('peak_C1C_center', value=284.8, min=284.0, max=285.6)
parameters_C1s.add('peak_C1C_amplitude', value=numpy.max(intensity_C1s), min=0)
parameters_C1s.add('peak_C1C_gamma', value=0, vary=False)
parameters_C1s.add('peak_C1C_sigma', value=0.2, min=0.1, max=0.3)
parameters_C1s.add('peak_C1C_gaussian_sigma', value=0.5, min=0.2, max=0.8)
parameters_C1s.add('peak_C1O_center_factor', value=1.5, min=1.3, max=1.7)
parameters_C1s.add('peak_C1O_center', expr='peak_C1C_center + peak_C1O_center_factor')
parameters_C1s.add('peak_C1O_amplitude', value=1000, min=0)
parameters_C1s.add('peak_C1O_gamma', expr='peak_C1C_gamma')
parameters_C1s.add('peak_C1O_sigma', expr='peak_C1C_sigma')
parameters_C1s.add('peak_C1O_gaussian_sigma', expr='peak_C1C_gaussian_sigma')
parameters_C1s.add('peak_C3O_center_factor', value=3.9, min=3.7, max=4.1)
parameters_C1s.add('peak_C3O_center', expr='peak_C1C_center + peak_C3O_center_factor')
parameters_C1s.add('peak_C3O_amplitude', value=1000, min=0)
parameters_C1s.add('peak_C3O_gamma', expr='peak_C1C_gamma')
parameters_C1s.add('peak_C3O_sigma', expr='peak_C1C_sigma')
parameters_C1s.add('peak_C3O_gaussian_sigma', expr='peak_C1C_gaussian_sigma')
result_C1s = model_C1s.fit(intensity_C1s, parameters_C1s, y=intensity_C1s, x=binding_energy_C1s, weights=1 / numpy.sqrt(numpy.maximum(intensity_C1s, 1)))
residual_C1s = result_C1s.residual
components_C1s = result_C1s.eval_components(y=intensity_C1s, x=binding_energy_C1s)

# fitting_V2p
binding_energy_V2p = binding_energy_V2p + (284.8 - result_C1s.params['peak_C1C_center'].value)
sigma_C1C = result_C1s.params['peak_C1C_sigma'].value
gaussian_sigma_C1C = result_C1s.params['peak_C1C_gaussian_sigma'].value
amplitude_C1O = result_C1s.params['peak_C1O_amplitude'].value
amplitude_C3O = result_C1s.params['peak_C3O_amplitude'].value
baseline_V2p = numpy.max(intensity_V2p[numpy.where((binding_energy_V2p >= 515) & (binding_energy_V2p <= 520))[0]])
model_V2p = (
    lmfitxps.models.TougaardBG(prefix='background_V2p_', independent_vars=['y', 'x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_OV_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachDublett(prefix='peak_V4_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachDublett(prefix='peak_V5_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='satellite_peak_V5_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_O3C_', independent_vars=['x']) +
    lmfitxps.models.ConvGaussianDoniachSinglett(prefix='peak_O1C_', independent_vars=['x'])
)
parameters_V2p = lmfit.Parameters()
parameters_V2p.add('background_V2p_B', value=82.7)
parameters_V2p.add('background_V2p_C', value=182.9, vary=False)
parameters_V2p.add('background_V2p_C_d', value=0.544, vary=False)
parameters_V2p.add('background_V2p_D', value=70.6, vary=False)
parameters_V2p.add('background_V2p_extend', value=30, vary=False)
parameters_V2p.add('peak_OV_center', value=530, min=529.5, max=530.5)
parameters_V2p.add('peak_OV_amplitude', value=numpy.max(intensity_V2p) * 0.8, min=0)
parameters_V2p.add('peak_OV_gamma', value=0, vary=False)
parameters_V2p.add('peak_OV_sigma', value=0.2, min=0.1, max=0.3)
parameters_V2p.add('peak_OV_gaussian_sigma', value=0.35, min=0.2, max=gaussian_sigma_C1C)
parameters_V2p.add('peak_V4_center_factor', value=14.16, min=13.96, max=14.36)
parameters_V2p.add('peak_V4_center', expr='peak_OV_center - peak_V4_center_factor')
parameters_V2p.add('peak_V4_amplitude', value=baseline_V2p * 0.5, min=0)
parameters_V2p.add('peak_V4_soc', value=7.33, vary=False)
parameters_V2p.add('peak_V4_fct_coster_kronig', value=1.4, min=1.05, max=1.5)
parameters_V2p.add('peak_V4_height_ratio', expr='0.5 / peak_V4_fct_coster_kronig')
parameters_V2p.add('peak_V4_gamma', value=0, vary=False)
parameters_V2p.add('peak_V4_sigma', value=0.4, min=sigma_C1C, max=0.6)
parameters_V2p.add('peak_V4_gaussian_sigma', value=0.4, min=0.2, max=gaussian_sigma_C1C)
parameters_V2p.add('peak_V5_center_factor', value=12.8, min=12.7, max=12.9)
parameters_V2p.add('peak_V5_center', expr='peak_OV_center - peak_V5_center_factor')
parameters_V2p.add('peak_V5_amplitude', value=baseline_V2p * 0.5, min=0)
parameters_V2p.add('peak_V5_soc', value=7.33, vary=False)
parameters_V2p.add('peak_V5_fct_coster_kronig', expr='peak_V4_fct_coster_kronig - 0.05')
parameters_V2p.add('peak_V5_height_ratio', expr='0.5 / peak_V5_fct_coster_kronig')
parameters_V2p.add('peak_V5_gamma', value=0, vary=False)
parameters_V2p.add('peak_V5_sigma', value=0.3, min=sigma_C1C, max=0.5)
parameters_V2p.add('peak_V5_gaussian_sigma', value=0.45, min=0.2, max=gaussian_sigma_C1C)
parameters_V2p.add('satellite_peak_V5_center', expr='peak_V5_center + 13.7')
parameters_V2p.add('satellite_peak_V5_amplitude', expr='peak_V5_amplitude * 0.1')
parameters_V2p.add('satellite_peak_V5_gamma', value=0, vary=False)
parameters_V2p.add('satellite_peak_V5_sigma', value=0.1, vary=False)
parameters_V2p.add('satellite_peak_V5_gaussian_sigma', value=0.3, vary=False)
parameters_V2p.add('peak_O3C_center', value=532, min=531.5, max=532.5)
parameters_V2p.add('peak_O3C_amplitude', value=amplitude_C3O * 2.93 * 2, min=amplitude_C3O * 2.93 * 2 * 0.5)
parameters_V2p.add('peak_O3C_gamma', value=0, vary=False)
parameters_V2p.add('peak_O3C_sigma', value=0.2, min=0.1, max=0.3)
parameters_V2p.add('peak_O3C_gaussian_sigma', value=gaussian_sigma_C1C, vary=False)
parameters_V2p.add('peak_O1C_center', value=533, min=532.5, max=533.5)
parameters_V2p.add('peak_O1C_amplitude', value=amplitude_C1O * 2.93, min=amplitude_C1O * 2.93 * 0.5)
parameters_V2p.add('peak_O1C_gamma', value=0, vary=False)
parameters_V2p.add('peak_O1C_sigma', value=0.2, min=0.1, max=0.3)
parameters_V2p.add('peak_O1C_gaussian_sigma', value=gaussian_sigma_C1C, vary=False)
result_V2p = model_V2p.fit(intensity_V2p, parameters_V2p, y=intensity_V2p, x=binding_energy_V2p, weights=1 / numpy.sqrt(numpy.maximum(intensity_V2p, 1)))
residual_V2p = result_V2p.residual
components_V2p = result_V2p.eval_components(y=intensity_V2p, x=binding_energy_V2p)
lmfit.report_fit(result_V2p)

# saving
data_C1s = {
    'binding_energy': binding_energy_C1s, 
    'intensity': intensity_C1s, 
    'result': result_C1s.best_fit,
    'residual': residual_C1s, 
    'component_background': components_C1s['background_C1s_'], 
    'component_C1C': components_C1s['peak_C1C_'] + components_C1s['background_C1s_'],
    'component_C1O': components_C1s['peak_C1O_'] + components_C1s['background_C1s_'],
    'component_C3O': components_C1s['peak_C3O_'] + components_C1s['background_C1s_'],
}
data_frame_C1s = pandas.DataFrame(data_C1s)
data_frame_C1s.to_csv('data_C1s.csv', index=False)
data_V2p = {
    'binding_energy': binding_energy_V2p,
    'intensity': intensity_V2p,
    'result': result_V2p.best_fit,
    'residual': residual_V2p,
    'component_background': components_V2p['background_V2p_'], 
    'component_OV': components_V2p['peak_OV_'] + components_V2p['background_V2p_'],
    'component_V4': components_V2p['peak_V4_'] + components_V2p['background_V2p_'],
    'component_V5': components_V2p['peak_V5_'] + components_V2p['background_V2p_'],
    'component_V5_satellite': components_V2p['satellite_peak_V5_'] + components_V2p['background_V2p_'],
    'component_OC': components_V2p['peak_O1C_'] + components_V2p['peak_O3C_'] + components_V2p['background_V2p_']
}
data_frame_V2p = pandas.DataFrame(data_V2p)
data_frame_V2p.to_csv('data_V2p.csv', index=False)
centers = {
    'center_peak_C1C': result_C1s.params['peak_C1C_center'].value,
    'center_peak_C1O': result_C1s.params['peak_C1O_center'].value,
    'center_peak_C3O': result_C1s.params['peak_C3O_center'].value,
    'center_peak_OV': result_V2p.params['peak_OV_center'].value,
    'center_peak_V4': result_V2p.params['peak_V4_center'].value,
    'center_peak_V5': result_V2p.params['peak_V5_center'].value,
    'center_satellite_peak_V5': result_V2p.params['satellite_peak_V5_center'].value
}
data_frame_centers = pandas.DataFrame([centers])
data_frame_centers.to_csv('centers.csv', index=False)
