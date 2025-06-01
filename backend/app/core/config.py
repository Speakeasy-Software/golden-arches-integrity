"""
Configuration settings for the Golden Arches Integrity application.
"""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with Azure integration."""
    
    # Application settings
    app_name: str = "Golden Arches Integrity"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_v1_str: str = "/api/v1"
    secret_key: str = Field(..., description="Secret key for JWT tokens")
    access_token_expire_minutes: int = 60 * 24 * 8  # 8 days
    
    # Azure settings
    azure_subscription_id: str = "e93bc54d-78c1-418a-85a8-ab40fe3e7547"
    azure_resource_group: str = "golden-arches"
    azure_ml_workspace: str = "Golden-Arches"
    azure_storage_account: str = "kparches"
    azure_tenant_id: str = "08aee1f9-1f48-4edc-bbbd-51bca1140430"
    azure_region: str = "westus2"
    
    # Azure Storage settings
    azure_storage_connection_string: Optional[str] = None
    azure_blob_container_images: str = "images"
    azure_blob_container_annotations: str = "annotations"
    azure_blob_container_models: str = "models"
    
    # Azure AD settings
    azure_ad_client_id: Optional[str] = None
    azure_ad_client_secret: Optional[str] = None
    azure_ad_authority: str = f"https://login.microsoftonline.com/{azure_tenant_id}"
    
    # Database settings
    database_url: str = "sqlite:///./golden_arches.db"  # Default to SQLite for development
    
    # ML settings
    model_name: str = "golden-arches-compliance"
    model_version: str = "latest"
    confidence_threshold: float = 0.7
    batch_size: int = 32
    max_image_size: int = 1024
    
    # Brand rule settings
    golden_arches_rgb: tuple[int, int, int] = (255, 188, 13)
    color_tolerance: int = 10
    min_logo_size: int = 50
    max_rotation_degrees: float = 5.0
    
    # File upload settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 