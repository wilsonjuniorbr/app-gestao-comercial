# Arquitetura do projeto

## Objetivo

Centralizar informações de clientes, vendedores, visitas e negociações de uma equipe comercial externa.

## Camadas

- **Banco:** SQL/SQLite para persistência.
- **Python:** camada de aplicação e automações.
- **Power BI:** indicadores e análises gerenciais.
- **GitHub:** versionamento e documentação.

## Fluxo

1. Vendedor é cadastrado.
2. Cliente é associado a um vendedor.
3. Vendedor registra visitas.
4. Visitas podem registrar coordenadas GPS.
5. Negociações são acompanhadas por etapa e valor estimado.
6. Dados alimentam indicadores comerciais.
