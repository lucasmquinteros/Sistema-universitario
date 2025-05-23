-- Crear tabla Institucion
CREATE TABLE Institucion (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    Direccion VARCHAR(128) NOT NULL
);

-- Crear tabla Carrera
CREATE TABLE Carrera (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL
);

-- Crear tabla InstitucionxCarrera (tabla de relación)
CREATE TABLE InstitucionxCarrera (
    Id_Institucion INTEGER NOT NULL,
    Id_Carrera INTEGER NOT NULL,
    PRIMARY KEY (Id_Institucion, Id_Carrera),
    FOREIGN KEY (Id_Institucion) REFERENCES Institucion(Id),
    FOREIGN KEY (Id_Carrera) REFERENCES Carrera(Id)
);

-- Crear tabla Departamento
CREATE TABLE Departamento (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    Integrantes VARCHAR(128) NOT NULL,
    Id_carrera INTEGER NOT NULL,
    FOREIGN KEY (Id_carrera) REFERENCES Carrera(Id)
);

-- Crear tabla Regimen
CREATE TABLE Regimen (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL
);

-- Crear tabla Area
CREATE TABLE Area (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL
);

-- Crear tabla PlanEstudio
CREATE TABLE PlanEstudio (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Año DATETIME NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    AñoFin DATETIME,  -- Puede ser NULL
    Id_carrera INTEGER NOT NULL,
    FOREIGN KEY (Id_carrera) REFERENCES Carrera(Id)
);

-- Crear tabla Cuatrimestre
CREATE TABLE Cuatrimestre (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Id_plan INTEGER NOT NULL,
    Nro INTEGER NOT NULL,
    FOREIGN KEY (Id_plan) REFERENCES PlanEstudio(Id)
);

-- Crear tabla Asignatura
CREATE TABLE Asignatura (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Hsemanal INTEGER NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    Htotales INTEGER NOT NULL,
    Creditos INTEGER NOT NULL,
    Id_area INTEGER NOT NULL,
    Id_Regimen INTEGER NOT NULL,
    Id_depto INTEGER NOT NULL,
    FOREIGN KEY (Id_area) REFERENCES Area(Id),
    FOREIGN KEY (Id_Regimen) REFERENCES Regimen(Id),
    FOREIGN KEY (Id_depto) REFERENCES Departamento(Id)
);

-- Crear tabla AsignaturaxPlan (tabla de relación)
CREATE TABLE AsignaturaxPlan (
    Id_Plan INTEGER NOT NULL,
    Id_Asignatura INTEGER NOT NULL,
    PRIMARY KEY (Id_Plan, Id_Asignatura),
    FOREIGN KEY (Id_Plan) REFERENCES PlanEstudio(Id),
    FOREIGN KEY (Id_Asignatura) REFERENCES Asignatura(Id)
);

-- Crear tabla MateriasxCuatrimestre (tabla de relación)
CREATE TABLE MateriasxCuatrimestre (
    Id_Asignatura INTEGER NOT NULL,
    Id_cuatrimestre INTEGER NOT NULL,
    PRIMARY KEY (Id_Asignatura, Id_cuatrimestre),
    FOREIGN KEY (Id_Asignatura) REFERENCES Asignatura(Id),
    FOREIGN KEY (Id_cuatrimestre) REFERENCES Cuatrimestre(Id)
);

-- Crear tabla Correlativa (prerrequisitos)
CREATE TABLE Correlativa (
    Id_asignatura INTEGER NOT NULL,
    Id_Correlativa INTEGER NOT NULL,
    PRIMARY KEY (Id_asignatura, Id_Correlativa),
    FOREIGN KEY (Id_asignatura) REFERENCES Asignatura(Id),
    FOREIGN KEY (Id_Correlativa) REFERENCES Asignatura(Id)
);

-- Crear tabla Alumno
CREATE TABLE Alumno (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    Apellido VARCHAR(128) NOT NULL,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    FechaNacimiento DATE NOT NULL,
    Email VARCHAR(128) NOT NULL,
    Telefono VARCHAR(20),
    Direccion VARCHAR(255),
    FechaIngreso DATE NOT NULL,
    Estado VARCHAR(20) NOT NULL DEFAULT 'Activo' -- Activo, Graduado, Baja, etc.
);

