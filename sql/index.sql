-- Remover os indices

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_EstabelecimentoLocalidade')
DROP INDEX Ix_EstabelecimentoLocalidade ON Estabelecimento;
GO

IF EXISTS (SELECT * FROM sys.indexes WHERE name = 'Ix_PessoaNome')
DROP INDEX Ix_PessoaNome ON Pessoa;
GO


-- Índice para acelerar a pesquisa de estabelecimentos por localidade
CREATE INDEX Ix_EstabelecimentoLocalidade
ON Estabelecimento (localidade);
GO

-- Índice para acelerar a pesquisa de pessoas por nome
CREATE INDEX Ix_PessoaNome
ON Pessoa (Pnome, Unome);