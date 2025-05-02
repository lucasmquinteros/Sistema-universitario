from typing import Dict, Any, Optional
from datetime import date

class Entidad:
    """Clase base para todas las entidades del sistema"""
    
    def __init__(self, id: Optional[int] = None):
        self.id = id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario"""
        # Filtrar atributos privados (que empiezan con _)
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]):
        """Crea una instancia desde un diccionario"""
        instance = cls()
        for k, v in datos.items():
            if hasattr(instance, k):
                setattr(instance, k, v)
        return instance