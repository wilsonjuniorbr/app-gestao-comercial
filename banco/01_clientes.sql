CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    razao_social VARCHAR(150) NOT NULL,
    nome_fantasia VARCHAR(150),
    cnpj VARCHAR(18) UNIQUE,
    cidade VARCHAR(100),
    estado TEXT CHECK (estado IS NULL OR length(estado) = 2),
    telefone VARCHAR(20),
    email VARCHAR(150),
    status TEXT NOT NULL DEFAULT 'Ativo' CHECK (status IN ('Ativo', 'Inativo')),
    vendedor_id INTEGER,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_clientes_vendedor ON clientes(vendedor_id);
