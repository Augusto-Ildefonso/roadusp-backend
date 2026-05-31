import io
import threading

from src.repositories import historico_db, processamento_db
from src.services import pdf_parsing


def processar_historico_background(processamento_id: str, id_usuario: str, arquivo_bytes: bytes):
    try:
        resultado = pdf_parsing.extracao_materias(io.BytesIO(arquivo_bytes))

        aprovadas = resultado["aprovadas"]
        cursando = resultado["cursando"]
        unidade = resultado.get("unidade")
        curso = resultado.get("curso")

        processamento_db.atualizar_status(
            processamento_id,
            status="processando",
        )

        historico_db.limpar_historico(id_usuario)

        disciplinas = []
        for codigo in aprovadas:
            disciplinas.append({"codigo": codigo, "status": "aprovada"})
        for codigo in cursando:
            disciplinas.append({"codigo": codigo, "status": "cursando"})

        if disciplinas:
            historico_db.inserir_varias_disciplinas(id_usuario, disciplinas)

        processamento_db.atualizar_status(
            processamento_id,
            status="concluido",
            resultado={
                "aprovadas": aprovadas,
                "cursando": cursando,
                "unidade": unidade,
                "curso": curso,
            }
        )
    except Exception as e:
        processamento_db.atualizar_status(
            processamento_id,
            status="erro",
            erro=str(e),
        )
        raise


def iniciar_processamento(id_usuario: str, arquivo_bytes: bytes) -> str:
    processamento_id = processamento_db.criar(id_usuario)

    thread = threading.Thread(
        target=processar_historico_background,
        args=(processamento_id, id_usuario, arquivo_bytes),
        daemon=True,
    )
    thread.start()

    return processamento_id
