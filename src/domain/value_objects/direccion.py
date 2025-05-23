from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Direccion:
    calle: str
    numero: str
    piso: Optional[str] = None
    departamento: Optional[str] = None
    ciudad: str = ""
    provincia: str = ""
    codigo_postal: str = ""

    def __str__(self):
        base = f"{self.calle} {self.numero}"
        if self.piso and self.departamento:
            base += f", Piso {self.piso}, Depto {self.departamento}"
        if self.ciudad:
            base += f", {self.ciudad}"
        if self.provincia:
            base += f", {self.provincia}"
        if self.codigo_postal:
            base += f" ({self.codigo_postal})"
        return base

    @classmethod
    def from_string(cls, direccion_str: str) -> "Direccion":
        """Crea una instancia de Direccion desde un string"""
        # Implementación simple, en un caso real se haría parsing más sofisticado
        partes = direccion_str.split(",")
        if len(partes) >= 1:
            calle_numero = partes[0].strip().split(" ")
            if len(calle_numero) >= 2:
                calle = " ".join(calle_numero[:-1])
                numero = calle_numero[-1]
                return cls(calle=calle, numero=numero)
        # Si no se puede parsear, retornar una dirección con valores por defecto
        return cls(calle="", numero="")
