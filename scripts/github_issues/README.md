# Golden Arches AI Training - GitHub Issues Management

## Overview
This directory contains comprehensive scripts for managing GitHub Issues for the Golden Arches AI Training project. The scripts are organized by training phases and provide complete project tracking with detailed requirements from expert input.

## Script Files

### 1. Setup Scripts
- **`setup_comprehensive_labels.sh`** - Creates all necessary labels for the project
- **`setup_complete_github_system.sh`** - Master script that runs all setup scripts

### 2. Phase-Specific Issue Creation
- **`create_phase1_issues.sh`** - Infrastructure & Data Foundation (4 issues)
- **`create_phase2_issues.sh`** - Rule-Specific Training Development (6 issues)
- **`create_phase3_issues.sh`** - Model Optimization & Unification (3 issues)
- **`create_phase4_issues.sh`** - Production Integration & Validation (3 issues)

### 3. Legacy Scripts (Reference)
- **`create_issues.sh`** - Original issue creation script
- **`setup_github.sh`** - Original setup script
- **`issues.json`** - Original issue definitions
- **`labels.json`** - Original label definitions
- **`milestones.json`** - Milestone definitions

## Quick Start

### Prerequisites
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`
3. Navigate to project root directory

### Complete Setup
```bash
cd scripts/github_issues
chmod +x setup_complete_github_system.sh
./setup_complete_github_system.sh
```

### Individual Phase Setup
```bash
# Phase 1 only
chmod +x create_phase1_issues.sh
./create_phase1_issues.sh

# Phase 2 only
chmod +x create_phase2_issues.sh
./create_phase2_issues.sh

# etc.
```

## Project Structure

### Phase 1: Infrastructure & Data Foundation
1. **Frontend Integration for Asset Collection** - Enhanced upload interface, metadata capture, annotation tools
2. **Heritage Mark Recognition System** - Recognition and flagging without interference
3. **Quality Assurance Portal Implementation** - Expert review interface, validation workflows
4. **Azure ML Pipeline Architecture** - Individual rule pipelines with expert control

### Phase 2: Rule-Specific Training Development
1. **Color Rules Training** - RGB 255,188,13 compliance with tolerance system
2. **Geometry Rules Training** - Rotation, flipping, warping detection with minimal tolerance
3. **Visibility Rules Training** - Logo vs token distinction, size, contrast analysis
4. **Composition Rules Training** - Clear space, placement, content appropriateness
5. **Effects Rules Training** - 100% logo integrity, authorized effects only
6. **Integration Rules Training** - Multi-rule coordination with token recommendations

### Phase 3: Model Optimization & Unification
1. **Cross-Rule Feature Sharing** - Shared feature optimization without accuracy sacrifice
2. **Unified Model Architecture** - Single model with 14 output heads
3. **Performance Harmonization** - 90%+ accuracy across all rules

### Phase 4: Production Integration & Validation
1. **Production Deployment Strategy** - Gradual rollout with expert control and A/B testing
2. **Continuous Learning Integration** - Real-world feedback with expert oversight
3. **Performance Monitoring & Validation** - Success criteria tracking and validation

## Key Features from Expert Input

### Heritage Mark Integration (Phase 1 Priority)
- Recognition of all heritage McDonald's logo variations
- High precision identification with unique traits
- Workflow interruption and expert review flagging
- Complete separation from Golden Arches training data

### Expert Control System
- **Senior Reviewers**: Sven (training authority), Huan, George
- **Guest Reviewer**: Limited access for external experts
- **Manual Triggers**: Sven controls all retraining decisions
- **Expert Approval**: Required for all production deployments

### Detailed Rule Requirements
- **Color**: RGB 255,188,13 with configurable tolerance, multi-region sampling
- **Geometry**: Minimal tolerance rotation, zero warping, photography exceptions
- **Visibility**: Logo vs token distinction, WCAG contrast, token recommendations
- **Composition**: Context-aware rules, partner vs competing logo detection
- **Effects**: 100% logo integrity, McDonald's authorization for exceptions
- **Integration**: Priority hierarchy (Color > Geometry > Placement > Context)

## Labels Used

### Priority Labels
- `priority:critical` - Must be completed immediately
- `priority:high` - High importance
- `priority:medium` - Medium importance
- `priority:low` - Low importance

### Phase Labels
- `phase-1` - Infrastructure & Data Foundation
- `phase-2` - Rule-Specific Training Development
- `phase-3` - Model Optimization & Unification
- `phase-4` - Production Integration & Validation

### Component Labels
- `frontend` - Frontend development
- `backend` - Backend development
- `azure-ml` - Azure ML pipeline
- `training` - Model training
- `qa-portal` - Quality assurance portal
- `heritage` - Heritage mark detection

### Rule-Specific Labels
- `color-rules` - Color compliance (RGB 255,188,13)
- `geometry-rules` - Geometry compliance (rotation, flipping, warping)
- `visibility-rules` - Visibility compliance (size, contrast, backgrounds)
- `composition-rules` - Composition compliance (clear space, placement)
- `effects-rules` - Effects compliance (100% logo integrity)
- `integration-rules` - Multi-rule integration and coordination

## Success Criteria

### Overall Project Success (in priority order)
1. All 14 McDonald's brand rules consistently performing at 90% accuracy in production
2. Expert validation confirming real-world performance meets expectations
3. System handling target load of 10,000 daily analysis reliably

### Phase Completion Criteria
Each phase has specific acceptance criteria defined in the individual issues. All criteria must be met before proceeding to the next phase.

### Quality Standards
- **Accuracy Priority**: Accuracy always paramount over inference speed
- **Expert Validation**: All major decisions require expert approval
- **No Sacrifice Policy**: No accuracy sacrifice for optimization
- **Heritage Separation**: Complete isolation of heritage mark training data

## Useful Commands

### View Issues
```bash
# All open issues
gh issue list

# Phase-specific issues
gh issue list --label phase-1
gh issue list --label phase-2

# Priority-specific issues
gh issue list --label priority:high
gh issue list --label priority:critical

# Rule-specific issues
gh issue list --label color-rules
gh issue list --label geometry-rules
```

### Manage Issues
```bash
# Assign issue
gh issue edit <issue-number> --add-assignee username

# Add labels
gh issue edit <issue-number> --add-label "additional-label"

# Close issue
gh issue close <issue-number>
```

### View Labels
```bash
# All labels
gh label list

# Specific label pattern
gh label list | grep phase
gh label list | grep priority
```

## Expert Input Integration

### Key Requirements Captured
- **Upload Interface**: 100MB support, zip files, URL fetch, multiple file types
- **Metadata**: Optional unless required, partner usage, versioning
- **Annotation**: Bounding boxes, explanations, confidence scores
- **Heritage Marks**: Phase 1 priority, recognition and flagging only
- **Expert Control**: Sven primary authority, manual triggers, approval required

### Technical Specifications
- **Color Tolerance**: Configurable for pixelization, multi-region sampling
- **Geometry Standards**: Minimal tolerance, zero warping, photography exceptions
- **Token System**: Logo vs token distinction, smart recommendations
- **Integration Priority**: Color > Geometry > Placement > Context

## Notes
- No specific timelines included in issues (to be determined based on progress)
- All scripts designed to be extensible and modifiable
- Expert approval required for all major decisions and deployments
- Focus on accuracy over speed in initial implementation
- Heritage mark recognition as Phase 1 priority without interference
- Complete separation of heritage training data from current Golden Arches training 