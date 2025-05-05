# sistema_universitario/api/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import sys
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import Token, create_access_token, get_current_user, get_current_active_user
from services.usuario_service import UsuarioService

# Agregar directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.manager import DatabaseManager
from db.sqlalchemy_config import SQLAlchemyManager
from services.profesor_sevices_hibrid import ProfesorServiceHybrid
from api.schemas import ProfesorCreate, ProfesorResponse, ProfesorList
from utils.logger import Logger

# Inicializar FastAPI
app = FastAPI(
    title="Sistema Universitario API",
    description="API para el sistema de gestión universitaria",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar conexión a base de datos
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=Facultad;Trusted_Connection=yes;"
db_manager = DatabaseManager(connection_string)
sqlalchemy_manager = SQLAlchemyManager.get_instance(connection_string)

# Inicializar logger
logger = Logger.get_instance()

# Configurar autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencia para obtener sesión de SQLAlchemy
def get_db():
    db = sqlalchemy_manager.get_session()
    try:
        yield db
    finally:
        db.close()

# Inicializar servicios
profesor_service = ProfesorServiceHybrid(db_manager, sqlalchemy_manager)

# Rutas de la API
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Sistema Universitario"}

# Rutas para profesores
@app.post("/profesores/", response_model=ProfesorResponse, status_code=status.HTTP_201_CREATED)
def create_profesor(profesor: ProfesorCreate):
    """Crear un nuevo profesor"""
    profesor_id = profesor_service.crear(profesor.dict())
    if not profesor_id:
        raise HTTPException(status_code=400, detail="No se pudo crear el profesor")
    
    # Obtener el profesor creado
    nuevo_profesor = profesor_service.obtener(profesor_id)
    if not nuevo_profesor:
        raise HTTPException(status_code=404, detail="Profesor creado pero no se pudo recuperar")
        
    return nuevo_profesor

@app.get("/profesores/{profesor_id}", response_model=ProfesorResponse)
def get_profesor(profesor_id: int):
    """Obtener un profesor por ID"""
    profesor = profesor_service.obtener(profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@app.get("/profesores/", response_model=List[ProfesorList])
def list_profesores(
    departamento_id: Optional[int] = None,
    especialidad: Optional[str] = None,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None
):
    """Listar profesores con filtros opcionales"""
    filtros = {}
    if departamento_id:
        filtros["departamento_id"] = departamento_id
    if especialidad:
        filtros["especialidad"] = especialidad
    if nombre:
        filtros["nombre"] = nombre
    if apellido:
        filtros["apellido"] = apellido
        
    profesores = profesor_service.listar(filtros)
    return profesores

@app.post("/profesores/{profesor_id}/asignaturas/{asignatura_id}")
def assign_asignatura(
    profesor_id: int,
    asignatura_id: int,
    rol: str,
    año_academico: int,
    cuatrimestre: int
):
    """Asignar una asignatura a un profesor"""
    result = profesor_service.asignar_asignatura(
        profesor_id, asignatura_id, rol, año_academico, cuatrimestre
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo asignar la asignatura")
        
    return {"message": "Asignatura asignada correctamente"}



# Inicializar servicio de usuario
usuario_service = UsuarioService(db_manager)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    success, user = usuario_service.autenticar(form_data.username, form_data.password)
    if not success or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["Username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=dict)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user

# Ejemplo de ruta protegida
@app.get("/profesores/protegido/")
async def protected_route(current_user: dict = Depends(get_current_active_user)):
    return {"message": "Esta es una ruta protegida", "user": current_user["Username"]}

# Punto de entrada para ejecutar con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)