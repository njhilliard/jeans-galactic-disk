import gadget
import astropy.units as u
from astropy.constants import G as G_u

#Some useful astronomy constants in cgs units
constants = {
    gravity: (G_u / u.m**3) * (100*u.cm)**3 * u.kg / (1000 * u.g),
    boltzmann: 1.3806e-16,
    protonmass: 1.6726e-24,
    sec_per_megayear: 3.155e13,
    gamma_minus1: (5.0 / 3.0) - 1.0,
    h_massfrac: 0.76
}

class File():
    def __init__(self):
        self.is_cosmological = False
        self.convert_bh = False
        self.gas = None
        self.halo = None
        self.disk = None
        self.bulge = None
        self.star = None
        self.boundary = None
        self.mass_conversion_factor = 1.0
    
    def save(self, filename):
        with open(filename, 'wb') as file:
            pass

    def convert(self, gadget_params, gadget_file, mass_conversion_factor, convert_bh=False):
        if not isinstance(gadget_file, gadget.File):
            raise ValueError("input file must be a gadget.File")
        
        if not isinstance(gadget_params, gadget.Parameter_file):
            raise ValueError("input file must be a gadget.Parameter_file")
        
        self.set_units(gadget_params)
        self.halo = gadget_file.halo
        self.disk = gadget_file.disk
        self.bulge = gadget_file.bulge
        self.star = gadget_file.star
        self.boundary = gadget_file.boundary
        self.mass_conversion_factor = mass_conversion_factor
        self.convert_bh = convert_bh
        
        if gadget_file.gas is not None:
            self.gas = gadget_file.gas
            self.gas.temperature = np.copy(gadget_file.gas.internal_energy)
            
            # Convert temperature to Kelvin
            mean_weight = (4.0 / 
                           (3 * constants['h_massfrac'] + 1 + 
                             4 * constants['h_massfrac'] * P[i].Ne
                           ) * constants['protonmass'])
            
            self.gas.temperature *= (mean_weight / constants['boltzmann'] * 
                                     constants['gamma_minus1'] * self.units['Energy_in_cgs'] / 
                                     self.units['Mass_in_g'])

        if float(gadget_file.header.attrs['Redshift']) > 0.0:
            self.is_cosmological = True
        
    def set_units(self, gadget_params):
        if not isinstance(gadget_params, gadget.Parameter_file):
            raise ValueError("parameter file is not a 'gadget.Parameter_file'")
    
        constants['hubble'] = float(gadget_params['dHubble0'])
        if constants['hubble'] == 0.0:
            constants['hubble'] = 1.0

        self.units['Length_in_cm'] = float(gadget_params['UnitLength_in_cm']) / hubble
        self.units['Mass_in_g'] = float(gadget_params['UnitMass_in_g']) / hubble
        self.units['Velocity_in_cm_per_s'] = float(gadget_params['UnitVelocity_in_cm_per_s'])
        self.units['Time_in_s'] = self.units['Length_in_cm'] / self.units['Velocity_in_cm_per_s']
        self.units['Time_in_Megayears'] = self.units['Time_in_s'] / constants['sec_per_megayear']
        self.units['Density_in_cgs'] = self.units['Mass_in_g'] / self.units['Length_in_cm'] ** 3
        self.units['Pressure_in_cgs'] = self.units['Mass_in_g'] / self.units['Length_in_cm'] / self.units['Time_in_s'] ** 2
        self.units['CoolingRate_in_cgs'] = self.units['Pressure_in_cgs'] / self.units['Time_in_s']
        self.units['Energy_in_cgs'] = self.units['Mass_in_g'] * self.units['Length_in_cm'] ** 2 / self.units['Time_in_s'] ** 2
        self.units['Natural_vel_in_cgs'] = sqrt(constants['gravity_in_cm'] * self.units['Mass_in_g'] / self.units['Length_in_cm'])
