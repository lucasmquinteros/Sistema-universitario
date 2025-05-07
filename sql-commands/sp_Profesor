
CREATE PROCEDURE sp_CrearProfesor
    @Nombre NVARCHAR(128),
    @Apellido NVARCHAR(128),
    @DNI NVARCHAR(20),
    @Email NVARCHAR(128),
    @Telefono NVARCHAR(20) = NULL,
    @Titulo NVARCHAR(128),
    @Especialidad NVARCHAR(128) = NULL,
    @TipoContrato NVARCHAR(50),
    @FechaIngreso DATE = NULL,
    @Id_Departamento INT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM Profesor WHERE DNI = @DNI)
    BEGIN
        RAISERROR('Ya existe un profesor con ese DNI', 16, 1);
        RETURN;
    END

    IF @FechaIngreso IS NULL
        SET @FechaIngreso = GETDATE();
    
    BEGIN TRANSACTION;
    
    BEGIN TRY

        INSERT INTO Profesor (Nombre, Apellido, DNI, Email, Telefono, 
                             Titulo, Especialidad, TipoContrato, FechaIngreso, Id_Departamento)
        VALUES (@Nombre, @Apellido, @DNI, @Email, @Telefono,
               @Titulo, @Especialidad, @TipoContrato, @FechaIngreso, @Id_Departamento);
        
        SELECT SCOPE_IDENTITY() AS ProfesorId;
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END



-- Obtener Profesor
CREATE PROCEDURE sp_ObtenerProfesor
    @ProfesorId INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Datos básicos del profesor con nombre del departamento
    SELECT p.*, d.Nombre AS Departamento
    FROM Profesor p
    LEFT JOIN Departamento d ON p.Id_Departamento = d.Id
    WHERE p.Id = @ProfesorId;
    
    -- Asignaturas que imparte
    SELECT a.Id, a.Nombre, pa.Rol, pa.AñoAcademico, pa.Cuatrimestre
    FROM Asignatura a
    JOIN ProfesorxAsignatura pa ON a.Id = pa.Id_Asignatura
    WHERE pa.Id_Profesor = @ProfesorId;
    
    RETURN 0;
END



-- Listar Profesores
CREATE PROCEDURE sp_ListarProfesores
    @DepartamentoId INT = NULL,
    @Especialidad NVARCHAR(128) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT p.*, d.Nombre AS Departamento
    FROM Profesor p
    LEFT JOIN Departamento d ON p.Id_Departamento = d.Id
    WHERE (@DepartamentoId IS NULL OR p.Id_Departamento = @DepartamentoId)
      AND (@Especialidad IS NULL OR p.Especialidad LIKE '%' + @Especialidad + '%')
    ORDER BY p.Apellido, p.Nombre;
    
    RETURN 0;
END



-- Asignar Profesor a Asignatura
CREATE PROCEDURE sp_AsignarProfesorAsignatura
    @ProfesorId INT,
    @AsignaturaId INT,
    @Rol NVARCHAR(50),
    @AñoAcademico INT,
    @Cuatrimestre INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Verificar que el profesor existe
    IF NOT EXISTS (SELECT 1 FROM Profesor WHERE Id = @ProfesorId)
    BEGIN
        RAISERROR('El profesor no existe', 16, 1);
        RETURN -1;
    END
    
    -- Verificar que la asignatura existe
    IF NOT EXISTS (SELECT 1 FROM Asignatura WHERE Id = @AsignaturaId)
    BEGIN
        RAISERROR('La asignatura no existe', 16, 1);
        RETURN -2;
    END
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Verificar si ya existe la asignación
        IF EXISTS (
            SELECT 1 
            FROM ProfesorxAsignatura 
            WHERE Id_Profesor = @ProfesorId 
              AND Id_Asignatura = @AsignaturaId
              AND AñoAcademico = @AñoAcademico
              AND Cuatrimestre = @Cuatrimestre
        )
        BEGIN
            -- Actualizar rol si ya existe
            UPDATE ProfesorxAsignatura
            SET Rol = @Rol
            WHERE Id_Profesor = @ProfesorId 
              AND Id_Asignatura = @AsignaturaId
              AND AñoAcademico = @AñoAcademico
              AND Cuatrimestre = @Cuatrimestre;
        END
        ELSE
        BEGIN
            -- Insertar nueva asignación
            INSERT INTO ProfesorxAsignatura (Id_Profesor, Id_Asignatura, Rol, AñoAcademico, Cuatrimestre)
            VALUES (@ProfesorId, @AsignaturaId, @Rol, @AñoAcademico, @Cuatrimestre);
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


CREATE PROCEDURE sp_MoficarProfesor
    @ProfesorId INT,
    @Nombre NVARCHAR(128),
    @Apellido VARCHAR(128),
    @DNI VARCHAR(128),
    @Email VARCHAR(128),
    @Telefono VARCHAR(128),
    @Titulo VARCHAR(128),
    @Especialidad VARCHAR(128),
    @TipoContrato VARCHAR(128),
    @FechaIngreso DATE
AS
BEGIN
    SET NOCOUNT ON;
        
        IF @FechaIngreso IS NULL
        SET @FechaIngreso = GETDATE();

        BEGIN TRANSACTION;
        
        BEGIN TRY
            UPDATE Profesor
            SET 
			    Nombre = ISNULL(@Nombre, Nombre),
                Apellido = ISNULL(@Apellido, Apellido),
                DNI = ISNULL(@DNI, DNI),
                Email = ISNULL(@Email, Email),
                Telefono = ISNULL(@Telefono, Telefono),
                Titulo = ISNULL(@Titulo, Titulo),
                Especialidad = ISNULL(@Especialidad, Especialidad),
                TipoContrato = ISNULL(@TipoContrato, TipoContrato),
                FechaIngreso = @FechaIngreso
            WHERE Id = @ProfesorId;
            
            COMMIT TRANSACTION;
            RETURN 0; 
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW; 
            RETURN ERROR_NUMBER();
        END CATCH
END

CREATE PROCEDURE sp_EliminarProfesor
    @ProfesorId
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRANSACTION;

    BEGIN TRY 
        DELETE FROM ProfesorxAsignatura WHERE Id_Profesor = @ProfesorId

        DELETE FROM ExamenFinal WHERE Id_Profesor = @ProfesorId

        DELETE FROM  Profesor WHERE Id = @ProfesorId

    COMMIT TRANSACTION;
    RETURN 0;
    END TRY
    BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW; 
            RETURN ERROR_NUMBER();
    END CATCH
END
    

CREATE PROCEDURE sp_ObtenerAsignaturasProfesor
    @ProfesorId INT 
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        IF NOT EXISTS (SELECT 1 FROM Profesor WHERE Id = @ProfesorId)
        BEGIN
            RAISERROR('El profesor no existe', 16, 1);
            RETURN;
        END

        SELECT 
            p.Nombre AS ProfesorNombre, 
            a.Nombre AS AsignaturaNombre, 
            PA.Rol, 
            PA.CuatrimestreAP, 
            PA.AñoAcademico 
        FROM ProfesorxAsignatura PA
        LEFT JOIN Asignatura a ON PA.Id_asignatura = a.Id 
        LEFT JOIN Profesor p ON PA.Id_Profesor = p.Id
        WHERE PA.Id_Profesor = @ProfesorId;
    END TRY
    BEGIN CATCH

        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;