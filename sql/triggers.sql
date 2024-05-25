-- Remover os triggers

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

-- Trigger para atribuir um novo horário a um funcionário quando o horário é eliminado

CREATE TRIGGER DeleteHorarioTrigger ON Horario
INSTEAD OF DELETE
AS
BEGIN
    DECLARE @deletedHorarioId INT;
    DECLARE @novoHorarioId INT;

    -- Obter o id do horário a ser eliminado
    SELECT @deletedHorarioId = id
    FROM deleted;

    -- Obter o id de um novo horário disponível (diferente do horário a ser eliminado)
    SELECT TOP 1 @novoHorarioId = id
    FROM Horario
    WHERE id <> @deletedHorarioId
    ORDER BY NEWID(); -- Para obter um horário aleatório e não o primeiro

    IF @novoHorarioId IS NOT NULL -- Se existir um novo horário
        BEGIN
            -- Atualizar o funcionário com o novo horário
            UPDATE Funcionario
            SET id_horario = @novoHorarioId
            WHERE id_horario = @deletedHorarioId;

            -- Eliminar o horário
            DELETE FROM Horario
            WHERE id = @deletedHorarioId;
        END
    ELSE -- Se não existir um novo horário
        BEGIN
            RAISERROR('Não é possível eliminar o horário pois não existe outro horário disponível.', 16, 1);
        END
END
GO

-- Trigger para dar delete a Pessoa

CREATE TRIGGER DeletePessoaTrigger ON Pessoa
INSTEAD OF DELETE
AS
BEGIN
    DECLARE @nif INT
    SELECT @nif = nif FROM deleted
    EXEC DeletePessoa @nif;
    DELETE FROM Pessoa
    WHERE nif = @nif;
END
GO


-- Trigger para eliminar um estabelecimento

CREATE TRIGGER DeleteEstabelecimentoTrigger ON Estabelecimento
INSTEAD OF DELETE
AS
BEGIN
    -- Obter uma tabela com os nifs dos trabalhadores do estabelecimento
    DECLARE @nifs TABLE (nif INT);
    INSERT INTO @nifs
    SELECT nif
    FROM Funcionario
    WHERE num_estabelecimento = (SELECT id FROM deleted);

    -- Cursor para percorrer os nifs
    DECLARE @nif INT;
    DECLARE nif_cursor CURSOR FOR
    SELECT nif
    FROM @nifs;

    OPEN nif_cursor;

    FETCH NEXT FROM nif_cursor INTO @nif;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Eliminar os trabalhadores
        EXEC DeleteFuncionariosEstabelecimento @nif;

        FETCH NEXT FROM nif_cursor INTO @nif;
    END
    CLOSE nif_cursor;
    DEALLOCATE nif_cursor;

    -- Eliminar o estabelecimento
    DELETE FROM Estabelecimento
    WHERE id = (SELECT id FROM deleted);

    -- Alterar novamente a restrição de chave estrangeira
    ALTER TABLE Estabelecimento ALTER COLUMN nif_gerente INT NOT NULL;
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

    -- Obter os valores a inserir n db
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

    -- Verificar se o nif_gerente existe na tabela Efetivo
    IF EXISTS (SELECT 1 FROM Efetivo WHERE nif = @nif_gerente)
    BEGIN
        -- Verificar se o gerente não está associado a outro estabelecimento
        IF NOT EXISTS (SELECT 1 FROM Estabelecimento WHERE nif_gerente = @nif_gerente)
            BEGIN
                -- Inserir o novo estabelecimento
                INSERT INTO Estabelecimento (id, especificacao, cod_postal, localidade, rua, numero, nif_gerente, data_inicio_gerente)
                VALUES (@id, @especificacao, @cod_postal, @localidade, @rua, @numero, @nif_gerente, @data_inicio_gerente);

                -- Transferir o efetivo para o estabelecimento criado
                UPDATE Funcionario
                SET num_estabelecimento = @id
                WHERE nif = @nif_gerente;
            END
        ELSE
            BEGIN
                RAISERROR('O NIF que foi inserido corresponde a um gerente de outro estabelecimento', 16, 1);
            END
    END
    ELSE
        BEGIN
            RAISERROR('O NIF que foi inserido não corresponde a nenhum efetivo', 16, 1);
        END
END