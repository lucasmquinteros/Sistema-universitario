CREATE PROCEDURE sp_EliminarAlumno
    @id INT,
    @DNI NVARCHAR(20)
AS
BEGIN 
    SET NOCOUNT ON;
   
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE id = @id AND DNI = @DNI)
    BEGIN
        RETURN -1;
    END
    
    BEGIN TRY
        BEGIN TRANSACTION;
        

        DELETE FROM InscripcionExamen WHERE Id_Alumno = @id;
        DELETE FROM Cursada WHERE Id_Alumno = @id;
        DELETE FROM AlumnoxCarrera WHERE Id_Alumno = @id;
        DELETE FROM Alumno WHERE Id = @id;
        
        COMMIT TRANSACTION;
        
        RETURN 0; 
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        RAISERROR('Error en sp_EliminarAlumno (ID: %d): %s', 
                 @ErrorSeverity, 
                 @ErrorState,
                 @id,
                 @ErrorMessage);
        RETURN ERROR_NUMBER();
    END CATCH
END


-- Crear Alumno
CREATE PROCEDURE sp_CrearAlumno
    @Nombre NVARCHAR(128),
    @Apellido NVARCHAR(128),
    @DNI NVARCHAR(20),
    @FechaNacimiento DATE,
    @Email NVARCHAR(128),
    @Telefono NVARCHAR(20) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @FechaIngreso DATE = NULL,
    @CarreraId INT = NULL,
    @AlumnoId INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Validar que el DNI no exista
    IF EXISTS (SELECT 1 FROM Alumno WHERE DNI = @DNI)
    BEGIN
        RAISERROR('Ya existe un alumno con ese DNI', 16, 1);
        RETURN -1;
    END
    
    -- Establecer fecha de ingreso si no se proporciona
    IF @FechaIngreso IS NULL
        SET @FechaIngreso = GETDATE();
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Insertar alumno
        INSERT INTO Alumno (Nombre, Apellido, DNI, FechaNacimiento, Email, 
                           Telefono, Direccion, FechaIngreso, Estado)
        VALUES (@Nombre, @Apellido, @DNI, @FechaNacimiento, @Email,
               @Telefono, @Direccion, @FechaIngreso, 'Activo');
        
        -- Obtener ID generado
        SET @AlumnoId = SCOPE_IDENTITY();
        
        -- Si se proporciona carrera, inscribir al alumno
        IF @CarreraId IS NOT NULL
        BEGIN
            INSERT INTO AlumnoxCarrera (Id_Alumno, Id_Carrera, FechaInscripcion)
            VALUES (@AlumnoId, @CarreraId, GETDATE());
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW; -- Re-lanzar la excepción
        RETURN ERROR_NUMBER();
    END CATCH
END


-- Obtener Alumno
CREATE PROCEDURE sp_ObtenerAlumno
    @AlumnoId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Datos básicos del alumno
    SELECT * FROM Alumno WHERE Id = @AlumnoId;
    
    -- Carreras del alumno
    SELECT c.Id, c.Nombre, ac.FechaInscripcion
    FROM Carrera c
    JOIN AlumnoxCarrera ac ON c.Id = ac.Id_Carrera
    WHERE ac.Id_Alumno = @AlumnoId;
    
    -- Cursadas actuales
    SELECT a.Id, a.Nombre, c.Estado, c.NotaFinal
    FROM Asignatura a
    JOIN Cursada c ON a.Id = c.Id_Asignatura
    WHERE c.Id_Alumno = @AlumnoId AND c.Estado = 'Cursando';
    
    -- Usuario asociado
    SELECT u.Id, u.Username, u.Email
    FROM Usuario u
    JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
    WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
    
    RETURN 0;
END



