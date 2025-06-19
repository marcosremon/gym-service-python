import os
import string
from random import random
from sqlalchemy import LargeBinary
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
from typing import Optional, Union

class PasswordUtils:
    _SECRET_KEY: Optional[bytes] = None
    _SALT: Optional[bytes] = None
    _CONFIG_LOADED = False

    @classmethod
    def load_config(cls, config_path: str = None):
        try:
            if not config_path:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(base_dir, '..', '..', 'service', 'configuration', 'appsettings.json')
                config_path = os.path.abspath(config_path)

            with open(config_path, 'r') as f:
                config = json.load(f)

            encryption_settings = config.get('encryption_settings', {})
            cls._SECRET_KEY = encryption_settings.get('secret_key', '').encode()
            cls._SALT = encryption_settings.get('salt', '').encode()

            if not cls._SECRET_KEY or not cls._SALT:
                raise ValueError("Configuración de encriptación incompleta en el archivo JSON")

            cls._CONFIG_LOADED = True

        except Exception as e:
            raise RuntimeError(f"Error cargando configuración: {str(e)}")

    @classmethod
    def _get_cipher(cls):
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
    def encrypt_password(password: str) -> LargeBinary:
        cipher = PasswordUtils._get_cipher()
        encrypted_password = cipher.encrypt(password.encode())
        return encrypted_password

    @staticmethod
    def decrypt_password(encrypted_password: LargeBinary) -> str:
        cipher = PasswordUtils._get_cipher()
        decrypted_password = cipher.decrypt(encrypted_password)
        return decrypted_password.decode()

    @staticmethod
    def is_password_encrypted(password: Union[str, bytes]) -> bool:
        if isinstance(password, bytes):
            password = password.decode('utf-8')

        try:
            decoded_bytes = base64.b64decode(password)
            return len(decoded_bytes) % 16 == 0
        except (base64.binascii.Error, ValueError):
            return False

    @staticmethod
    def create_password(length: int) -> str:
        if length < 8:
            raise ValueError("La longitud mínima debe ser 8 caracteres")

        chars = f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}!@#$%^&*()_-+=<>?"
        password = ""

        for _ in range(length):
            password += random.choice(chars)

        return password

    @staticmethod
    def is_password_valid(password: str) -> bool:
        if not password or len(password) < 8:
            return False

        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() and not c.isspace() for c in password)

        return has_lower and has_upper and has_digit and has_special