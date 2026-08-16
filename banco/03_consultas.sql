-- Clientes ativos
SELECT *
FROM clientes
WHERE status = 'Ativo';

-- Clientes por cidade
SELECT *
FROM clientes
WHERE cidade = 'Lucas do Rio Verde';

-- Clientes e respectivos vendedores
SELECT
    c.id,
    c.razao_social,
    c.nome_fantasia,
    c.cidade,
    c.estado,
    v.nome AS vendedor
FROM clientes c
LEFT JOIN vendedores v ON c.vendedor_id = v.id
ORDER BY c.razao_social;

-- Quantidade de clientes por vendedor
SELECT
    v.nome AS vendedor,
    COUNT(c.id) AS total_clientes
FROM vendedores v
LEFT JOIN clientes c ON c.vendedor_id = v.id
GROUP BY v.id, v.nome
ORDER BY total_clientes DESC;

-- Visitas por vendedor
SELECT
    v.nome AS vendedor,
    COUNT(vis.id) AS total_visitas
FROM vendedores v
LEFT JOIN visitas vis ON vis.vendedor_id = v.id
GROUP BY v.id, v.nome
ORDER BY total_visitas DESC;

-- Negociações em andamento
SELECT
    n.id,
    c.nome_fantasia AS cliente,
    v.nome AS vendedor,
    n.valor_estimado,
    n.etapa,
    n.data_atualizacao
FROM negociacoes n
JOIN clientes c ON c.id = n.cliente_id
JOIN vendedores v ON v.id = n.vendedor_id
WHERE n.etapa NOT IN ('Ganha', 'Perdida')
ORDER BY n.data_atualizacao DESC;
