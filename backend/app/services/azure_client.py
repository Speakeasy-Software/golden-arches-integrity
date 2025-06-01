import os
import logging
from typing import Optional, List, Dict, Any
from azure.storage.blob import BlobServiceClient
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)

class AzureClient:
    def __init__(self):
        """Initialize Azure clients with proper authentication."""
        try:
            # Use DefaultAzureCredential for authentication
            self.credential = DefaultAzureCredential()
            
            # Initialize blob storage client
            storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if storage_connection_string:
                self.blob_service_client = BlobServiceClient.from_connection_string(
                    storage_connection_string
                )
            else:
                logger.warning("AZURE_STORAGE_CONNECTION_STRING not found")
                self.blob_service_client = None
            
            # Initialize ML client
            subscription_id = os.getenv("AZURE_ML_SUBSCRIPTION_ID")
            resource_group = os.getenv("AZURE_ML_RESOURCE_GROUP")
            workspace_name = os.getenv("AZURE_ML_WORKSPACE_NAME")
            
            if all([subscription_id, resource_group, workspace_name]):
                self.ml_client = MLClient(
                    credential=self.credential,
                    subscription_id=subscription_id,
                    resource_group_name=resource_group,
                    workspace_name=workspace_name
                )
            else:
                logger.warning("Azure ML configuration incomplete")
                self.ml_client = None
                
        except Exception as e:
            logger.error(f"Failed to initialize Azure clients: {e}")
            self.blob_service_client = None
            self.ml_client = None
    
    async def upload_blob(self, container_name: str, blob_name: str, data: bytes) -> str:
        """Upload blob to Azure Storage."""
        if not self.blob_service_client:
            raise AzureError("Blob service client not initialized")
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob_name
            )
            blob_client.upload_blob(data, overwrite=True)
            return blob_client.url
        except Exception as e:
            logger.error(f"Failed to upload blob: {e}")
            raise AzureError(f"Upload failed: {e}")
    
    async def download_blob(self, container_name: str, blob_name: str) -> bytes:
        """Download blob from Azure Storage."""
        if not self.blob_service_client:
            raise AzureError("Blob service client not initialized")
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob_name
            )
            return blob_client.download_blob().readall()
        except Exception as e:
            logger.error(f"Failed to download blob: {e}")
            raise AzureError(f"Download failed: {e}")
    
    async def list_blobs(self, container_name: str, prefix: Optional[str] = None) -> List[str]:
        """List blobs in container."""
        if not self.blob_service_client:
            raise AzureError("Blob service client not initialized")
        
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blobs = container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            logger.error(f"Failed to list blobs: {e}")
            raise AzureError(f"List failed: {e}")
    
    async def submit_ml_job(self, job_config: Dict[str, Any]) -> str:
        """Submit ML job to Azure ML."""
        if not self.ml_client:
            raise AzureError("ML client not initialized")
        
        try:
            # This would be implemented based on specific ML job requirements
            logger.info(f"Submitting ML job with config: {job_config}")
            return "job-id-placeholder"
        except Exception as e:
            logger.error(f"Failed to submit ML job: {e}")
            raise AzureError(f"ML job submission failed: {e}")
    
    async def get_ml_job_status(self, job_id: str) -> str:
        """Get ML job status."""
        if not self.ml_client:
            raise AzureError("ML client not initialized")
        
        try:
            # This would be implemented based on specific ML job requirements
            logger.info(f"Getting status for job: {job_id}")
            return "completed"
        except Exception as e:
            logger.error(f"Failed to get job status: {e}")
            raise AzureError(f"Job status check failed: {e}")

# Global instance
azure_client = AzureClient() 