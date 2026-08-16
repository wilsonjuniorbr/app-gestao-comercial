CREATE TABLE vendedores (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    regiao VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE
);
