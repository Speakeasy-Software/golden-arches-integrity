import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow } from 'date-fns';
import { ComplianceStatus, AssetType, BrandRule } from '@/types';

// Tailwind CSS class merging utility
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Format file size
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Format date
export function formatDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return format(dateObj, 'MMM dd, yyyy HH:mm');
}

// Format relative time
export function formatRelativeTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return formatDistanceToNow(dateObj, { addSuffix: true });
}

// Get compliance status color
export function getComplianceStatusColor(status: ComplianceStatus): string {
  switch (status) {
    case ComplianceStatus.COMPLIANT:
      return 'text-green-600 bg-green-100';
    case ComplianceStatus.NON_COMPLIANT:
      return 'text-red-600 bg-red-100';
    case ComplianceStatus.PENDING_REVIEW:
      return 'text-yellow-600 bg-yellow-100';
    case ComplianceStatus.NEEDS_ANNOTATION:
      return 'text-blue-600 bg-blue-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

// Get compliance status label
export function getComplianceStatusLabel(status: ComplianceStatus): string {
  switch (status) {
    case ComplianceStatus.COMPLIANT:
      return 'Compliant';
    case ComplianceStatus.NON_COMPLIANT:
      return 'Non-Compliant';
    case ComplianceStatus.PENDING_REVIEW:
      return 'Pending Review';
    case ComplianceStatus.NEEDS_ANNOTATION:
      return 'Needs Annotation';
    default:
      return 'Unknown';
  }
}

// Get asset type color
export function getAssetTypeColor(type: AssetType): string {
  switch (type) {
    case AssetType.PHOTOGRAPHY:
      return 'text-blue-600 bg-blue-100';
    case AssetType.RENDER:
      return 'text-purple-600 bg-purple-100';
    case AssetType.HERITAGE:
      return 'text-amber-600 bg-amber-100';
    case AssetType.TOKEN:
      return 'text-green-600 bg-green-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

// Get asset type label
export function getAssetTypeLabel(type: AssetType): string {
  switch (type) {
    case AssetType.PHOTOGRAPHY:
      return 'Photography';
    case AssetType.RENDER:
      return 'Render';
    case AssetType.HERITAGE:
      return 'Heritage';
    case AssetType.TOKEN:
      return 'Token';
    default:
      return 'Unknown';
  }
}

// Get severity color
export function getSeverityColor(severity: 'low' | 'medium' | 'high' | 'critical'): string {
  switch (severity) {
    case 'low':
      return 'text-green-600 bg-green-100';
    case 'medium':
      return 'text-yellow-600 bg-yellow-100';
    case 'high':
      return 'text-orange-600 bg-orange-100';
    case 'critical':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
}

// Get brand rule category
export function getBrandRuleCategory(rule: BrandRule): string {
  const colorRules = [BrandRule.GOLD_COLOR_ONLY];
  const geometryRules = [
    BrandRule.NO_ROTATION,
    BrandRule.NO_FLIPPING,
    BrandRule.NO_WARPING_STRETCHING,
    BrandRule.APPROVED_CROPPING,
  ];
  const visualRules = [
    BrandRule.BACKGROUND_LEGIBILITY,
    BrandRule.NO_DROP_SHADOWS,
    BrandRule.NOT_OBSCURED,
    BrandRule.NO_TEXTURE_MASKING,
    BrandRule.NO_OVER_MODIFICATION,
  ];
  const usageRules = [
    BrandRule.NOT_AS_LETTERS_NUMBERS,
    BrandRule.CURRENT_LOGO_STYLES,
    BrandRule.TOKEN_COMPLIANCE,
    BrandRule.HERITAGE_DETECTION,
  ];

  if (colorRules.includes(rule)) return 'Color';
  if (geometryRules.includes(rule)) return 'Geometry';
  if (visualRules.includes(rule)) return 'Visual';
  if (usageRules.includes(rule)) return 'Usage';
  return 'Other';
}

// Validate image file
export function validateImageFile(file: File): { valid: boolean; error?: string } {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: 'Invalid file type. Please upload JPEG, PNG, GIF, or WebP images.',
    };
  }

  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File size too large. Maximum size is ${formatFileSize(maxSize)}.`,
    };
  }

  return { valid: true };
}

// Generate random ID (for demo purposes)
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}

// Calculate compliance score color
export function getScoreColor(score: number): string {
  if (score >= 0.9) return 'text-green-600';
  if (score >= 0.7) return 'text-yellow-600';
  if (score >= 0.5) return 'text-orange-600';
  return 'text-red-600';
}

// Format percentage
export function formatPercentage(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

// Debounce function
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Download file
export function downloadFile(data: any, filename: string, type: string = 'application/json') {
  const blob = new Blob([typeof data === 'string' ? data : JSON.stringify(data, null, 2)], {
    type,
  });
  
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Copy to clipboard
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy to clipboard:', error);
    return false;
  }
} 