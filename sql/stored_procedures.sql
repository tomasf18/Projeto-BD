-- Eliminar os Sp

IF OBJECT_ID('DeleteCliente', 'P') IS NOT NULL
DROP PROCEDURE DeleteCliente;
GO

IF OBJECT_ID('DeleteEfetivo', 'P') IS NOT NULL
DROP PROCEDURE DeleteEfetivo;
GO

IF OBJECT_ID('DeleteFuncionario', 'P') IS NOT NULL
DROP PROCEDURE DeleteFuncionario;
GO

IF OBJECT_ID('DeletePessoa', 'P') IS NOT NULL
DROP PROCEDURE DeletePessoa;
GO

IF OBJECT_ID('DeleteFuncionariosEstabelecimento', 'P') IS NOT NULL
DROP PROCEDURE DeleteFuncionariosEstabelecimento;
GO

IF OBJECT_ID('UpdateEmployeeDetails', 'P') IS NOT NULL
DROP PROCEDURE UpdateEmployeeDetails;
GO

IF OBJECT_ID('CreateEmployee', 'P') IS NOT NULL
DROP PROCEDURE CreateEmployee;
GO

IF OBJECT_ID('CreateTem', 'P') IS NOT NULL
DROP PROCEDURE CreateTem;
GO

IF OBJECT_ID('DeleteAppointment', 'P') IS NOT NULL
DROP PROCEDURE DeleteAppointment;
GO


-- SP to delete a client
CREATE PROCEDURE DeleteCliente @nif INT
AS
BEGIN
    -- delete the client's reviews
    DELETE FROM Avaliacao
    WHERE nif_cliente = @nif;

    -- delete the client's appointments
    DELETE FROM Marcacao
    WHERE nif_cliente = @nif;

    -- delete the client
    DELETE FROM Cliente
    WHERE nif = @nif;
END
GO

-- SP to delete an effective employee
CREATE PROCEDURE DeleteEfetivo @nif INT
AS
BEGIN
    DECLARE @nif_estabelecimento INT;
    DECLARE @novo_gerente INT;

    -- Check if the employee is a manager
    SELECT @nif_estabelecimento = id
    FROM Estabelecimento
    WHERE nif_gerente = @nif;

    IF @nif_estabelecimento IS NOT NULL -- It is a manager
    BEGIN
        -- Try to find another effective employee in the establishment
        SELECT TOP 1 @novo_gerente = Efetivo.nif
        FROM Efetivo
        JOIN Funcionario ON Efetivo.nif = Funcionario.nif
        WHERE Funcionario.num_estabelecimento = @nif_estabelecimento
        AND Efetivo.nif <> @nif;

        IF @novo_gerente IS NULL -- If there is no other effective employee in the establishment, find another
        BEGIN
            SELECT TOP 1 @novo_gerente = Efetivo.nif
            FROM Efetivo
            WHERE Efetivo.nif <> @nif
            AND Efetivo.nif NOT IN (SELECT nif_gerente FROM Estabelecimento);

            IF @novo_gerente IS NOT NULL -- Move the employee to the establishment
            BEGIN
                UPDATE Funcionario
                SET num_estabelecimento = @nif_estabelecimento
                WHERE nif = @novo_gerente;
            END
            ELSE -- there is no other effective employee available
            BEGIN
                RAISERROR('It is not possible to remove the manager, there is no other available', 16, 1);
                RETURN;
            END
        END

        -- update the establishment manager
        UPDATE Estabelecimento
        SET nif_gerente = @novo_gerente
        WHERE id = @nif_estabelecimento;

        -- delete the entries in the Tem table
        DELETE FROM Tem
        WHERE nif_efetivo = @nif;

        -- delete the employee's contract
        DELETE FROM Contrato
        WHERE nif_efetivo = @nif;

        -- delete the effective
        DELETE FROM Efetivo
        WHERE nif = @nif;
    END
    ELSE -- it is not a manager
    BEGIN
        -- delete the entries in the Tem table
        DELETE FROM Tem
        WHERE nif_efetivo = @nif;

        -- delete the employee's contract
        DELETE FROM Contrato
        WHERE nif_efetivo = @nif;

        -- delete the effective
        DELETE FROM Efetivo
        WHERE nif = @nif;
    END
END
GO

-- SP to delete an employee
CREATE PROCEDURE DeleteFuncionario @nif INT
AS
BEGIN
    -- check if the employee is an effective
    IF EXISTS (SELECT 1 FROM Efetivo WHERE nif = @nif)
        BEGIN
            EXEC DeleteEfetivo @nif;
        END
    ELSE -- it is an intern
        BEGIN
            DELETE FROM Estagiario
            WHERE nif = @nif;
        END
    -- delete the employee's reviews
    DELETE FROM Avaliacao
    WHERE nif_funcionario = @nif;

    -- delete the employee's appointments
    DELETE FROM Marcacao
    WHERE nif_funcionario = @nif;

    -- delete the employee's phone numbers
    DELETE FROM Nums_telem_func
    WHERE nif_func = @nif;

    -- delete the employee
    DELETE FROM Funcionario
    WHERE nif = @nif;
