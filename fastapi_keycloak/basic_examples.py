import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# Keycloak Configuration (Example values)
KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...\n-----END PUBLIC KEY-----"
KEYCLOAK_TOKEN_URL = "http://localhost:8090/realms/example/protocol/openid-connect/token"

# ==========================================
# APPROACH 1: HTTPBearer (Production Standard)
# ==========================================
security_bearer = HTTPBearer()

def get_current_user_bearer(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    token = credentials.credentials
    try:
        # Decode and verify the JWT using Keycloak's public key
        payload = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"], audience="account")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Keycloak Token")

# ==========================================
# APPROACH 2: OAuth2PasswordBearer (Better for Swagger Testing)
# ==========================================
# Pointing the tokenUrl directly to Keycloak's token endpoint
security_oauth2 = OAuth2PasswordBearer(tokenUrl=KEYCLOAK_TOKEN_URL)

def get_current_user_oauth2(token: str = Depends(security_oauth2)):
    try:
        payload = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"], audience="account")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Keycloak Token")

# ==========================================
# Protected Endpoints
# ==========================================

@app.get("/items-bearer")
def read_items_bearer(user: dict = Depends(get_current_user_bearer)):
    """Works out of the box with external apps.
    In Swagger UI, you must manually paste 'Bearer <JWT>'."""
    return {"message": "Authenticated via HTTPBearer", "user": user.get("preferred_username")}

@app.get("/items-oauth2")
def read_items_oauth2(user: dict = Depends(get_current_user_oauth2)):
    """In Swagger UI, clicking 'Authorize' opens a form where you type
    your Keycloak username/password. Swagger handles the exchange behind the scenes."""
    return {"message": "Authenticated via OAuth2PasswordBearer", "user": user.get("preferred_username")}
