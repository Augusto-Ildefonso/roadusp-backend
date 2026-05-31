from src.core.config import supabase


def inserir_disciplina(id_usuario: str, codigo: str, status: str):
    response = supabase.table("historico_disciplinas").insert({
        "id_usuario": id_usuario,
        "codigo_disciplina": codigo,
        "status": status,
    }).execute()

    return response


def inserir_varias_disciplinas(id_usuario: str, disciplinas: list[dict]):
    registros = [
        {
            "id_usuario": id_usuario,
            "codigo_disciplina": d["codigo"],
            "status": d["status"],
        }
        for d in disciplinas
    ]

    response = supabase.table("historico_disciplinas").insert(registros).execute()

    return response


def limpar_historico(id_usuario: str):
    response = supabase.table("historico_disciplinas").delete().eq(
        "id_usuario", id_usuario
    ).execute()

    return response


def buscar_historico(id_usuario: str):
    response = supabase.table("historico_disciplinas").select(
        "codigo_disciplina", "status", "created_at"
    ).eq("id_usuario", id_usuario).execute()

    return response.data if response.data else []
