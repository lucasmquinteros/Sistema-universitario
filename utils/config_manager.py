# sistema_universitario/utils/config_manager.py
import os
import json
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Clase para gestionar la configuración del sistema
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, config_file: Optional[str] = None):
        """Implementación de Singleton para el ConfigManager"""
        if cls._instance is None:
            cls._instance = cls(config_file)
        return cls._instance
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Inicializa el gestor de configuración
        
        Args:
            config_file: Ruta al archivo de configuración
        """
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
        self.config = {}
        self.load_config()
    
    def load_config(self, config_file: Optional[str] = None) -> bool:
        """
        Carga la configuración desde un archivo
        
        Args:
            config_file: Ruta al archivo de configuración (opcional)
            
        Returns:
            True si se cargó correctamente, False en caso contrario
        """
        if config_file:
            self.config_file = config_file
            
        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.config_file):
                # Crear configuración por defecto
                self._create_default_config()
                return True
                
            # Determinar el formato del archivo
            file_ext = os.path.splitext(self.config_file)[1].lower()
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                if file_ext == '.json':
                    self.config = json.load(f)
                elif file_ext in ['.yml', '.yaml']:
                    self.config = yaml.safe_load(f)
                else:
                    # Formato no soportado
                    return False
                    
            return True
            
        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
            # Crear configuración por defecto en caso de error
            self._create_default_config()
            return False
    
    def _create_default_config(self) -> None:
        """Crea una configuración por defecto"""
        self.config = {
            'database': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'server': 'localhost\\SQLEXPRESS',
                'database': 'Facultad',
                'trusted_connection': True
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/sistema.log',
                'max_size': 10485760,  # 10 MB
                'backup_count': 5
            },
            'security': {
                'token_expiry': 3600,  # 1 hora
                'password_min_length': 8,
                'token_expiry': 3600,  # 1 hora
                'password_min_length': 8,
                'password_require_special': True,
                'password_require_number': True,
                'password_require_uppercase': True
            },
            'app': {
                'name': 'Sistema Universitario',
                'version': '1.0.0',
                'debug': True
            }
        }
        
        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Guardar la configuración
        self.save_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración
        
        Args:
            key: Clave de configuración (puede usar notación de punto para acceder a subniveles)
            default: Valor por defecto si la clave no existe
            
        Returns:
            Valor de configuración o valor por defecto
        """
        # Manejar notación de punto (ej: "database.server")
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor de configuración
        
        Args:
            key: Clave de configuración (puede usar notación de punto para acceder a subniveles)
            value: Valor a establecer
        """
        # Manejar notación de punto (ej: "database.server")
        keys = key.split('.')
        config = self.config
        
        # Navegar hasta el último nivel
        for i, k in enumerate(keys[:-1]):
            if k not in config:
                config[k] = {}
            config = config[k]
            
        # Establecer el valor
        config[keys[-1]] = value
    
    def save_config(self) -> bool:
        """
        Guarda la configuración en el archivo
        
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Determinar el formato del archivo
            file_ext = os.path.splitext(self.config_file)[1].lower()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                if file_ext == '.json':
                    json.dump(self.config, f, indent=4)
                elif file_ext in ['.yml', '.yaml']:
                    yaml.dump(self.config, f, default_flow_style=False)
                else:
                    # Formato no soportado, usar JSON por defecto
                    json.dump(self.config, f, indent=4)
                    
            return True
            
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")
            return False