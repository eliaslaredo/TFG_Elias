
class Bateria:
    def __init__(self, numero: int, soh: float, impedancia: float):
        self.numero = numero        # Identificador de la batería
        self.soh = soh              # State of Health (%) — rango 0.0 a 100.0
        self.impedancia = impedancia  # Impedancia interna (Ohmios)

    def __repr__(self):
        return (f"Bateria(numero={self.numero}, "
                f"soh={self.soh}, "
                f"impedancia={self.impedancia}Ω)")