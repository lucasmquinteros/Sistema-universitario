# sistema_universitario/db/models/sqlalchemy_models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Table, Text, Float
from sqlalchemy.orm import relationship
from sistema_universitario.db.sqlalchemy_config import Base

# Tabla de relación entre profesores y asignaturas
profesor_asignatura = Table(
    'ProfesorxAsignatura',
    Base.metadata,
    Column('Id', Integer, primary_key=True),
    Column('Id_Profesor', Integer, ForeignKey('Profesor.Id')),
    Column('Id_Asignatura', Integer, ForeignKey('Asignatura.Id')),
    Column('Rol', String(50)),
    Column('AñoAcademico', Integer),
    Column('Cuatrimestre', Integer)
)

# Tabla de relación entre alumnos y carreras
alumno_carrera = Table(
    'AlumnoxCarrera',
    Base.metadata,
    Column('Id', Integer, primary_key=True),
    Column('Id_Alumno', Integer, ForeignKey('Alumno.Id')),
    Column('Id_Carrera', Integer, ForeignKey('Carrera.Id')),
    Column('FechaInscripcion', Date)
)

class Profesor(Base):
    __tablename__ = 'Profesor'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Apellido = Column(String(128), nullable=False)
    DNI = Column(String(20), unique=True, nullable=False)
    Email = Column(String(128))
    Telefono = Column(String(20))
    Titulo = Column(String(128))
    Especialidad = Column(String(128))
    TipoContrato = Column(String(50))
    FechaIngreso = Column(Date)
    Id_Departamento = Column(Integer, ForeignKey('Departamento.Id'))
    
    # Relaciones
    departamento = relationship("Departamento", back_populates="profesores")
    asignaturas = relationship("Asignatura", secondary=profesor_asignatura, back_populates="profesores")
    
    def __repr__(self):
        return f"<Profesor(Id={self.Id}, Nombre='{self.Nombre}', Apellido='{self.Apellido}')>"

class Alumno(Base):
    __tablename__ = 'Alumno'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Apellido = Column(String(128), nullable=False)
    DNI = Column(String(20), unique=True, nullable=False)
    Email = Column(String(128))
    Telefono = Column(String(20))
    Direccion = Column(String(256))
    FechaNacimiento = Column(Date)
    FechaIngreso = Column(Date)
    Estado = Column(String(20))
    
    # Relaciones
    carreras = relationship("Carrera", secondary=alumno_carrera, back_populates="alumnos")
    cursadas = relationship("Cursada", back_populates="alumno")
    
    def __repr__(self):
        return f"<Alumno(Id={self.Id}, Nombre='{self.Nombre}', Apellido='{self.Apellido}')>"

class Asignatura(Base):
    __tablename__ = 'Asignatura'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Hsemanal = Column(Integer)
    Htotales = Column(Integer)
    Creditos = Column(Integer)
    Id_area = Column(Integer, ForeignKey('Area.Id'))
    Id_Regimen = Column(Integer, ForeignKey('Regimen.Id'))
    Id_depto = Column(Integer, ForeignKey('Departamento.Id'))
    
    # Relaciones
    area = relationship("Area", back_populates="asignaturas")
    regimen = relationship("Regimen", back_populates="asignaturas")
    departamento = relationship("Departamento", back_populates="asignaturas")
    profesores = relationship("Profesor", secondary=profesor_asignatura, back_populates="asignaturas")
    
    def __repr__(self):
        return f"<Asignatura(Id={self.Id}, Nombre='{self.Nombre}')>"

class Departamento(Base):
    __tablename__ = 'Departamento'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Descripcion = Column(Text)
    
    # Relaciones
    profesores = relationship("Profesor", back_populates="departamento")
    asignaturas = relationship("Asignatura", back_populates="departamento")
    
    def __repr__(self):
        return f"<Departamento(Id={self.Id}, Nombre='{self.Nombre}')>"

class Area(Base):
    __tablename__ = 'Area'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Descripcion = Column(Text)
    
    # Relaciones
    asignaturas = relationship("Asignatura", back_populates="area")
    
    def __repr__(self):
        return f"<Area(Id={self.Id}, Nombre='{self.Nombre}')>"

class Regimen(Base):
    __tablename__ = 'Regimen'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Descripcion = Column(Text)
    
    # Relaciones
    asignaturas = relationship("Asignatura", back_populates="regimen")
    
    def __repr__(self):
        return f"<Regimen(Id={self.Id}, Nombre='{self.Nombre}')>"

class Carrera(Base):
    __tablename__ = 'Carrera'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Descripcion = Column(Text)
    Duracion = Column(Integer)  # En cuatrimestres
    
    # Relaciones
    alumnos = relationship("Alumno", secondary=alumno_carrera, back_populates="carreras")
    planes = relationship("PlanEstudio", back_populates="carrera")
    
    def __repr__(self):
        return f"<Carrera(Id={self.Id}, Nombre='{self.Nombre}')>"

class PlanEstudio(Base):
    __tablename__ = 'PlanEstudio'
    
    Id = Column(Integer, primary_key=True)
    Nombre = Column(String(128), nullable=False)
    Año = Column(Integer, nullable=False)
    Descripcion = Column(Text)
    Activo = Column(Boolean, default=True)
    Id_Carrera = Column(Integer, ForeignKey('Carrera.Id'))
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="planes")
    
    def __repr__(self):
        return f"<PlanEstudio(Id={self.Id}, Nombre='{self.Nombre}', Año={self.Año})>"

class Cursada(Base):
    __tablename__ = 'Cursada'
    
    Id = Column(Integer, primary_key=True)
    Id_Alumno = Column(Integer, ForeignKey('Alumno.Id'))
    Id_Asignatura = Column(Integer, ForeignKey('Asignatura.Id'))
    AñoAcademico = Column(Integer)
    Cuatrimestre = Column(Integer)
    Estado = Column(String(20))  # Cursando, Aprobada, Desaprobada, Abandonada
    
    # Relaciones
    alumno = relationship("Alumno", back_populates="cursadas")
    
    def __repr__(self):
        return f"<Cursada(Id={self.Id}, Id_Alumno={self.Id_Alumno}, Id_Asignatura={self.Id_Asignatura})>"