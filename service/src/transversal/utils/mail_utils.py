import re
import smtplib
from email.message import EmailMessage
import json

class MailUtils:
    _config = None

    @staticmethod
    def _load_config() -> dict:
        if MailUtils._config is None:
            try:
                with open('config.json', 'r') as f:
                    MailUtils._config = json.load(f)
            except FileNotFoundError:
                raise Exception("Config file not found")
            except json.JSONDecodeError:
                raise Exception("Invalid config file format")
        return MailUtils._config

    @staticmethod
    def send_email_after_created_google_account_by_google(recipient_name: str, recipient_email: str) -> bool:
        try:
            if not MailUtils.is_email_valid(recipient_email):
                raise ValueError(f"Invalid email address: {recipient_email}")

            config = MailUtils._load_config()
            email_settings = config.get("email_settings")

            if not email_settings:
                raise Exception("Email settings not found in config")

            msg = EmailMessage()
            msg['From'] = f"{email_settings['sender_name']} <{email_settings['sender_email']}>"
            msg['To'] = f"{recipient_name} <{recipient_email}>"
            msg['Subject'] = "Account Information - Your New Account"

            email_body = (
                f"Hello {recipient_name},\n\n"
                "Thank you for creating an account with Google login.\n\n"
                "For your security, please change your temporary password "
                "the first time you log in to our system.\n\n"
                "Best regards,\n"
                f"{email_settings['sender_name']}"
            )
            msg.set_content(email_body)

            with smtplib.SMTP(
                    host=email_settings['smtp_host'],
                    port=email_settings['smtp_port'],
                    timeout=10
            ) as server:
                server.starttls()
                server.login(
                    user=email_settings['sender_email'],
                    password=email_settings['app_password']
                )
                server.send_message(msg)

            return True

        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    @staticmethod
    def send_password_email(recipient_name: str, recipient_email: str, new_password: str) -> bool:
        try:
            if not MailUtils.is_email_valid(recipient_email):
                raise ValueError(f"Invalid email address: {recipient_email}")

            config = MailUtils._load_config()
            email_settings = config.get("email_settings")

            if not email_settings:
                raise Exception("Email settings not found in config")

            msg = EmailMessage()
            msg['From'] = f"{email_settings['sender_name']} <{email_settings['sender_email']}>"
            msg['To'] = f"{recipient_name} <{recipient_email}>"
            msg['Subject'] = "Tu nueva contraseña"

            email_body = (
                f"Hola {recipient_name},\n\n"
                f"Tu nueva contraseña es: {new_password}\n\n"
                "Por seguridad, te recomendamos cambiar esta contraseña después de iniciar sesión.\n\n"
                "Atentamente,\n"
                f"{email_settings['sender_name']}"
            )
            msg.set_content(email_body)

            with smtplib.SMTP(
                    host=email_settings['smtp_host'],
                    port=email_settings['smtp_port'],
                    timeout=10
            ) as server:
                server.starttls()
                server.login(
                    user=email_settings['sender_email'],
                    password=email_settings['app_password']
                )
                server.send_message(msg)

            print(f"Email con contraseña enviado a {recipient_email}")
            return True

        except smtplib.SMTPException as e:
            print(f"Error SMTP al enviar contraseña: {str(e)}")
            raise Exception(f"Error al enviar email: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            raise

    @staticmethod
    def is_email_valid(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.fullmatch(pattern, email) is not None