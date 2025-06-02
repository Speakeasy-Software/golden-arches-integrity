"""
Review and workload models for Quality Assurance Portal.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class WorkloadStatus(str, Enum):
    """Workload status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReviewStatus(str, Enum):
    """Individual asset review status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_SENIOR_APPROVAL = "needs_senior_approval"


class ReviewMode(str, Enum):
    """Review interface mode."""
    SINGLE_ASSET = "single_asset"
    FULL_WORKLOAD = "full_workload"


class FeedbackCategory(str, Enum):
    """Feedback categories for extensible feedback system."""
    RULE_CLARITY = "rule_clarity"
    EDGE_CASES = "edge_cases"
    TRAINING_GAPS = "training_gaps"
    USABILITY = "usability"
    GENERAL = "general"


class Workload(BaseModel):
    """Workload assignment model."""
    id: int
    title: str = Field(..., description="Unique workload identifier")
    description: Optional[str] = None
    assigned_to: int  # User ID
    assigned_by: int  # User ID who created the assignment
    asset_ids: List[int]
    status: WorkloadStatus
    review_mode: ReviewMode
    priority: str = "normal"  # low, normal, high, urgent
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0  # 0.0 to 1.0


class WorkloadCreate(BaseModel):
    """Workload creation model."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    assigned_to: int
    asset_ids: List[int] = Field(..., min_items=1)
    review_mode: ReviewMode = ReviewMode.SINGLE_ASSET
    priority: str = "normal"
    due_date: Optional[datetime] = None


class AssetReview(BaseModel):
    """Individual asset review model."""
    id: int
    asset_id: int
    workload_id: int
    reviewer_id: int
    status: ReviewStatus
    annotations: List[Dict[str, Any]] = []
    confidence_score: Optional[float] = None
    notes: Optional[str] = None
    bounding_boxes: List[Dict[str, Any]] = []
    compliance_flags: List[str] = []
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    approved_by: Optional[int] = None  # Senior reviewer who approved
    approved_at: Optional[datetime] = None


class AssetReviewCreate(BaseModel):
    """Asset review creation model."""
    asset_id: int
    workload_id: int
    annotations: List[Dict[str, Any]] = []
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    notes: Optional[str] = None
    bounding_boxes: List[Dict[str, Any]] = []
    compliance_flags: List[str] = []


class AssetReviewUpdate(BaseModel):
    """Asset review update model."""
    status: Optional[ReviewStatus] = None
    annotations: Optional[List[Dict[str, Any]]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    notes: Optional[str] = None
    bounding_boxes: Optional[List[Dict[str, Any]]] = None
    compliance_flags: Optional[List[str]] = None


class ReviewFeedback(BaseModel):
    """Review feedback model for extensible feedback system."""
    id: int
    reviewer_id: int
    asset_id: Optional[int] = None
    workload_id: Optional[int] = None
    category: FeedbackCategory
    title: str
    description: str
    severity: str = "medium"  # low, medium, high, critical
    status: str = "open"  # open, acknowledged, resolved
    created_at: datetime
    updated_at: datetime
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None


class ReviewFeedbackCreate(BaseModel):
    """Review feedback creation model."""
    asset_id: Optional[int] = None
    workload_id: Optional[int] = None
    category: FeedbackCategory
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    severity: str = "medium"


class BoundingBox(BaseModel):
    """Bounding box annotation model."""
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)
    width: float = Field(..., ge=0.0, le=1.0)
    height: float = Field(..., ge=0.0, le=1.0)
    label: str
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    notes: Optional[str] = None


class Annotation(BaseModel):
    """Annotation model for asset reviews."""
    id: int
    asset_id: int
    reviewer_id: int
    annotation_type: str  # bounding_box, text, flag, etc.
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class ReviewSession(BaseModel):
    """Review session tracking model."""
    id: int
    reviewer_id: int
    workload_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    assets_reviewed: int = 0
    auto_save_enabled: bool = True
    last_activity: datetime 