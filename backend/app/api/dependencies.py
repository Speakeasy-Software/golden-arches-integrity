"""
Shared dependencies for API endpoints.
"""
from typing import Optional
from fastapi import HTTPException, Depends, Header, Cookie
from loguru import logger

from ..services.auth_service import auth_service
from ..api.models.user import UserSession


def get_session_token(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)) -> Optional[str]:
    """Extract session token from Authorization header or cookie."""
    if authorization and authorization.startswith("Bearer "):
        return authorization[7:]  # Remove "Bearer " prefix
    return session_token


def get_current_user(token: Optional[str] = Depends(get_session_token)) -> UserSession:
    """Get current authenticated user."""
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user = auth_service.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return user


def require_permission(permission: str):
    """Dependency to require specific permission."""
    def check_permission(token: Optional[str] = Depends(get_session_token)):
        if not token or not auth_service.has_permission(token, permission):
            raise HTTPException(status_code=403, detail=f"Permission required: {permission}")
        return token
    return check_permission


def require_senior_reviewer():
    """Dependency to require senior reviewer or training authority role."""
    def check_senior_reviewer(token: Optional[str] = Depends(get_session_token)):
        if not token or not auth_service.is_senior_reviewer(token):
            raise HTTPException(status_code=403, detail="Senior reviewer access required")
        return token
    return check_senior_reviewer


def require_training_authority():
    """Dependency to require training authority role."""
    def check_training_authority(token: Optional[str] = Depends(get_session_token)):
        if not token or not auth_service.is_training_authority(token):
            raise HTTPException(status_code=403, detail="Training authority access required")
        return token
    return check_training_authority 