# sistema_universitario/db/sqlalchemy_config.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

Base = declarative_base()

class SQLAlchemyManager:
    """Gestor de conexiones y sesiones de SQLAlchemy"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls, connection_string=None):
        """Implementación de Singleton para el manager de SQLAlchemy"""
        if cls._instance is None and connection_string:
            cls._instance = cls(connection_string)
        return cls._instance
    
    def __init__(self, connection_string):
        """
        Inicializa el gestor de SQLAlchemy
        
        Args:
            connection_string: Cadena de conexión a SQL Server
        """
        # Convertir la cadena de conexión ODBC a formato SQLAlchemy
        params = {}
        parts = connection_string.split(';')
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key.strip()] = value.strip()
        
        # Construir URL de conexión para SQLAlchemy
        driver = params.get('DRIVER', '{ODBC Driver 17 for SQL Server}').replace('{', '').replace('}', '')
        server = params.get('SERVER', 'localhost')
        database = params.get('DATABASE', '')
        
        # Determinar el tipo de autenticación
        if 'Trusted_Connection' in params and params['Trusted_Connection'].lower() == 'yes':
            # Autenticación de Windows
            conn_str = f"mssql+pyodbc://{server}/{database}?driver={urllib.parse.quote_plus(driver)}&trusted_connection=yes"
        else:
            # Autenticación SQL Server
            uid = params.get('UID', '')
            pwd = params.get('PWD', '')
            conn_str = f"mssql+pyodbc://{uid}:{pwd}@{server}/{database}?driver={urllib.parse.quote_plus(driver)}"
        
        # Crear engine y sessionmaker
        self.engine = create_engine(conn_str, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        """Obtiene una sesión de SQLAlchemy"""
        return self.SessionLocal()
    
    def create_tables(self):
        """Crea todas las tablas definidas en los modelos"""
        Base.metadata.create_all(bind=self.engine)