-- Crear tabla AlumnoxCarrera (relación entre alumnos y carreras)
CREATE TABLE AlumnoxCarrera (
    Id_Alumno INTEGER NOT NULL,
    Id_Carrera INTEGER NOT NULL,
    FechaInscripcion DATE NOT NULL,
    PRIMARY KEY (Id_Alumno, Id_Carrera),
    FOREIGN KEY (Id_Alumno) REFERENCES Alumno(Id),
    FOREIGN KEY (Id_Carrera) REFERENCES Carrera(Id)
);

-- Crear tabla Profesor
CREATE TABLE Profesor (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(128) NOT NULL,
    Apellido VARCHAR(128) NOT NULL,
    DNI VARCHAR(20) NOT NULL UNIQUE,
    Email VARCHAR(128) NOT NULL,
    Telefono VARCHAR(20),
    Titulo VARCHAR(128) NOT NULL,
    Especialidad VARCHAR(128),
    TipoContrato VARCHAR(50) NOT NULL, -- Tiempo completo, parcial, etc.
    FechaIngreso DATE NOT NULL,
    Id_Departamento INTEGER NOT NULL,
    FOREIGN KEY (Id_Departamento) REFERENCES Departamento(Id)
);

-- Crear tabla ProfesorxAsignatura (relación entre profesores y asignaturas)
Create table ProfesorxAsignatura (
	Profesor_id int,
	Asignatura_id int,
	rol NVARCHAR(128),
	Cuatrimestre_id int,
	AñoAcademico datetime,
	PRIMARY KEY (Profesor_id, Asignatura_id, AñoAcademico, Cuatrimestre_id),
	Foreign Key (Profesor_id) REFERENCES profesor(id),
	Foreign key (Asignatura_id) REFERENCES Asignatura(id),
	Foreign key (cuatrimestre_id) REFERENCES Cuatrimestre(id)
)

-- Crear tabla Cursada (inscripción de alumnos a asignaturas)
CREATE TABLE Cursada (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Id_Alumno INTEGER NOT NULL,
    Id_Asignatura INTEGER NOT NULL,
    Id_Plan INTEGER NOT NULL,
    AñoAcademico INTEGER NOT NULL,
    Cuatrimestre INTEGER NOT NULL,
    Estado VARCHAR(20) NOT NULL, -- Cursando, Regular, Libre, Promocionado
    NotaFinal DECIMAL(4,2),
    FOREIGN KEY (Id_Alumno) REFERENCES Alumno(Id),
    FOREIGN KEY (Id_Asignatura) REFERENCES Asignatura(Id),
    FOREIGN KEY (Id_Plan) REFERENCES PlanEstudio(Id),
    UNIQUE (Id_Alumno, Id_Asignatura, AñoAcademico, Cuatrimestre)
);

-- Crear tabla ExamenFinal
CREATE TABLE ExamenFinal (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Fecha DATE NOT NULL,
    Id_Asignatura INTEGER NOT NULL,
    Id_Profesor INTEGER NOT NULL, -- Profesor que preside la mesa
    Llamado INTEGER NOT NULL, -- 1er llamado, 2do llamado, etc.
    FOREIGN KEY (Id_Asignatura) REFERENCES Asignatura(Id),
    FOREIGN KEY (Id_Profesor) REFERENCES Profesor(Id)
);

-- Crear tabla InscripcionExamen (relación entre alumnos y exámenes finales)
CREATE TABLE InscripcionExamen (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Id_Alumno INTEGER NOT NULL,
    Id_ExamenFinal INTEGER NOT NULL,
    Estado VARCHAR(20) NOT NULL DEFAULT 'Inscripto', -- Inscripto, Presente, Ausente
    Calificacion DECIMAL(4,2),
    Observaciones TEXT,
    FOREIGN KEY (Id_Alumno) REFERENCES Alumno(Id),
    FOREIGN KEY (Id_ExamenFinal) REFERENCES ExamenFinal(Id),
    UNIQUE (Id_Alumno, Id_ExamenFinal)
);



