"""
Authentication service for Quality Assurance Portal.
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from loguru import logger

from ..api.models.user import User, UserRole, UserStatus, UserLogin, UserSession, EXPERT_USERS


class AuthService:
    """Simple authentication service for QA Portal."""
    
    def __init__(self):
        # In-memory storage for Phase 1 (would use database in production)
        self.users: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, UserSession] = {}
        self.session_duration = timedelta(hours=8)  # 8-hour sessions
        
        # Initialize expert users
        self._initialize_expert_users()
    
    def _initialize_expert_users(self):
        """Initialize predefined expert users."""
        for username, user_data in EXPERT_USERS.items():
            # Simple password hashing (would use proper bcrypt in production)
            password_hash = self._hash_password("password123")  # Default password
            
            self.users[username] = {
                "id": len(self.users) + 1,
                "username": username,
                "email": user_data["email"],
                "full_name": user_data["full_name"],
                "role": user_data["role"],
                "status": UserStatus.ACTIVE,
                "password_hash": password_hash,
                "permissions": user_data["permissions"],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "last_login": None
            }
        
        logger.info(f"Initialized {len(self.users)} expert users")
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing (would use bcrypt in production)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_session_token(self) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(32)
    
    def authenticate(self, login_data: UserLogin) -> Optional[str]:
        """Authenticate user and return session token."""
        username = login_data.username.lower()
        
        if username not in self.users:
            logger.warning(f"Authentication failed: user {username} not found")
            return None
        
        user = self.users[username]
        password_hash = self._hash_password(login_data.password)
        
        if user["password_hash"] != password_hash:
            logger.warning(f"Authentication failed: invalid password for {username}")
            return None
        
        if user["status"] != UserStatus.ACTIVE:
            logger.warning(f"Authentication failed: user {username} is not active")
            return None
        
        # Create session
        session_token = self._generate_session_token()
        expires_at = datetime.now() + self.session_duration
        
        session = UserSession(
            user_id=user["id"],
            username=user["username"],
            role=user["role"],
            permissions=user["permissions"],
            expires_at=expires_at
        )
        
        self.sessions[session_token] = session
        
        # Update last login
        user["last_login"] = datetime.now()
        
        logger.info(f"User {username} authenticated successfully")
        return session_token
    
    def get_current_user(self, session_token: str) -> Optional[UserSession]:
        """Get current user from session token."""
        if not session_token or session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check if session is expired
        if datetime.now() > session.expires_at:
            del self.sessions[session_token]
            return None
        
        return session
    
    def logout(self, session_token: str) -> bool:
        """Logout user and invalidate session."""
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
    
    def has_permission(self, session_token: str, permission: str) -> bool:
        """Check if user has specific permission."""
        session = self.get_current_user(session_token)
        if not session:
            return False
        
        return permission in session.permissions
    
    def is_training_authority(self, session_token: str) -> bool:
        """Check if user is training authority (Sven)."""
        session = self.get_current_user(session_token)
        if not session:
            return False
        
        return session.role == UserRole.TRAINING_AUTHORITY
    
    def is_senior_reviewer(self, session_token: str) -> bool:
        """Check if user is senior reviewer (Huan, George) or training authority."""
        session = self.get_current_user(session_token)
        if not session:
            return False
        
        return session.role in [UserRole.TRAINING_AUTHORITY, UserRole.SENIOR_REVIEWER]
    
    def can_approve_reviews(self, session_token: str) -> bool:
        """Check if user can approve reviews."""
        return self.has_permission(session_token, "approve_reviews")
    
    def can_assign_workloads(self, session_token: str) -> bool:
        """Check if user can assign workloads."""
        return self.has_permission(session_token, "assign_workloads")
    
    def can_make_final_decisions(self, session_token: str) -> bool:
        """Check if user can make final decisions."""
        return self.has_permission(session_token, "make_final_decisions")
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        return self.users.get(username.lower())
    
    def get_all_users(self) -> Dict[str, Dict[str, Any]]:
        """Get all users (for admin purposes)."""
        return self.users
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        now = datetime.now()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if now > session.expires_at
        ]
        
        for token in expired_tokens:
            del self.sessions[token]
        
        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")


# Global auth service instance
auth_service = AuthService() 