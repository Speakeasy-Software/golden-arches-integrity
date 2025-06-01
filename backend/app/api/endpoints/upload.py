"""
Upload endpoints for image assets.
"""
import os
import uuid
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from PIL import Image
import io
from loguru import logger

from ...core.config import settings
from ...core.azure_client import azure_client
from ...api.models.asset import AssetCreate, Asset, AssetType


router = APIRouter()


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Allowed types: {settings.allowed_extensions}"
        )
    
    # Check file size
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size {file.size} exceeds maximum allowed size {settings.max_file_size}"
        )


def extract_image_metadata(image_data: bytes) -> dict:
    """Extract metadata from image."""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        metadata = {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "has_transparency": image.mode in ("RGBA", "LA") or "transparency" in image.info
        }
        
        # Extract EXIF data if available
        if hasattr(image, '_getexif') and image._getexif():
            exif_data = image._getexif()
            if exif_data:
                metadata["exif"] = {k: v for k, v in exif_data.items() if isinstance(v, (str, int, float))}
        
        return metadata
        
    except Exception as e:
        logger.warning(f"Failed to extract image metadata: {e}")
        return {}


@router.post("/single", response_model=dict)
async def upload_single_image(
    file: UploadFile = File(...),
    asset_type: AssetType = Form(...),
    description: str = Form(None),
    tags: str = Form(None)  # Comma-separated tags
):
    """Upload a single image for brand compliance analysis."""
    
    # Validate file
    validate_image_file(file)
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract image metadata
        image_metadata = extract_image_metadata(file_content)
        
        # Generate unique filename
        file_ext = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        
        # Upload to Azure Blob Storage
        blob_url = await azure_client.upload_image(
            file_content=io.BytesIO(file_content),
            filename=unique_filename
        )
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        # Create asset record (in a real app, this would go to a database)
        asset_data = {
            "id": int(str(uuid.uuid4().int)[:10]),  # Simplified ID for demo
            "filename": unique_filename,
            "original_filename": file.filename,
            "asset_type": asset_type,
            "description": description,
            "tags": tag_list,
            "blob_url": blob_url,
            "file_size": len(file_content),
            "image_width": image_metadata.get("width", 0),
            "image_height": image_metadata.get("height", 0),
            "compliance_status": "needs_annotation",
            "overall_score": 0.0,
            "metadata": image_metadata,
            "created_at": "2024-01-01T00:00:00Z",  # Would use actual timestamp
            "updated_at": "2024-01-01T00:00:00Z"
        }
        
        logger.info(f"Successfully uploaded image: {unique_filename}")
        
        return {
            "success": True,
            "message": "Image uploaded successfully",
            "asset": asset_data
        }
        
    except Exception as e:
        logger.error(f"Failed to upload image {file.filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/batch", response_model=dict)
async def upload_batch_images(
    files: List[UploadFile] = File(...),
    asset_type: AssetType = Form(...),
    description: str = Form(None)
):
    """Upload multiple images for batch processing."""
    
    if len(files) > 50:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail="Batch size cannot exceed 50 files"
        )
    
    uploaded_assets = []
    failed_uploads = []
    
    for file in files:
        try:
            # Validate each file
            validate_image_file(file)
            
            # Read file content
            file_content = await file.read()
            
            # Extract metadata
            image_metadata = extract_image_metadata(file_content)
            
            # Generate unique filename
            file_ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            
            # Upload to Azure
            blob_url = await azure_client.upload_image(
                file_content=io.BytesIO(file_content),
                filename=unique_filename
            )
            
            # Create asset record
            asset_data = {
                "id": int(str(uuid.uuid4().int)[:10]),
                "filename": unique_filename,
                "original_filename": file.filename,
                "asset_type": asset_type,
                "description": description,
                "blob_url": blob_url,
                "file_size": len(file_content),
                "image_width": image_metadata.get("width", 0),
                "image_height": image_metadata.get("height", 0),
                "compliance_status": "needs_annotation",
                "overall_score": 0.0,
                "metadata": image_metadata,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            
            uploaded_assets.append(asset_data)
            logger.info(f"Successfully uploaded: {unique_filename}")
            
        except Exception as e:
            logger.error(f"Failed to upload {file.filename}: {e}")
            failed_uploads.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "success": len(failed_uploads) == 0,
        "message": f"Uploaded {len(uploaded_assets)} of {len(files)} files",
        "uploaded_assets": uploaded_assets,
        "failed_uploads": failed_uploads,
        "total_uploaded": len(uploaded_assets),
        "total_failed": len(failed_uploads)
    }


@router.get("/list")
async def list_uploaded_images(
    prefix: str = "",
    limit: int = 100
):
    """List uploaded images from blob storage."""
    
    try:
        blob_list = await azure_client.list_images(prefix=prefix)
        
        # Limit results
        if limit:
            blob_list = blob_list[:limit]
        
        return {
            "success": True,
            "images": blob_list,
            "count": len(blob_list)
        }
        
    except Exception as e:
        logger.error(f"Failed to list images: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list images: {str(e)}"
        )


@router.delete("/{filename}")
async def delete_image(filename: str):
    """Delete an uploaded image."""
    
    try:
        # In a real application, you would:
        # 1. Check if user has permission to delete
        # 2. Delete from database
        # 3. Delete from blob storage
        
        # For now, just return success
        logger.info(f"Delete request for image: {filename}")
        
        return {
            "success": True,
            "message": f"Image {filename} deletion requested"
        }
        
    except Exception as e:
        logger.error(f"Failed to delete image {filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete image: {str(e)}"
        ) 