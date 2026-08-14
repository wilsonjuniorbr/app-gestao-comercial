-- Clientes e seus respectivos vendedores

SELECT
    c.razao_social,
    v.nome AS vendedor
FROM clientes c
JOIN vendedores v
    ON c.vendedor_id = v.id;
