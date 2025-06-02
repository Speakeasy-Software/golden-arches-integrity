import axios from 'axios';
import { Asset, AssetType, Annotation, AnnotationCreate, ComplianceReport, DashboardStats } from '@/types';

// Get API base URL from environment variables
const getApiBaseUrl = () => {
  // In production, use the environment variable
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // In development, use the proxy configuration
  if (import.meta.env.DEV) {
    return '/api/v1';
  }
  
  // Fallback for production if env var is not set
  return 'https://golden-arches-prod-backend.azurewebsites.net/api/v1';
};

// Create axios instance with base configuration
const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Upload API
export const uploadApi = {
  // Upload single asset (images, documents, design files)
  uploadSingle: async (
    file: File,
    assetType: AssetType,
    description?: string,
    tags?: string[],
    partnerUsage?: boolean,
    sourceUrl?: string,
    version?: string
  ): Promise<{ success: boolean; message: string; asset?: Asset; assets?: Asset[]; total_assets?: number }> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('asset_type', assetType);
    
    if (description) {
      formData.append('description', description);
    }
    
    if (tags && tags.length > 0) {
      formData.append('tags', tags.join(','));
    }
    
    if (partnerUsage !== undefined) {
      formData.append('partner_usage', partnerUsage.toString());
    }
    
    if (sourceUrl) {
      formData.append('source_url', sourceUrl);
    }
    
    if (version) {
      formData.append('version', version);
    }

    const response = await api.post('/upload/single', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Upload multiple images
  uploadBatch: async (
    files: File[],
    assetType: AssetType,
    description?: string
  ): Promise<{
    success: boolean;
    uploaded_assets: Asset[];
    failed_uploads: Array<{ filename: string; error: string }>;
  }> => {
    const formData = new FormData();
    
    files.forEach((file) => {
      formData.append('files', file);
    });
    
    formData.append('asset_type', assetType);
    
    if (description) {
      formData.append('description', description);
    }

    const response = await api.post('/upload/batch', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // List uploaded images
  listImages: async (prefix?: string, limit?: number): Promise<Asset[]> => {
    const params = new URLSearchParams();
    if (prefix) params.append('prefix', prefix);
    if (limit) params.append('limit', limit.toString());

    const response = await api.get(`/upload/list?${params.toString()}`);
    return response.data;
  },

  // Delete image
  deleteImage: async (filename: string): Promise<{ success: boolean; message: string }> => {
    const response = await api.delete(`/upload/${filename}`);
    return response.data;
  },
};

// Analysis API
export const analysisApi = {
  // Analyze single asset
  analyzeSingle: async (assetId: number): Promise<ComplianceReport> => {
    const response = await api.post(`/analysis/single/${assetId}`);
    return response.data;
  },

  // Batch analysis
  analyzeBatch: async (assetIds: number[]): Promise<{
    job_id: string;
    status: string;
    total_assets: number;
    estimated_completion_time?: string;
  }> => {
    const response = await api.post('/analysis/batch', {
      asset_ids: assetIds,
      force_reanalysis: false,
      notify_on_completion: true,
    });
    return response.data;
  },

  // Get analysis results
  getResults: async (assetId: number): Promise<ComplianceReport> => {
    const response = await api.get(`/analysis/results/${assetId}`);
    return response.data;
  },

  // Get batch job status
  getBatchStatus: async (jobId: string): Promise<{
    job_id: string;
    status: string;
    progress: number;
    completed_assets: number;
    total_assets: number;
    results?: ComplianceReport[];
  }> => {
    const response = await api.get(`/analysis/batch/${jobId}/status`);
    return response.data;
  },
};

// Annotation API
export const annotationApi = {
  // Create annotation
  create: async (annotation: AnnotationCreate): Promise<Annotation> => {
    const response = await api.post('/annotation/create', annotation);
    return response.data;
  },

  // Get annotations for asset
  getByAsset: async (assetId: number): Promise<Annotation[]> => {
    const response = await api.get(`/annotation/asset/${assetId}`);
    return response.data;
  },

  // Update annotation
  update: async (
    annotationId: number,
    updates: Partial<AnnotationCreate>
  ): Promise<Annotation> => {
    const response = await api.put(`/annotation/${annotationId}`, updates);
    return response.data;
  },

  // Delete annotation
  delete: async (annotationId: number): Promise<{ success: boolean; message: string }> => {
    const response = await api.delete(`/annotation/${annotationId}`);
    return response.data;
  },

  // Get pending annotations
  getPending: async (limit?: number): Promise<{
    pending_assets: Array<{
      id: number;
      filename: string;
      asset_type: string;
      uploaded_at: number;
      priority: string;
    }>;
    total_pending: number;
    estimated_time_per_asset: number;
  }> => {
    const params = limit ? `?limit=${limit}` : '';
    const response = await api.get(`/annotation/pending${params}`);
    return response.data;
  },

  // Bulk approve assets
  bulkApprove: async (assetIds: number[]): Promise<{
    success: boolean;
    approved_count: number;
    failed_count: number;
    total_requested: number;
  }> => {
    const response = await api.post('/annotation/bulk-approve', assetIds);
    return response.data;
  },

  // Get annotation statistics
  getStats: async (): Promise<{
    total_annotations: number;
    annotations_by_rule: Record<string, number>;
    violations_by_severity: Record<string, number>;
    annotators_activity: Array<{
      annotator: string;
      annotations_count: number;
      last_activity: string;
    }>;
  }> => {
    const response = await api.get('/annotation/stats');
    return response.data;
  },

  // Export annotations
  exportAnnotations: async (
    assetId: number,
    format: 'json' | 'csv' | 'coco' = 'json'
  ): Promise<any> => {
    const response = await api.get(`/annotation/export/${assetId}?format=${format}`);
    return response.data;
  },
};

// Health check
export const healthApi = {
  check: async (): Promise<{
    status: string;
    app_name: string;
    version: string;
    timestamp: number;
  }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

// Mock dashboard stats (since not implemented in backend yet)
export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    // This would be a real API call in production
    return {
      total_assets: 1247,
      compliant_assets: 1089,
      pending_review: 158,
      critical_violations: 23,
      compliance_rate: 87.3,
      recent_uploads: 45,
    };
  },
};

export default api; 