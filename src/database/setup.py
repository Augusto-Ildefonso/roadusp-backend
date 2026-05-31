import os
import sys
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent


def ler_migracao(nome: str) -> str:
    caminho = MIGRATIONS_DIR / nome
    if not caminho.exists():
        print(f"  ERRO: Arquivo {caminho} não encontrado.")
        return None
    return caminho.read_text()


def verificar_tabela(supabase, tabela: str) -> bool:
    try:
        supabase.table(tabela).select("*").limit(1).execute()
        return True
    except Exception:
        return False


def check():
    sys.path.insert(0, str(MIGRATIONS_DIR.parent.parent))
    from src.core.config import supabase

    print("Verificando tabelas no Supabase...")
    print()

    tabelas = ["usuarios", "historico_disciplinas", "processamentos_historico", "preferencias_usuario"]
    for tabela in tabelas:
        existe = verificar_tabela(supabase, tabela)
        status = "OK" if existe else "NÃO CRIADA"
        print(f"  {tabela}: {status}")

    print()
    if all(verificar_tabela(supabase, t) for t in tabelas):
        print("Banco de dados pronto!")
        return True
    else:
        print("Execute as migrações abaixo para completar a configuração.")
        return False


def sql():
    migracoes = [
        ("000_create_usuarios.sql", "Tabela de usuários"),
        ("001_create_historico_disciplinas.sql", "Tabela de histórico"),
        ("002_create_processamentos_historico.sql", "Tabela de processamentos"),
        ("003_create_preferencias_usuario.sql", "Tabela de preferências"),
    ]

    for nome, desc in migracoes:
        sql_content = ler_migracao(nome)
        if sql_content is None:
            continue
        print("=" * 60)
        print(f"  {nome} — {desc}")
        print("=" * 60)
        print(sql_content)
        print()
        print(f"  Link: https://supabase.com/dashboard/project/PROJECT_REF/sql/new")
        print()


def run(database_url: str = None):
    if not database_url:
        print("Para executar as migrações diretamente, informe DATABASE_URL.")
        print()
        sql()
        return

    try:
        import psycopg2
    except ImportError:
        print("psycopg2 não instalado. Execute: pip install psycopg2-binary")
        return

    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cur = conn.cursor()

    migracoes = [
        "000_create_usuarios.sql",
        "001_create_historico_disciplinas.sql",
        "002_create_processamentos_historico.sql",
        "003_create_preferencias_usuario.sql",
    ]

    for nome in migracoes:
        sql_content = ler_migracao(nome)
        if sql_content is None:
            continue
        print(f"Executando {nome}...")
        cur.execute(sql_content)
        print(f"  OK")

    cur.close()
    conn.close()
    print()
    print("Migrações executadas com sucesso!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Setup do banco de dados RoadUSP")
    parser.add_argument(
        "comando",
        nargs="?",
        default="check",
        choices=["check", "sql", "run"],
        help="Comando a executar (default: check)",
    )
    parser.add_argument(
        "--database-url",
        help="URL de conexão ao PostgreSQL (ex: postgresql://postgres:senha@db.xxxxx.supabase.co:5432/postgres)",
    )

    args = parser.parse_args()

    if args.comando == "check":
        ok = check()
        sys.exit(0 if ok else 1)
    elif args.comando == "sql":
        sql()
    elif args.comando == "run":
        run(args.database_url)
