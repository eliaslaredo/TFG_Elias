"""
Data model for battery information.

Contains the Bateria class which represents a lithium battery 13300 cell
with state of health (SoH) and impedance information.
"""

from config import SOH_HEALTH_THRESHOLD


class Bateria:
    """
    Represents a lithium battery 13300 cell with health and impedance data.
    
    Attributes
    ----------
    numero : int
        Battery identifier/number (e.g., 1-36 for the 36 batteries tested)
    soh : float
        State of Health as Ah (Ampere-hours), indicating capacity remaining
    impedancia : float
        Internal impedance in Ohms (Ω), measured via EIS
    
    Examples
    --------
    >>> bat = Bateria(numero=1, soh=2.5, impedancia=0.15)
    >>> print(bat)
    Bateria(numero=1, soh=2.5Ah, impedancia=0.15Ω)
    >>> bat.esta_en_buen_estado()
    True
    """

    def __init__(self, numero: int, soh: float, impedancia: float = 0):
        """
        Initialize a Battery object.
        
        Parameters
        ----------
        numero : int
            Battery identifier
        soh : float
            State of Health in Ah (Ampere-hours)
        impedancia : float, optional
            Internal impedance in Ohms. Defaults to 0 if unknown.
        """
        self.numero = numero
        self.soh = soh
        self.impedancia = impedancia

    def __repr__(self):
        """Return formal string representation of the battery."""
        return (
            f"Bateria(numero={self.numero}, "
            f"soh={self.soh}Ah, "
            f"impedancia={self.impedancia}Ω)"
        )

    def __str__(self):
        """Return user-friendly string representation."""
        return (
            f"Batería #{self.numero} | "
            f"SoH: {self.soh}Ah | Impedancia: {self.impedancia}Ω"
        )

    def resumen(self) -> str:
        """
        Get a formatted summary of the battery condition.
        
        Returns
        -------
        str
            Summary string with status, SoH, and impedance
        """
        return str(self)

    def to_dict(self) -> dict:
        """
        Convert battery to dictionary format.
        
        Returns
        -------
        dict
            Dictionary with keys: 'numero', 'soh', 'impedancia'
        """
        return {
            "numero": self.numero,
            "soh": self.soh,
            "impedancia": self.impedancia,
        }
