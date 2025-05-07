CREATE PROCEDURE sp_CrearCarrera
    @Nombre
    @Titulo
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM Carrera WHERE Nombre = @Nombre)
    BEGIN
        RAISERROR('Ya existe esa carrera', 16, 1);
        RETURN -1;
    END

    BEGIN TRANSACTION
        BEGIN TRY
            INSERT INTO Carrera(Nombre, Titulo) VALUES @Nombre, @Titulo
    
        COMMIT TRANSACTION;
        END TRY
        BEGIN CATCH
            ROLLBACK TRANSACTION;
            THROW;
            RETURN ERROR_NUMBER();
        END CATCH
END


CREATE PROCEDURE sp_ObtenerCarrera
    @CarreraId
AS
BEGIN
    SET NOCOUNT ON;

    SELECT Nombre, Titulo FROM Carrera
    WHERE Id = @CarreraId

    RETURN 0;
END


    