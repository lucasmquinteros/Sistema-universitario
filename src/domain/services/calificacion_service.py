from typing import Optional, Tuple
from ..repositories.alumno_repository import AlumnoRepository


class CalificacionService:
    """Servicio de dominio para gestionar calificaciones de alumnos"""

    def __init__(self, alumno_repository: AlumnoRepository):
        self.alumno_repository = alumno_repository

    def registrar_nota(
        self,
        alumno_id: int,
        asignatura_id: int,
        nota: float,
        tipo_evaluacion: str,
        fecha_evaluacion: str,
    ) -> Tuple[bool, Optional[str]]:
        """
        Registra una nota para un alumno en una asignatura

        Args:
            alumno_id: ID del alumno
            asignatura_id: ID de la asignatura
            nota: Calificación obtenida
            tipo_evaluacion: Tipo de evaluación (Parcial, Final, etc.)
            fecha_evaluacion: Fecha de la evaluación

        Returns:
            Tupla con (éxito, mensaje)
        """
        # Verificar que el alumno existe
        alumno = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno:
            return False, "El alumno no existe"

        # Verificar que la nota es válida
        if nota < 0 or nota > 10:
            return False, "La nota debe estar entre 0 y 10"

        # Aquí iría la lógica para registrar la nota
        # ...

        return True, "Nota registrada con éxito"

    def calcular_promedio(
        self, alumno_id: int
    ) -> Tuple[bool, Optional[float], Optional[str]]:
        """
        Calcula el promedio general de un alumno

        Args:
            alumno_id: ID del alumno

        Returns:
            Tupla con (éxito, promedio, mensaje)
        """
        # Verificar que el alumno existe
        alumno = self.alumno_repository.obtener_por_id(alumno_id)
        if not alumno:
            return False, None, "El alumno no existe"

        # Obtener historial académico
        historial = self.alumno_repository.obtener_historial_academico(alumno_id)

        # Calcular promedio
        if not historial:
            return True, 0.0, "El alumno no tiene calificaciones registradas"

        # Lógica para calcular el promedio
        # ...

        return True, 8.5, "Promedio calculado con éxito"  # Valor de ejemplo