-- Modificar Alumno
CREATE PROCEDURE sp_ModificarAlumno
    @AlumnoId INT,
    @Nombre NVARCHAR(128) = NULL,
    @Apellido NVARCHAR(128) = NULL,
    @Email NVARCHAR(128) = NULL,
    @Telefono NVARCHAR(20) = NULL,
    @Direccion NVARCHAR(255) = NULL,
    @Estado NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar que el alumno existe
    IF NOT EXISTS (SELECT 1 FROM Alumno WHERE Id = @AlumnoId)
    BEGIN
        RAISERROR('El alumno no existe', 16, 1);
        RETURN -1;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Actualizar solo los campos proporcionados
        UPDATE Alumno
        SET 
            Nombre = ISNULL(@Nombre, Nombre),
            Apellido = ISNULL(@Apellido, Apellido),
            Email = ISNULL(@Email, Email),
            Telefono = ISNULL(@Telefono, Telefono),
            Direccion = ISNULL(@Direccion, Direccion),
            Estado = ISNULL(@Estado, Estado)
        WHERE Id = @AlumnoId;
        
        -- Si se actualizó el email, actualizar también en Usuario si existe
        IF @Email IS NOT NULL
        BEGIN
            UPDATE u
            SET u.Email = @Email
            FROM Usuario u
            JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
            WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
        END
        
        -- Si se cambió el estado a inactivo, actualizar usuario
        IF @Estado = 'Inactivo'
        BEGIN
            UPDATE u
            SET u.Estado = 'Inactivo'
            FROM Usuario u
            JOIN UsuarioEntidad ue ON u.Id = ue.Id_Usuario
            WHERE ue.TipoEntidad = 'Alumno' AND ue.Id_Entidad = @AlumnoId;
        END
        
        COMMIT TRANSACTION;
        RETURN 0; -- Éxito
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
        RETURN ERROR_NUMBER();
    END CATCH
END


CREATE PROCEDURE sp_ListarAlumnos
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        A.Id,
        A.DNI,
        A.Nombre,
        A.Apellido,
        CASE 
            WHEN A.Email IS NULL THEN 'No proporcionado'
            ELSE A.Email
        END AS Email,
        CASE
            WHEN C.Nombre IS NULL THEN 'Carrera no asignada'
            WHEN C.Nombre = '' THEN 'Carrera en proceso'
            ELSE C.Nombre
        END AS NombreCarrera,
        A.FechaIngreso,
        A.Estado
    FROM 
        Alumno A
    LEFT JOIN 
        AlumnoxCarrera AC ON A.Id = AC.Id_Alumno
    LEFT JOIN
        Carrera C ON AC.Id_Carrera = C.Id
    ORDER BY 
        A.Apellido, A.Nombre;
END


CREATE PROCEDURE InsertarAlumno(
    @Nombre VARCHAR(255),
    @Apellido VARCHAR(255),
    @DNI VARCHAR(255),
    @FechaNacimiento DATE,
    @Email VARCHAR(255),
    @Telefono VARCHAR(255),
    @Direccion VARCHAR(255),
    @Fechaingreso DATE,
    @Estado VARCHAR(255)
)
BEGIN
    IF EXISTS (SELECT 1 FROM Alumno WHERE DNI = @DNI) THEN
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
            @Nombre,
            @Apellido,
            @DNI,
            @FechaNacimiento,
            @Email,
            @Telefono,
            @Direccion,
            @FechaIngreso,
            @Estado
        );
    END IF;
END //

CREATE PROCEDURE sp_ObtenerCursadasAlumno
    @AlumnoId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        c.Id,
        a.Nombre AS Asignatura,
        c.AñoAcademico,
        c.Cuatrimestre,
        c.Estado,
        c.NotaFinal
    FROM 
        Cursada c
    JOIN 
        Asignatura a ON c.Id_Asignatura = a.Id
    WHERE 
        c.Id_Alumno = @AlumnoId;
END


CREATE PROCEDURE sp_InscribirAlumnoCarrera
    @AlumnoId INT,
    @CarreraId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    IF EXISTS (SELECT 1 FROM AlumnoxCarrera WHERE Id_Alumno = @AlumnoId AND Id_Carrera = @CarreraId)
    BEGIN
        RAISERROR('El alumno ya está inscrito en esta carrera', 16, 1);
        RETURN -1;
    END
    
    INSERT INTO AlumnoxCarrera (Id_Alumno, Id_Carrera, FechaInscripcion)
    VALUES (@AlumnoId, @CarreraId, GETDATE());
    
    RETURN 0; -- Éxito
END 