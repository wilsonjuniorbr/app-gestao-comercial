CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    razao_social VARCHAR(150) NOT NULL,
    nome_fantasia VARCHAR(150),
    cnpj VARCHAR(18) UNIQUE,
    cidade VARCHAR(100),
    estado CHAR(2),
    telefone VARCHAR(20),
    email VARCHAR(150),
    status VARCHAR(20) DEFAULT 'Ativo',
    vendedor_id INTEGER,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id)
);
