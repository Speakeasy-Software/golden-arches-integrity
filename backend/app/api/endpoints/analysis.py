"""
Analysis endpoints for brand compliance checking.
"""
import asyncio
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from loguru import logger

from ...core.config import settings
from ...api.models.asset import (
    ComplianceReport, BatchAnalysisRequest, BatchAnalysisResponse,
    BrandRule, RuleViolation, ColorAnalysis, GeometryAnalysis,
    ComplianceStatus
)
from ...rule_engine.brand_rules.color_compliance import ColorComplianceChecker
from ...rule_engine.brand_rules.geometry_rules import GeometryChecker
from ...services.ml_service import MLService


router = APIRouter()
ml_service = MLService()


@router.post("/analyze/{asset_id}", response_model=ComplianceReport)
async def analyze_asset(asset_id: int, force_reanalysis: bool = False):
    """Analyze a single asset for brand compliance."""
    
    start_time = time.time()
    
    try:
        logger.info(f"Starting analysis for asset {asset_id}")
        
        # In a real app, fetch asset from database
        # For demo, create mock asset data
        asset_data = {
            "id": asset_id,
            "filename": f"asset_{asset_id}.jpg",
            "blob_url": f"https://kparches.blob.core.windows.net/images/uploads/asset_{asset_id}.jpg"
        }
        
        # Initialize rule checkers
        color_checker = ColorComplianceChecker()
        geometry_checker = GeometryChecker()
        
        violations = []
        
        # Simulate downloading and analyzing the image
        # In production, this would download from blob storage
        logger.info(f"Analyzing image: {asset_data['filename']}")
        
        # Mock analysis results for demonstration
        # Color compliance check
        color_analysis = ColorAnalysis(
            dominant_colors=[(255, 188, 13), (255, 255, 255), (0, 0, 0)],
            golden_arches_color_match=True,
            color_accuracy_score=0.95,
            non_compliant_regions=[]
        )
        
        # Geometry analysis
        geometry_analysis = GeometryAnalysis(
            rotation_angle=2.5,
            is_flipped=False,
            is_warped=False,
            aspect_ratio=1.2,
            scale_factor=1.0,
            geometry_score=0.88
        )
        
        # Check for violations based on analysis
        if geometry_analysis.rotation_angle > settings.max_rotation_degrees:
            violations.append(RuleViolation(
                rule=BrandRule.NO_ROTATION,
                severity="medium",
                confidence=0.92,
                description=f"Logo rotated by {geometry_analysis.rotation_angle}° (max allowed: {settings.max_rotation_degrees}°)"
            ))
        
        if geometry_analysis.is_flipped:
            violations.append(RuleViolation(
                rule=BrandRule.NO_FLIPPING,
                severity="high",
                confidence=0.98,
                description="Logo appears to be horizontally flipped"
            ))
        
        if not color_analysis.golden_arches_color_match:
            violations.append(RuleViolation(
                rule=BrandRule.GOLD_COLOR_ONLY,
                severity="critical",
                confidence=0.85,
                description="Logo color does not match McDonald's gold (RGB: 255,188,13)"
            ))
        
        # Calculate overall compliance
        critical_violations = len([v for v in violations if v.severity == "critical"])
        overall_score = max(0.0, 1.0 - (len(violations) * 0.2) - (critical_violations * 0.3))
        
        if critical_violations > 0:
            compliance_status = ComplianceStatus.NON_COMPLIANT
        elif len(violations) > 0:
            compliance_status = ComplianceStatus.PENDING_REVIEW
        else:
            compliance_status = ComplianceStatus.COMPLIANT
        
        # Generate recommendations
        recommendations = []
        if violations:
            for violation in violations:
                if violation.rule == BrandRule.NO_ROTATION:
                    recommendations.append("Ensure logo is not rotated - use original orientation")
                elif violation.rule == BrandRule.GOLD_COLOR_ONLY:
                    recommendations.append("Use only McDonald's approved gold color (RGB: 255,188,13)")
                elif violation.rule == BrandRule.NO_FLIPPING:
                    recommendations.append("Do not flip or mirror the Golden Arches logo")
        else:
            recommendations.append("Asset meets all brand compliance requirements")
        
        processing_time = int((time.time() - start_time) * 1000)
        
        report = ComplianceReport(
            asset_id=asset_id,
            overall_compliance=compliance_status,
            compliance_score=overall_score,
            violations_count=len(violations),
            critical_violations=critical_violations,
            recommendations=recommendations,
            color_compliance=color_analysis.golden_arches_color_match,
            geometry_compliance=len([v for v in violations if v.rule in [BrandRule.NO_ROTATION, BrandRule.NO_FLIPPING]]) == 0,
            heritage_detected=False,  # Would be determined by ML model
            token_asset_detected=False,  # Would be determined by ML model
            model_version=settings.model_version,
            analysis_timestamp=time.time(),
            processing_time_ms=processing_time
        )
        
        logger.info(f"Analysis completed for asset {asset_id} in {processing_time}ms")
        return report
        
    except Exception as e:
        logger.error(f"Analysis failed for asset {asset_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/batch", response_model=BatchAnalysisResponse)
