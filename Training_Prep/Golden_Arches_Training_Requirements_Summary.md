# Golden Arches AI Training Requirements Summary

## Executive Summary
This document captures the comprehensive training requirements for the Golden Arches Integrity AI system, developed through detailed expert consultation sessions. The system will replace mock implementations with real Azure ML models for 14 McDonald's brand compliance rules.

## Core Training Principles

### 1. Accuracy Priority
- **Primary Goal**: Accuracy always paramount over inference speed
- **No Sacrifice Policy**: No accuracy reduction for optimization
- **Quality First**: No hard deadlines, focus on quality and completeness
- **Expert Validation**: All major decisions require expert approval

### 2. Expert Control Framework
- **Training Authority**: Sven (primary control)
- **Senior Reviewers**: Huan, George (full access and permissions)
- **Guest Reviewer**: Limited access for external experts
- **Manual Triggers**: Expert reviewer Sven controls all retraining triggers
- **Deployment Control**: Sven controls all production deployment decisions

### 3. Heritage Mark Separation
- **Complete Isolation**: Heritage training data completely separated from Golden Arches
- **Priority Recognition**: Phase 1 priority for heritage mark identification
- **Workflow Interruption**: Heritage detection stops normal processing
- **Expert Review**: Automatic escalation for heritage mark validation

## Detailed Training Requirements by Phase

### Phase 1: Infrastructure & Data Foundation

#### 1.1 Frontend Integration for Asset Collection
**Upload Interface Requirements:**
- **File Size**: Support up to 100MB files
- **Interaction**: Drag-and-drop functionality
- **Bulk Upload**: ZIP file support
- **External Sources**: URL/GitHub repository fetch capability
- **File Types**: PNG, JPG, JPEG, WebP, SVG, Adobe Illustrator (.ai), PSD, PDF, DOC, DOCX

**Metadata Capture:**
- **Optional Unless Required**: Metadata capture only when needed for training
- **Partner Usage Flags**: Track partner vs internal usage
- **Versioning**: Asset version tracking and management
- **Source Tracking**: Origin and context information

**Annotation Tools:**
- **Bounding Boxes**: Precise region marking
- **Explanatory Text**: Detailed annotations
- **Confidence Scores**: Expert confidence levels
- **Multi-Expert Dispute Resolution**: Consensus tracking

**Asset Categorization:**
- **Media Type Focus**: Logo-focused categorization
- **Usage Context**: Digital primary, extensible to print
- **Search and Filtering**: Tailwind chips interface
- **Training Integration**: Retrain with filtered assets, batch queuing, real-time triggers

#### 1.2 Quality Assurance Portal
**Expert User Management:**
- **Sven**: Training authority with full control
- **Huan, George**: Senior reviewers with full access
- **Guest Reviewer**: Limited access for external experts
- **Role-Based Permissions**: Granular access control

**Review Assignment System:**
- **Unique Workload Titles**: Distinctive identifiers for each assignment
- **Individual Assignment**: Capability to assign to specific users
- **Workload Tracking**: Progress monitoring and distribution

**Interface Options:**
- **Single Asset Mode**: Side-by-side asset view with annotation tools
- **Full Workload Mode**: Scrollable page with all assigned assets
- **Real-Time Saving**: Automatic annotation saving
- **Immediate Processing**: Upload and processing upon review completion

**Validation Workflows:**
- **Single Senior Expert**: Sufficient for validation
- **Guest Reviews**: Require senior expert approval
- **Escalation Process**: Any senior reviewer can make final decisions

**Extensible Feedback System:**
- **Rule Clarity**: Issues and ambiguity identification
- **Edge Cases**: Discovery and documentation
- **Training Gaps**: Data gap identification and suggestions
- **Usability**: Interface and workflow improvements
- **General Feedback**: Uncategorized issues

#### 1.3 Azure ML Pipeline Architecture
**Pipeline Structure:**
- **Individual Pipelines**: Separate pipelines for each of 14 rules initially
- **Manual Triggers**: Expert reviewer Sven controls all retraining
- **Granular Data Versioning**: Comprehensive tracking with extensible framework
- **A/B Testing**: Critical for comparing mock vs trained models

**Data Management:**
- **Heritage Separation**: Complete isolation of heritage mark data
- **Versioning Strategy**: Asset changes, annotation updates, rule modifications
- **Batch Correction**: Periodic retraining based on expert corrections

#### 1.4 Heritage Mark Recognition System
**Recognition Requirements:**
- **Comprehensive Coverage**: All heritage McDonald's logo variations
- **High Precision**: Focus on unique identifying elements
- **Individual Traits**: Distinct characteristics for each heritage mark
- **Near 100% Accuracy**: Using specific visual traits

**Workflow Integration:**
- **Specific Flagging**: Unique flag category for each heritage mark
- **Workflow Interruption**: Detection stops normal rule processing
- **Expert Review**: Automatic escalation for validation
- **Enhanced Metadata**: Variant ID, confidence, context clues, partner usage

### Phase 2: Rule-Specific Training Development

