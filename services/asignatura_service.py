# sistema_universitario/services/asignatura_service.py
from typing import Dict, List, Any, Optional
from .base_service import BaseService
from ..models.asignatura import Asignatura

class AsignaturaService(BaseService):
    """Servicio para gestionar asignaturas"""
    
    def crear(self, datos: Dict[str, Any]) -> Optional[int]:
        try:
            params = (
                datos['nombre'],
                datos['hsemanal'],
                datos['htotales'],
                datos['creditos'],
                datos['id_area'],
                datos['id_regimen'],
                datos['id_depto']
            )
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DECLARE @AsignaturaId INT;
                EXEC sp_CrearAsignatura ?, ?, ?, ?, ?, ?, ?, @AsignaturaId OUTPUT;
                SELECT @AsignaturaId AS Id;
            """, params)
            row = cursor.fetchone()
            asignatura_id = row.Id if row else None
            
            conn.commit()
            conn.close()
            
            return asignatura_id
            
        except Exception as e:
            print(f"Error al crear asignatura: {str(e)}")
            return None
    
    def obtener(self, asignatura_id: int) -> Optional[Asignatura]:
        try:
            resultados = self.db.execute_stored_procedure("sp_ObtenerAsignatura", (asignatura_id,))
            
            if not resultados or not resultados[0]:
                return None
            
            # Si el SP devuelve múltiples conjuntos de resultados
            if isinstance(resultados, list) and len(resultados) > 0:
                # Datos básicos de la asignatura
                datos_asignatura = resultados[0][0]
                asignatura = Asignatura.from_dict(datos_asignatura)
                
                # Profesores que la imparten
                if len(resultados) > 1:
                    asignatura.profesores = resultados[1]
                
                # Planes de estudio que la incluyen
                if len(resultados) > 2:
                    asignatura.planes_estudio = resultados[2]
                
                # Correlativas
                if len(resultados) > 3:
                    asignatura.correlativas = resultados[3]
                
                return asignatura
            else:
                # Si el SP devuelve un solo conjunto de resultados
                datos_asignatura = resultados[0]
                return Asignatura.from_dict(datos_asignatura)
            
        except Exception as e:
            print(f"Error al obtener asignatura: {str(e)}")
            return None
    
    def agregar_correlativa(self, asignatura_id: int, correlativa_id: int) -> bool:
        try:
            # Ejecutar consulta directa (o SP si se implementa)
            query = """
                INSERT INTO Correlativa (Id_asignatura, Id_Correlativa)
                VALUES (?, ?)
            """
            self.db.execute_query(query, (asignatura_id, correlativa_id))
            return True
            
        except Exception as e:
            print(f"Error al agregar correlativa: {str(e)}")
            return False
    
    def asignar_a_plan(self, asignatura_id: int, plan_id: int, año: int, cuatrimestre: Optional[int] = None) -> bool:
        try:
            # Ejecutar consulta directa (o SP si se implementa)
            query = """
                INSERT INTO AsignaturaxPlan (Id_Asignatura, Id_Plan, Año, Cuatrimestre)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_query(query, (asignatura_id, plan_id, año, cuatrimestre))
            return True
            
        except Exception as e:
            print(f"Error al asignar asignatura a plan: {str(e)}")
            return False