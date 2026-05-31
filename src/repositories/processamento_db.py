from uuid import uuid4
from datetime import datetime, timezone

from src.core.config import supabase


def criar(id_usuario: str) -> str:
    processamento_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    supabase.table("processamentos_historico").insert({
        "id": processamento_id,
        "id_usuario": id_usuario,
        "status": "processando",
        "created_at": now,
        "updated_at": now,
    }).execute()

    return processamento_id


def atualizar_status(processamento_id: str, status: str, resultado: dict = None, erro: str = None):
    dados = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    if resultado is not None:
        dados["resultado"] = resultado
    if erro is not None:
        dados["erro"] = erro

    supabase.table("processamentos_historico").update(dados).eq("id", processamento_id).execute()


def buscar(processamento_id: str) -> dict | None:
    response = supabase.table("processamentos_historico").select("*").eq("id", processamento_id).execute()
    data = response.data
    if data:
        return data[0]
    return None
