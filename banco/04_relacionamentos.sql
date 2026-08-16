-- Clientes, visitas e negociações

CREATE TABLE visitas (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    vendedor_id INTEGER NOT NULL,
    data_visita DATE NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    status VARCHAR(30) DEFAULT 'Realizada',
    observacao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id)
);

CREATE TABLE negociacoes (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    vendedor_id INTEGER NOT NULL,
    valor_estimado DECIMAL(15, 2) DEFAULT 0,
    etapa VARCHAR(30) DEFAULT 'Prospecção',
    data_criacao DATE NOT NULL,
    data_atualizacao DATE NOT NULL,
    observacao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id)
);
