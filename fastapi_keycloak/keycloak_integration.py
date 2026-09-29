import time
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from loguru import logger
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import urlparse

logger.disable("cobra_keycloak")


class KeyCloakSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="keycloak_",
        env_file=Path(__file__).parent.parent / ".env",
        extra="ignore"
    )

    base_url: str = ""
    realm: str = ""
    ttl: int = 60
    algorithms: List[str] = ["HS256", "RS256"]

    @property
    def public_endpoint(self):
        base_url = self.base_url.rstrip("/")
        realm = self.realm.rstrip("/").lstrip("/")
        return f"{base_url}/auth/realms/{realm}"

    @field_validator("algorithms", mode="before")
    @classmethod
    def validate_algorithm(cls, value):
        if isinstance(value, list):
            for alg in value:
                if alg not in ALGORITHMS.SUPPORTED:
                    raise ValueError(f"unsupported JWS algorithm: {alg!r}")
            return value
        if value not in ALGORITHMS.SUPPORTED:
            raise ValueError(f"unsupported JWS algorithm: {value!r}")
        return value


class User(BaseModel):
    username: str
    family_name: str
    given_name: str
    name: str
    scope: List[str]
    roles: Dict[str, List[str]]

    @field_validator("scope", mode="before")
    @classmethod
    def split_scope(cls, v):
        if isinstance(v, str):
            return v.split(" ")
        return v

    @field_validator("roles", mode="before")
    @classmethod
    def split_roles(cls, v):
        if isinstance(v, dict):
            roles = {}
            for app, access in v.items():
                roles[app] = access["roles"]

            return roles
        return v  # pragma: no cover

    def has_role(self, context: str, role: str) -> bool:
        return role in self.roles.get(context, list())


class KeyCloakClient:
    def __init__(self):
        self.settings = KeyCloakSettings()
        self.ttl = self.settings.ttl
        self.last_fetch: int = -1
        self._public_key: str = ""

    @property
    def cache_expired(self):
        return (self.last_fetch + self.ttl) < time.perf_counter()

    def public_key(self):
        if not self._public_key or self.cache_expired:  # pragma: no cover
            self._public_key = self._get_keycloak_public_key()
            self.last_fetch = time.perf_counter()

        return (
            f"-----BEGIN PUBLIC KEY-----\n"
            f"{self._public_key}\n"
            f"-----END PUBLIC KEY-----"
        )

    def _get_keycloak_public_key(self):  # pragma: no cover
        try:
            realm_info = requests.get(self.settings.public_endpoint).json()
            if not realm_info.get("public_key"):
                raise ValueError("missing public key")

            logger.success("fetched public keycloak information")
            return realm_info["public_key"]
        except Exception as exc:
            msg = (
                f"Unable to fetch public keycloak "
                f"information from {self.settings.public_endpoint}: {exc}"
            )
            logger.error(msg)
            raise RuntimeError(msg)


@lru_cache()
def get_keycloak_client() -> KeyCloakClient:
    return KeyCloakClient()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def parse_token(payload: Dict) -> User:
    kwargs = {
        "username": payload["preferred_username"],
        "family_name": payload["family_name"],
        "given_name": payload["given_name"],
        "name": payload["name"],
        "scope": payload["scope"],
        "roles": payload.get("resource_access", {}),
    }
    user = User(**kwargs)
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    keycloak: KeyCloakClient = Depends(get_keycloak_client),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        public_key = keycloak.public_key()
        payload = jwt.decode(
            token,
            key=public_key,
            audience="account",
            algorithms=keycloak.settings.algorithms,
        )
        user = parse_token(payload=payload)
        if not payload.get("sub"):  # pragma: no cover
            credentials_exception.detail = "Missing sub"
            raise credentials_exception

        token_issuer = urlparse(payload.get("iss"))
        expected_issuer = urlparse(keycloak.settings.public_endpoint)

        # protocol returned by KeyCloak can be "http",
        # if behind a reverse proxy, while the endpoint will
        # most likely always be "https"
        if (token_issuer.netloc, token_issuer.path) != (
            expected_issuer.netloc,
            expected_issuer.path,
        ):
            credentials_exception.detail = "Invalid issuer"
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


def access_guard(context: str, roles: List[str]):
    async def guard(user: User = Depends(get_current_user)):
        if not any(
            user.has_role(context=context, role=role) for role in roles  # noqa
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    return guard
