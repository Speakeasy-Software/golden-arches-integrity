import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation, useQueryClient } from 'react-query';
import { toast } from 'react-hot-toast';
import {
  Upload as UploadIcon,
  X,
  CheckCircle,
  AlertCircle,
  Tag,
} from 'lucide-react';
import { uploadApi } from '@/services/api';
import { AssetType, UploadProgress } from '@/types';
import { validateFile, formatFileSize, cn } from '@/utils';

interface UploadFormData {
  assetType: AssetType;
  description: string;
  tags: string[];
  partnerUsage: boolean;
  sourceUrl?: string;
  version?: string;
}

interface ExternalSource {
  type: 'url' | 'github';
  url: string;
  isProcessing: boolean;
}

export default function Upload() {
  const [uploadProgress, setUploadProgress] = useState<UploadProgress[]>([]);
  const [formData, setFormData] = useState<UploadFormData>({
    assetType: AssetType.PHOTOGRAPHY,
    description: '',
    tags: [],
    partnerUsage: false,
  });
  const [tagInput, setTagInput] = useState('');
  const [externalSource, setExternalSource] = useState<ExternalSource>({
    type: 'url',
    url: '',
    isProcessing: false,
  });
  const [showExternalSource, setShowExternalSource] = useState(false);

  const queryClient = useQueryClient();

  const uploadMutation = useMutation(
    async (files: File[]) => {
      const results = [];
      
      for (const file of files) {
        try {
          const result = await uploadApi.uploadSingle(
            file,
            formData.assetType,
            formData.description,
            formData.tags,
            formData.partnerUsage,
            formData.sourceUrl,
            formData.version
          );
          results.push({ file, result, success: true });
        } catch (error) {
          results.push({ file, error, success: false });
        }
      }
      
      return results;
    },
    {
      onSuccess: (results) => {
        const successCount = results.filter(r => r.success).length;
        const failCount = results.filter(r => !r.success).length;
        
        if (successCount > 0) {
          toast.success(`Successfully uploaded ${successCount} file(s)`);
          queryClient.invalidateQueries('assets');
        }
        
        if (failCount > 0) {
          toast.error(`Failed to upload ${failCount} file(s)`);
        }
        
        // Clear upload progress after a delay
        setTimeout(() => {
          setUploadProgress([]);
        }, 3000);
      },
      onError: () => {
        toast.error('Upload failed');
        setUploadProgress(prev => 
          prev.map(p => ({ ...p, status: 'error' as const, error: 'Upload failed' }))
        );
      },
    }
  );

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const validFiles: File[] = [];
    const invalidFiles: { file: File; error: string }[] = [];

    acceptedFiles.forEach((file) => {
      const validation = validateFile(file);
      if (validation.valid) {
        validFiles.push(file);
      } else {
        invalidFiles.push({ file, error: validation.error || 'Invalid file' });
      }
    });

    // Show errors for invalid files
    invalidFiles.forEach(({ file, error }) => {
      toast.error(`${file.name}: ${error}`);
    });

    if (validFiles.length > 0) {
      // Initialize upload progress
      const progressItems: UploadProgress[] = validFiles.map((file) => ({
        file,
        progress: 0,
        status: 'uploading',
      }));
      
      setUploadProgress(progressItems);
      
      // Start upload
      uploadMutation.mutate(validFiles);
    }
  }, [formData, uploadMutation]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      // Image formats
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp', '.svg'],
      // Design formats
      'application/postscript': ['.ai'],
      'image/vnd.adobe.photoshop': ['.psd'],
      'application/x-photoshop': ['.psd'],
      // Document formats
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      // Archive formats
      'application/zip': ['.zip'],
      'application/x-zip-compressed': ['.zip'],
    },
    maxFiles: 50, // Increased for bulk uploads
    maxSize: 100 * 1024 * 1024, // 100MB (Phase 1 requirement)
  });

  const removeUploadItem = (index: number) => {
    setUploadProgress(prev => prev.filter((_, i) => i !== index));
  };

  const addTag = () => {
    if (tagInput.trim() && !formData.tags.includes(tagInput.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tagInput.trim()],
      }));
      setTagInput('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove),
    }));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addTag();
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Upload Assets</h1>
        <p className="text-gray-600 mt-1">
          Upload McDonald's brand assets for compliance analysis and annotation.
        </p>
      </div>

      {/* Upload Form */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Configuration */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-medium text-gray-900">Upload Settings</h3>
            </div>
            <div className="card-content space-y-4">
              {/* Asset Type */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Asset Type
                </label>
                <select
                  value={formData.assetType}
                  onChange={(e) =>
                    setFormData(prev => ({ ...prev, assetType: e.target.value as AssetType }))
                  }
                  className="input"
                >
                  <option value={AssetType.PHOTOGRAPHY}>Photography</option>
                  <option value={AssetType.RENDER}>Render</option>
                  <option value={AssetType.HERITAGE}>Heritage</option>
                  <option value={AssetType.TOKEN}>Token</option>
                </select>
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) =>
                    setFormData(prev => ({ ...prev, description: e.target.value }))
                  }
                  placeholder="Optional description for these assets..."
                  rows={3}
                  className="input resize-none"
                />
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tags
                </label>
                <div className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    value={tagInput}
                    onChange={(e) => setTagInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Add a tag..."
                    className="input flex-1"
                  />
                  <button
                    onClick={addTag}
                    disabled={!tagInput.trim()}
                    className="btn-secondary px-3"
                  >
                    <Tag className="w-4 h-4" />
                  </button>
                </div>
                {formData.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {formData.tags.map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {tag}
                        <button
                          onClick={() => removeTag(tag)}
                          className="ml-1 text-blue-600 hover:text-blue-800"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Partner Usage Flag */}
              <div>
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.partnerUsage}
                    onChange={(e) =>
                      setFormData(prev => ({ ...prev, partnerUsage: e.target.checked }))
                    }
                    className="rounded border-gray-300 text-mcdonalds-gold focus:ring-mcdonalds-gold"
                  />
                  <span className="text-sm font-medium text-gray-700">
                    Partner Usage Asset
                  </span>
                </label>
                <p className="text-xs text-gray-500 mt-1">
                  Check if this asset is intended for partner use
                </p>
              </div>

              {/* Source URL */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Source URL (Optional)
                </label>
                <input
                  type="url"
                  value={formData.sourceUrl || ''}
                  onChange={(e) =>
                    setFormData(prev => ({ ...prev, sourceUrl: e.target.value }))
                  }
                  placeholder="https://example.com/asset-source"
                  className="input"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Original source or reference URL
                </p>
              </div>

              {/* Version */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Version (Optional)
                </label>
                <input
                  type="text"
                  value={formData.version || ''}
                  onChange={(e) =>
                    setFormData(prev => ({ ...prev, version: e.target.value }))
                  }
                  placeholder="v1.0, 2024-01, etc."
                  className="input"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Asset version or revision identifier
                </p>
              </div>

              {/* External Source Toggle */}
              <div>
                <button
                  onClick={() => setShowExternalSource(!showExternalSource)}
                  className="btn-secondary w-full"
                >
                  {showExternalSource ? 'Hide' : 'Show'} External Source Options
                </button>
              </div>

              {/* External Source Options */}
              {showExternalSource && (
                <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Source Type
                    </label>
                    <select
                      value={externalSource.type}
                      onChange={(e) =>
                        setExternalSource(prev => ({ ...prev, type: e.target.value as 'url' | 'github' }))
                      }
                      className="input"
                    >
                      <option value="url">URL</option>
                      <option value="github">GitHub Repository</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {externalSource.type === 'github' ? 'GitHub Repository URL' : 'Asset URL'}
                    </label>
                    <input
                      type="url"
                      value={externalSource.url}
                      onChange={(e) =>
                        setExternalSource(prev => ({ ...prev, url: e.target.value }))
                      }
                      placeholder={
                        externalSource.type === 'github'
                          ? 'https://github.com/user/repo'
                          : 'https://example.com/asset.jpg'
                      }
                      className="input"
                    />
                  </div>

                  <button
                    onClick={() => {
                      // TODO: Implement external source fetching
                      toast.success('External source fetching will be implemented');
                    }}
                    disabled={!externalSource.url || externalSource.isProcessing}
                    className="btn-primary w-full"
                  >
                    {externalSource.isProcessing ? 'Fetching...' : 'Fetch Assets'}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-content">
              {/* Dropzone */}
              <div
                {...getRootProps()}
                className={cn(
                  'dropzone cursor-pointer',
                  isDragActive && !isDragReject && 'dropzone-active',
                  isDragReject && 'dropzone-reject'
                )}
              >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center">
                  <UploadIcon className="w-12 h-12 text-gray-400 mb-4" />
                  {isDragActive ? (
                    isDragReject ? (
                      <p className="text-red-600 font-medium">
                        Some files are not supported
                      </p>
                    ) : (
                      <p className="text-mcdonalds-gold font-medium">
                        Drop the files here...
                      </p>
                    )
                  ) : (
                    <>
                      <p className="text-lg font-medium text-gray-900 mb-2">
                        Drag & drop files here, or click to select
                      </p>
                      <p className="text-sm text-gray-500 mb-4">
                        Supports JPEG, PNG, GIF, WebP, SVG, AI, PSD, PDF, DOC, DOCX, ZIP up to 100MB each
                      </p>
                      <button className="btn-primary">
                        Choose Files
                      </button>
                    </>
                  )}
                </div>
              </div>

              {/* Upload Progress */}
              {uploadProgress.length > 0 && (
                <div className="mt-6 space-y-3">
                  <h4 className="text-sm font-medium text-gray-900">Upload Progress</h4>
                  {uploadProgress.map((item, index) => (
                    <div
                      key={index}
                      className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex-shrink-0">
                        {item.status === 'uploading' && (
                          <div className="w-5 h-5 spinner"></div>
                        )}
                        {item.status === 'success' && (
                          <CheckCircle className="w-5 h-5 text-green-500" />
                        )}
                        {item.status === 'error' && (
                          <AlertCircle className="w-5 h-5 text-red-500" />
                        )}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {item.file.name}
                          </p>
                          <span className="text-xs text-gray-500">
                            {formatFileSize(item.file.size)}
                          </span>
                        </div>
                        
                        {item.status === 'uploading' && (
                          <div className="progress-bar">
                            <div
                              className="progress-fill"
                              style={{ width: `${item.progress}%` }}
                            ></div>
                          </div>
                        )}
                        
                        {item.status === 'success' && (
                          <p className="text-xs text-green-600">Upload complete</p>
                        )}
                        
                        {item.status === 'error' && (
                          <p className="text-xs text-red-600">{item.error}</p>
                        )}
                      </div>
                      
                      <button
                        onClick={() => removeUploadItem(index)}
                        className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-600"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Guidelines */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Upload Guidelines</h3>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Supported Formats</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• JPEG/JPG files</li>
                <li>• PNG files (with transparency support)</li>
                <li>• GIF files</li>
                <li>• WebP files</li>
                <li>• SVG files</li>
                <li>• AI files</li>
                <li>• PSD files</li>
                <li>• PDF files</li>
                <li>• DOC files</li>
                <li>• DOCX files</li>
                <li>• ZIP files</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Best Practices</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Use high-resolution images (minimum 300px width)</li>
                <li>• Ensure good lighting and contrast</li>
                <li>• Include context around the logo when possible</li>
                <li>• Use descriptive filenames</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 