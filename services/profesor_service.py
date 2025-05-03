# sistema_universitario/services/profesor_service.py
from typing import Dict, List, Any, Optional
from datetime import date
from services.base_service import BaseService
from models.profesor import Profesor

class ProfesorService(BaseService):
    
    def crear(self, datos: Dict[str, Any]) -> Optional[int]:
        try:
            # Preparar parámetros para el SP
            params = (
                datos['nombre'],
                datos['apellido'],
                datos['dni'],
                datos['email'],
                datos.get('telefono'),
                datos['titulo'],
                datos.get('especialidad'),
                datos['tipo_contrato'],
                datos.get('fecha_ingreso', date.today().isoformat()),
                datos['id_departamento']
            )
            
            # Ejecutar SP con parámetro de salida
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            profesor_id = self.db.execute_stored_procedure("sp_CrearProfesor", params)

            conn.commit()
            conn.close()
            
            return profesor_id
            
        except Exception as e:
            print(f"Error al crear profesor: {str(e)}")
            return None
    
    def obtener(self, profesor_id: int) -> Optional[Profesor]:
        try:
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_ObtenerProfesor", (profesor_id,))
            
            if not resultados or not resultados[0]:
                return None
            
            # Convertir a objeto Profesor
            datos_profesor = resultados[0]
            profesor = Profesor.from_dict(datos_profesor)
            
            # Si hay más resultados, son las asignaturas
            if isinstance(resultados, list) and len(resultados) > 1:
                profesor.asignaturas = resultados[1]
                
            return profesor
            
        except Exception as e:
            print(f"Error al obtener profesor: {str(e)}")
            return None
    
    def listar(self, filtros: Optional[Dict[str, Any]] = None) -> List[Profesor]:
        try:
            # Construir parámetros para el SP según los filtros
            params = []
            
            if filtros:
                if 'departamento_id' in filtros:
                    params.append(filtros['departamento_id'])
                else:
                    params.append(None)
                    
                if 'especialidad' in filtros:
                    params.append(filtros['especialidad'])
                else:
                    params.append(None)
            else:
                params = [None, None]  # Sin filtros
                
            # Ejecutar SP
            resultados = self.db.execute_stored_procedure("sp_ListarProfesores", tuple(params))
            
            if not resultados:
                return []
                
            # Convertir a objetos Profesor
            profesores = []
            for datos in resultados:
                profesor = Profesor.from_dict(datos)
                profesores.append(profesor)
                
            return profesores
            
        except Exception as e:
            print(f"Error al listar profesores: {str(e)}")
            return []
    
    def asignar_asignatura(self, profesor_id: int, asignatura_id: int, rol: str, año_academico: int, cuatrimestre: int) -> bool:
        try:
            # Ejecutar SP
            params = (profesor_id, asignatura_id, rol, año_academico, cuatrimestre)
            self.db.execute_stored_procedure("sp_AsignarProfesorAsignatura", params)
            return True
            
        except Exception as e:
            print(f"Error al asignar asignatura: {str(e)}")
            return False