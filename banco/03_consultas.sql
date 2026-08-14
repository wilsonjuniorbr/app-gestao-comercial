-- Listar todos os clientes
SELECT * FROM clientes;

-- Listar apenas clientes ativos
SELECT * FROM clientes
WHERE status = 'Ativo';

-- Listar clientes da cidade de Lucas do Rio Verde
SELECT * FROM clientes
WHERE cidade = 'Lucas do Rio Verde';

-- Listar apenas razão social e telefone
SELECT razao_social, telefone
FROM clientes;
