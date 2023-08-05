from dataclasses import dataclass

@dataclass(slots=True, init=True)
class Thermochemistry:
    """
    Results of thermochemistry calculations at single temperature.
    All energies are in kJ/mol.

    Attributes
    ----------

    temperature : float
        Temperature in Kelvin

    single_point_energy : float
        Electronic single point energy
    
    zpe : float
        Zero point energy - vibrational correction to electronic energy

    inner_energy : float
        Inner energy `U`
    
    enthalpy : float
        Enthalpy `H`
    
    entropy : float
        Entropy `S`
    
    gibbs_energy : float
        Gibb's energy `G`
        
    """
    temperature : float
    single_point_energy : float
    zpe : float
    inner_energy : float
    enthalpy : float
    entropy : float
    gibbs_energy : float
