# Gestão Comercial

Aplicação web local para equipes comerciais externas. Gerencia clientes, vendedores, visitas e negociações em SQLite, com painel de indicadores.

## Funcionalidades

- Dashboard com clientes e vendedores ativos, visitas, valor do pipeline, clientes por vendedor e negociações por etapa.
- Cadastro, edição, exclusão segura e associação de clientes a vendedores.
- Cadastro, edição e exclusão segura de vendedores.
- Registro de visitas, status, observações e gasto de combustível.
- Registro e atualização de negociações nas etapas **Prospecção**, **Contato**, **Proposta**, **Negociação**, **Fechada** e **Perdida**.
- Inicialização idempotente do SQLite e proteção dos relacionamentos por chaves estrangeiras.

## Tecnologias

- Python 3.10 ou superior
- Streamlit
- Pandas
- SQLite (incluído no Python)

## Instalação e execução

No terminal, entre na pasta `python` e execute:

```bash
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt
streamlit run app.py
```

No macOS/Linux, ative com `source .venv/bin/activate` e use `python3` no lugar de `py -3`.

O Streamlit exibirá o endereço local no terminal (normalmente `http://localhost:8501`).

## Banco de dados

O arquivo local `python/gestao_comercial.db` é criado ou atualizado automaticamente ao iniciar o aplicativo. Ele é ignorado pelo Git para evitar o envio de dados de operação, pessoais ou sensíveis. A atualização apenas adiciona o campo de gasto de combustível quando necessário; não exclui tabelas nem registros existentes.

Os scripts de referência ficam em `banco/` e usam `CREATE TABLE IF NOT EXISTS` e índices para consultas frequentes.

## Estrutura

```text
gestao-comercial/
├── banco/                 # esquema e consultas SQL de referência
├── docs/                  # arquitetura e modelo de dados
├── powerbi/               # espaço para modelo analítico
└── python/
    ├── app.py             # aplicação Streamlit
    └── requirements.txt   # dependências
```

## Publicação no GitHub

Antes do primeiro envio, confira os arquivos que serão versionados:

```bash
git init
git add .
git status
```

O `.gitignore` já exclui bancos SQLite, ambientes virtuais, segredos locais e arquivos temporários. Não inclua dados reais em commits.
