-- Remover os indices

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_EstabelecimentoLocalidade')
DROP INDEX Ix_EstabelecimentoLocalidade ON Estabelecimento;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_PessoaNome')
DROP INDEX Ix_PessoaNome ON Pessoa;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_HorarioDiaFolga')
DROP INDEX Ix_HorarioDiaFolga ON Horario;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_TipoServicoDesignacao')
DROP INDEX Ix_TipoServicoDesignacao ON TipoServico;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_FuncionarioNumero')
DROP INDEX Ix_FuncionarioNumero ON Funcionario;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_ClienteNumeroConta')
DROP INDEX Ix_ClienteNumeroConta ON Cliente;
GO

-- Índice para acelerar a pesquisa de estabelecimentos por localidade
CREATE INDEX Ix_EstabelecimentoLocalidade
ON Estabelecimento (localidade);
GO

-- Índice para acelerar a pesquisa de pessoas por nome
CREATE INDEX Ix_PessoaNome
ON Pessoa (Pnome, Unome);
GO

-- Índice para acelerar a pesquisa de horários por dia de folga
CREATE INDEX Ix_HorarioDiaFolga
ON Horario (dia_folga);
GO

-- Índice para acelerar a pesquisa de tipos de serviço por designação
CREATE INDEX Ix_TipoServicoDesignacao
ON Tipo_servico (designacao);
GO

-- Índice para acelerar a pesquisa de funcionário pelo seu número
CREATE INDEX Ix_FuncionarioNumero
ON Funcionario (num_funcionario);
GO

-- Índice para acelerar a pesquisa de cliente pelo seu número de conta
CREATE INDEX Ix_ClienteNumeroConta
ON Cliente (num_conta);
GO