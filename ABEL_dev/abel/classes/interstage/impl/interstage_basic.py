import scipy.constants as SI
from abel import Interstage
import numpy as np
import matplotlib.pyplot as plt

class InterstageBasic(Interstage):
    
    def __init__(self, nom_energy=None, length=None, dipole_length=None, dipole_field=None, beta0=None, R56=None, phase_advance=1.5*np.pi):
        self.nom_energy = nom_energy
        self.length = length
        self.dipole_length = dipole_length
        self.dipole_field = dipole_field
        self.beta0 = beta0
        self.phase_advance = phase_advance
        self.R56 = R56
    
    
    def track(self, beam, savedepth=0, runnable=None, verbose=False):
        
        # compress beam
        beam.compress(R_56=self.get_R56(), nom_energy=self.nom_energy)
        
        # rotate transverse phase spaces (assumed achromatic)
        if callable(self.beta0):
            betas = self.beta0(beam.Es())
        else:
            betas = self.beta0
        theta = self.phase_advance
        xs_rotated = beam.xs()*np.cos(theta) + betas*beam.xps()*np.sin(theta)
        xps_rotated = -beam.xs()*np.sin(theta)/betas + beam.xps()*np.cos(theta)
        beam.set_xs(xs_rotated)
        beam.set_xps(xps_rotated)
        ys_rotated = beam.ys()*np.cos(theta) + betas*beam.yps()*np.sin(theta)
        yps_rotated = -beam.ys()*np.sin(theta)/betas + beam.yps()*np.cos(theta)
        beam.set_ys(ys_rotated)
        beam.set_yps(yps_rotated)
        
        return super().track(beam, savedepth, runnable, verbose)

    
    # evaluate dipole length (if it is a function)
    def get_dipole_length(self):
        if callable(self.dipole_length):
            return self.dipole_length(self.nom_energy)
        else:
            return self.dipole_length

    
    # evaluate dipole field (if it is a function)
    def get_dipole_field(self):
        if callable(self.dipole_field):
            return self.dipole_field(self.nom_energy)
        else:
            return self.dipole_field

    
    # evaluate longitudinal dispersion (R56)
    def get_R56(self):
        if self.R56 is not None:
            if callable(self.R56):
                return self.R56(self.nom_energy)
            else:
                return self.R56
        else:
            return -self.get_dipole_field()**2*SI.c**2*self.get_dipole_length()**3/(3*self.nom_energy**2)
    
    
    # lattice length
    def get_length(self):
        if self.length is not None:
            if callable(self.length):
                return self.length(self.nom_energy)
            else:
                return self.length
        else:
            return 4.7875*self.get_dipole_length()
        