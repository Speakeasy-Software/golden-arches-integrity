#!/bin/bash
# Create Phase 1 Issues for Golden Arches AI Training

echo "📋 Creating Phase 1 Issues (Infrastructure & Data Foundation)..."
echo ""

echo "Creating Phase 1.1: Frontend Integration for Asset Collection..."
gh issue create --title "Phase 1.1: Frontend Integration for Asset Collection" \
--body "### Enhanced Frontend Integration for Comprehensive Asset Collection

**Objective**: Streamline data collection through existing frontend with advanced capabilities

**Upload Interface Enhancement:**
- Support up to 100MB file uploads (individual files, drag-and-drop)
- Zip file upload capability for batch processing
- URL/GitHub repo fetch functionality for remote asset collection
- **Supported File Types**: PNG, JPG, JPEG, WebP, SVG, Adobe Illustrator (.ai), Photoshop (.psd), PDF, DOC, DOCX
- No hard file size limits (reasonable rate limiting if needed)

**Enhanced Metadata Capture:**
- Optional metadata unless required for specific rule training
- Source information, brand guideline versions
- **Partner Usage**: Flag for partner collaboration contexts
- **Special Clear-Space Partner Rules**: Boolean field for partner-specific spacing
- Asset versioning capability

**Advanced Annotation Tools:**
- Bounding box creation and editing
- Explanatory text annotations for system learning
- Confidence score input and tracking
- Multi-expert annotation with dispute resolution

**Smart Asset Categorization:**
- Media type organization (Logo focus, Signage/Packaging planned)
- Usage context (Digital primary, Print and Storefront built-in)
- Advanced search & filtering with Tailwind CSS chips
- Training integration options (retrain with filtered assets, mark as training-ready, real-time triggers)" \
--label "phase-1,frontend,data-collection,priority:high,enhancement"

echo ""
echo "Creating Phase 1.2: Heritage Mark Recognition System..."
gh issue create --title "Phase 1.2: Heritage Mark Recognition System" \
--body "### Heritage Mark Recognition and Flagging System

**Objective**: Identify and flag heritage brand marks without interfering with current Golden Arches processing

**Recognition Requirements:**
- **Comprehensive Coverage**: Recognize all heritage McDonald's logo variations
- **High Precision**: Focus on key identifying elements unique to each heritage mark
- **Individual Traits**: Each heritage mark has distinct characteristics for identification
- **Confidence Target**: Near 100% accuracy using specific visual traits

**Workflow Integration:**
- **Specific Flagging**: Each heritage mark gets unique flag category
- **Workflow Interruption**: Detection stops normal rule processing immediately
- **Expert Review**: Automatic escalation for Heritage Mark validation
- **Enhanced Metadata**: Specific variant ID, confidence, context clues, partner usage

**Training Data Management:**
- **Explicit Separation**: Heritage assets completely separated from Golden Arches training data
- **Future Ready**: Assets flagged for future heritage rule development
- **Expert Corrections**: Allow false positive corrections and return to normal processing
- **Batch Processing**: Periodic retraining based on expert corrections

**Processing Continuation:**
- **Modified Processing**: Continue current rules with \"Heritage Mark Rules May Not Apply\" notation
- **Result Qualification**: All compliance results marked as potentially invalid for heritage marks
- **Future Integration**: Framework prepared for heritage-specific rules

**Note**: This is now a **Phase 1 priority** - recognition and flagging only, separate training later" \
--label "phase-1,heritage,recognition,priority:high,ml-pipeline"

echo ""
echo "Creating Phase 1.3: Quality Assurance Portal Implementation..."
gh issue create --title "Phase 1.3: Quality Assurance Portal Implementation" \
--body "### Comprehensive Expert Validation and Review System

**Expert User Management:**
- **Senior Reviewers**: Sven (training authority), Huan, George (full access)
- **Guest Reviewer**: Limited access for external experts
- **Role-Based Permissions**: Clear access control and responsibility hierarchy

**Review Assignment System:**
- **Workload Management**: Unique titles/identifiers for assignments
- **Individual Assignment**: Capability to assign to specific users or guest account
- **Progress Tracking**: Workload monitoring and assignment distribution

**Interface Layout Options:**
- **Single Asset Mode**: Side-by-side view with annotation tools, sequential loading
- **Full Workload Mode**: Scrollable page with all assigned assets loaded
- **Real-Time Processing**: Immediate annotation saving and training flagging

**Validation Workflows:**
- **Consensus Requirements**: Single senior expert review sufficient for validation
- **Guest Review Approval**: Guest reviews require senior expert approval
- **Decision Authority**: Any senior reviewer can make final decisions

**Extensible Feedback Collection:**
- **Structured Categories**: Rule clarity, edge cases, training gaps, usability, general feedback
- **System Integration**: Real-time training data priority identification
- **Training Data Priorities** (primary focus): Live identification of data gaps and rule struggles
- **Extensible Framework**: Add feedback categories as system evolves" \
--label "phase-1,qa-portal,expert-review,priority:high,frontend"

echo ""
echo "Creating Phase 1.4: Azure ML Pipeline Architecture..."
gh issue create --title "Phase 1.4: Azure ML Pipeline Architecture" \
--body "### Scalable Training Infrastructure for Individual Rule Models

**Pipeline Structure:**
- **Individual Pipelines**: Separate pipelines for each of 14 rules initially
- **Future Unification**: Transparent unified pipeline when system becomes intelligent enough
- **Manual Triggers**: Expert reviewer Sven controls all retraining triggers
- **Granular Data Versioning**: Comprehensive tracking with extensible framework

**Monitoring and Validation:**
- **A/B Testing**: Critical for comparing mock rules vs trained models
- **Performance Tracking**: Model performance per rule monitoring
- **Training Data Analysis**: Identification of data gaps for specific rules
- **Success Criteria**: Manual expert validation of 90% accuracy thresholds
- **Export Approval**: Required before production deployment

**Data Management:**
- **Versioning Strategy**: Asset changes, annotation updates, rule modifications, expert feedback
- **Heritage Separation**: Complete isolation of heritage mark data from main training
- **Batch Correction**: Periodic retraining based on expert corrections

**Infrastructure Requirements:**
- **Azure ML Workspace**: Configured for individual rule training
- **Compute Clusters**: Optimized for accuracy over speed
- **Storage Integration**: Azure Blob Storage for datasets and models
- **Monitoring Systems**: Real-time performance and accuracy tracking" \
--label "phase-1,azure,ml-pipeline,infrastructure,priority:high"

echo ""
echo "✅ Phase 1 Issues created successfully!"
echo ""
echo "📊 Phase 1 Summary:"
echo "- 1.1: Frontend Integration for Asset Collection"
echo "- 1.2: Heritage Mark Recognition System (Updated Priority)"
echo "- 1.3: Quality Assurance Portal Implementation"
echo "- 1.4: Azure ML Pipeline Architecture"
echo ""
echo "🔍 Run 'gh issue list --label phase-1' to see Phase 1 issues." 