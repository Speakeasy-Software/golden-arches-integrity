import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

from app.main import app
from app.api.models.asset import AssetType, ComplianceStatus


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "app_name" in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_upload_invalid_file_type(client, sample_image):
    """Test uploading an invalid file type"""
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    data = {"asset_type": AssetType.PHOTOGRAPHY.value}
    response = client.post("/api/v1/upload/single", files=files, data=data)
    
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_analyze_asset(client):
    """Test analyzing an asset for brand compliance"""
    response = client.post("/api/v1/analysis/analyze/123")
    
    assert response.status_code == 200
    result = response.json()
    assert result["asset_id"] == 123
    assert "overall_compliance" in result
    assert "compliance_score" in result


def test_create_annotation(client):
    """Test creating an annotation for an asset"""
    annotation_data = {
        "asset_id": 123,
        "rule": "gold_color_only",
        "is_violation": False,
        "confidence": 0.95,
        "notes": "Color matches standard"
    }
    
    response = client.post("/api/v1/annotation/create", json=annotation_data)
    
    assert response.status_code == 200
    result = response.json()
    assert result["asset_id"] == 123


def test_get_annotations(client):
    """Test retrieving annotations for an asset"""
    response = client.get("/api/v1/annotation/asset/123")
    
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)


def test_get_brand_rules(client):
    """Test getting brand rules"""
    response = client.get("/api/v1/analysis/rules")
    
    assert response.status_code == 200
    result = response.json()
    assert "rules" in result
    assert "total_rules" in result


def test_get_analysis_stats(client):
    """Test getting analysis statistics"""
    response = client.get("/api/v1/analysis/stats")
    
    assert response.status_code == 200
    result = response.json()
    assert "total_assets_analyzed" in result
    assert "compliance_rate" in result


def test_get_annotation_stats(client):
    """Test getting annotation statistics"""
    response = client.get("/api/v1/annotation/stats")
    
    assert response.status_code == 200
    result = response.json()
    assert "total_assets" in result
    assert "annotation_progress" in result 