END
GO

-- SP para eliminar uma pessoa

CREATE PROCEDURE DeletePessoa @nif INT
AS
BEGIN
    -- Check if the person is a client
    IF EXISTS (SELECT 1 FROM Cliente WHERE nif = @nif)
        BEGIN
            EXEC DeleteCliente @nif;
        END
    ELSE
        BEGIN
            EXEC DeleteFuncionario @nif;
        END
END
GO

-- SP para eliminar todos os funcionários de um estabelecimento
CREATE PROCEDURE DeleteFuncionariosEstabelecimento @nif INT
AS
BEGIN
    -- Verificar se é um efetivo
    IF EXISTS (SELECT 1 FROM Efetivo WHERE nif = @nif)
        BEGIN
            -- Eliminar as entradas na tabela Tem
            DELETE FROM Tem
            WHERE nif_efetivo = @nif;

            -- Eliminar o contrato do efetivo
            DELETE FROM Contrato
            WHERE nif_efetivo = @nif;

            -- Mudar temporariamente a restrição NOT NULL para NULL para permitir a eliminação do efetivo
            ALTER TABLE Estabelecimento ALTER COLUMN nif_gerente INT NULL;

            -- Meter o gerente do estabelecimento a null
            UPDATE Estabelecimento
            SET nif_gerente = NULL
            WHERE nif_gerente = @nif;

            -- Eliminar o efetivo
            DELETE FROM Efetivo
            WHERE nif = @nif;
        END
    ELSE
        BEGIN
            -- Eliminar o estagiário
            DELETE FROM Estagiario
            WHERE nif = @nif;
        END
    
    -- Eliminar as avaliações do funcionário
    DELETE FROM Avaliacao
    WHERE nif_funcionario = @nif;

    -- Eliminar as marcações do funcionário
    DELETE FROM Marcacao
    WHERE nif_funcionario = @nif;

    -- Eliminar os numeros de telemovel do funcionário
    DELETE FROM Nums_telem_func
    WHERE nif_func = @nif;

    -- Eliminar o funcionário
    DELETE FROM Funcionario
    WHERE nif = @nif;

    -- Desativar temporariamente o trigger de eliminação de pessoa
    DISABLE TRIGGER DeletePessoaTrigger ON Pessoa;

    -- Eliminar a pessoa
    DELETE FROM Pessoa
    WHERE nif = @nif;

    -- Ativar novamente o trigger de eliminação de pessoa
    ENABLE TRIGGER DeletePessoaTrigger ON Pessoa;
END
GO


-- SP to update employee details

CREATE PROCEDURE UpdateEmployeeDetails @establishment_number INT, @schedule_id INT, @nif INT, @company_phone INT, @private_phone INT
AS
    BEGIN
        UPDATE Funcionario 
        SET num_estabelecimento = @establishment_number, id_horario = @schedule_id
        WHERE nif = @nif;
        
        UPDATE Nums_telem_func
        SET num_telem = @company_phone
        WHERE nif_func = @nif AND num_telem LIKE '234%';

        UPDATE Nums_telem_func
        SET num_telem = @private_phone
        WHERE nif_func = @nif AND num_telem NOT LIKE '234%';
    END
GO


CREATE PROCEDURE CreateEmployee @nif INT, @emp_num INT, @establishment_number INT, @schedule_id INT, @company_phone INT, @private_phone INT
AS
    BEGIN
        INSERT INTO Funcionario (nif, num_funcionario, num_estabelecimento, id_horario) VALUES (@nif, @emp_num, @establishment_number, @schedule_id);
        INSERT INTO Nums_telem_func (nif_func, num_telem) VALUES (@nif, @company_phone);
        INSERT INTO Nums_telem_func (nif_func, num_telem) VALUES (@nif, @private_phone);
    END
GO


CREATE PROC CreateTem @nif INT, @speciality VARCHAR(20)
AS
    BEGIN
        IF NOT EXISTS (SELECT * FROM Especialidade WHERE designacao = @speciality)
        BEGIN
            INSERT INTO Especialidade (designacao) VALUES (@speciality);
        END
        INSERT INTO Tem (nif_efetivo, especialidade) VALUES (@nif, @speciality);
    END
GO


-- SP para eliminar uma marcação
CREATE PROCEDURE DeleteAppointment @emp_nif INT, @client_nif INT, @date DATETIME
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        DELETE FROM Inclui
        WHERE data_marcacao = @date AND nif_funcionario = @emp_nif AND nif_cliente = @client_nif;

        DELETE FROM Marcacao
        WHERE nif_funcionario = @emp_nif AND nif_cliente = @client_nif AND data_marcacao = @date;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        RAISERROR('Ocorreu um erro ao eliminar a marcação.', 16, 1);
    END CATCH
END
GO  