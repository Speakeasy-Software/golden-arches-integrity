// Asset Types
export enum AssetType {
  PHOTOGRAPHY = 'photography',
  RENDER = 'render',
  HERITAGE = 'heritage',
  TOKEN = 'token',
}

export enum ComplianceStatus {
  COMPLIANT = 'compliant',
  NON_COMPLIANT = 'non_compliant',
  PENDING_REVIEW = 'pending_review',
  NEEDS_ANNOTATION = 'needs_annotation',
}

export enum BrandRule {
  GOLD_COLOR_ONLY = 'gold_color_only',
  BACKGROUND_LEGIBILITY = 'background_legibility',
  NO_DROP_SHADOWS = 'no_drop_shadows',
  NOT_AS_LETTERS_NUMBERS = 'not_as_letters_numbers',
  NO_ROTATION = 'no_rotation',
  NOT_OBSCURED = 'not_obscured',
  NO_TEXTURE_MASKING = 'no_texture_masking',
  NO_WARPING_STRETCHING = 'no_warping_stretching',
  NO_OVER_MODIFICATION = 'no_over_modification',
  NO_FLIPPING = 'no_flipping',
  CURRENT_LOGO_STYLES = 'current_logo_styles',
  APPROVED_CROPPING = 'approved_cropping',
  TOKEN_COMPLIANCE = 'token_compliance',
  HERITAGE_DETECTION = 'heritage_detection',
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number;
}

export interface RuleViolation {
  rule: BrandRule;
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  description: string;
  bounding_box?: BoundingBox;
  metadata: Record<string, any>;
}

export interface ColorAnalysis {
  dominant_colors: [number, number, number][];
  golden_arches_color_match: boolean;
  color_accuracy_score: number;
  non_compliant_regions: BoundingBox[];
}

export interface GeometryAnalysis {
  rotation_angle: number;
  is_flipped: boolean;
  is_warped: boolean;
  aspect_ratio: number;
  scale_factor: number;
  geometry_score: number;
}

export interface Asset {
  id: number;
  filename: string;
  original_filename?: string;
  asset_type: AssetType;
  description?: string;
  tags: string[];
  blob_url: string;
  file_size: number;
  image_width: number;
  image_height: number;
  compliance_status: ComplianceStatus;
  overall_score: number;
  rule_violations: RuleViolation[];
  color_analysis?: ColorAnalysis;
  geometry_analysis?: GeometryAnalysis;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
  analyzed_at?: string;
  uploaded_by?: string;
  reviewed_by?: string;
}

export interface AssetCreate {
  filename: string;
  asset_type: AssetType;
  description?: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

export interface Annotation {
  id: number;
  asset_id: number;
  rule: BrandRule;
  is_violation: boolean;
  confidence: number;
  notes?: string;
  bounding_box?: BoundingBox;
  created_at: string;
  updated_at: string;
  annotated_by: string;
}

export interface AnnotationCreate {
  asset_id: number;
  rule: BrandRule;
  is_violation: boolean;
  confidence: number;
  notes?: string;
  bounding_box?: BoundingBox;
}

export interface ComplianceReport {
  asset_id: number;
  overall_compliance: ComplianceStatus;
  compliance_score: number;
  violations_count: number;
  critical_violations: number;
  recommendations: string[];
  color_compliance: boolean;
  geometry_compliance: boolean;
  heritage_detected: boolean;
  token_asset_detected: boolean;
  model_version: string;
  analysis_timestamp: string;
  processing_time_ms: number;
}

// UI-specific types
export interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'success' | 'error';
  error?: string;
  asset?: Asset;
}

export interface FilterOptions {
  assetType?: AssetType;
  complianceStatus?: ComplianceStatus;
  tags?: string[];
  dateRange?: {
    start: Date;
    end: Date;
  };
}

export interface DashboardStats {
  total_assets: number;
  compliant_assets: number;
  pending_review: number;
  critical_violations: number;
  compliance_rate: number;
  recent_uploads: number;
}

// Brand rule descriptions for UI
export const BRAND_RULE_DESCRIPTIONS: Record<BrandRule, string> = {
  [BrandRule.GOLD_COLOR_ONLY]: 'Use only McDonald\'s gold color (RGB: 255,188,13)',
  [BrandRule.BACKGROUND_LEGIBILITY]: 'Backgrounds must not compromise legibility',
  [BrandRule.NO_DROP_SHADOWS]: 'No drop shadows allowed',
  [BrandRule.NOT_AS_LETTERS_NUMBERS]: 'Not used as letters or numbers',
  [BrandRule.NO_ROTATION]: 'No rotation allowed',
  [BrandRule.NOT_OBSCURED]: 'Logo must not be obscured',
  [BrandRule.NO_TEXTURE_MASKING]: 'Not masked with textures',
  [BrandRule.NO_WARPING_STRETCHING]: 'No warping or stretching',
  [BrandRule.NO_OVER_MODIFICATION]: 'No over-modification',
  [BrandRule.NO_FLIPPING]: 'No flipping allowed',
  [BrandRule.CURRENT_LOGO_STYLES]: 'Only current logo styles allowed',
  [BrandRule.APPROVED_CROPPING]: 'Cropping allowed only via approved assets',
  [BrandRule.TOKEN_COMPLIANCE]: 'Token assets must follow separate compliance rules',
  [BrandRule.HERITAGE_DETECTION]: 'Heritage marks must be detected and routed appropriately',
}; 