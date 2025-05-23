from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.profesor import Profesor


class ProfesorRepository(ABC):
    """Interfaz para el repositorio de Profesores"""

    @abstractmethod
    def obtener_por_id(self, profesor_id: int) -> Optional[Profesor]:
        """Obtiene un profesor por su ID"""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Profesor]:
        """Obtiene todos los profesores"""
        pass

    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Profesor]:
        """Obtiene un profesor por su DNI"""
        pass

    @abstractmethod
    def obtener_por_departamento(self, departamento_id: int) -> List[Profesor]:
        """Obtiene todos los profesores de un departamento"""
        pass

    @abstractmethod
    def crear(self, profesor: Profesor) -> Profesor:
        """Crea un nuevo profesor"""
        pass

    @abstractmethod
    def actualizar(self, profesor: Profesor) -> Profesor:
        """Actualiza un profesor existente"""
        pass

    @abstractmethod
    def eliminar(self, profesor_id: int) -> bool:
        """Elimina un profesor por su ID"""
        pass

    @abstractmethod
    def obtener_asignaturas(self, profesor_id: int) -> List[dict]:
        """Obtiene las asignaturas que imparte un profesor"""
        pass
