from src.core.config import supabase


def buscar(id_usuario):
    response = supabase.table("preferencias_usuario").select("*").eq("id_usuario", id_usuario).execute()
    if response.data:
        return response.data[0]
    return None


def salvar(id_usuario, unidade, curso):
    existing = supabase.table("preferencias_usuario").select("id_usuario").eq("id_usuario", id_usuario).execute()

    if existing.data:
        response = supabase.table("preferencias_usuario").update({
            "unidade": unidade,
            "curso": curso,
            "updated_at": "now()",
        }).eq("id_usuario", id_usuario).execute()
    else:
        response = supabase.table("preferencias_usuario").insert({
            "id_usuario": id_usuario,
            "unidade": unidade,
            "curso": curso,
        }).execute()

    return response
