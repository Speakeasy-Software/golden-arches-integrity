#!/bin/bash
# Create Phase 2 Issues: Rule-Specific Training Development

echo "📋 Creating Phase 2 Issues: Rule-Specific Training Development..."
echo ""

# Phase 2.1: Color Rules Training
gh issue create \
  --title "2.1 Color Rules Training - RGB Compliance Detection" \
  --body "## Objective
Develop and train models for McDonald's Golden Arches color compliance detection.

## Key Requirements
- **Target RGB**: 255,188,13 (McDonald's Gold)
- **Tolerance System**: Configurable tolerance ranges for pixelization
- **Multi-Region Sampling**: Sample 5+ regions around detected logo (no averaging initially)
- **Digital Focus**: Web and PDF usage contexts
- **Extensible**: Prepare for CMYK (print) and lighting conditions

## Technical Specifications
- **Color Space Analysis**: RGB primary (extensible to CMYK for future print materials)
- **Background Separation**: Logo shape detection for accurate color sampling within boundaries
- **Tolerance Configuration**: Configurable ranges that can be tightened or loosened
- **Multi-Region Detection**: Pick from multiple regions around logo, report individual results
- **Context Awareness**: Different processing for web vs PDF usage

## Detailed Requirements from Expert Input
- Tolerance for pixelization and compression artifacts
- Focus on digital assets (web/PDF) initially
- No averaging of color samples - report individual region results
- Configurable tolerance system for future adjustments
- Background detection to avoid sampling outside logo area

## Acceptance Criteria
- [ ] Accurate RGB detection within configurable tolerance
- [ ] Multi-region color sampling implemented (5+ regions)
- [ ] Configurable tolerance system with modification capability
- [ ] Digital asset optimization (web and PDF contexts)
- [ ] Expert validation interface for color compliance
- [ ] Training pipeline integration with heritage mark separation

## Dependencies
- Heritage Mark detection (1.4) - must not interfere
- Asset upload system (1.1) with file type support
- Expert review interface (1.2) for validation" \
  --label "phase-2,color-rules,training,priority:high"

# Phase 2.2: Geometry Rules Training
gh issue create \
  --title "2.2 Geometry Rules Training - Rotation, Flipping & Warping Detection" \
  --body "## Objective
Develop models to detect geometry violations in Golden Arches logo usage.

## Key Requirements
- **Rotation Detection**: Minimal tolerance, upright horizontal base required
- **Flip Detection**: Both horizontal and vertical flips (hard violations)
- **Warping Detection**: Zero tolerance for intentional warping
- **Photography Exception**: Flag but don't penalize warping in photographs
- **Template Matching**: Create reference logo template from training assets

## Technical Specifications
- **Minimal Tolerance**: Exact alignment preferred, minimal tolerance for pass/fail
- **Upright Requirement**: Golden arches must always be upright horizontally based
- **Hard Violations**: Both horizontal and vertical flips are not allowed
- **Zero Warping Tolerance**: No intentional warping permitted for digital assets
- **Photography Context**: Detect photographs and report warping not judged

## Detailed Requirements from Expert Input
- Minimal tolerance for rotation (configurable for future adjustment)
- Hard violation status for any flipping
- Zero tolerance for warping except in photographs
- Photography detection to exempt from warping rules
- Template creation from multiple training assets
- Keypoint-based comparison system

## Template Creation Strategy
- Generate logo template from multiple high-quality assets
- Use keypoint-based comparison for geometric analysis
- Train system to recognize proper Golden Arches proportions
- Enable comparison against reference template

## Acceptance Criteria
- [ ] Rotation detection with minimal tolerance implementation
- [ ] Horizontal and vertical flip detection (hard violations)
- [ ] Warping detection with zero tolerance for digital assets
- [ ] Photography context awareness and exemption reporting
- [ ] Logo template creation system from training assets
- [ ] Keypoint comparison implementation for geometric analysis

## Dependencies
- Heritage Mark detection (1.4) - separate processing
- Asset categorization system (1.1) for photography detection
- Expert validation workflows (1.2) for template approval" \
  --label "phase-2,geometry-rules,training,priority:high"

# Phase 2.3: Visibility Rules Training
gh issue create \
  --title "2.3 Visibility Rules Training - Size, Contrast & Background Analysis" \
  --body "## Objective
Develop models for logo visibility compliance including size, contrast, and background analysis.

## Key Requirements
- **Logo vs Token**: Distinguish between Golden Arches logo and token usage
- **Size Standards**: Different minimums for logo vs token (15px x 15px for token)
- **Contrast**: WCAG accessibility standards (configurable for McDonald's requirements)
- **Background Analysis**: Busy/cluttered background detection
- **Token Recommendation**: Suggest token usage for difficult backgrounds

## Technical Specifications
- **Logo/Token Classification**: Automatic detection of logo vs token usage
- **Size Measurement**: Different minimum standards (token: 15px x 15px minimum)
- **Contrast Analysis**: WCAG-based with McDonald's specific adjustments
- **Background Complexity**: Analysis of busy/cluttered backgrounds
- **Token Suggestions**: Smart recommendations when visibility compromised

## Detailed Requirements from Expert Input
- Logo vs token distinction critical for different rule applications
- Token (red/green background square) enhances visibility on difficult backgrounds
- Size thresholds differ between logo and token (details to be defined)
- WCAG contrast standards as baseline (open to McDonald's specific requirements)
- Busy backgrounds compete with logo visibility - token solves this
- Web display optimization priority, PDF support included

## Background Analysis Strategy
- Detect busy/cluttered backgrounds that compete with logo visibility
- Identify textured or patterned backgrounds requiring evaluation
- Flag uncertain visibility cases for expert review
- Recommend token usage for challenging background scenarios

## Acceptance Criteria
- [ ] Logo vs token detection and classification
- [ ] Size measurement implementation with different standards
- [ ] WCAG contrast compliance checking (configurable)
- [ ] Background complexity analysis and busy background detection
- [ ] Token recommendation system for visibility challenges
- [ ] Web display optimization with PDF support

## Dependencies
- Heritage Mark detection (1.4) for proper classification
- Asset upload and categorization (1.1) for context awareness
- Expert review interface (1.2) for visibility validation" \
  --label "phase-2,visibility-rules,training,priority:high"

# Phase 2.4: Composition Rules Training
gh issue create \
  --title "2.4 Composition Rules Training - Clear Space & Placement Analysis" \
  --body "## Objective
Develop models for composition compliance including clear space, placement, and contextual usage.

## Key Requirements
- **Clear Space Standards**: Logo vs token specific requirements (to be defined via frontend)
- **Placement Analysis**: Context-aware positioning rules
- **Content Appropriateness**: Brand tone and messaging alignment
- **Partner Logo Detection**: Distinguish competing vs partner logos
- **Template Compliance**: Email signatures, PDF layouts, etc.

## Technical Specifications
- **Clear Space Measurement**: Different standards for logo vs token usage
- **Context-Aware Rules**: Different requirements for PDF vs image assets
- **Content Analysis**: Brand tone and messaging appropriateness detection
- **Logo Classification**: Competing vs partner logo identification
- **Template Matching**: Email signatures, PDF document layouts

## Detailed Requirements from Expert Input
- Clear space standards will be fully defined via frontend interface
- All violations depend on logo vs token usage context
- Context-sensitive rules based on asset type and usage
- Competing logos inappropriate, partner logos may be acceptable
- Inappropriate imagery detection very important to McDonald's
- Template compliance for various document types

## Content Appropriateness Strategy
- Brand tone and messaging alignment analysis
- Inappropriate associate matter or imagery detection
- Context consideration for logo vs token usage appropriateness
- Partner logo vs competing logo classification
- Template compliance checking for standard layouts

## Acceptance Criteria
- [ ] Clear space measurement system (logo vs token specific)
- [ ] Placement rule implementation with context awareness
- [ ] Content appropriateness detection for brand alignment
- [ ] Partner vs competing logo classification system
- [ ] Template compliance checking for document layouts
- [ ] Context-sensitive rule application (PDF vs image)

## Dependencies
- Logo vs token detection (2.3) for proper rule application
- Heritage Mark detection (1.4) for complete classification
- Expert validation system (1.2) for content appropriateness review" \
  --label "phase-2,composition-rules,training,priority:medium"

# Phase 2.5: Effects Rules Training
gh issue create \
  --title "2.5 Effects Rules Training - Drop Shadows, Textures & Logo Integrity" \
  --body "## Objective
Develop models to detect unauthorized effects and maintain 100% logo integrity.

## Key Requirements
- **Drop Shadow Detection**: All types constitute violations
- **Texture Masking**: Zero tolerance (with rare authorized exceptions)
- **Logo Integrity**: 100% integrity standard
- **Authorized Effects**: Basic scaling only, flag others for McDonald's approval
- **Context Awareness**: Different rules for PDF vs image assets

## Technical Specifications
- **Shadow Detection**: All drop shadow types identified as violations
- **Texture Analysis**: Distinguish texture masking vs acceptable background textures
- **Integrity Measurement**: 100% logo integrity scoring system
- **Effect Classification**: Authorized vs unauthorized effect identification
- **Authorization Workflow**: Flag unauthorized effects for McDonald's approval

## Detailed Requirements from Expert Input
- All drop shadows constitute violations (no exceptions)
- Texture masking generally not allowed (rare corner cases exist)
- 100% logo integrity standard except for corner cases requiring authorization
- Basic scaling acceptable, other effects need explicit McDonald's authorization
- Context awareness for PDF vs image file processing
- Authorization flagging for effects that don't meet 100% integrity

## Logo Integrity Strategy
- Maintain 100% logo integrity as primary standard
- Flag any effects that compromise integrity for authorization review
- Distinguish between texture masking and acceptable background textures
- Context-aware processing based on asset type
- Authorization workflow for effects requiring McDonald's approval

## Acceptance Criteria
- [ ] Drop shadow detection (all types flagged as violations)
- [ ] Texture masking detection with rare exception handling
- [ ] Logo integrity scoring system (100% standard)
- [ ] Authorized effect identification (basic scaling acceptable)
- [ ] McDonald's approval flagging system for unauthorized effects
- [ ] Context-aware rule application (PDF vs image assets)

## Dependencies
- Logo detection system (2.2) for integrity measurement
- Expert review workflows (1.2) for authorization decisions
- Asset type classification (1.1) for context-aware processing" \
  --label "phase-2,effects-rules,training,priority:medium"

# Phase 2.6: Integration Rules Training
gh issue create \
  --title "2.6 Integration Rules Training - Multi-Rule Coordination & Conflict Resolution" \
  --body "## Objective
Develop unified system for coordinating multiple rules and resolving conflicts.

## Key Requirements
- **Priority Hierarchy**: Color > Geometry > Placement > Context
- **Token Recommendations**: Smart suggestions when compliance difficult
- **Conflict Resolution**: Expert review flagging for conflicts
- **Brand Integrity Scoring**: Weighted scoring system
- **Threshold-Based Results**: Pass/fail with detailed violation reports

## Technical Specifications
- **Rule Coordination**: Multi-rule processing with priority hierarchy
- **Conflict Resolution Framework**: Expert review integration for disputes
- **Weighted Scoring**: Brand integrity scoring with rule-specific weights
- **Token Logic**: Smart token recommendations for compliance challenges
- **Detailed Reporting**: Comprehensive violation reports with tolerance scores

## Detailed Requirements from Expert Input
- Color compliance always priority (use token when difficult)
- Token usage makes compliance easier in many scenarios
- Flag conflicts for expert review, retrain based on expert decisions
- McDonald's brand guidelines hierarchy as foundation
- Adaptability for guideline changes and performance improvements
- Heavy weighting for critical violations (color, geometry)

## Priority System Strategy
- **Fundamental Rules** (highest weight): Color compliance, geometry compliance
- **Placement Rules** (medium weight): Clear space, positioning
- **Context Rules** (lower weight): Appropriateness, messaging alignment
- **Token Recommendations**: Always consider token usage for difficult scenarios
- **Extensible Weighting**: Ability to adjust weights based on performance

## Scoring and Reporting Strategy
- Threshold-based pass/fail with detailed violation breakdown
- Show tolerance scores for passing rules (e.g., color compliance margin)
- Comprehensive reporting on each rule evaluation
- Token usage recommendations when compliance challenging
- Expert review integration for borderline cases

## Acceptance Criteria
- [ ] Rule priority hierarchy implementation (Color > Geometry > Placement > Context)
- [ ] Token recommendation system for compliance challenges
- [ ] Conflict resolution framework with expert review integration
- [ ] Brand integrity scoring with weighted rule evaluation
- [ ] Threshold-based pass/fail system with detailed reporting
- [ ] Extensible weighting system for rule importance adjustment

## Dependencies
- All individual rule models (2.1-2.5) for coordination
- Expert review system (1.2) for conflict resolution
- Token detection (2.3) for smart recommendations" \
  --label "phase-2,integration-rules,training,priority:high"

echo "✅ Phase 2 Issues created successfully!"
echo ""
echo "📊 Phase 2 Summary:"
echo "- 2.1: Color Rules Training (RGB 255,188,13 with tolerance)"
echo "- 2.2: Geometry Rules Training (Rotation, flipping, warping detection)" 
echo "- 2.3: Visibility Rules Training (Logo vs token, size, contrast)"
echo "- 2.4: Composition Rules Training (Clear space, placement, appropriateness)"
echo "- 2.5: Effects Rules Training (100% logo integrity, authorized effects)"
echo "- 2.6: Integration Rules Training (Multi-rule coordination, token recommendations)"
echo "" 