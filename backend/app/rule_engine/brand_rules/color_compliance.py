"""
Color compliance checker for McDonald's Golden Arches.
"""
import numpy as np
from typing import List, Tuple, Optional
from PIL import Image
import cv2
from loguru import logger

from ...core.config import settings


class ColorComplianceChecker:
    """Checker for McDonald's golden arches color compliance."""
    
    def __init__(self):
        self.golden_arches_rgb = settings.golden_arches_rgb
        self.color_tolerance = settings.color_tolerance
    
    def check_color_compliance(self, image: np.ndarray) -> dict:
        """Check if image colors comply with McDonald's brand guidelines."""
        
        try:
            # Convert to RGB if needed
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Assume BGR from OpenCV, convert to RGB
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Extract dominant colors
            dominant_colors = self._extract_dominant_colors(image_rgb)
            
            # Check for golden arches color
            golden_match = self._check_golden_color_presence(dominant_colors)
            
            # Calculate color accuracy score
            accuracy_score = self._calculate_color_accuracy(image_rgb)
            
            # Find non-compliant regions
            non_compliant_regions = self._find_non_compliant_regions(image_rgb)
            
            return {
                "dominant_colors": dominant_colors,
                "golden_arches_color_match": golden_match,
                "color_accuracy_score": accuracy_score,
                "non_compliant_regions": non_compliant_regions,
                "total_pixels": image_rgb.shape[0] * image_rgb.shape[1],
                "compliant_pixel_ratio": self._calculate_compliant_pixel_ratio(image_rgb)
            }
            
        except Exception as e:
            logger.error(f"Color compliance check failed: {e}")
            return {
                "dominant_colors": [],
                "golden_arches_color_match": False,
                "color_accuracy_score": 0.0,
                "non_compliant_regions": [],
                "error": str(e)
            }
    
    def _extract_dominant_colors(self, image: np.ndarray, k: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors using K-means clustering."""
        
        # Reshape image to be a list of pixels
        pixels = image.reshape(-1, 3)
        
        # Use K-means to find dominant colors
        from sklearn.cluster import KMeans
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (dominant colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert to list of tuples
        return [tuple(color) for color in colors]
    
    def _check_golden_color_presence(self, dominant_colors: List[Tuple[int, int, int]]) -> bool:
        """Check if McDonald's golden color is present in dominant colors."""
        
        target_r, target_g, target_b = self.golden_arches_rgb
        
        for r, g, b in dominant_colors:
            # Calculate Euclidean distance in RGB space
            distance = np.sqrt((r - target_r)**2 + (g - target_g)**2 + (b - target_b)**2)
            
            if distance <= self.color_tolerance:
                return True
        
        return False
    
    def _calculate_color_accuracy(self, image: np.ndarray) -> float:
        """Calculate overall color accuracy score."""
        
        target_r, target_g, target_b = self.golden_arches_rgb
        
        # Calculate distance for each pixel
        distances = np.sqrt(
            (image[:, :, 0] - target_r)**2 + 
            (image[:, :, 1] - target_g)**2 + 
            (image[:, :, 2] - target_b)**2
        )
        
        # Calculate percentage of pixels within tolerance
        compliant_pixels = np.sum(distances <= self.color_tolerance)
        total_pixels = image.shape[0] * image.shape[1]
        
        accuracy = compliant_pixels / total_pixels
        return min(1.0, accuracy * 2)  # Scale to make it more meaningful
    
    def _find_non_compliant_regions(self, image: np.ndarray) -> List[dict]:
        """Find regions that don't match the golden color."""
        
        target_r, target_g, target_b = self.golden_arches_rgb
        
        # Calculate distance for each pixel
        distances = np.sqrt(
            (image[:, :, 0] - target_r)**2 + 
            (image[:, :, 1] - target_g)**2 + 
            (image[:, :, 2] - target_b)**2
        )
        
        # Create mask for non-compliant pixels
        non_compliant_mask = distances > self.color_tolerance
        
        # Find contours of non-compliant regions
        contours, _ = cv2.findContours(
            non_compliant_mask.astype(np.uint8), 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        regions = []
        height, width = image.shape[:2]
        
        for contour in contours:
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Only include significant regions
            if w * h > (width * height * 0.01):  # At least 1% of image
                regions.append({
                    "x": x / width,  # Normalized coordinates
                    "y": y / height,
                    "width": w / width,
                    "height": h / height,
                    "area": w * h,
                    "confidence": 1.0 - (np.mean(distances[y:y+h, x:x+w]) / 255.0)
                })
        
        return regions
    
    def _calculate_compliant_pixel_ratio(self, image: np.ndarray) -> float:
        """Calculate ratio of pixels that match the golden color."""
        
        target_r, target_g, target_b = self.golden_arches_rgb
        
        distances = np.sqrt(
            (image[:, :, 0] - target_r)**2 + 
            (image[:, :, 1] - target_g)**2 + 
            (image[:, :, 2] - target_b)**2
        )
        
        compliant_pixels = np.sum(distances <= self.color_tolerance)
        total_pixels = image.shape[0] * image.shape[1]
        
        return compliant_pixels / total_pixels
    
    def validate_hex_color(self, hex_color: str) -> bool:
        """Validate if a hex color matches McDonald's golden color."""
        
        try:
            # Remove # if present
            hex_color = hex_color.lstrip('#')
            
            # Convert hex to RGB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            # Check distance from target color
            target_r, target_g, target_b = self.golden_arches_rgb
            distance = np.sqrt((r - target_r)**2 + (g - target_g)**2 + (b - target_b)**2)
            
            return distance <= self.color_tolerance
            
        except Exception as e:
            logger.error(f"Hex color validation failed: {e}")
            return False
    
    def get_color_recommendations(self, image: np.ndarray) -> List[str]:
        """Get recommendations for color compliance."""
        
        recommendations = []
        
        try:
            analysis = self.check_color_compliance(image)
            
            if not analysis["golden_arches_color_match"]:
                recommendations.append(
                    f"Use McDonald's approved golden color: RGB({self.golden_arches_rgb[0]}, "
                    f"{self.golden_arches_rgb[1]}, {self.golden_arches_rgb[2]}) or #FFBC0D"
                )
            
            if analysis["color_accuracy_score"] < 0.8:
                recommendations.append(
                    "Ensure consistent color application across the entire logo"
                )
            
            if analysis["compliant_pixel_ratio"] < 0.5:
                recommendations.append(
                    "Increase the proportion of golden color in the logo"
                )
            
            if len(analysis["non_compliant_regions"]) > 3:
                recommendations.append(
                    "Reduce color variations - logo should use uniform golden color"
                )
            
        except Exception as e:
            logger.error(f"Failed to generate color recommendations: {e}")
            recommendations.append("Unable to analyze color compliance")
        
        return recommendations 