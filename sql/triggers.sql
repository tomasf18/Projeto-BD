-- Delete all triggers

IF OBJECT_ID('DeleteHorarioTrigger', 'TR') IS NOT NULL
DROP TRIGGER DeleteHorarioTrigger;
GO

IF OBJECT_ID('DeletePessoaTrigger', 'TR') IS NOT NULL
DROP TRIGGER DeletePessoaTrigger;
GO

IF OBJECT_ID('DeleteEstabelecimentoTrigger', 'TR') IS NOT NULL
DROP TRIGGER DeleteEstabelecimentoTrigger;
GO

IF OBJECT_ID('InsertEstabelecimentoTrigger', 'TR') IS NOT NULL
DROP TRIGGER InsertEstabelecimentoTrigger;
GO

IF OBJECT_ID('InsertAppointment', 'TR') IS NOT NULL
DROP TRIGGER InsertAppointment;
GO

IF OBJECT_ID('InsertInclui', 'TR') IS NOT NULL
DROP TRIGGER InsertInclui;
GO

IF OBJECT_ID('DeleteTipoServicoTrigger', 'TR') IS NOT NULL
DROP TRIGGER DeleteTipoServicoTrigger;
GO

-- Trigger to assign a new schedule to the employees when a schedule is deleted

CREATE TRIGGER DeleteHorarioTrigger ON Horario
INSTEAD OF DELETE
AS
BEGIN
    DECLARE @deletedHorarioId INT;
    DECLARE @novoHorarioId INT;

    -- get the id of the deleted schedule
    SELECT @deletedHorarioId = id
    FROM deleted;

    -- get the id of a random schedule different from the deleted one
    SELECT TOP 1 @novoHorarioId = id
    FROM Horario
    WHERE id <> @deletedHorarioId
    ORDER BY NEWID(); -- to get a random schedule

    BEGIN TRANSACTION;

    BEGIN TRY
        IF @novoHorarioId IS NOT NULL -- if exists a new schedule
            BEGIN
                -- update the employees with the new schedule
                UPDATE Funcionario
                SET id_horario = @novoHorarioId
                WHERE id_horario = @deletedHorarioId;

                -- delete the schedule
                DELETE FROM Horario
                WHERE id = @deletedHorarioId;
            END
        ELSE -- if there is no other schedule
            BEGIN
                RAISERROR('It is not possible to delete this shcedule because there is no other schedule available', 16, 1);
            END
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        RAISERROR('An error occurred deleting this schedule', 16, 1);
    END CATCH
END
GO

-- Trigger to delete a person

CREATE TRIGGER DeletePessoaTrigger ON Pessoa
INSTEAD OF DELETE
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY

        DECLARE @nif INT
        SELECT @nif = nif FROM deleted
        EXEC DeletePessoa @nif;
        DELETE FROM Pessoa
        WHERE nif = @nif;

        COMMIT TRANSACTION;

    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        RAISERROR('An error occurred deleting this person', 16, 1);
    END CATCH
END
GO


-- Trigger to delete an establishment

CREATE TRIGGER DeleteEstabelecimentoTrigger ON Estabelecimento
INSTEAD OF DELETE
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        -- get the nifs of the employees of the establishment
        DECLARE @nifs TABLE (nif INT);
        INSERT INTO @nifs
        SELECT nif
        FROM Funcionario
        WHERE num_estabelecimento = (SELECT id FROM deleted);

        -- cursor for the nifs of the employees
        DECLARE @nif INT;
        DECLARE nif_cursor CURSOR FOR
        SELECT nif
        FROM @nifs;

        OPEN nif_cursor;

        FETCH NEXT FROM nif_cursor INTO @nif;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- delete the employees of the establishment
            EXEC DeleteFuncionariosEstabelecimento @nif;

            FETCH NEXT FROM nif_cursor INTO @nif;
        END
        CLOSE nif_cursor;
        DEALLOCATE nif_cursor;

        -- delete the establishment
        DELETE FROM Estabelecimento
        WHERE id = (SELECT id FROM deleted);

        -- alter again the column nif_gerente to not null
        ALTER TABLE Estabelecimento ALTER COLUMN nif_gerente INT NOT NULL;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        RAISERROR('An error occurred deleting this establishment', 16, 1);
    END CATCH
