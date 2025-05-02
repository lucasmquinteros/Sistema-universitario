# sistema_universitario/utils/logger.py
import logging
import os
from datetime import datetime

class Logger:
    """Sistema de registro de actividades y errores"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls, log_dir="logs"):
        """Implementación de Singleton para el logger"""
        if cls._instance is None:
            cls._instance = cls(log_dir)
        return cls._instance
    
    def __init__(self, log_dir="logs"):
        """
        Inicializa el sistema de logging
        
        Args:
            log_dir: Directorio donde se guardarán los logs
        """
        # Crear directorio de logs si no existe
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar logger principal
        self.logger = logging.getLogger("sistema_universitario")
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler para archivo de log general
            log_file = os.path.join(log_dir, f"sistema_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # Handler para archivo de errores
            error_file = os.path.join(log_dir, f"errores_{datetime.now().strftime('%Y%m%d')}.log")
            error_handler = logging.FileHandler(error_file)
            error_handler.setLevel(logging.ERROR)
            
            # Handler para consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            
            # Formato de los logs
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            error_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Agregar handlers al logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(error_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """Registra un mensaje de depuración"""
        self.logger.debug(message)
    
    def info(self, message):
        """Registra un mensaje informativo"""
        self.logger.info(message)
    
    def warning(self, message):
        """Registra un mensaje de advertencia"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=True):
        """Registra un mensaje de error"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=True):
        """Registra un mensaje crítico"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_db_operation(self, operation, entity, entity_id=None, user_id=None, details=None):
        """
        Registra una operación en la base de datos
        
        Args:
            operation: Tipo de operación (CREATE, READ, UPDATE, DELETE)
            entity: Entidad afectada (Alumno, Profesor, etc.)
            entity_id: ID de la entidad (opcional)
            user_id: ID del usuario que realizó la operación (opcional)
            details: Detalles adicionales (opcional)
        """
        message = f"DB_OPERATION: {operation} - {entity}"
        
        if entity_id:
            message += f" - ID: {entity_id}"
        
        if user_id:
            message += f" - User: {user_id}"
        
        if details:
            message += f" - Details: {details}"
            
        self.info(message)