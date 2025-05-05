# sistema_universitario/main.py
from db.manager import DatabaseManager
from services.profesor_service import ProfesorService
from models.profesor import Profesor
from utils.logger import Logger

def main():
    # Inicializar logger
    logger = Logger.get_instance()
    logger.info("Iniciando aplicación")
    
    try:
        # Configuración
        connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=sistema_universitario2;Trusted_Connection=yes;"
        db_manager = DatabaseManager(connection_string)
        logger.info("Conexión a base de datos establecida")

        # Crear servicio
        profesor_service = ProfesorService(db_manager)

        ## Crear un profesor
        #datos_profesor = {
        #    'nombre': 'Juan',
        #    'apellido': 'Pérez',
        #    'dni': '12345678',
        #    'email': 'juan.perez@universidad.edu',
        #    'telefono': '555-1234',
        #    'titulo': 'Doctor en Informática',
        #    'especialidad': 'Inteligencia Artificial',
        #    'tipo_contrato': 'Titular',
        #    'id_departamento': 1  # ID del departamento de Informática
        #}

        #profesor_id = profesor_service.crear(datos_profesor)
        #logger.info(f"Profesor creado con ID: {profesor_id}")

        # Obtener un profesor
        profesor_id = 10 
        profesor = profesor_service.obtener(profesor_id)
        if profesor:
            logger.info(f"Profesor recuperado: {profesor.nombre_completo}")
            
            # Asignar a una asignatura
            resultado = profesor_service.asignar_asignatura(
                profesor_id, 
                asignatura_id=3,
                rol="Titular", 
                año_academico=2023, 
                cuatrimestre=1
            )
            
            if resultado:
                logger.info(f"Profesor asignado a asignatura correctamente")
            else:
                logger.warning("No se pudo asignar el profesor a la asignatura")
        else:
            logger.warning(f"No se pudo recuperar el profesor con ID {profesor_id}")
            
    except Exception as e:
        logger.error(f"Error en la aplicación: {str(e)}")
    
    logger.info("Finalizando aplicación")

if __name__ == "__main__":
    main()