END
GO


-- Trigger para verificar se o gerente de um estabelecimento é válido ao ser inserido

CREATE TRIGGER InsertEstabelecimentoTrigger ON Estabelecimento
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @id INT;
    DECLARE @especificacao VARCHAR(12);
    DECLARE @cod_postal VARCHAR(8);
    DECLARE @localidade VARCHAR(20);
    DECLARE @rua VARCHAR(30);
    DECLARE @numero INT;
    DECLARE @nif_gerente INT;
    DECLARE @data_inicio_gerente DATE;

    -- get the values to insert in the table Estabelecimento
    SELECT 
        @id = id,
        @especificacao = especificacao,
        @cod_postal = cod_postal,
        @localidade = localidade,
        @rua = rua,
        @numero = numero,
        @nif_gerente = nif_gerente,
        @data_inicio_gerente = data_inicio_gerente
    FROM inserted;

    -- check if the manager is an effective
    IF EXISTS (SELECT 1 FROM Efetivo WHERE nif = @nif_gerente)
    BEGIN
        -- check if the manager is not already a manager of an establishment
        IF NOT EXISTS (SELECT 1 FROM Estabelecimento WHERE nif_gerente = @nif_gerente)
            BEGIN
                BEGIN TRANSACTION;
                BEGIN TRY

                    -- insert the establishment
                    INSERT INTO Estabelecimento (id, especificacao, cod_postal, localidade, rua, numero, nif_gerente, data_inicio_gerente)
                    VALUES (@id, @especificacao, @cod_postal, @localidade, @rua, @numero, @nif_gerente, @data_inicio_gerente);

                    -- transfer the manager to the establishment
                    UPDATE Funcionario
                    SET num_estabelecimento = @id
                    WHERE nif = @nif_gerente;

                    COMMIT TRANSACTION;
                END TRY
                BEGIN CATCH
                    ROLLBACK TRANSACTION;
                    RAISERROR('An error occurred creating the establishment', 16, 1);
                END CATCH
            END
        ELSE
            BEGIN
                RAISERROR('The NIF inserted is from an establishment manager', 16, 1);
            END
    END
    ELSE
        BEGIN
            RAISERROR('The NIF inserted is not from an efective', 16, 1);
        END
END
GO


-- Trigger para verificar se as informações de uma Marcação foram inseridas corretamente

CREATE TRIGGER InsertAppointment ON Marcacao
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @data_marcacao DATETIME;
    DECLARE @nif_funcionario INT;
    DECLARE @nif_cliente INT;
    DECLARE @data_pedido DATETIME;

    -- get the values to insert in the table Marcacao
    SELECT 
        @data_marcacao = data_marcacao,
        @nif_funcionario = nif_funcionario,
        @nif_cliente = nif_cliente,
        @data_pedido = data_pedido
    FROM inserted;

    -- check if the employee is working at the time of the appointment
    DECLARE @id_horario INT;
    SELECT @id_horario = id_horario
    FROM Funcionario
    WHERE nif = @nif_funcionario;

    DECLARE @hora_marcacao TIME;
    SELECT @hora_marcacao = CAST(FORMAT(@data_marcacao, 'HH:mm:ss') AS TIME);

    IF EXISTS (SELECT 1 FROM Horario WHERE id = @id_horario AND h_entrada <= @hora_marcacao AND h_saida > @hora_marcacao)
        BEGIN

            -- check if the employee already have an appointment at the same date & hour
            IF EXISTS (SELECT 1 FROM Marcacao WHERE data_marcacao = @data_marcacao AND nif_funcionario = @nif_funcionario)
                BEGIN
                    RAISERROR('The employee already have an appointment at this date & hour', 16, 1);
                END
            ELSE
                BEGIN
                    -- insert the appointment
                    INSERT INTO Marcacao(data_marcacao, nif_funcionario, nif_cliente, data_pedido)
                    VALUES (@data_marcacao, @nif_funcionario, @nif_cliente, @data_pedido);
                END            
        END
    ELSE
        BEGIN
            RAISERROR('The employee is not working at this hour', 16, 1);
        END