CREATE PROCEDURE InsertarAlumno(
    IN pNombre VARCHAR(255),
    IN pApellido VARCHAR(255),
    IN pDNI VARCHAR(255),
    IN pFechaNacimiento DATE,
    IN pEmail VARCHAR(255),
    IN pTelefono VARCHAR(255),
    IN pDireccion VARCHAR(255),
    IN pFechaIngreso DATE,
    IN pEstado VARCHAR(255)
)
BEGIN
    IF EXISTS (SELECT 1 FROM Alumno WHERE DNI = pDNI) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ya existe un alumno con ese DNI.';
    ELSE
        INSERT INTO Alumno (
            Nombre,
            Apellido,
            DNI,
            FechaNacimiento,
            Email,
            Telefono,
            Direccion,
            FechaIngreso,
            Estado
        )
        VALUES (
            pNombre,
            pApellido,
            pDNI,
            pFechaNacimiento,
            pEmail,
            pTelefono,
            pDireccion,
            pFechaIngreso,
            pEstado
        );
    END IF;
END //

DELIMITER //

CREATE PROCEDURE InsertarInscripcionExamen(
    IN pIdAlumno INTEGER,
    IN pIdExamenFinal INTEGER,
    IN pEstado VARCHAR(255),
    IN pCalificacion DECIMAL(10,2),
    IN pObservaciones TEXT
)
BEGIN
    -- Validar que el alumno exista
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE Id = pIdAlumno) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El alumno no existe.';
    
    -- Validar que el examen final exista
    ELSEIF NOT EXISTS (SELECT 1 FROM ExamenFinal WHERE Id = pIdExamenFinal) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El examen final no existe.';
    
    ELSE
        INSERT INTO InscripcionExamen (
            Id_Alumno,
            Id_ExamenFinal,
            Estado,
            Calificacion,
            Observaciones
        )
        VALUES (
            pIdAlumno,
            pIdExamenFinal,
            pEstado,
            pCalificacion,
            pObservaciones
        );
    END IF;
END 

-- Sistema de Usuarios, Roles y Permisos

-- Tabla de Usuarios (sistema de autenticación)
CREATE TABLE Usuario (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL, -- Almacenar siempre hash, nunca contraseñas en texto plano
    Email VARCHAR(128) NOT NULL UNIQUE,
    FechaCreacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UltimoAcceso DATETIME,
    Estado VARCHAR(20) NOT NULL DEFAULT 'Activo', -- Activo, Bloqueado, Inactivo
    IntentosFallidos INTEGER NOT NULL DEFAULT 0,
    TokenRecuperacion VARCHAR(255),
    ExpiracionToken DATETIME,
    RequiereCambioPassword BIT NOT NULL DEFAULT 0
);

-- Tabla de Roles
CREATE TABLE Rol (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Nombre VARCHAR(50) NOT NULL UNIQUE,
    Descripcion VARCHAR(255),
    NivelAcceso INTEGER NOT NULL -- Útil para jerarquía de roles (1: bajo, 100: alto)
);

-- Tabla de Permisos
CREATE TABLE Permiso (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Codigo VARCHAR(50) NOT NULL UNIQUE, -- Ej: "CREAR_CURSO", "VER_NOTAS"
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255),
    Modulo VARCHAR(50) NOT NULL -- Ej: "Académico", "Administración", "Reportes"
);

-- Relación entre Roles y Permisos (qué permisos tiene cada rol)
CREATE TABLE RolPermiso (
    Id_Rol INTEGER NOT NULL,
    Id_Permiso INTEGER NOT NULL,
    PRIMARY KEY (Id_Rol, Id_Permiso),
    FOREIGN KEY (Id_Rol) REFERENCES Rol(Id) ON DELETE CASCADE,
    FOREIGN KEY (Id_Permiso) REFERENCES Permiso(Id) ON DELETE CASCADE
);

-- Relación entre Usuarios y Roles (qué roles tiene cada usuario)
CREATE TABLE UsuarioRol (
    Id_Usuario INTEGER NOT NULL,
    Id_Rol INTEGER NOT NULL,
    FechaAsignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    AsignadoPor INTEGER, -- ID del usuario que asignó el rol
    PRIMARY KEY (Id_Usuario, Id_Rol),
    FOREIGN KEY (Id_Usuario) REFERENCES Usuario(Id) ON DELETE CASCADE,
    FOREIGN KEY (Id_Rol) REFERENCES Rol(Id) ON DELETE CASCADE,
    FOREIGN KEY (AsignadoPor) REFERENCES Usuario(Id)
);

