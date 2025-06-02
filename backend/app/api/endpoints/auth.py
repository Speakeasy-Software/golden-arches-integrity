"""
Authentication endpoints for Quality Assurance Portal.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Header, Cookie
from fastapi.responses import JSONResponse
from loguru import logger

from ...services.auth_service import auth_service
from ...api.models.user import UserLogin, UserSession


router = APIRouter()


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


@router.post("/login")
async def login(login_data: UserLogin):
    """Authenticate user and create session."""
    try:
        session_token = auth_service.authenticate(login_data)
        
        if not session_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        user_session = auth_service.get_current_user(session_token)
        
        response = JSONResponse(content={
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user_session.user_id,
                "username": user_session.username,
                "role": user_session.role,
                "permissions": user_session.permissions
            }
        })
        
        # Set session token as HTTP-only cookie
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=8 * 60 * 60  # 8 hours
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/logout")
async def logout(token: Optional[str] = Depends(get_session_token)):
    """Logout user and invalidate session."""
    if token:
        auth_service.logout(token)
    
    response = JSONResponse(content={
        "success": True,
        "message": "Logout successful"
    })
    
    # Clear session cookie
    response.delete_cookie(key="session_token")
    
    return response


@router.get("/me")
async def get_current_user_info(current_user: UserSession = Depends(get_current_user)):
    """Get current user information."""
    return {
        "success": True,
        "user": {
            "id": current_user.user_id,
            "username": current_user.username,
            "role": current_user.role,
            "permissions": current_user.permissions,
            "expires_at": current_user.expires_at
        }
    }


@router.get("/users")
async def list_users(token: str = Depends(require_permission("manage_users"))):
    """List all users (training authority only)."""
    users = auth_service.get_all_users()
    
    # Remove sensitive information
    safe_users = []
    for username, user_data in users.items():
        safe_users.append({
            "id": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "role": user_data["role"],
            "status": user_data["status"],
            "last_login": user_data["last_login"],
            "created_at": user_data["created_at"]
        })
    
    return {
        "success": True,
        "users": safe_users,
        "total": len(safe_users)
    }


@router.get("/permissions")
async def get_user_permissions(current_user: UserSession = Depends(get_current_user)):
    """Get current user's permissions."""
    return {
        "success": True,
        "permissions": current_user.permissions,
        "role": current_user.role,
        "checks": {
            "is_training_authority": current_user.role == "training_authority",
            "is_senior_reviewer": current_user.role in ["training_authority", "senior_reviewer"],
            "can_assign_workloads": "assign_workloads" in current_user.permissions,
            "can_approve_reviews": "approve_reviews" in current_user.permissions,
            "can_make_final_decisions": "make_final_decisions" in current_user.permissions
        }
    }


@router.post("/cleanup-sessions")
async def cleanup_expired_sessions(token: str = Depends(require_training_authority())):
    """Clean up expired sessions (training authority only)."""
    auth_service.cleanup_expired_sessions()
    
    return {
        "success": True,
        "message": "Expired sessions cleaned up"
    } 