END
GO


-- Trigger to insert a new appointment

CREATE TRIGGER InsertInclui ON Inclui
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @data_marcacao DATETIME;
    DECLARE @nif_funcionario INT;
    DECLARE @nif_cliente INT;
    DECLARE @sexo CHAR(1);
    DECLARE @designacao_tipo_serv VARCHAR(30);

    -- get the values to insert in the table Inclui
    SELECT 
        @data_marcacao = data_marcacao,
        @nif_funcionario = nif_funcionario,
        @nif_cliente = nif_cliente,
        @sexo = sexo,
        @designacao_tipo_serv = designacao_tipo_serv
    FROM inserted;

    -- check if the appointment exists
    IF EXISTS (SELECT 1 FROM Marcacao WHERE data_marcacao = @data_marcacao AND nif_funcionario = @nif_funcionario AND nif_cliente = @nif_cliente)
        BEGIN
            INSERT INTO Inclui(data_marcacao, nif_funcionario, nif_cliente, sexo, designacao_tipo_serv)
            VALUES (@data_marcacao, @nif_funcionario, @nif_cliente, @sexo, @designacao_tipo_serv);
        END
    ELSE
        BEGIN
            RAISERROR('This appointment doesnt exist', 16, 1);
        END
    
END
GO


-- Trigger to delete a type of service

CREATE TRIGGER DeleteTipoServicoTrigger ON Tipo_servico
INSTEAD OF DELETE
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        
        DECLARE @designacao_tipo_serv VARCHAR(30);
        DECLARE @sexo CHAR(1);

        -- get the values to delete in the table Tipo_servico
        SELECT 
            @designacao_tipo_serv = designacao,
            @sexo = sexo
        FROM deleted;

        -- create a temporary table to store the values to delete in Inclui and Marcacao
        CREATE TABLE #tempIncluiDeleted (
            data_marcacao DATETIME,
            nif_funcionario INT,
            nif_cliente INT
        );

        -- get the values to delete in Inclui
        INSERT INTO #tempIncluiDeleted
        SELECT data_marcacao, nif_funcionario, nif_cliente
        FROM Inclui
        WHERE designacao_tipo_serv = @designacao_tipo_serv AND sexo = @sexo;

        -- delete the appointments
        DECLARE @data_marcacao DATETIME, @nif_funcionario INT, @nif_cliente INT;
        DECLARE cur CURSOR FOR 
        SELECT data_marcacao, nif_funcionario, nif_cliente FROM #tempIncluiDeleted;
        OPEN cur;
        FETCH NEXT FROM cur INTO @data_marcacao, @nif_funcionario, @nif_cliente;
        WHILE @@FETCH_STATUS = 0
        BEGIN
            EXEC DeleteAppointment @emp_nif = @nif_funcionario, @client_nif = @nif_cliente, @date = @data_marcacao;
            FETCH NEXT FROM cur INTO @data_marcacao, @nif_funcionario, @nif_cliente;
        END;
        CLOSE cur;
        DEALLOCATE cur;

        DROP TABLE #tempIncluiDeleted;

        -- delete the type of service
        DELETE FROM Tipo_servico
        WHERE designacao = @designacao_tipo_serv AND sexo = @sexo;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        RAISERROR('An error occurred deleting this type of service', 16, 1);
    END CATCH
END
GO