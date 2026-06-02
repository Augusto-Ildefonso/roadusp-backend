import smtplib
import socket
import sys
from email.mime.text import MIMEText
from src.core.config import settings

SMTP_TIMEOUT = 10

def log(msg: str):
    sys.stderr.write(f"[EMAIL] {msg}\n")
    sys.stderr.flush()

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

    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASS:
        log(f"SMTP não configurado. Link que seria enviado: {link}")
        return

    try:
        log(f"Conectando a {settings.SMTP_HOST}:{settings.SMTP_PORT}...")
        with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT), timeout=SMTP_TIMEOUT) as server:
            server.starttls()
            log("Autenticando...")
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            log(f"Enviando para {email_destino}...")
            server.send_message(msg)
            log("Enviado com sucesso!")
    except smtplib.SMTPAuthenticationError:
        log("ERRO: Autenticação falhou. Verifique SMTP_USER e SMTP_PASS.")
    except socket.timeout:
        log(f"ERRO: Timeout ao conectar em {settings.SMTP_HOST}:{settings.SMTP_PORT}")
    except (socket.gaierror, ConnectionRefusedError) as e:
        log(f"ERRO: Não foi possível conectar ao servidor SMTP: {e}")
    except smtplib.SMTPException as e:
        log(f"ERRO SMTP: {e}")
