"""
Kaix — API dependencies.

Provides:
    - get_db: async database session per request
    - get_current_user: JWT validation via Supabase
"""

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import create_client

from app.config import settings
from app.db.models import User
from app.db.session import get_db

logger = logging.getLogger(__name__)

security = HTTPBearer()

DBSession = Annotated[AsyncSession, Depends(get_db)]

# ── Supabase client (shared) ──
_supabase = None


def _get_supabase():
    global _supabase
    if _supabase is None:
        _supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
    return _supabase


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: DBSession,
) -> User:
    """
    Validate Supabase JWT and return the authenticated user.

    Uses Supabase's auth.get_user() to validate the token server-side,
    which is more reliable than manual JWT decode. If the user exists in
    Supabase Auth but not in our users table, this will create the user
    record automatically (first-login sync).
    """
    token = credentials.credentials

    try:
        sb = _get_supabase()
        auth_response = sb.auth.get_user(token)
        sb_user = auth_response.user

        if sb_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid / Invalid token",
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Supabase token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid / Invalid token",
        )

    sub = str(sb_user.id)
    email = sb_user.email or ""
    user_metadata = sb_user.user_metadata or {}
    name = user_metadata.get("full_name") or user_metadata.get("name") or email.split("@")[0]

    # Look up user in our DB
    result = await db.execute(select(User).where(User.id == sub))
    user = result.scalar_one_or_none()

    if not user:
        # First-login: auto-create user record from Supabase user data
        user = User(
            id=sub,
            name=name,
            email=email,
            locale=user_metadata.get("locale", "id"),
        )
        db.add(user)
        await db.flush()
        logger.info(f"Created new user from Supabase: {user.id}")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
