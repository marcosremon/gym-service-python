import os
import string
import random
import json
import base64
from typing import Optional, Union

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

class PasswordUtils:
    _SECRET_KEY: Optional[bytes] = None
    _SALT: Optional[bytes] = None
    _CONFIG_LOADED: bool = False
    _PASSWORD_LENGTH: int = 12
    _FRIEND_CODE_LENGTH: int = 8

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> None:
        try:
            if not config_path:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(
                    base_dir, '..', '..', 'service', 'configuration', 'appsettings.json'
                )
                config_path = os.path.abspath(config_path)

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            encryption_settings = config.get('encryption_settings', {})
            cls._SECRET_KEY = encryption_settings.get('secret_key', '').encode()
            cls._SALT = encryption_settings.get('salt', '').encode()

            if not cls._SECRET_KEY or not cls._SALT:
                raise ValueError("Configuración de encriptación incompleta")

            cls._CONFIG_LOADED = True

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error decodificando JSON: {str(e)}") from e
        except FileNotFoundError as e:
            raise RuntimeError(f"Archivo de configuración no encontrado: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Error cargando configuración: {str(e)}") from e

    @classmethod
    def _get_cipher(cls) -> Fernet:
        if not cls._CONFIG_LOADED:
            cls.load_config()

        if not cls._SECRET_KEY or not cls._SALT:
            raise RuntimeError("Configuración de encriptación no disponible")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=cls._SALT,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(cls._SECRET_KEY))
        return Fernet(key)

    @staticmethod
    def encrypt_password(password: str) -> bytes:
        if not password:
            raise ValueError("La contraseña no puede estar vacía")
        cipher = PasswordUtils._get_cipher()
        return cipher.encrypt(password.encode())

    @staticmethod
    def decrypt_password(encrypted_password: bytes) -> str:
        cipher = PasswordUtils._get_cipher()
        return cipher.decrypt(encrypted_password).decode()

    @staticmethod
    def is_password_encrypted(password: Union[str, bytes]) -> bool:
        if isinstance(password, str):
            try:
                password = password.encode('utf-8')
            except UnicodeEncodeError:
                return False

        try:
            decoded = base64.urlsafe_b64decode(password)
            return len(decoded) > 0
        except (ValueError, Exception):
            return False

    @classmethod
    def generate_friend_code(cls) -> str:
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(chars) for _ in range(cls._FRIEND_CODE_LENGTH))

    @classmethod
    def generate_password(cls) -> str:
        chars = (
            string.ascii_letters +
            string.digits +
            "!@#$%^&*()_-+=<>?"
        )
        while True:
            password = ''.join(random.SystemRandom().choice(chars) for _ in range(cls._PASSWORD_LENGTH))
            if cls.is_password_valid(password):
                return password

    @staticmethod
    def is_password_valid(password: str) -> bool:
        if not password or len(password) < 8:
            return False

        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() and not c.isspace() for c in password)

        return all([has_lower, has_upper, has_digit, has_special])