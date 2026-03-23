from src.core.config import supabase

def criar(email, hash):
    response = supabase.table("usuarios").insert({
        "email": email,
        "senha": hash
    }).execute()

    return response

def busca_user(email):
    response = supabase.table("usuarios").select("email", "senha", "id").eq("email", email).execute().data[0]
    
    return response