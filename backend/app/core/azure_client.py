"""
Azure client for blob storage and ML workspace operations.
"""
import asyncio
import os
from typing import Optional, BinaryIO
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from loguru import logger

from .config import settings


class MockAzureClient:
    """Mock Azure client for development."""
    
    def __init__(self):
        self._initialized = False
    
    async def initialize(self):
        """Mock initialization."""
        self._initialized = True
        logger.info("Mock Azure client initialized (development mode)")
    
    async def upload_image(self, file_content: BinaryIO, filename: str, container: str = None) -> str:
        """Mock image upload."""
        mock_url = f"https://mock-storage.blob.core.windows.net/images/uploads/{filename}"
        logger.info(f"Mock uploaded image: {mock_url}")
        return mock_url
    
    async def download_image(self, blob_name: str, container: str = None) -> bytes:
        """Mock image download."""
        logger.info(f"Mock downloaded image: {blob_name}")
        return b"mock_image_data"
    
    async def list_images(self, prefix: str = "", container: str = None) -> list[str]:
        """Mock image listing."""
        mock_images = [
            "uploads/sample1.jpg",
            "uploads/sample2.png",
            "uploads/sample3.jpg"
        ]
        logger.info(f"Mock listed {len(mock_images)} images")
        return mock_images
    
    def get_latest_model(self, model_name: str = None) -> Optional[Model]:
        """Mock model retrieval."""
        logger.info(f"Mock retrieved model: {model_name or 'golden-arches-compliance'}")
        return None
    
    async def close(self):
        """Mock close."""
        self._initialized = False
        logger.info("Mock Azure client closed")


class AzureClient:
    """Azure client for storage and ML operations."""
    
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.blob_service_client: Optional[BlobServiceClient] = None
        self.ml_client: Optional[MLClient] = None
        self._initialized = False
        self._skip_ml_client = os.environ.get('SKIP_AZURE_ML_CLIENT', 'false').lower() == 'true'
    
    async def initialize(self):
        """Initialize Azure clients."""
        if self._initialized:
            return
        
        try:
            # Initialize blob storage client
            if settings.azure_storage_connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(
                    settings.azure_storage_connection_string
                )
            else:
                account_url = f"https://{settings.azure_storage_account}.blob.core.windows.net"
                self.blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=self.credential
                )
            
            # Initialize ML client (synchronous) - skip in App Service to avoid chmod permission errors
            if not self._skip_ml_client:
                try:
                    self.ml_client = MLClient(
                        credential=self.credential,
                        subscription_id=settings.azure_subscription_id,
                        resource_group_name=settings.azure_resource_group,
                        workspace_name=settings.azure_ml_workspace
                    )
                    logger.info("Azure ML client initialized successfully")
                except Exception as e:
                    logger.warning(f"Failed to initialize Azure ML client: {e}")
                    self.ml_client = None
            else:
                logger.info("Skipping Azure ML client initialization (SKIP_AZURE_ML_CLIENT=true)")
                self.ml_client = None
            
            # Create containers if they don't exist
            await self._ensure_containers()
            
            self._initialized = True
            logger.info("Azure clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure clients: {e}")
            raise
    
    async def _ensure_containers(self):
        """Ensure required blob containers exist."""
        containers = [
            settings.azure_blob_container_images,
            settings.azure_blob_container_annotations,
            settings.azure_blob_container_models
        ]
        
        for container_name in containers:
            try:
                container_client = self.blob_service_client.get_container_client(container_name)
                await container_client.create_container()
                logger.info(f"Created container: {container_name}")
            except Exception as e:
                if "ContainerAlreadyExists" in str(e):
                    logger.debug(f"Container already exists: {container_name}")
                else:
                    logger.warning(f"Failed to create container {container_name}: {e}")
    
    async def upload_image(self, file_content: BinaryIO, filename: str, container: str = None) -> str:
        """Upload an image to blob storage."""
        if not self._initialized:
            await self.initialize()
        
        container_name = container or settings.azure_blob_container_images
        blob_name = f"uploads/{filename}"
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            
            await blob_client.upload_blob(file_content, overwrite=True)
            
            blob_url = f"https://{settings.azure_storage_account}.blob.core.windows.net/{container_name}/{blob_name}"
            logger.info(f"Uploaded image: {blob_url}")
            return blob_url
            
        except Exception as e:
            logger.error(f"Failed to upload image {filename}: {e}")
            raise
    
    async def download_image(self, blob_name: str, container: str = None) -> bytes:
        """Download an image from blob storage."""
        if not self._initialized:
            await self.initialize()
        
        container_name = container or settings.azure_blob_container_images
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            
            download_stream = await blob_client.download_blob()
            return await download_stream.readall()
            
        except Exception as e:
            logger.error(f"Failed to download image {blob_name}: {e}")
            raise
    
    async def list_images(self, prefix: str = "", container: str = None) -> list[str]:
        """List images in blob storage."""
        if not self._initialized:
            await self.initialize()
        
        container_name = container or settings.azure_blob_container_images
        
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_list = []
            
            async for blob in container_client.list_blobs(name_starts_with=prefix):
                blob_list.append(blob.name)
            
            return blob_list
            
        except Exception as e:
            logger.error(f"Failed to list images: {e}")
            raise
    
    def get_latest_model(self, model_name: str = None) -> Optional[Model]:
        """Get the latest version of a model from Azure ML."""
        if not self.ml_client:
            logger.warning("Azure ML client not available - returning None for model")
            return None
        
        model_name = model_name or settings.model_name
        
        try:
            latest_model = self.ml_client.models.get(
                name=model_name,
                version=settings.model_version
            )
            logger.info(f"Retrieved model: {model_name} version {latest_model.version}")
            return latest_model
            
        except Exception as e:
            logger.warning(f"Failed to get model {model_name}: {e}")
            return None
    
    async def close(self):
        """Close Azure clients."""
        if self.blob_service_client:
            await self.blob_service_client.close()
        if self.credential:
            await self.credential.close()
        
        self._initialized = False
        logger.info("Azure clients closed")


# Global Azure client instance - use mock in development
if os.getenv("AZURE_MOCK_MODE", "false").lower() == "true":
    azure_client = MockAzureClient()
    logger.info("Using mock Azure client for development")
else:
    azure_client = AzureClient()
    logger.info("Using real Azure client for production") 