async def analyze_batch(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Start batch analysis of multiple assets."""
    
    if len(request.asset_ids) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size cannot exceed 100 assets"
        )
    
    # Generate job ID
    job_id = f"batch_{int(time.time())}_{len(request.asset_ids)}"
    
    # Add background task for processing
    background_tasks.add_task(
        process_batch_analysis,
        job_id,
        request.asset_ids,
        request.force_reanalysis
    )
    
    logger.info(f"Started batch analysis job {job_id} for {len(request.asset_ids)} assets")
    
    return BatchAnalysisResponse(
        job_id=job_id,
        status="started",
        total_assets=len(request.asset_ids),
        estimated_completion_time=None
    )


async def process_batch_analysis(job_id: str, asset_ids: List[int], force_reanalysis: bool):
    """Background task to process batch analysis."""
    
    logger.info(f"Processing batch analysis job {job_id}")
    
    try:
        for asset_id in asset_ids:
            # Analyze each asset
            await analyze_asset(asset_id, force_reanalysis)
            
            # Small delay to prevent overwhelming the system
            await asyncio.sleep(0.1)
        
        logger.info(f"Completed batch analysis job {job_id}")
        
    except Exception as e:
        logger.error(f"Batch analysis job {job_id} failed: {e}")


@router.get("/batch/{job_id}")
async def get_batch_status(job_id: str):
    """Get status of a batch analysis job."""
    
    # In a real application, this would check job status from database/cache
    return {
        "job_id": job_id,
        "status": "completed",  # Mock status
        "progress": 100,
        "completed_assets": 10,
        "total_assets": 10,
        "failed_assets": 0
    }


@router.get("/rules")
async def get_brand_rules():
    """Get list of all brand rules and their descriptions."""
    
    rules = {
        BrandRule.GOLD_COLOR_ONLY: {
            "name": "Gold Color Only",
            "description": "Use only McDonald's approved gold color (RGB: 255,188,13)",
            "severity": "critical",
            "category": "color"
        },
        BrandRule.BACKGROUND_LEGIBILITY: {
            "name": "Background Legibility",
            "description": "Backgrounds must not compromise logo legibility",
            "severity": "high",
            "category": "visibility"
        },
        BrandRule.NO_DROP_SHADOWS: {
            "name": "No Drop Shadows",
            "description": "Logo must not have drop shadows or 3D effects",
            "severity": "medium",
            "category": "effects"
        },
        BrandRule.NO_ROTATION: {
            "name": "No Rotation",
            "description": "Logo must not be rotated from its original orientation",
            "severity": "high",
            "category": "geometry"
        },
        BrandRule.NO_FLIPPING: {
            "name": "No Flipping",
            "description": "Logo must not be horizontally or vertically flipped",
            "severity": "high",
            "category": "geometry"
        },
        BrandRule.NOT_OBSCURED: {
            "name": "Not Obscured",
            "description": "Logo must be fully visible and not partially hidden",
            "severity": "high",
            "category": "visibility"
        },
        BrandRule.NO_WARPING_STRETCHING: {
            "name": "No Warping or Stretching",
            "description": "Logo proportions must remain unchanged",
            "severity": "high",
            "category": "geometry"
        },
        BrandRule.APPROVED_CROPPING: {
            "name": "Approved Cropping Only",
            "description": "Only use pre-approved cropping variations",
            "severity": "medium",
            "category": "composition"
        },
        BrandRule.HERITAGE_DETECTION: {
            "name": "Heritage Mark Detection",
            "description": "Detect and route heritage marks to appropriate rules",
            "severity": "low",
            "category": "classification"
        },
        BrandRule.TOKEN_COMPLIANCE: {
            "name": "Token Asset Compliance",
            "description": "Token assets must follow separate compliance rules",
            "severity": "medium",
            "category": "classification"
        }
    }
    
    return {
        "rules": rules,
        "total_rules": len(rules),
        "categories": list(set(rule["category"] for rule in rules.values()))
    }


@router.get("/stats")
async def get_analysis_stats():
    """Get analysis statistics and metrics."""
    
    # Mock statistics for demonstration
    return {
        "total_assets_analyzed": 1247,
        "compliant_assets": 892,
        "non_compliant_assets": 234,
        "pending_review": 121,
        "compliance_rate": 71.5,
        "most_common_violations": [
            {"rule": "no_rotation", "count": 89},
            {"rule": "gold_color_only", "count": 67},
            {"rule": "background_legibility", "count": 45}
        ],
        "average_processing_time_ms": 1250,
        "last_updated": time.time()
    } 