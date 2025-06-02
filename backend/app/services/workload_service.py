"""
Workload management service for Quality Assurance Portal.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from loguru import logger

from ..api.models.review import (
    Workload, WorkloadCreate, WorkloadStatus, ReviewStatus, ReviewMode,
    AssetReview, AssetReviewCreate, AssetReviewUpdate, ReviewFeedback, ReviewFeedbackCreate,
    FeedbackCategory
)


class WorkloadService:
    """Service for managing workloads and asset reviews."""
    
    def __init__(self):
        # In-memory storage for Phase 1 (would use database in production)
        self.workloads: Dict[int, Dict[str, Any]] = {}
        self.asset_reviews: Dict[int, Dict[str, Any]] = {}
        self.feedback: Dict[int, Dict[str, Any]] = {}
        self.next_workload_id = 1
        self.next_review_id = 1
        self.next_feedback_id = 1
    
    def create_workload(self, workload_data: WorkloadCreate, assigned_by: int) -> Dict[str, Any]:
        """Create a new workload assignment."""
        workload_id = self.next_workload_id
        self.next_workload_id += 1
        
        # Generate unique title if not provided or ensure uniqueness
        title = workload_data.title
        if not title or self._is_title_taken(title):
            title = f"Workload-{workload_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        workload = {
            "id": workload_id,
            "title": title,
            "description": workload_data.description,
            "assigned_to": workload_data.assigned_to,
            "assigned_by": assigned_by,
            "asset_ids": workload_data.asset_ids,
            "status": WorkloadStatus.PENDING,
            "review_mode": workload_data.review_mode,
            "priority": workload_data.priority,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "due_date": workload_data.due_date,
            "completed_at": None,
            "progress": 0.0
        }
        
        self.workloads[workload_id] = workload
        
        # Create individual asset reviews for each asset
        for asset_id in workload_data.asset_ids:
            self._create_asset_review(asset_id, workload_id, workload_data.assigned_to)
        
        logger.info(f"Created workload {workload_id} with {len(workload_data.asset_ids)} assets")
        return workload
    
    def _is_title_taken(self, title: str) -> bool:
        """Check if workload title is already taken."""
        return any(w["title"] == title for w in self.workloads.values())
    
    def _create_asset_review(self, asset_id: int, workload_id: int, reviewer_id: int) -> Dict[str, Any]:
        """Create an asset review record."""
        review_id = self.next_review_id
        self.next_review_id += 1
        
        review = {
            "id": review_id,
            "asset_id": asset_id,
            "workload_id": workload_id,
            "reviewer_id": reviewer_id,
            "status": ReviewStatus.PENDING,
            "annotations": [],
            "confidence_score": None,
            "notes": None,
            "bounding_boxes": [],
            "compliance_flags": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "completed_at": None,
            "approved_by": None,
            "approved_at": None
        }
        
        self.asset_reviews[review_id] = review
        return review
    
    def get_workload(self, workload_id: int) -> Optional[Dict[str, Any]]:
        """Get workload by ID."""
        return self.workloads.get(workload_id)
    
    def get_workloads_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all workloads assigned to a user."""
        return [
            workload for workload in self.workloads.values()
            if workload["assigned_to"] == user_id
        ]
    
    def get_all_workloads(self) -> List[Dict[str, Any]]:
        """Get all workloads."""
        return list(self.workloads.values())
    
    def update_workload_status(self, workload_id: int, status: WorkloadStatus) -> bool:
        """Update workload status."""
        if workload_id not in self.workloads:
            return False
        
        workload = self.workloads[workload_id]
        workload["status"] = status
        workload["updated_at"] = datetime.now()
        
        if status == WorkloadStatus.COMPLETED:
            workload["completed_at"] = datetime.now()
        
        return True
    
    def get_asset_review(self, review_id: int) -> Optional[Dict[str, Any]]:
        """Get asset review by ID."""
        return self.asset_reviews.get(review_id)
    
    def get_asset_reviews_by_workload(self, workload_id: int) -> List[Dict[str, Any]]:
        """Get all asset reviews for a workload."""
        return [
            review for review in self.asset_reviews.values()
            if review["workload_id"] == workload_id
        ]
    
    def get_asset_reviews_by_asset(self, asset_id: int) -> List[Dict[str, Any]]:
        """Get all reviews for a specific asset."""
        return [
            review for review in self.asset_reviews.values()
            if review["asset_id"] == asset_id
        ]
    
    def update_asset_review(self, review_id: int, update_data: AssetReviewUpdate) -> bool:
        """Update asset review."""
        if review_id not in self.asset_reviews:
            return False
        
        review = self.asset_reviews[review_id]
        
        # Update fields
        if update_data.status is not None:
            review["status"] = update_data.status
        if update_data.annotations is not None:
            review["annotations"] = update_data.annotations
        if update_data.confidence_score is not None:
            review["confidence_score"] = update_data.confidence_score
        if update_data.notes is not None:
            review["notes"] = update_data.notes
        if update_data.bounding_boxes is not None:
            review["bounding_boxes"] = update_data.bounding_boxes
        if update_data.compliance_flags is not None:
            review["compliance_flags"] = update_data.compliance_flags
        
        review["updated_at"] = datetime.now()
        
        if update_data.status == ReviewStatus.COMPLETED:
            review["completed_at"] = datetime.now()
        
        # Update workload progress
        self._update_workload_progress(review["workload_id"])
        
        return True
    
    def approve_asset_review(self, review_id: int, approver_id: int) -> bool:
        """Approve asset review (senior reviewer action)."""
        if review_id not in self.asset_reviews:
            return False
        
        review = self.asset_reviews[review_id]
        review["status"] = ReviewStatus.APPROVED
        review["approved_by"] = approver_id
        review["approved_at"] = datetime.now()
        review["updated_at"] = datetime.now()
        
        # Update workload progress
        self._update_workload_progress(review["workload_id"])
        
        return True
    
    def _update_workload_progress(self, workload_id: int):
        """Update workload progress based on completed reviews."""
        if workload_id not in self.workloads:
            return
        
        workload = self.workloads[workload_id]
        reviews = self.get_asset_reviews_by_workload(workload_id)
        
        if not reviews:
            return
        
        completed_reviews = sum(
            1 for review in reviews
            if review["status"] in [ReviewStatus.COMPLETED, ReviewStatus.APPROVED]
        )
        
        progress = completed_reviews / len(reviews)
        workload["progress"] = progress
        workload["updated_at"] = datetime.now()
        
        # Auto-complete workload if all reviews are done
        if progress == 1.0 and workload["status"] != WorkloadStatus.COMPLETED:
            workload["status"] = WorkloadStatus.COMPLETED
            workload["completed_at"] = datetime.now()
    
    def create_feedback(self, feedback_data: ReviewFeedbackCreate, reviewer_id: int) -> Dict[str, Any]:
        """Create review feedback."""
        feedback_id = self.next_feedback_id
        self.next_feedback_id += 1
        
        feedback = {
            "id": feedback_id,
            "reviewer_id": reviewer_id,
            "asset_id": feedback_data.asset_id,
            "workload_id": feedback_data.workload_id,
            "category": feedback_data.category,
            "title": feedback_data.title,
            "description": feedback_data.description,
            "severity": feedback_data.severity,
            "status": "open",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "resolved_by": None,
            "resolved_at": None
        }
        
        self.feedback[feedback_id] = feedback
        logger.info(f"Created feedback {feedback_id} for category {feedback_data.category}")
        return feedback
    
    def get_feedback_by_category(self, category: FeedbackCategory) -> List[Dict[str, Any]]:
        """Get feedback by category."""
        return [
            feedback for feedback in self.feedback.values()
            if feedback["category"] == category
        ]
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """Get all feedback."""
        return list(self.feedback.values())
    
    def resolve_feedback(self, feedback_id: int, resolver_id: int) -> bool:
        """Resolve feedback item."""
        if feedback_id not in self.feedback:
            return False
        
        feedback = self.feedback[feedback_id]
        feedback["status"] = "resolved"
        feedback["resolved_by"] = resolver_id
        feedback["resolved_at"] = datetime.now()
        feedback["updated_at"] = datetime.now()
        
        return True
    
    def get_workload_statistics(self) -> Dict[str, Any]:
        """Get workload statistics."""
        total_workloads = len(self.workloads)
        pending_workloads = sum(1 for w in self.workloads.values() if w["status"] == WorkloadStatus.PENDING)
        in_progress_workloads = sum(1 for w in self.workloads.values() if w["status"] == WorkloadStatus.IN_PROGRESS)
        completed_workloads = sum(1 for w in self.workloads.values() if w["status"] == WorkloadStatus.COMPLETED)
        
        total_reviews = len(self.asset_reviews)
        pending_reviews = sum(1 for r in self.asset_reviews.values() if r["status"] == ReviewStatus.PENDING)
        completed_reviews = sum(1 for r in self.asset_reviews.values() if r["status"] in [ReviewStatus.COMPLETED, ReviewStatus.APPROVED])
        
        open_feedback = sum(1 for f in self.feedback.values() if f["status"] == "open")
        
        return {
            "workloads": {
                "total": total_workloads,
                "pending": pending_workloads,
                "in_progress": in_progress_workloads,
                "completed": completed_workloads
            },
            "reviews": {
                "total": total_reviews,
                "pending": pending_reviews,
                "completed": completed_reviews,
                "completion_rate": completed_reviews / total_reviews if total_reviews > 0 else 0
            },
            "feedback": {
                "open": open_feedback,
                "total": len(self.feedback)
            }
        }


# Global workload service instance
workload_service = WorkloadService() 