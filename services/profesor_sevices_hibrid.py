# sistema_universitario/services/profesor_service_hybrid.py
from typing import Dict, List, Any, Optional
from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session
from sistema_universitario.db.sqlalchemy_config import SQLAlchemyManager
from sistema_universitario.db.database_manager import DatabaseManager
from sistema_universitario.models.profesor import Profesor as ProfesorModel
from sistema_universitario.db.models.sqlalchemy_models import Profesor as ProfesorORM
from sistema_universitario.utils.logger import Logger

class ProfesorServiceHybrid:
    """Servicio híbrido para gestionar profesores usando SQLAlchemy y Stored Procedures"""
    
    def __init__(self, db_manager: DatabaseManager, sqlalchemy_manager: SQLAlchemyManager):
        self.db = db_manager
        self.sqlalchemy = sqlalchemy_manager
        self.logger = Logger.get_instance()
    
    def crear(self, datos: Dict[str, Any]) -> Optional[int]:
        """
        Crea un nuevo profesor usando stored procedure
        
        Args:
            datos: Diccionario con los datos del profesor
            
        Returns:
            ID del profesor creado o None si hubo error
        """
        try:
            # Usar el stored procedure para crear el profesor
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
            
            cursor.execute("""
                DECLARE @ProfesorId INT;
                EXEC sp_CrearProfesor ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, @ProfesorId OUTPUT;
                SELECT @ProfesorId AS Id;
            """, params)
            
            # Obtener el ID generado
            row = cursor.fetchone()
            profesor_id = row.Id if row else None
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Profesor creado con ID: {profesor_id}")
            return profesor_id
            
        except Exception as e:
            self.logger.error(f"Error al crear profesor: {str(e)}")
            return None
    
    def obtener(self, profesor_id: int) -> Optional[ProfesorModel]:
        """
        Obtiene un profesor por ID usando SQLAlchemy
        
        Args:
            profesor_id: ID del profesor
            
        Returns:
            Objeto Profesor o None si no existe
        """
        try:
            # Usar SQLAlchemy para obtener el profesor
            session = self.sqlalchemy.get_session()
            
            # Consulta con joins para obtener datos relacionados
            profesor_orm = session.query(ProfesorORM)\
                .filter(ProfesorORM.Id == profesor_id)\
                .first()
                
            if not profesor_orm:
                session.close()
                return None
                
            # Convertir a modelo de dominio
            profesor = ProfesorModel(profesor_orm.Id)
            profesor.nombre = profesor_orm.Nombre
            profesor.apellido = profesor_orm.Apellido
            profesor.dni = profesor_orm.DNI
            profesor.email = profesor_orm.Email
            profesor.telefono = profesor_orm.Telefono
            profesor.titulo = profesor_orm.Titulo
            profesor.especialidad = profesor_orm.Especialidad
            profesor.tipo_contrato = profesor_orm.TipoContrato
            profesor.fecha_ingreso = profesor_orm.FechaIngreso
            profesor.id_departamento = profesor_orm.Id_Departamento
            
            # Obtener nombre del departamento
            if profesor_orm.departamento:
                profesor.departamento = profesor_orm.departamento.Nombre
                
            # Obtener asignaturas
            profesor.asignaturas = []
            for rel in profesor_orm.asignaturas:
                asignatura_info = {
                    'id': rel.Id,
                    'nombre': rel.Nombre,
                    'rol': next((pa.Rol for pa in rel.profesores if pa.Id == profesor_id), None),
                    'año_academico': next((pa.AñoAcademico for pa in rel.profesores if pa.Id == profesor_id), None),
                    'cuatrimestre': next((pa.Cuatrimestre for pa in rel.profesores if pa.Id == profesor_id), None)
                }
                profesor.asignaturas.append(asignatura_info)
                
            session.close()
            return profesor
            
        except Exception as e:
            self.logger.error(f"Error al obtener profesor: {str(e)}")
            return None
    
    def listar(self, filtros: Optional[Dict[str, Any]] = None) -> List[ProfesorModel]:
        """
        Lista profesores con filtros opcionales usando SQLAlchemy
        
        Args:
            filtros: Diccionario con filtros (departamento_id, especialidad, etc.)
            
        Returns:
            Lista de objetos Profesor
        """
        try:
            session = self.sqlalchemy.get_session()
            query = session.query(ProfesorORM)
            
            # Aplicar filtros
            if filtros:
                if 'departamento_id' in filtros and filtros['departamento_id']:
                    query = query.filter(ProfesorORM.Id_Departamento == filtros['departamento_id'])
                    
                if 'especialidad' in filtros and filtros['especialidad']:
                    query = query.filter(ProfesorORM.Especialidad.like(f"%{filtros['especialidad']}%"))
                    
                if 'nombre' in filtros and filtros['nombre']:
                    query = query.filter(ProfesorORM.Nombre.like(f"%{filtros['nombre']}%"))
                    
                if 'apellido' in filtros and filtros['apellido']:
                    query = query.filter(ProfesorORM.Apellido.like(f"%{filtros['apellido']}%"))
            
            # Ordenar resultados
            query = query.order_by(ProfesorORM.Apellido, ProfesorORM.Nombre)
            
            # Ejecutar consulta
            profesores_orm = query.all()
            
            # Convertir a modelos de dominio
            profesores = []
            for p_orm in profesores_orm:
                profesor = ProfesorModel(p_orm.Id)
                profesor.nombre = p_orm.Nombre
                profesor.apellido = p_orm.Apellido
                profesor.dni = p_orm.DNI
                profesor.email = p_orm.Email
                profesor.telefono = p_orm.Telefono
                profesor.titulo = p_orm.Titulo
                profesor.especialidad = p_orm.Especialidad
                profesor.tipo_contrato = p_orm.TipoContrato
                profesor.fecha_ingreso = p_orm.FechaIngreso
                profesor.id_departamento = p_orm.Id_Departamento
                
                # Obtener nombre del departamento
                if p_orm.departamento:
                    profesor.departamento = p_orm.departamento.Nombre
                
                profesores.append(profesor)
                
            session.close()
            return profesores
            
        except Exception as e:
            self.logger.error(f"Error al listar profesores: {str(e)}")
            return []
    
    def asignar_asignatura(self, profesor_id: int, asignatura_id: int, rol: str, año_academico: int, cuatrimestre: int) -> bool:
        """
        Asigna una asignatura a un profesor usando stored procedure
        
        Args:
            profesor_id: ID del profesor
            asignatura_id: ID de la asignatura
            rol: Rol del profesor (Titular, Adjunto, etc.)
            año_academico: Año académico
            cuatrimestre: Número de cuatrimestre
            
        Returns:
            True si se asignó correctamente, False en caso contrario
        """
        try:
            # Usar el stored procedure para asignar la asignatura
            params = (profesor_id, asignatura_id, rol, año_academico, cuatrimestre)
            self.db.execute_stored_procedure("sp_AsignarProfesorAsignatura", params)
            
            self.logger.info(f"Asignatura {asignatura_id} asignada al profesor {profesor_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al asignar asignatura: {str(e)}")
            return False