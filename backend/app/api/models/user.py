"""
User models for Quality Assurance Portal.
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class UserRole(str, Enum):
    """User roles for the QA Portal."""
    TRAINING_AUTHORITY = "training_authority"  # Sven - full control
    SENIOR_REVIEWER = "senior_reviewer"        # Huan, George - full access
    GUEST_REVIEWER = "guest_reviewer"          # Limited access


class UserStatus(str, Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class User(BaseModel):
    """User model for QA Portal."""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    permissions: List[str] = []


class UserCreate(BaseModel):
    """User creation model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    full_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None


class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str


class UserSession(BaseModel):
    """User session model."""
    user_id: int
    username: str
    role: UserRole
    permissions: List[str]
    expires_at: datetime


# Predefined expert users for Phase 1
EXPERT_USERS = {
    "sven": {
        "username": "sven",
        "email": "sven@mcdonalds.com",
        "full_name": "Sven Mesecke",
        "role": UserRole.TRAINING_AUTHORITY,
        "permissions": [
            "upload_assets",
            "review_assets", 
            "assign_workloads",
            "approve_reviews",
            "manage_users",
            "control_training",
            "access_all_data",
            "make_final_decisions"
        ]
    },
    "huan": {
        "username": "huan",
        "email": "huan@mcdonalds.com", 
        "full_name": "Huan",
        "role": UserRole.SENIOR_REVIEWER,
        "permissions": [
            "upload_assets",
            "review_assets",
            "assign_workloads", 
            "approve_reviews",
            "access_all_data",
            "make_final_decisions"
        ]
    },
    "george": {
        "username": "george",
        "email": "george@mcdonalds.com",
        "full_name": "George", 
        "role": UserRole.SENIOR_REVIEWER,
        "permissions": [
            "upload_assets",
            "review_assets",
            "assign_workloads",
            "approve_reviews", 
            "access_all_data",
            "make_final_decisions"
        ]
    },
    "guest": {
        "username": "guest",
        "email": "guest@external.com",
        "full_name": "Guest Reviewer",
        "role": UserRole.GUEST_REVIEWER,
        "permissions": [
            "review_assigned_assets",
            "provide_feedback"
        ]
    }
} 