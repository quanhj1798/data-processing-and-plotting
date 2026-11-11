#!/usr/bin/env -S nix develop ./data_processing --command python3
import decimal


decimal.getcontext().prec = 28
conversion_factor_atomic_unit_to_electron_volt = decimal.Decimal('2.72113838565563E+01')
conversion_factor_atomic_unit_to_wavenumber = decimal.Decimal('2.19474631370540E+05')
conversion_factor_atomic_unit_to_kilojoule_per_mole = decimal.Decimal('2.62549961709828E+03')
calculation_result = (decimal.Decimal('1') + decimal.Decimal('2'))
print(f'{calculation_result:.15f}')
