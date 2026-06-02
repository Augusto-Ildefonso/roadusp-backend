import os
import smtplib
from email.mime.text import MIMEText

def enviar_email_redefinicao(email_destino: str, token: str):
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    link = f"{frontend_url}/redefinir-senha?token={token}"

    corpo = f"""
    <p>Clique no link abaixo para redefinir sua senha:</p>
    <a href="{link}">{link}</a>
    <p>O link expira em 15 minutos.</p>
    """

    msg = MIMEText(corpo, "html")
    msg["Subject"] = "Redefinição de senha - RoadUSP"
    msg["From"] = os.getenv("EMAIL_REMETENTE")
    msg["To"] = email_destino

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)
