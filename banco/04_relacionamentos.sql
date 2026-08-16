-- Clientes, visitas e negociações

CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    vendedor_id INTEGER NOT NULL,
    data_visita DATE NOT NULL,
    latitude REAL,
    longitude REAL,
    status TEXT NOT NULL DEFAULT 'Realizada',
    observacao TEXT,
    custo_combustivel REAL NOT NULL DEFAULT 0 CHECK (custo_combustivel >= 0),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS negociacoes (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    vendedor_id INTEGER NOT NULL,
    valor_estimado REAL NOT NULL DEFAULT 0 CHECK (valor_estimado >= 0),
    etapa TEXT NOT NULL DEFAULT 'Prospecção' CHECK (etapa IN ('Prospecção', 'Contato', 'Proposta', 'Negociação', 'Fechada', 'Perdida')),
    data_criacao TEXT NOT NULL,
    data_atualizacao TEXT NOT NULL,
    observacao TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_visitas_cliente ON visitas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_visitas_vendedor ON visitas(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_negociacoes_cliente ON negociacoes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_negociacoes_vendedor ON negociacoes(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_negociacoes_etapa ON negociacoes(etapa);
