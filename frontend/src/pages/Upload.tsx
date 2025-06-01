import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation, useQueryClient } from 'react-query';
import { toast } from 'react-hot-toast';
import {
  Upload as UploadIcon,
  X,
  CheckCircle,
  AlertCircle,
  Image as ImageIcon,
  FileText,
  Tag,
} from 'lucide-react';
import { uploadApi } from '@/services/api';
import { AssetType, UploadProgress } from '@/types';
import { validateImageFile, formatFileSize, cn } from '@/utils';

interface UploadFormData {
  assetType: AssetType;
  description: string;
  tags: string[];
}

export default function Upload() {
  const [uploadProgress, setUploadProgress] = useState<UploadProgress[]>([]);
  const [formData, setFormData] = useState<UploadFormData>({
    assetType: AssetType.PHOTOGRAPHY,
    description: '',
    tags: [],
  });
  const [tagInput, setTagInput] = useState('');

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
            formData.tags
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
      const validation = validateImageFile(file);
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
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp'],
    },
    maxFiles: 10,
    maxSize: 10 * 1024 * 1024, // 10MB
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
                        Supports JPEG, PNG, GIF, WebP up to 10MB each
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