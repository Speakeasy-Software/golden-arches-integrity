"""
Upload endpoints for assets including images, documents, and design files.
"""
import os
import uuid
import zipfile
import tempfile
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from PIL import Image
import io
from loguru import logger

from ...core.config import settings
from ...core.azure_client import azure_client
from ...api.models.asset import AssetCreate, Asset, AssetType


router = APIRouter()


def validate_file(file: UploadFile) -> None:
    """Validate uploaded file (images, documents, design files)."""
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


def extract_file_metadata(file_content: bytes, filename: str) -> dict:
    """Extract metadata from various file types."""
    file_ext = os.path.splitext(filename)[1].lower()
    metadata = {
        "file_extension": file_ext,
        "file_size": len(file_content)
    }
    
    # Try to extract image metadata for image files
    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
        try:
            image = Image.open(io.BytesIO(file_content))
            
            metadata.update({
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode,
                "has_transparency": image.mode in ("RGBA", "LA") or "transparency" in image.info
            })
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                exif_data = image._getexif()
                if exif_data:
                    metadata["exif"] = {k: v for k, v in exif_data.items() if isinstance(v, (str, int, float))}
            
        except Exception as e:
            logger.warning(f"Failed to extract image metadata from {filename}: {e}")
    
    # Add file type specific metadata
    elif file_ext == '.pdf':
        metadata["file_type"] = "document"
        metadata["document_type"] = "pdf"
    elif file_ext in ['.doc', '.docx']:
        metadata["file_type"] = "document"
        metadata["document_type"] = "word"
    elif file_ext in ['.ai', '.psd']:
        metadata["file_type"] = "design"
        metadata["design_type"] = file_ext[1:]  # Remove the dot
    elif file_ext == '.svg':
        metadata["file_type"] = "vector"
        metadata["vector_type"] = "svg"
    
    return metadata


def process_zip_file(zip_content: bytes, filename: str) -> List[dict]:
    """Process ZIP file and extract individual files."""
    extracted_files = []
    
    try:
        with tempfile.NamedTemporaryFile() as temp_zip:
            temp_zip.write(zip_content)
            temp_zip.flush()
            
            with zipfile.ZipFile(temp_zip.name, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if not file_info.is_dir():
                        file_ext = os.path.splitext(file_info.filename)[1].lower()
                        if file_ext in settings.allowed_extensions:
                            file_content = zip_ref.read(file_info.filename)
                            extracted_files.append({
                                "filename": file_info.filename,
                                "content": file_content,
                                "size": len(file_content)
                            })
                        else:
                            logger.warning(f"Skipping unsupported file in ZIP: {file_info.filename}")
    
    except Exception as e:
        logger.error(f"Failed to process ZIP file {filename}: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process ZIP file: {str(e)}"
        )
    
    return extracted_files


@router.post("/single", response_model=dict)
async def upload_single_asset(
    file: UploadFile = File(...),
    asset_type: AssetType = Form(...),
    description: str = Form(None),
    tags: str = Form(None),  # Comma-separated tags
    partner_usage: bool = Form(False),
    source_url: str = Form(None),
    version: str = Form(None)
):
    """Upload a single asset (image, document, or design file) for brand compliance analysis."""
    
    # Validate file
    validate_file(file)
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check if it's a ZIP file and process accordingly
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext == '.zip':
            # Process ZIP file
            extracted_files = process_zip_file(file_content, file.filename)
            
            if not extracted_files:
                raise HTTPException(
                    status_code=400,
                    detail="ZIP file contains no supported files"
                )
            
            # Process each extracted file
            uploaded_assets = []
            for extracted_file in extracted_files:
                # Extract metadata
                file_metadata = extract_file_metadata(extracted_file["content"], extracted_file["filename"])
                
                # Generate unique filename
                extracted_ext = os.path.splitext(extracted_file["filename"])[1].lower()
                unique_filename = f"{uuid.uuid4()}{extracted_ext}"
                
                # Upload to Azure Blob Storage
                blob_url = await azure_client.upload_image(
                    file_content=io.BytesIO(extracted_file["content"]),
                    filename=unique_filename
                )
                
                # Parse tags
                tag_list = []
                if tags:
                    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                
                # Create asset record
                asset_data = {
                    "id": int(str(uuid.uuid4().int)[:10]),
                    "filename": unique_filename,
                    "original_filename": extracted_file["filename"],
                    "asset_type": asset_type,
                    "description": description,
                    "tags": tag_list,
                    "partner_usage": partner_usage,
                    "source_url": source_url,
                    "version": version,
                    "blob_url": blob_url,
                    "file_size": extracted_file["size"],
                    "image_width": file_metadata.get("width", 0),
                    "image_height": file_metadata.get("height", 0),
                    "compliance_status": "needs_annotation",
                    "overall_score": 0.0,
                    "metadata": file_metadata,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                }
                
                uploaded_assets.append(asset_data)
                logger.info(f"Successfully uploaded from ZIP: {unique_filename}")
            
            return {
                "success": True,
                "message": f"Successfully processed ZIP file with {len(uploaded_assets)} assets",
                "assets": uploaded_assets,
                "total_assets": len(uploaded_assets)
            }
        
        else:
            # Process single file
            # Extract file metadata
            file_metadata = extract_file_metadata(file_content, file.filename)
            
            # Generate unique filename
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
            
            # Create asset record
            asset_data = {
                "id": int(str(uuid.uuid4().int)[:10]),
                "filename": unique_filename,
                "original_filename": file.filename,
                "asset_type": asset_type,
                "description": description,
                "tags": tag_list,
                "partner_usage": partner_usage,
                "source_url": source_url,
                "version": version,
                "blob_url": blob_url,
                "file_size": len(file_content),
                "image_width": file_metadata.get("width", 0),
                "image_height": file_metadata.get("height", 0),
                "compliance_status": "needs_annotation",
                "overall_score": 0.0,
                "metadata": file_metadata,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            
            logger.info(f"Successfully uploaded asset: {unique_filename}")
            
            return {
                "success": True,
                "message": "Asset uploaded successfully",
                "asset": asset_data
            }
        
    except Exception as e:
        logger.error(f"Failed to upload asset {file.filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload asset: {str(e)}"
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
            validate_file(file)
            
            # Read file content
            file_content = await file.read()
            
            # Extract metadata
            image_metadata = extract_file_metadata(file_content, file.filename)
            
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