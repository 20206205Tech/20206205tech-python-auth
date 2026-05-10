import os

import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient

# Configuration from environment variables
JWKS_URL = os.getenv("SUPABASE_JWKS_URL")
AUDIENCE = os.getenv("SUPABASE_AUDIENCE", "authenticated")
ISSUER = os.getenv("SUPABASE_ISSUER")

# Fallback for Supabase projects
if not JWKS_URL or not ISSUER:
    PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
    if PROJECT_ID:
        if not JWKS_URL:
            JWKS_URL = f"https://{PROJECT_ID}.supabase.co/auth/v1/.well-known/jwks.json"
        if not ISSUER:
            ISSUER = f"https://{PROJECT_ID}.supabase.co/auth/v1"

if not JWKS_URL:
    raise RuntimeError("SUPABASE_JWKS_URL or SUPABASE_PROJECT_ID must be set")

jwks_client = PyJWKClient(JWKS_URL, cache_keys=True)


def verify_token(token: str) -> dict:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        return payload
    except jwt.PyJWKClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch JWKS",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
