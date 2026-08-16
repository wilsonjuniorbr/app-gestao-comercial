"""Aplicação Streamlit para gestão comercial de equipes externas."""

from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "gestao_comercial.db"
ETAPAS_NEGOCIACAO = ["Prospecção", "Contato", "Proposta", "Negociação", "Fechada", "Perdida"]
STATUS_CLIENTE = ["Ativo", "Inativo"]
STATUS_VISITA = ["Agendada", "Realizada", "Cancelada"]


def conectar() -> sqlite3.Connection:
    """Abre conexão SQLite com integridade referencial ativada."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco() -> None:
    """Cria e atualiza o esquema sem apagar dados existentes."""
    comandos = [
        """CREATE TABLE IF NOT EXISTS vendedores (
            id INTEGER PRIMARY KEY, nome TEXT NOT NULL, telefone TEXT, email TEXT,
            regiao TEXT, ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
        )""",
        """CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY, razao_social TEXT NOT NULL, nome_fantasia TEXT,
            cnpj TEXT UNIQUE, cidade TEXT, estado TEXT CHECK (estado IS NULL OR length(estado) = 2),
            telefone TEXT, email TEXT, status TEXT NOT NULL DEFAULT 'Ativo'
            CHECK (status IN ('Ativo', 'Inativo')), vendedor_id INTEGER,
            FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE SET NULL
        )""",
        """CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY, cliente_id INTEGER NOT NULL, vendedor_id INTEGER NOT NULL,
            data_visita TEXT NOT NULL, latitude REAL, longitude REAL,
            status TEXT NOT NULL DEFAULT 'Realizada', observacao TEXT,
            custo_combustivel REAL NOT NULL DEFAULT 0 CHECK (custo_combustivel >= 0),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
            FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE RESTRICT
        )""",
        """CREATE TABLE IF NOT EXISTS negociacoes (
            id INTEGER PRIMARY KEY, cliente_id INTEGER NOT NULL, vendedor_id INTEGER NOT NULL,
            valor_estimado REAL NOT NULL DEFAULT 0 CHECK (valor_estimado >= 0),
            etapa TEXT NOT NULL DEFAULT 'Prospecção', data_criacao TEXT NOT NULL,
            data_atualizacao TEXT NOT NULL, observacao TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
            FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE RESTRICT
        )""",
        "CREATE INDEX IF NOT EXISTS idx_clientes_vendedor ON clientes(vendedor_id)",
        "CREATE INDEX IF NOT EXISTS idx_visitas_cliente ON visitas(cliente_id)",
        "CREATE INDEX IF NOT EXISTS idx_visitas_vendedor ON visitas(vendedor_id)",
        "CREATE INDEX IF NOT EXISTS idx_negociacoes_cliente ON negociacoes(cliente_id)",
        "CREATE INDEX IF NOT EXISTS idx_negociacoes_vendedor ON negociacoes(vendedor_id)",
        "CREATE INDEX IF NOT EXISTS idx_negociacoes_etapa ON negociacoes(etapa)",
    ]
    with conectar() as conn:
        for comando in comandos:
            conn.execute(comando)
        colunas = {linha[1] for linha in conn.execute("PRAGMA table_info(visitas)")}
        if "custo_combustivel" not in colunas:
            conn.execute("ALTER TABLE visitas ADD COLUMN custo_combustivel REAL NOT NULL DEFAULT 0")


def consultar(sql: str, params: tuple[Any, ...] = ()) -> pd.DataFrame:
    with conectar() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def executar(sql: str, params: tuple[Any, ...] = ()) -> None:
    with conectar() as conn:
        conn.execute(sql, params)


def opcoes(tabela: str, somente_ativos: bool = False) -> list[tuple[int, str]]:
    if tabela == "vendedores":
        filtro = " WHERE ativo = 1" if somente_ativos else ""
        sql = f"SELECT id, nome FROM vendedores{filtro} ORDER BY nome"
    else:
        sql = "SELECT id, COALESCE(NULLIF(nome_fantasia, ''), razao_social) AS nome FROM clientes ORDER BY nome"
    with conectar() as conn:
        return [(r["id"], r["nome"]) for r in conn.execute(sql).fetchall()]


def rotulo(item: tuple[int | None, str]) -> str:
    return item[1]


def pagina_dashboard() -> None:
    st.title("Painel comercial")
    m = consultar("""SELECT
        (SELECT COUNT(*) FROM clientes WHERE status='Ativo') clientes,
        (SELECT COUNT(*) FROM vendedores WHERE ativo=1) vendedores,
        (SELECT COUNT(*) FROM visitas) visitas,
        (SELECT COALESCE(SUM(valor_estimado), 0) FROM negociacoes) valor""").iloc[0]
    for coluna, titulo, valor in zip(st.columns(4), ["Clientes ativos", "Vendedores ativos", "Visitas registradas", "Total em negociações"], [int(m.clientes), int(m.vendedores), int(m.visitas), f"R$ {m.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")]):
        coluna.metric(titulo, valor)
    esquerda, direita = st.columns(2)
    with esquerda:
        st.subheader("Clientes por vendedor")
        dados = consultar("SELECT v.nome AS Vendedor, COUNT(c.id) AS Clientes FROM vendedores v LEFT JOIN clientes c ON c.vendedor_id=v.id GROUP BY v.id, v.nome ORDER BY Clientes DESC, Vendedor")
        if dados.empty:
            st.info("Cadastre vendedores e clientes para ver o indicador.")
        else:
            st.bar_chart(dados.set_index("Vendedor"))
    with direita:
        st.subheader("Negociações por etapa")
        dados = consultar("SELECT etapa AS Etapa, COUNT(*) AS Negociações FROM negociacoes GROUP BY etapa ORDER BY Negociações DESC")
        if dados.empty:
            st.info("Registre negociações para visualizar o pipeline.")
        else:
            st.bar_chart(dados.set_index("Etapa"))


def pagina_clientes() -> None:
    st.title("Clientes")
    dados = consultar("""SELECT c.id ID, c.razao_social 'Razão social', c.nome_fantasia 'Nome fantasia', c.cnpj CNPJ, c.cidade Cidade, c.estado Estado, c.telefone Telefone, c.email 'E-mail', c.status Status, COALESCE(v.nome, 'Não atribuído') Vendedor FROM clientes c LEFT JOIN vendedores v ON v.id=c.vendedor_id ORDER BY c.nome_fantasia, c.razao_social""")
    st.dataframe(dados, use_container_width=True, hide_index=True)
    vendedores = [(None, "Não atribuído")] + opcoes("vendedores")
    cadastro, edicao, exclusao = st.tabs(["Cadastrar", "Editar", "Excluir"])
    with cadastro:
        with st.form("novo_cliente", clear_on_submit=True):
            razao = st.text_input("Razão social *"); fantasia = st.text_input("Nome fantasia")
            a, b = st.columns(2); cnpj = a.text_input("CNPJ"); status = b.selectbox("Status", STATUS_CLIENTE)
            a, b = st.columns(2); cidade = a.text_input("Cidade"); estado = b.text_input("Estado (UF)", max_chars=2).upper()
            a, b = st.columns(2); telefone = a.text_input("Telefone"); email = b.text_input("E-mail")
            vendedor = st.selectbox("Vendedor responsável", vendedores, format_func=rotulo)
            if st.form_submit_button("Salvar cliente"):
                if not razao.strip(): st.error("Informe a razão social.")
                else:
                    try:
                        executar("INSERT INTO clientes (razao_social,nome_fantasia,cnpj,cidade,estado,telefone,email,status,vendedor_id) VALUES (?,?,?,?,?,?,?,?,?)", (razao.strip(), fantasia.strip() or None, cnpj.strip() or None, cidade.strip() or None, estado.strip() or None, telefone.strip() or None, email.strip() or None, status, vendedor[0]))
                        st.success("Cliente cadastrado.")
                    except sqlite3.IntegrityError: st.error("CNPJ já cadastrado ou dados inválidos.")
    if dados.empty: return
    opcoes_cliente = [(int(x.ID), f"{x['Nome fantasia'] or x['Razão social']} (#{x.ID})") for _, x in dados.iterrows()]
    with edicao:
        escolhido = st.selectbox("Cliente", opcoes_cliente, format_func=rotulo, key="ec")
        atual = consultar("SELECT * FROM clientes WHERE id=?", (escolhido[0],)).iloc[0]
        with st.form("editar_cliente"):
            razao = st.text_input("Razão social *", atual.razao_social); fantasia = st.text_input("Nome fantasia", atual.nome_fantasia or "")
            a, b = st.columns(2); cnpj = a.text_input("CNPJ", atual.cnpj or ""); status = b.selectbox("Status", STATUS_CLIENTE, index=STATUS_CLIENTE.index(atual.status))
            a, b = st.columns(2); cidade = a.text_input("Cidade", atual.cidade or ""); estado = b.text_input("Estado (UF)", atual.estado or "", max_chars=2).upper()
            a, b = st.columns(2); telefone = a.text_input("Telefone", atual.telefone or ""); email = b.text_input("E-mail", atual.email or "")
            indice = next((i for i, x in enumerate(vendedores) if x[0] == atual.vendedor_id), 0); vendedor = st.selectbox("Vendedor responsável", vendedores, index=indice, format_func=rotulo)
            if st.form_submit_button("Salvar alterações"):
                if not razao.strip(): st.error("Informe a razão social.")
                else:
                    try:
                        executar("UPDATE clientes SET razao_social=?,nome_fantasia=?,cnpj=?,cidade=?,estado=?,telefone=?,email=?,status=?,vendedor_id=? WHERE id=?", (razao.strip(),fantasia.strip() or None,cnpj.strip() or None,cidade.strip() or None,estado.strip() or None,telefone.strip() or None,email.strip() or None,status,vendedor[0],escolhido[0]))
                        st.success("Cliente atualizado.")
                    except sqlite3.IntegrityError: st.error("CNPJ já cadastrado ou dados inválidos.")
    with exclusao:
        escolhido = st.selectbox("Cliente", opcoes_cliente, format_func=rotulo, key="xc")
        ok = st.checkbox("Confirmo a exclusão definitiva deste cliente.")
        if st.button("Excluir cliente", type="primary", disabled=not ok):
            try: executar("DELETE FROM clientes WHERE id=?", (escolhido[0],)); st.success("Cliente excluído.")
            except sqlite3.IntegrityError: st.error("Cliente possui visitas ou negociações vinculadas e não pode ser excluído.")


def pagina_vendedores() -> None:
    st.title("Vendedores")
    dados = consultar("SELECT id ID,nome Nome,telefone Telefone,email 'E-mail',regiao Região,CASE ativo WHEN 1 THEN 'Ativo' ELSE 'Inativo' END Status FROM vendedores ORDER BY nome")
    st.dataframe(dados, use_container_width=True, hide_index=True)
    cadastro, edicao, exclusao = st.tabs(["Cadastrar", "Editar", "Excluir"])
    with cadastro:
        with st.form("novo_vendedor", clear_on_submit=True):
            nome = st.text_input("Nome *"); a, b = st.columns(2); telefone = a.text_input("Telefone"); email = b.text_input("E-mail"); regiao = st.text_input("Região"); ativo = st.checkbox("Vendedor ativo", value=True)
            if st.form_submit_button("Salvar vendedor"):
                if not nome.strip(): st.error("Informe o nome.")
                else: executar("INSERT INTO vendedores (nome,telefone,email,regiao,ativo) VALUES (?,?,?,?,?)", (nome.strip(),telefone.strip() or None,email.strip() or None,regiao.strip() or None,int(ativo))); st.success("Vendedor cadastrado.")
    if dados.empty: return
    opcoes_vendedor = [(int(x.ID), f"{x.Nome} (#{x.ID})") for _, x in dados.iterrows()]
    with edicao:
        escolhido = st.selectbox("Vendedor", opcoes_vendedor, format_func=rotulo, key="ev")
        atual = consultar("SELECT * FROM vendedores WHERE id=?", (escolhido[0],)).iloc[0]
        with st.form("editar_vendedor"):
            nome = st.text_input("Nome *", atual.nome); a, b = st.columns(2); telefone = a.text_input("Telefone", atual.telefone or ""); email = b.text_input("E-mail", atual.email or ""); regiao = st.text_input("Região", atual.regiao or ""); ativo = st.checkbox("Vendedor ativo", value=bool(atual.ativo))
            if st.form_submit_button("Salvar alterações"):
                if not nome.strip(): st.error("Informe o nome.")
                else: executar("UPDATE vendedores SET nome=?,telefone=?,email=?,regiao=?,ativo=? WHERE id=?", (nome.strip(),telefone.strip() or None,email.strip() or None,regiao.strip() or None,int(ativo),escolhido[0])); st.success("Vendedor atualizado.")
    with exclusao:
        escolhido = st.selectbox("Vendedor", opcoes_vendedor, format_func=rotulo, key="xv"); ok = st.checkbox("Confirmo a exclusão definitiva deste vendedor.")
        if st.button("Excluir vendedor", type="primary", disabled=not ok):
            try: executar("DELETE FROM vendedores WHERE id=?", (escolhido[0],)); st.success("Vendedor excluído.")
            except sqlite3.IntegrityError: st.error("Vendedor possui visitas ou negociações vinculadas e não pode ser excluído.")


def pagina_visitas() -> None:
    st.title("Visitas")
    dados = consultar("""SELECT vis.id ID,vis.data_visita Data,COALESCE(c.nome_fantasia,c.razao_social) Cliente,v.nome Vendedor,vis.status Status,vis.custo_combustivel 'Gasto (R$)',vis.observacao Observações FROM visitas vis JOIN clientes c ON c.id=vis.cliente_id JOIN vendedores v ON v.id=vis.vendedor_id ORDER BY vis.data_visita DESC,vis.id DESC""")
    st.dataframe(dados, use_container_width=True, hide_index=True)
    clientes, vendedores = opcoes("clientes"), opcoes("vendedores", True)
    if not clientes or not vendedores: st.warning("Cadastre ao menos um cliente e um vendedor ativo antes de registrar visitas."); return
    with st.form("nova_visita", clear_on_submit=True):
        a,b = st.columns(2); data_visita = a.date_input("Data", date.today()); status = b.selectbox("Status", STATUS_VISITA, index=1)
        cliente = st.selectbox("Cliente", clientes, format_func=rotulo); vendedor = st.selectbox("Vendedor", vendedores, format_func=rotulo)
        gasto = st.number_input("Valor de combustível/gasto (R$)", min_value=0.0, step=10.0, format="%.2f"); observacao = st.text_area("Observações")
        if st.form_submit_button("Registrar visita"):
            executar("INSERT INTO visitas (cliente_id,vendedor_id,data_visita,status,observacao,custo_combustivel) VALUES (?,?,?,?,?,?)", (cliente[0],vendedor[0],data_visita.isoformat(),status,observacao.strip() or None,gasto)); st.success("Visita registrada.")


def pagina_negociacoes() -> None:
    st.title("Negociações")
    dados = consultar("""SELECT n.id ID,COALESCE(c.nome_fantasia,c.razao_social) Cliente,v.nome Vendedor,n.etapa Etapa,n.valor_estimado 'Valor (R$)',n.data_criacao 'Data de criação',n.data_atualizacao Atualização,n.observacao Observações FROM negociacoes n JOIN clientes c ON c.id=n.cliente_id JOIN vendedores v ON v.id=n.vendedor_id ORDER BY n.data_atualizacao DESC,n.id DESC""")
    st.dataframe(dados, use_container_width=True, hide_index=True)
    clientes, vendedores = opcoes("clientes"), opcoes("vendedores", True)
    if not clientes or not vendedores: st.warning("Cadastre ao menos um cliente e um vendedor ativo antes de registrar negociações."); return
    cadastro, edicao = st.tabs(["Registrar", "Atualizar etapa"])
    with cadastro:
        with st.form("nova_negociacao", clear_on_submit=True):
            cliente = st.selectbox("Cliente", clientes, format_func=rotulo); vendedor = st.selectbox("Vendedor", vendedores, format_func=rotulo)
            a,b = st.columns(2); etapa = a.selectbox("Etapa", ETAPAS_NEGOCIACAO); valor = b.number_input("Valor estimado (R$)", min_value=0.0, step=100.0, format="%.2f")
            data_registro = st.date_input("Data", date.today()); observacao = st.text_area("Observações")
            if st.form_submit_button("Registrar negociação"):
                executar("INSERT INTO negociacoes (cliente_id,vendedor_id,valor_estimado,etapa,data_criacao,data_atualizacao,observacao) VALUES (?,?,?,?,?,?,?)", (cliente[0],vendedor[0],valor,etapa,data_registro.isoformat(),data_registro.isoformat(),observacao.strip() or None)); st.success("Negociação registrada.")
    with edicao:
        if dados.empty: st.info("Não há negociações para atualizar."); return
        escolhido = st.selectbox("Negociação", [(int(x.ID),f"#{x.ID} — {x.Cliente} — {x.Etapa}") for _,x in dados.iterrows()], format_func=rotulo)
        atual = consultar("SELECT * FROM negociacoes WHERE id=?", (escolhido[0],)).iloc[0]
        with st.form("editar_negociacao"):
            etapa = st.selectbox("Etapa", ETAPAS_NEGOCIACAO, index=ETAPAS_NEGOCIACAO.index(atual.etapa) if atual.etapa in ETAPAS_NEGOCIACAO else 0)
            valor = st.number_input("Valor estimado (R$)", min_value=0.0, value=float(atual.valor_estimado), step=100.0, format="%.2f"); data_atualizacao = st.date_input("Data da atualização", date.fromisoformat(atual.data_atualizacao)); observacao = st.text_area("Observações", atual.observacao or "")
            if st.form_submit_button("Salvar atualização"):
                executar("UPDATE negociacoes SET etapa=?,valor_estimado=?,data_atualizacao=?,observacao=? WHERE id=?", (etapa,valor,data_atualizacao.isoformat(),observacao.strip() or None,escolhido[0])); st.success("Negociação atualizada.")


def main() -> None:
    st.set_page_config(page_title="Gestão Comercial", page_icon="📈", layout="wide")
    inicializar_banco()
    with st.sidebar:
        st.title("Gestão Comercial")
        pagina = st.radio("Menu", ["Dashboard", "Clientes", "Vendedores", "Visitas", "Negociações"])
        st.caption("Dados armazenados localmente em SQLite.")
    {"Dashboard": pagina_dashboard, "Clientes": pagina_clientes, "Vendedores": pagina_vendedores, "Visitas": pagina_visitas, "Negociações": pagina_negociacoes}[pagina]()


if __name__ == "__main__":
    main()
