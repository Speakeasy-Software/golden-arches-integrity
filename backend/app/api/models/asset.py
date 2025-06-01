"""
Pydantic models for image assets and brand compliance.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class AssetType(str, Enum):
    """Types of McDonald's assets."""
    PHOTOGRAPHY = "photography"
    RENDER = "render"
    HERITAGE = "heritage"
    TOKEN = "token"


class ComplianceStatus(str, Enum):
    """Compliance status for assets."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    NEEDS_ANNOTATION = "needs_annotation"


class BrandRule(str, Enum):
    """McDonald's brand integrity rules."""
    GOLD_COLOR_ONLY = "gold_color_only"
    BACKGROUND_LEGIBILITY = "background_legibility"
    NO_DROP_SHADOWS = "no_drop_shadows"
    NOT_AS_LETTERS_NUMBERS = "not_as_letters_numbers"
    NO_ROTATION = "no_rotation"
    NOT_OBSCURED = "not_obscured"
    NO_TEXTURE_MASKING = "no_texture_masking"
    NO_WARPING_STRETCHING = "no_warping_stretching"
    NO_OVER_MODIFICATION = "no_over_modification"
    NO_FLIPPING = "no_flipping"
    CURRENT_LOGO_STYLES = "current_logo_styles"
    APPROVED_CROPPING = "approved_cropping"
    TOKEN_COMPLIANCE = "token_compliance"
    HERITAGE_DETECTION = "heritage_detection"


class BoundingBox(BaseModel):
    """Bounding box coordinates for detected objects."""
    x: float = Field(..., ge=0, le=1, description="X coordinate (normalized)")
    y: float = Field(..., ge=0, le=1, description="Y coordinate (normalized)")
    width: float = Field(..., ge=0, le=1, description="Width (normalized)")
    height: float = Field(..., ge=0, le=1, description="Height (normalized)")
    confidence: float = Field(..., ge=0, le=1, description="Detection confidence")


class RuleViolation(BaseModel):
    """A specific brand rule violation."""
    rule: BrandRule
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    confidence: float = Field(..., ge=0, le=1)
    description: str
    bounding_box: Optional[BoundingBox] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ColorAnalysis(BaseModel):
    """Color analysis results for Golden Arches."""
    dominant_colors: List[tuple[int, int, int]]
    golden_arches_color_match: bool
    color_accuracy_score: float = Field(..., ge=0, le=1)
    non_compliant_regions: List[BoundingBox] = Field(default_factory=list)


class GeometryAnalysis(BaseModel):
    """Geometry analysis for logo detection."""
    rotation_angle: float
    is_flipped: bool
    is_warped: bool
    aspect_ratio: float
    scale_factor: float
    geometry_score: float = Field(..., ge=0, le=1)


class AssetBase(BaseModel):
    """Base model for image assets."""
    filename: str
    asset_type: AssetType
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AssetCreate(AssetBase):
    """Model for creating new assets."""
    pass


class AssetUpdate(BaseModel):
    """Model for updating assets."""
    filename: Optional[str] = None
    asset_type: Optional[AssetType] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    compliance_status: Optional[ComplianceStatus] = None


class Asset(AssetBase):
    """Complete asset model with analysis results."""
    id: int
    blob_url: HttpUrl
    file_size: int
    image_width: int
    image_height: int
    compliance_status: ComplianceStatus
    overall_score: float = Field(..., ge=0, le=1)
    
    # Analysis results
    rule_violations: List[RuleViolation] = Field(default_factory=list)
    color_analysis: Optional[ColorAnalysis] = None
    geometry_analysis: Optional[GeometryAnalysis] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    analyzed_at: Optional[datetime] = None
    
    # User tracking
    uploaded_by: Optional[str] = None
    reviewed_by: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnnotationBase(BaseModel):
    """Base model for annotations."""
    asset_id: int
    rule: BrandRule
    is_violation: bool
    confidence: float = Field(..., ge=0, le=1)
    notes: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None


class AnnotationCreate(AnnotationBase):
    """Model for creating annotations."""
    pass


class AnnotationUpdate(BaseModel):
    """Model for updating annotations."""
    is_violation: Optional[bool] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None


class Annotation(AnnotationBase):
    """Complete annotation model."""
    id: int
    created_at: datetime
    updated_at: datetime
    annotated_by: str
    
    class Config:
        from_attributes = True


class ComplianceReport(BaseModel):
    """Compliance analysis report for an asset."""
    asset_id: int
    overall_compliance: ComplianceStatus
    compliance_score: float = Field(..., ge=0, le=1)
    violations_count: int
    critical_violations: int
    recommendations: List[str] = Field(default_factory=list)
    
    # Detailed analysis
    color_compliance: bool
    geometry_compliance: bool
    heritage_detected: bool
    token_asset_detected: bool
    
    # Processing metadata
    model_version: str
    analysis_timestamp: datetime
    processing_time_ms: int


class BatchAnalysisRequest(BaseModel):
    """Request for batch analysis of multiple assets."""
    asset_ids: List[int]
    force_reanalysis: bool = False
    notify_on_completion: bool = True


class BatchAnalysisResponse(BaseModel):
    """Response for batch analysis request."""
    job_id: str
    status: str
    total_assets: int
    estimated_completion_time: Optional[datetime] = None 