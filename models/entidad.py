# models/entidad.py
from typing import Dict, Any, Optional

class Entidad:
    def __init__(self, id: Optional[int] = None):
        self.id = id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]):
        """Crea una instancia desde un diccionario"""
        instance = cls()
        for k, v in datos.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        return instance

