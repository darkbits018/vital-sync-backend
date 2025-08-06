import firebase_admin
from firebase_admin import auth, credentials
from fastapi import Depends, HTTPException, status
from typing import Optional
from pathlib import Path
import os
from app.core.config import get_settings
settings = get_settings()

# Initialize Firebase Admin SDK once
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token: str) -> Optional[dict]:
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Firebase ID token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(verify_firebase_token)):
    return token