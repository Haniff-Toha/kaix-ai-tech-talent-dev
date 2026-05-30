"""
Kaix — Auth endpoints (proxy to Supabase Auth).

The frontend calls these instead of hitting Supabase directly.
This keeps all auth logic on the backend.
"""

import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from supabase import create_client

from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

# Supabase Admin client
_supabase = None


def _get_supabase():
    global _supabase
    if _supabase is None:
        _supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
    return _supabase


# ── Schemas ──

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    locale: str = "id"


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: dict


class GoogleOAuthRequest(BaseModel):
    redirect_url: str | None = None


# ── Endpoints ──

@router.post("/signup", response_model=dict)
async def signup(body: SignupRequest):
    """
    Create a new user via Supabase Auth.
    Returns JWT token pair for immediate login.
    """
    try:
        sb = _get_supabase()
        result = sb.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {
                "data": {
                    "full_name": body.name,
                    "name": body.name,
                    "locale": body.locale,
                }
            }
        })

        if result.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal membuat akun. Coba lagi.",
            )

        # Check if email confirmation is required
        session = result.session
        if session is None:
            # Email confirmation required
            return {
                "status": "ok",
                "message": "Akun berhasil dibuat! Cek email untuk verifikasi.",
                "requires_confirmation": True,
                "data": {
                    "user_id": str(result.user.id),
                    "email": result.user.email,
                }
            }

        return {
            "status": "ok",
            "message": "Akun berhasil dibuat!",
            "requires_confirmation": False,
            "data": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "user": {
                    "id": str(result.user.id),
                    "email": result.user.email,
                    "name": body.name,
                    "locale": body.locale,
                }
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Signup failed: {error_msg}")

        if "already registered" in error_msg.lower() or "already been registered" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email sudah terdaftar. Silakan login.",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gagal membuat akun: {error_msg}",
        )


@router.post("/login", response_model=dict)
async def login(body: LoginRequest):
    """
    Login via Supabase Auth.
    Returns JWT token pair.
    """
    try:
        sb = _get_supabase()
        result = sb.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })

        if result.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah.",
            )

        user_meta = result.user.user_metadata or {}

        return {
            "status": "ok",
            "data": {
                "access_token": result.session.access_token,
                "refresh_token": result.session.refresh_token,
                "user": {
                    "id": str(result.user.id),
                    "email": result.user.email,
                    "name": user_meta.get("full_name") or user_meta.get("name") or body.email.split("@")[0],
                    "locale": user_meta.get("locale", "id"),
                }
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Login failed: {error_msg}")

        if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email atau password salah.",
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login gagal: {error_msg}",
        )


@router.post("/google", response_model=dict)
async def google_oauth(body: GoogleOAuthRequest):
    """
    Get Google OAuth URL for frontend redirect.
    """
    try:
        sb = _get_supabase()
        redirect_to = body.redirect_url or "http://localhost:5173/auth/callback"
        result = sb.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_to,
            }
        })
        return {
            "status": "ok",
            "data": {
                "url": result.url,
            }
        }
    except Exception as e:
        logger.error(f"Google OAuth failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google login gagal: {str(e)}",
        )


@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    """
    Refresh an expired JWT using the refresh token.
    """
    try:
        sb = _get_supabase()
        result = sb.auth.refresh_session(refresh_token)

        if result.session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token tidak valid.",
            )

        return {
            "status": "ok",
            "data": {
                "access_token": result.session.access_token,
                "refresh_token": result.session.refresh_token,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesi kedaluwarsa. Silakan login ulang.",
        )
