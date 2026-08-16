# Aplicativo de Gestão Comercial para Equipes Externas

Projeto de portfólio desenvolvido para aplicar conceitos de **Engenharia de Software, Banco de Dados, Python, análise de dados e gestão comercial**.

## Objetivo

Apoiar equipes comerciais externas no acompanhamento de clientes, vendedores, visitas, geolocalização, negociações e indicadores.

## Funcionalidades

- Cadastro de clientes e vendedores
- Associação entre cliente e vendedor
- Registro de visitas
- Registro de coordenadas GPS
- Pipeline de negociações
- Consultas SQL
- Estrutura preparada para Power BI
- Base Python para automação e evolução da aplicação

## Tecnologias

- **Python**
- **SQL / SQLite**
- **Power BI**
- **Git e GitHub**

## Estrutura

```text
aplicativo-gestao-comercial/
├── banco/
│   ├── 01_clientes.sql
│   ├── 02_vendedores.sql
│   ├── 03_consultas.sql
│   └── 04_relacionamentos.sql
├── docs/
│   ├── arquitetura.md
│   └── modelo-dados.md
├── python/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── powerbi/
│   └── README.md
└── README.md
```

## Arquitetura

```text
Vendedores
    │
    ├── Clientes
    │      ├── Visitas
    │      └── Negociações
    │
    └── Negociações

             ↓
        Banco SQL/SQLite
             ↓
          Python
             ↓
          Power BI
```

## Status

**Versão 1 — estruturação do projeto**

A base de dados, arquitetura, módulo Python e documentação inicial estão organizados. Próximas evoluções: autenticação, interface web, permissões, integração com dados reais e publicação do dashboard.

## Observação

O projeto utiliza dados fictícios e anonimizados, criados exclusivamente para estudo e portfólio.
