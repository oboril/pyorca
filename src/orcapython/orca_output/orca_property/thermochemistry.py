from dataclasses import dataclass

@dataclass(frozen=True, init=True)
class Thermochemistry:
    """
    Results of thermochemistry calculations at single temperature.
    
    All energies are in kJ/mol, entropy is in J/mol/K.
    """
    
    temperature : float
    """Temperature in Kelvin"""

    single_point_energy : float
    """Electronic single point energy"""

    zpe : float
    """Zero point energy - vibrational correction to electronic energy"""
    
    inner_energy : float
    """Inner energy `U`"""
    
    enthalpy : float
    """Enthalpy `H`"""
    
    entropy : float
    """Entropy `S`"""
    
    gibbs_energy : float
    """Gibb's energy `G`"""
    
