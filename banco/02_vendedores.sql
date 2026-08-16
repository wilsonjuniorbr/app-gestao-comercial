CREATE TABLE IF NOT EXISTS vendedores (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    regiao VARCHAR(100),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);
