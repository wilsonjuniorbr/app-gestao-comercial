# Modelo de dados

## Tabelas

- **vendedores:** nome, contatos, região e situação ativa da equipe comercial.
- **clientes:** razão social, nome fantasia, CNPJ, localização, contatos, status e vendedor responsável.
- **visitas:** cliente, vendedor, data, status, observações, coordenadas opcionais e gasto de combustível.
- **negociacoes:** cliente, vendedor, valor estimado, etapa, datas e observações do pipeline.

## Relacionamentos

- Um vendedor possui vários clientes.
- Um cliente pode receber várias visitas.
- Um vendedor pode realizar várias visitas.
- Um cliente pode possuir várias negociações.
- Um vendedor pode conduzir várias negociações.

## Integridade

- Clientes podem ficar sem vendedor; ao excluir um vendedor sem histórico, a associação do cliente é removida.
- Visitas e negociações exigem cliente e vendedor válidos e impedem a exclusão acidental de registros relacionados.
- O aplicativo ativa `PRAGMA foreign_keys = ON` a cada conexão SQLite.
