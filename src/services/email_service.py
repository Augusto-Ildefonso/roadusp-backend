import sys
import resend
from src.core.config import settings


def log(msg: str):
    sys.stderr.write(f"[EMAIL] {msg}\n")
    sys.stderr.flush()


def enviar_email_redefinicao(email_destino: str, token: str):
    if not settings.RESEND_API_KEY:
        log("RESEND_API_KEY não configurada")
        return

    resend.api_key = settings.RESEND_API_KEY

    link = f"{settings.FRONTEND_URL}/redefinir-senha?token={token}"

    corpo = f"""
    <p>Clique no link abaixo para redefinir sua senha:</p>
    <a href="{link}">{link}</a>
    <p>O link expira em {settings.RESET_TOKEN_EXPIRES} minutos.</p>
    """

    try:
        response = resend.Emails.send({
            "from": settings.EMAIL_REMETENTE,
            "to": [email_destino],
            "subject": "Redefinição de senha - RoadUSP",
            "html": corpo,
        })
        log(f"Enviado com sucesso para {email_destino} — id: {response.get('id')}")
    except Exception as e:
        log(f"ERRO: {e}")
