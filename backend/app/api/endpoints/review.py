"""
Review and workload management endpoints for Quality Assurance Portal.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from ...services.workload_service import workload_service
from ...api.endpoints.auth import get_current_user, require_permission, require_senior_reviewer
from ...api.models.user import UserSession
from ...api.models.review import (
    WorkloadCreate, AssetReviewUpdate, ReviewFeedbackCreate,
    WorkloadStatus, ReviewStatus, FeedbackCategory
)


router = APIRouter()


@router.post("/workload")
async def create_workload(
    workload_data: WorkloadCreate,
    current_user: UserSession = Depends(get_current_user),
    token: str = Depends(require_permission("assign_workloads"))
):
    """Create a new workload assignment."""
    try:
        workload = workload_service.create_workload(workload_data, current_user.user_id)
        
        return {
            "success": True,
            "message": "Workload created successfully",
            "workload": workload
        }
        
    except Exception as e:
        logger.error(f"Failed to create workload: {e}")
        raise HTTPException(status_code=500, detail="Failed to create workload")


@router.get("/workloads")
async def get_workloads(
    user_id: Optional[int] = None,
    current_user: UserSession = Depends(get_current_user)
):
    """Get workloads. If user_id is provided and user has permission, get workloads for that user."""
    try:
        # If no user_id specified, get current user's workloads
        if user_id is None:
            workloads = workload_service.get_workloads_by_user(current_user.user_id)
        else:
            # Check if user can view other users' workloads
            if user_id != current_user.user_id and "access_all_data" not in current_user.permissions:
                raise HTTPException(status_code=403, detail="Cannot access other users' workloads")
            
            workloads = workload_service.get_workloads_by_user(user_id)
        
        return {
            "success": True,
            "workloads": workloads,
            "total": len(workloads)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workloads: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workloads")


@router.get("/workloads/all")
async def get_all_workloads(
    current_user: UserSession = Depends(get_current_user),
    token: str = Depends(require_permission("access_all_data"))
):
    """Get all workloads (senior reviewers and training authority only)."""
    try:
        workloads = workload_service.get_all_workloads()
        
        return {
            "success": True,
            "workloads": workloads,
            "total": len(workloads)
        }
        
    except Exception as e:
        logger.error(f"Failed to get all workloads: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workloads")


@router.get("/workload/{workload_id}")
async def get_workload(
    workload_id: int,
    current_user: UserSession = Depends(get_current_user)
):
    """Get specific workload with reviews."""
    try:
        workload = workload_service.get_workload(workload_id)
        
        if not workload:
            raise HTTPException(status_code=404, detail="Workload not found")
        
        # Check access permissions
        if (workload["assigned_to"] != current_user.user_id and 
            "access_all_data" not in current_user.permissions):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get associated reviews
        reviews = workload_service.get_asset_reviews_by_workload(workload_id)
        
        return {
            "success": True,
            "workload": workload,
            "reviews": reviews,
            "total_reviews": len(reviews)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workload {workload_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get workload")


@router.put("/workload/{workload_id}/status")
async def update_workload_status(
    workload_id: int,
    status: WorkloadStatus,
    current_user: UserSession = Depends(get_current_user)
):
    """Update workload status."""
    try:
        workload = workload_service.get_workload(workload_id)
        
        if not workload:
            raise HTTPException(status_code=404, detail="Workload not found")
        
        # Check permissions
        if (workload["assigned_to"] != current_user.user_id and 
            "assign_workloads" not in current_user.permissions):
            raise HTTPException(status_code=403, detail="Cannot update workload status")
        
        success = workload_service.update_workload_status(workload_id, status)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update workload status")
        
        return {
            "success": True,
            "message": "Workload status updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update workload status: {e}")
        raise HTTPException(status_code=500, detail="Failed to update workload status")


@router.get("/asset/{asset_id}/reviews")
async def get_asset_reviews(
    asset_id: int,
    current_user: UserSession = Depends(get_current_user)
):
    """Get all reviews for a specific asset."""
    try:
        reviews = workload_service.get_asset_reviews_by_asset(asset_id)
        
        # Filter reviews based on permissions
        if "access_all_data" not in current_user.permissions:
            reviews = [r for r in reviews if r["reviewer_id"] == current_user.user_id]
        
        return {
            "success": True,
            "reviews": reviews,
            "total": len(reviews)
        }
        
    except Exception as e:
        logger.error(f"Failed to get asset reviews: {e}")
        raise HTTPException(status_code=500, detail="Failed to get asset reviews")


@router.put("/review/{review_id}")
async def update_asset_review(
    review_id: int,
    update_data: AssetReviewUpdate,
    current_user: UserSession = Depends(get_current_user)
):
    """Update asset review (real-time saving)."""
    try:
        review = workload_service.get_asset_review(review_id)
        
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        # Check permissions
        if (review["reviewer_id"] != current_user.user_id and 
            "access_all_data" not in current_user.permissions):
            raise HTTPException(status_code=403, detail="Cannot update this review")
        
        success = workload_service.update_asset_review(review_id, update_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update review")
        
        return {
            "success": True,
            "message": "Review updated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update review: {e}")
        raise HTTPException(status_code=500, detail="Failed to update review")


@router.post("/review/{review_id}/approve")
async def approve_asset_review(
    review_id: int,
    current_user: UserSession = Depends(get_current_user),
    token: str = Depends(require_senior_reviewer())
):
    """Approve asset review (senior reviewer action)."""
    try:
        review = workload_service.get_asset_review(review_id)
        
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        success = workload_service.approve_asset_review(review_id, current_user.user_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to approve review")
        
        return {
            "success": True,
            "message": "Review approved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to approve review: {e}")
        raise HTTPException(status_code=500, detail="Failed to approve review")


@router.post("/feedback")
async def create_feedback(
    feedback_data: ReviewFeedbackCreate,
    current_user: UserSession = Depends(get_current_user)
):
    """Create review feedback."""
    try:
        feedback = workload_service.create_feedback(feedback_data, current_user.user_id)
        
        return {
            "success": True,
            "message": "Feedback created successfully",
            "feedback": feedback
        }
        
    except Exception as e:
        logger.error(f"Failed to create feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to create feedback")


@router.get("/feedback")
async def get_feedback(
    category: Optional[FeedbackCategory] = None,
    current_user: UserSession = Depends(get_current_user)
):
    """Get feedback, optionally filtered by category."""
    try:
        if category:
            feedback = workload_service.get_feedback_by_category(category)
        else:
            feedback = workload_service.get_all_feedback()
        
        # Filter feedback based on permissions
        if "access_all_data" not in current_user.permissions:
            feedback = [f for f in feedback if f["reviewer_id"] == current_user.user_id]
        
        return {
            "success": True,
            "feedback": feedback,
            "total": len(feedback)
        }
        
    except Exception as e:
        logger.error(f"Failed to get feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to get feedback")


@router.post("/feedback/{feedback_id}/resolve")
async def resolve_feedback(
    feedback_id: int,
    current_user: UserSession = Depends(get_current_user),
    token: str = Depends(require_senior_reviewer())
):
    """Resolve feedback item (senior reviewer action)."""
    try:
        success = workload_service.resolve_feedback(feedback_id, current_user.user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        return {
            "success": True,
            "message": "Feedback resolved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to resolve feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to resolve feedback")


@router.get("/statistics")
async def get_workload_statistics(
    current_user: UserSession = Depends(get_current_user),
    token: str = Depends(require_permission("access_all_data"))
):
    """Get workload and review statistics."""
    try:
        stats = workload_service.get_workload_statistics()
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics") 