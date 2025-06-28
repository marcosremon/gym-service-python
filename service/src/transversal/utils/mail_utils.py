import re
import json
import smtplib
from email.message import EmailMessage
from pathlib import Path


class MailUtils:
    _config = None

    @staticmethod
    def _load_config() -> dict:
        if MailUtils._config is None:
            config_path = Path(__file__).resolve().parents[2] / "service/configuration" / "appsettings.json"
            try:
                with open(config_path, 'r') as f:
                    MailUtils._config = json.load(f)

                if "email_settings" not in MailUtils._config:
                    raise KeyError("Falta la sección 'email_settings' en appsettings.json")

            except FileNotFoundError:
                raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
            except json.JSONDecodeError:
                raise ValueError("El archivo appsettings.json tiene un formato inválido")

        return MailUtils._config["email_settings"]

    @staticmethod
    def is_email_valid(email: str) -> bool:
        return re.fullmatch(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

    @staticmethod
    def _send_email(recipient_name: str, recipient_email: str, subject: str, body: str) -> bool:
        if not MailUtils.is_email_valid(recipient_email):
            raise ValueError(f"Dirección de correo no válida: {recipient_email}")

        email_settings = MailUtils._load_config()

        msg = EmailMessage()
        msg['From'] = f"{email_settings['sender_name']} <{email_settings['sender_email']}>"
        msg['To'] = f"{recipient_name} <{recipient_email}>"
        msg['Subject'] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP(email_settings['smtp_host'], email_settings['smtp_port'], timeout=10) as server:
                server.starttls()
                server.login(email_settings['sender_email'], email_settings['app_password'])
                server.send_message(msg)

            print(f"Correo enviado correctamente a {recipient_email}")
            return True

        except smtplib.SMTPException as e:
            raise Exception(f"Error SMTP: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al enviar correo: {str(e)}")

    @staticmethod
    def send_email_after_created_google_account_by_google(recipient_name: str, recipient_email: str) -> bool:
        body = (
            f"Hello {recipient_name},\n\n"
            "Thank you for creating an account with Google login.\n\n"
            "For your security, please change your temporary password the first time you log in.\n\n"
            "Best regards,\n"
            f"{MailUtils._load_config()['sender_name']}"
        )
        return MailUtils._send_email(recipient_name, recipient_email, "Account Information - Your New Account", body)

    @staticmethod
    def send_password_email(recipient_name: str, recipient_email: str, new_password: str) -> bool:
        body = (
            f"Hola {recipient_name},\n\n"
            f"Tu nueva contraseña es: {new_password}\n\n"
            "Por seguridad, te recomendamos cambiar esta contraseña después de iniciar sesión.\n\n"
            "Atentamente,\n"
            f"{MailUtils._load_config()['sender_name']}"
        )
        return MailUtils._send_email(recipient_name, recipient_email, "Tu nueva contraseña", body)
