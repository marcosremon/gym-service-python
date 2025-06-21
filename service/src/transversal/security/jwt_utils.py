import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError, DecodeError
from fastapi import HTTPException, status


class JWTUtils:
    def __init__(self):
        self._load_config()
        self._validate_config()

    def _load_config(self):
        config_path = Path("src/service/configuration/appsettings.json")
        try:
            with open(config_path) as config_file:
                self.config = json.load(config_file).get("JwtSettings", {})
        except Exception as e:
            raise RuntimeError(f"Error cargando configuración JWT: {e}")

    def _validate_config(self):
        required_keys = {
            "secret_key",
            "algorithm",
            "access_token_expire_minutes",
            "admin_access_token_expire_minutes",
            "refresh_token_expire_days"
        }
        missing = required_keys - self.config.keys()
        if missing:
            raise ValueError(f"Faltan claves de configuración JWT: {missing}")

    def _create_token(
        self,
        data: Dict[str, Any],
        minutes: int,
        is_admin: bool = False,
        custom_expires_delta: Optional[timedelta] = None
    ) -> str:
        payload = data.copy()
        expire = datetime.utcnow() + (custom_expires_delta or timedelta(minutes=minutes))
        payload.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "scope": "admin" if is_admin else "user",
            "is_admin": is_admin
        })

        return jwt.encode(payload, self.config["secret_key"], algorithm=self.config["algorithm"])

    def create_user_token(self, user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        return self._create_token(
            user_data,
            self.config["access_token_expire_minutes"],
            is_admin=False,
            custom_expires_delta=expires_delta
        )

    def create_admin_token(self, user_data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        return self._create_token(
            user_data,
            self.config["admin_access_token_expire_minutes"],
            is_admin=True,
            custom_expires_delta=expires_delta
        )

    def create_refresh_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(days=self.config["refresh_token_expire_days"]))
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }

        return jwt.encode(payload, self.config["secret_key"], algorithm=self.config["algorithm"])

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.config["secret_key"],
                algorithms=[self.config["algorithm"]]
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except DecodeError:
            raise HTTPException(status_code=401, detail="Token malformado")
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

    def is_token_valid(self, token: str) -> bool:
        try:
            self.verify_token(token)
            return True
        except Exception:
            return False

    def get_token_payload(self, token: str, verify_exp: bool = True) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.config["secret_key"],
                algorithms=[self.config["algorithm"]],
                options={"verify_exp": verify_exp}
            )
        except Exception as e:
            raise ValueError(f"Error al obtener payload: {e}")

    def is_admin(self, payload: Dict[str, Any]) -> bool:
        return payload.get("scope") == "admin" or payload.get("is_admin", False)
