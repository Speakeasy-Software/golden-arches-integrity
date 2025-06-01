"""
Geometry rules checker for McDonald's Golden Arches.
"""
import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional
from loguru import logger

from ...core.config import settings


class GeometryChecker:
    """Checker for geometric compliance of McDonald's Golden Arches."""
    
    def __init__(self):
        self.max_rotation_degrees = settings.max_rotation_degrees
        self.min_logo_size = settings.min_logo_size
    
    def check_geometry_compliance(self, image: np.ndarray) -> Dict:
        """Check geometric compliance of the logo in the image."""
        
        try:
            # Convert to grayscale for analysis
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Detect logo contours
            logo_contours = self._detect_logo_contours(gray)
            
            if not logo_contours:
                return {
                    "rotation_angle": 0.0,
                    "is_flipped": False,
                    "is_warped": False,
                    "aspect_ratio": 1.0,
                    "scale_factor": 1.0,
                    "geometry_score": 0.0,
                    "error": "No logo detected"
                }
            
            # Analyze the largest contour (assumed to be the main logo)
            main_contour = max(logo_contours, key=cv2.contourArea)
            
            # Check rotation
            rotation_angle = self._detect_rotation(main_contour)
            
            # Check if flipped
            is_flipped = self._detect_flipping(main_contour, image.shape)
            
            # Check for warping/stretching
            is_warped = self._detect_warping(main_contour)
            
            # Calculate aspect ratio
            aspect_ratio = self._calculate_aspect_ratio(main_contour)
            
            # Calculate scale factor
            scale_factor = self._calculate_scale_factor(main_contour, image.shape)
            
            # Calculate overall geometry score
            geometry_score = self._calculate_geometry_score(
                rotation_angle, is_flipped, is_warped, aspect_ratio
            )
            
            return {
                "rotation_angle": rotation_angle,
                "is_flipped": is_flipped,
                "is_warped": is_warped,
                "aspect_ratio": aspect_ratio,
                "scale_factor": scale_factor,
                "geometry_score": geometry_score,
                "contour_area": cv2.contourArea(main_contour),
                "bounding_box": cv2.boundingRect(main_contour)
            }
            
        except Exception as e:
            logger.error(f"Geometry compliance check failed: {e}")
            return {
                "rotation_angle": 0.0,
                "is_flipped": False,
                "is_warped": False,
                "aspect_ratio": 1.0,
                "scale_factor": 1.0,
                "geometry_score": 0.0,
                "error": str(e)
            }
    
    def _detect_logo_contours(self, gray_image: np.ndarray) -> List:
        """Detect potential logo contours in the image."""
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
        
        # Apply threshold to create binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and shape
        filtered_contours = []
        min_area = self.min_logo_size * self.min_logo_size
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # Check if contour could be a logo (roughly arch-shaped)
                if self._is_potential_logo_shape(contour):
                    filtered_contours.append(contour)
        
        return filtered_contours
    
    def _is_potential_logo_shape(self, contour) -> bool:
        """Check if contour could potentially be a Golden Arches logo."""
        
        # Calculate basic shape properties
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return False
        
        # Calculate circularity (4π * area / perimeter²)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Golden Arches should have moderate circularity (not too round, not too linear)
        if 0.2 < circularity < 0.8:
            return True
        
        return False
    
    def _detect_rotation(self, contour) -> float:
        """Detect rotation angle of the logo."""
        
        try:
            # Fit an ellipse to the contour
            if len(contour) >= 5:  # Minimum points needed for ellipse fitting
                ellipse = cv2.fitEllipse(contour)
                angle = ellipse[2]  # Rotation angle
                
                # Normalize angle to [-90, 90] range
                if angle > 90:
                    angle = angle - 180
                
                return abs(angle)
            else:
                # Use minimum area rectangle as fallback
                rect = cv2.minAreaRect(contour)
                angle = rect[2]
                
                # Normalize angle
                if angle < -45:
                    angle = 90 + angle
                
                return abs(angle)
                
        except Exception as e:
            logger.warning(f"Rotation detection failed: {e}")
            return 0.0
    
    def _detect_flipping(self, contour, image_shape: Tuple[int, int]) -> bool:
        """Detect if the logo is horizontally flipped."""
        
        try:
            # Calculate moments to find centroid
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return False
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Analyze the shape's orientation
            # This is a simplified check - in practice, you'd use more sophisticated methods
            # like template matching or feature analysis
            
            # For Golden Arches, check if the arch opening faces the expected direction
            # This is a mock implementation - real detection would be more complex
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            contour_area = cv2.contourArea(contour)
            
            # If the ratio is significantly different from expected, might be flipped
            solidity = contour_area / hull_area if hull_area > 0 else 0
            
            # This is a placeholder - real flipping detection would require
            # template matching or machine learning
            return solidity < 0.7  # Arbitrary threshold for demo
            
        except Exception as e:
            logger.warning(f"Flipping detection failed: {e}")
            return False
    
    def _detect_warping(self, contour) -> bool:
        """Detect if the logo is warped or stretched."""
        
        try:
            # Fit ellipse and check if it's significantly non-circular
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                major_axis = max(ellipse[1])
                minor_axis = min(ellipse[1])
                
                if minor_axis > 0:
                    eccentricity = major_axis / minor_axis
                    # If eccentricity is too high, logo might be warped
                    return eccentricity > 2.0
            
            return False
            
        except Exception as e:
            logger.warning(f"Warping detection failed: {e}")
            return False
    
    def _calculate_aspect_ratio(self, contour) -> float:
        """Calculate the aspect ratio of the logo."""
        
        try:
            x, y, w, h = cv2.boundingRect(contour)
            if h > 0:
                return w / h
            return 1.0
            
        except Exception as e:
            logger.warning(f"Aspect ratio calculation failed: {e}")
            return 1.0
    
    def _calculate_scale_factor(self, contour, image_shape: Tuple[int, int]) -> float:
        """Calculate the scale factor of the logo relative to image size."""
        
        try:
            contour_area = cv2.contourArea(contour)
            image_area = image_shape[0] * image_shape[1]
            
            if image_area > 0:
                return np.sqrt(contour_area / image_area)
            return 1.0
            
        except Exception as e:
            logger.warning(f"Scale factor calculation failed: {e}")
            return 1.0
    
    def _calculate_geometry_score(self, rotation_angle: float, is_flipped: bool, 
                                 is_warped: bool, aspect_ratio: float) -> float:
        """Calculate overall geometry compliance score."""
        
        score = 1.0
        
        # Penalize rotation
        if rotation_angle > self.max_rotation_degrees:
            rotation_penalty = min(0.5, (rotation_angle - self.max_rotation_degrees) / 45.0)
            score -= rotation_penalty
        
        # Penalize flipping
        if is_flipped:
            score -= 0.3
        
        # Penalize warping
        if is_warped:
            score -= 0.4
        
        # Penalize unusual aspect ratios
        # Golden Arches should have a specific aspect ratio
        expected_ratio = 1.2  # Approximate expected ratio
        ratio_diff = abs(aspect_ratio - expected_ratio) / expected_ratio
        if ratio_diff > 0.2:  # More than 20% difference
            score -= min(0.2, ratio_diff)
        
        return max(0.0, score)
    
    def get_geometry_recommendations(self, analysis: Dict) -> List[str]:
        """Get recommendations for geometry compliance."""
        
        recommendations = []
        
        if analysis.get("rotation_angle", 0) > self.max_rotation_degrees:
            recommendations.append(
                f"Logo is rotated by {analysis['rotation_angle']:.1f}°. "
                f"Ensure logo is not rotated more than {self.max_rotation_degrees}°"
            )
        
        if analysis.get("is_flipped", False):
            recommendations.append(
                "Logo appears to be flipped. Use the original orientation only"
            )
        
        if analysis.get("is_warped", False):
            recommendations.append(
                "Logo appears warped or stretched. Maintain original proportions"
            )
        
        aspect_ratio = analysis.get("aspect_ratio", 1.0)
        if aspect_ratio < 0.8 or aspect_ratio > 1.6:
            recommendations.append(
                f"Aspect ratio ({aspect_ratio:.2f}) is unusual. "
                "Ensure logo maintains proper proportions"
            )
        
        scale_factor = analysis.get("scale_factor", 1.0)
        if scale_factor < 0.1:
            recommendations.append(
                "Logo appears too small. Ensure adequate size for visibility"
            )
        elif scale_factor > 0.8:
            recommendations.append(
                "Logo appears too large relative to image. Consider appropriate sizing"
            )
        
        if not recommendations:
            recommendations.append("Logo geometry meets compliance requirements")
        
        return recommendations 