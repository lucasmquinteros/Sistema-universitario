from typing import Dict, List, Any, Optional
from db.manager import DatabaseManager

class BaseService:
    """Clase base para todos los servicios que interactúan con la base de datos"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager