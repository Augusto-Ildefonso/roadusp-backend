import smtplib
import socket
from email.mime.text import MIMEText
from src.core.config import settings

SMTP_TIMEOUT = 10

def enviar_email_redefinicao(email_destino: str, token: str):
    link = f"{settings.FRONTEND_URL}/redefinir-senha?token={token}"

    corpo = f"""
    <p>Clique no link abaixo para redefinir sua senha:</p>
    <a href="{link}">{link}</a>
    <p>O link expira em {settings.RESET_TOKEN_EXPIRES} minutos.</p>
    """

    msg = MIMEText(corpo, "html")
    msg["Subject"] = "Redefinição de senha - RoadUSP"
    msg["From"] = settings.EMAIL_REMETENTE
    msg["To"] = email_destino

    try:
        with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT), timeout=SMTP_TIMEOUT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, smtplib.SMTPException) as e:
        raise RuntimeError(f"Falha ao enviar email: {e}") from e
