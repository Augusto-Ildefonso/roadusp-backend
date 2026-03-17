from src.core.config import supabase

def get_id_unidade(nome_unidade):
    return (supabase.table("unidades").select("id").eq("nome", nome_unidade).maybe_single().execute().data)["id"]

def get_cursos(id_unidade):
    data = supabase.table("cursos").select("nome").eq("id_unidade", id_unidade).execute().data
    return [curso["nome"] for curso in data] if data else None

def get_id_curso(id_unidade, nome_curso):
    return (supabase.table("cursos").select("id").eq("id_unidade", id_unidade).eq("nome", nome_curso).maybe_single().execute().data)["id"]

def get_disciplinas(id_curso):
    return (supabase.table("disciplinas").select("*").eq("id_curso", id_curso).execute().data)

def get_id_requisitos(ids_disciplinas):
    return supabase.table("requisitos").select("id_disciplina, id_requisito").in_("id_disciplina", ids_disciplinas).execute().data

def get_requisitos(ids_requisitos):
    return supabase.table("disciplinas").select("id, codigo").in_("id", ids_requisitos).execute().data