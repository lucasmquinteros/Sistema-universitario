from datetime import datetime
from db.manager import DatabaseManager
from services.alumno_service import AlumnoService

print("Intento de creacion de alumno:")

datos_alumno = {
    "nombre": "Lucas",
    "apellido": "Martini Quinteros",
    "dni": "46330415",
    "fecha_nacimiento": datetime(2004, 10, 1),
    "email": "lmartiniquinteros@gmail.com",
    "telefono": "3364628400",
    "direccion": "Camelia 2275",
    "fecha_ingreso": datetime(2023, 1, 1),
    "carrera_id": 1,
}

db_manager = DatabaseManager(
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=sistema_universitario2;Trusted_Connection=yes;"
)
alumno_service = AlumnoService(db_manager)


# Ejecutar el stored procedure
resultado = db_manager.execute_stored_procedure(
    "sp_CrearAlumno",  # Nombre de tu stored procedure
    datos_alumno,
)
# El resultado debería contener el ID generado
alumno_id = resultado["@id"] if resultado else None

if alumno_id:
    print(f"Alumno creado con ID: {alumno_id}")
    datosIngresados = alumno_service.obtener(alumno_id)
    print(datosIngresados)
else:
    print("Error al crear el alumno.")