#### 2.1 Color Rules Training
**Target Specifications:**
- **RGB Target**: 255,188,13 (McDonald's Gold)
- **Tolerance**: Configurable tolerance bands
- **Multi-Region Sampling**: 5+ regions, no averaging initially
- **Digital Focus**: Web/PDF primary, extensible to CMYK for print
- **Background Separation**: Accurate color sampling

#### 2.2 Geometry Rules Training
**Rotation Detection:**
- **Minimal Tolerance**: Upright horizontal base required
- **Hard Violations**: Flip detection (horizontal/vertical)
- **Zero Warping**: Except in photographs (metadata-based detection)
- **Template Creation**: Multiple training assets using keypoint comparison

#### 2.3 Visibility Rules Training
**Logo vs Token Distinction:**
- **Token Minimum**: 15px x 15px minimum size
- **WCAG Standards**: Contrast standards (configurable for McDonald's)
- **Background Analysis**: Complexity analysis with token recommendations
- **Web Optimization**: Display optimization with PDF support

#### 2.4 Composition Rules Training
**Clear Space Standards:**
- **Logo vs Token**: Specific standards for each
- **Frontend Definition**: Clear space defined via frontend interface
- **Context-Aware**: Positioning rules (PDF vs image assets)
- **Content Appropriateness**: Detection and partner vs competing logo classification

#### 2.5 Effects Rules Training
**Zero Tolerance Standards:**
- **Drop Shadow**: All types constitute violations
- **Texture Masking**: Zero tolerance with rare authorized exceptions
- **100% Logo Integrity**: Basic scaling only acceptable
- **Authorization Flagging**: McDonald's authorization for unauthorized effects

#### 2.6 Integration Rules Training
**Priority Hierarchy:**
- **Order**: Color > Geometry > Placement > Context
- **Token Recommendations**: For compliance challenges
- **Conflict Resolution**: Expert review flagging
- **Weighted Scoring**: Threshold-based pass/fail with detailed reports

### Phase 3: Model Optimization & Unification

#### 3.1 Cross-Rule Feature Sharing
**No Accuracy Sacrifice Policy:**
- **Individual Excellence**: Priority over shared optimization
- **Natural Overlaps**: Identification without forcing
- **High-Performing Rules**: First priority for optimization

#### 3.2 Unified Model Architecture
**Single Model Design:**
- **14 Output Heads**: One per rule
- **Attention Mechanisms**: Relevant rules per asset type
- **Automatic Detection**: Logo vs token with context-based rule application

#### 3.3 Performance Harmonization
**Consistency Requirements:**
- **90%+ Accuracy**: Across all rules
- **Performance Gap Analysis**: Identification and remediation
- **Expert Validation**: A/B testing and regression testing

### Phase 4: Production Integration & Validation

#### 4.1 Production Deployment Strategy
**Gradual Rollout:**
- **Highest Performing**: Models first
- **A/B Testing**: Visual review with expert control switches
- **Sven Control**: All deployment decisions

#### 4.2 Continuous Learning Integration
**Feedback Collection:**
- **Real-World Performance**: Feedback collection
- **Low Confidence**: Automatic flagging
- **Expert Approval**: Required for all production model updates

#### 4.3 Performance Monitoring & Validation
**Success Criteria (Priority Order):**
1. **90% Accuracy**: Across all 14 rules
2. **Expert Validation**: Real-world performance validation
3. **10,000 Daily Capacity**: Analysis capacity target

**Monitoring Requirements:**
- **Individual Rule Performance**: Tracking per rule
- **Quality Assurance**: Expert oversight
- **Performance Consistency**: Across all rules

## Technical Specifications

### Color Compliance
- **Target RGB**: 255,188,13 with configurable tolerance
- **Multi-Region Sampling**: 5+ regions without averaging
- **Background Separation**: For accurate color sampling

### Geometry Standards
- **Rotation**: Minimal tolerance, upright horizontal base
- **Warping**: Zero tolerance except photography exceptions
- **Template Matching**: Keypoint comparison across multiple assets

### Token System
- **Logo vs Token**: Clear distinction and smart recommendations
- **Size Requirements**: 15px x 15px minimum for tokens
- **Context Awareness**: Appropriate recommendations per situation

### Heritage Integration
- **Phase 1 Priority**: Recognition and flagging system
- **Complete Separation**: From Golden Arches training data
- **Workflow Integration**: Interruption and expert review

## Success Metrics

### Primary Success Criteria
1. **90% Accuracy**: Across all 14 rules (non-negotiable)
2. **Expert Validation**: Real-world performance approval
3. **10,000 Daily Capacity**: Processing capability

### Quality Gates
- **Expert Approval**: Required for all major decisions
- **Performance Consistency**: No rule below 90% accuracy
- **Heritage Recognition**: Near 100% accuracy for heritage marks
- **Production Readiness**: Expert-validated deployment approval

## Implementation Notes

### Extensibility Requirements
- **Rule Addition**: System designed for new rule integration
- **Feedback Categories**: Expandable feedback system
- **Data Versioning**: Comprehensive tracking framework
- **Expert Interface**: Scalable to additional expert users

### Quality Assurance
- **No Hard Deadlines**: Quality over speed
- **Expert Control**: All critical decisions require approval
- **Continuous Improvement**: Based on real-world feedback
- **Heritage Separation**: Maintained throughout all phases 