import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "gestao_comercial.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    """Cria as tabelas da aplicação usando os scripts SQL do projeto."""
    banco = Path(__file__).resolve().parents[1] / "banco"

    with conectar() as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # A ordem respeita as dependências entre tabelas.
        scripts = [
            "02_vendedores.sql",
            "01_clientes.sql",
            "04_relacionamentos.sql",
        ]

        for arquivo in scripts:
            sql = (banco / arquivo).read_text(encoding="utf-8")
            for bloco in (item.strip() for item in sql.split(";") if item.strip()):
                conn.execute(bloco)

        conn.commit()


def listar_clientes():
    with conectar() as conn:
        return conn.execute(
            """SELECT c.id, c.nome_fantasia, c.cidade, c.estado,
                      v.nome AS vendedor, c.status
               FROM clientes c
               LEFT JOIN vendedores v ON v.id = c.vendedor_id
               ORDER BY c.nome_fantasia"""
        ).fetchall()


if __name__ == "__main__":
    inicializar_banco()
    print("Banco inicializado em:", DB_PATH)
    print("Clientes cadastrados:", len(listar_clientes()))