-- Tabla para vincular usuarios con entidades del sistema
CREATE TABLE UsuarioEntidad (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Id_Usuario INTEGER NOT NULL,
    TipoEntidad VARCHAR(50) NOT NULL, -- "Alumno", "Profesor", "Administrativo", etc.
    Id_Entidad INTEGER NOT NULL, -- ID en la tabla correspondiente (Alumno, Profesor, etc.)
    FOREIGN KEY (Id_Usuario) REFERENCES Usuario(Id),
    UNIQUE (Id_Usuario, TipoEntidad)
);

-- Tabla para registro de actividad (auditoría)
CREATE TABLE LogActividad (
    Id INTEGER PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Id_Usuario INTEGER NOT NULL,
    FechaHora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Accion VARCHAR(100) NOT NULL,
    Detalles TEXT,
    DireccionIP VARCHAR(45),
    UserAgent VARCHAR(255),
    FOREIGN KEY (Id_Usuario) REFERENCES Usuario(Id)
);

-- Insertar roles básicos
INSERT INTO Rol (Nombre, Descripcion, NivelAcceso) VALUES 
('Administrador', 'Control total del sistema', 100),
('Director', 'Gestión académica y administrativa', 80),
('Profesor', 'Gestión de cursos y evaluaciones', 60),
('Alumno', 'Acceso a cursos y calificaciones', 20),
('Invitado', 'Acceso limitado a información pública', 10);

-- Insertar algunos permisos de ejemplo
INSERT INTO Permiso (Codigo, Nombre, Descripcion, Modulo) VALUES
-- Permisos administrativos
('ADMIN_TOTAL', 'Administración Total', 'Control completo del sistema', 'Administración'),
('GESTIONAR_USUARIOS', 'Gestionar Usuarios', 'Crear, modificar y eliminar usuarios', 'Administración'),
('GESTIONAR_ROLES', 'Gestionar Roles', 'Asignar y revocar roles', 'Administración'),

-- Permisos académicos
('CREAR_CARRERA', 'Crear Carrera', 'Crear nuevas carreras', 'Académico'),
('MODIFICAR_PLAN', 'Modificar Plan de Estudio', 'Editar planes de estudio', 'Académico'),
('CREAR_ASIGNATURA', 'Crear Asignatura', 'Crear nuevas asignaturas', 'Académico'),
('ASIGNAR_PROFESOR', 'Asignar Profesor', 'Asignar profesores a asignaturas', 'Académico'),

-- Permisos para profesores
('CARGAR_NOTAS', 'Cargar Notas', 'Registrar calificaciones', 'Evaluación'),
('CREAR_EXAMEN', 'Crear Examen', 'Crear nuevos exámenes', 'Evaluación'),
('VER_ALUMNOS', 'Ver Alumnos', 'Ver lista de alumnos inscriptos', 'Académico'),

-- Permisos para alumnos
('VER_NOTAS', 'Ver Notas', 'Ver calificaciones propias', 'Académico'),
('INSCRIBIR_MATERIA', 'Inscribirse a Materia', 'Inscribirse en asignaturas', 'Académico'),
('INSCRIBIR_EXAMEN', 'Inscribirse a Examen', 'Inscribirse a exámenes finales', 'Académico');

-- Asignar permisos a roles
-- Administrador tiene todos los permisos
INSERT INTO RolPermiso (Id_Rol, Id_Permiso) 
SELECT 1, Id FROM Permiso;

-- Director
INSERT INTO RolPermiso (Id_Rol, Id_Permiso)
SELECT 2, Id FROM Permiso 
WHERE Codigo IN ('CREAR_CARRERA', 'MODIFICAR_PLAN', 'CREAR_ASIGNATURA', 'ASIGNAR_PROFESOR', 'VER_ALUMNOS', 'GESTIONAR_USUARIOS');

-- Profesor
INSERT INTO RolPermiso (Id_Rol, Id_Permiso)
SELECT 3, Id FROM Permiso 
WHERE Codigo IN ('CARGAR_NOTAS', 'CREAR_EXAMEN', 'VER_ALUMNOS');

-- Alumno
INSERT INTO RolPermiso (Id_Rol, Id_Permiso)
SELECT 4, Id FROM Permiso 
WHERE Codigo IN ('VER_NOTAS', 'INSCRIBIR_MATERIA', 'INSCRIBIR_EXAMEN');
