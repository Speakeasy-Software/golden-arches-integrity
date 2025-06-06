#!/bin/bash
# Setup comprehensive labels for Golden Arches training phases

echo "🏷️ Setting up comprehensive labels for Golden Arches AI Training..."
echo ""

echo "Creating Phase labels..."
gh label create "phase-1" --description "Phase 1: Infrastructure & Data Foundation" --color "0052cc" || echo "Label 'phase-1' already exists"
gh label create "phase-2" --description "Phase 2: Rule-Specific Training Development" --color "1d76db" || echo "Label 'phase-2' already exists"
gh label create "phase-3" --description "Phase 3: Model Optimization & Unification" --color "0e8a16" || echo "Label 'phase-3' already exists"
gh label create "phase-4" --description "Phase 4: Production Integration & Validation" --color "b60205" || echo "Label 'phase-4' already exists"

echo ""
echo "Creating Rule-specific labels..."
gh label create "color-rules" --description "Golden Color RGB compliance training" --color "fbca04" || echo "Label 'color-rules' already exists"
gh label create "geometry-rules" --description "Rotation, flipping, warping detection" --color "d93f0b" || echo "Label 'geometry-rules' already exists"
gh label create "visibility-rules" --description "Background legibility and size requirements" --color "0052cc" || echo "Label 'visibility-rules' already exists"
gh label create "composition-rules" --description "Placement and context appropriateness" --color "5319e7" || echo "Label 'composition-rules' already exists"
gh label create "effects-rules" --description "Drop shadows and texture detection" --color "e99695" || echo "Label 'effects-rules' already exists"
gh label create "integration-rules" --description "Multi-rule compliance and scoring" --color "c2e0c6" || echo "Label 'integration-rules' already exists"

echo ""
echo "Creating Component labels..."
gh label create "heritage" --description "Heritage brand mark recognition" --color "f9d0c4" || gh label edit "heritage" --description "Heritage brand mark recognition" --color "f9d0c4"
gh label create "qa-portal" --description "Quality assurance portal and expert review" --color "c5def5" || echo "Label 'qa-portal' already exists"
gh label create "data-collection" --description "Asset collection and metadata capture" --color "bfd4f2" || echo "Label 'data-collection' already exists"
gh label create "recognition" --description "Pattern and logo recognition systems" --color "d4c5f9" || echo "Label 'recognition' already exists"
gh label create "optimization" --description "Performance and model optimization" --color "c2e0c6" || echo "Label 'optimization' already exists"
gh label create "unified-model" --description "Single model architecture development" --color "0e8a16" || echo "Label 'unified-model' already exists"
gh label create "harmonization" --description "Performance consistency across rules" --color "5319e7" || echo "Label 'harmonization' already exists"
gh label create "continuous-learning" --description "Production learning and adaptation" --color "1d76db" || echo "Label 'continuous-learning' already exists"
gh label create "reliability" --description "System reliability and monitoring" --color "0052cc" || echo "Label 'reliability' already exists"

echo ""
echo "Creating Training and ML labels..."
gh label create "feature-analysis" --description "Cross-rule feature analysis" --color "bfd4f2" || echo "Label 'feature-analysis' already exists"
gh label create "architecture" --description "Model architecture design" --color "d93f0b" || echo "Label 'architecture' already exists"
gh label create "validation" --description "Model and system validation" --color "0e8a16" || echo "Label 'validation' already exists"

echo ""
echo "✅ Comprehensive labels setup complete!"
echo ""
echo "📋 Created labels for:"
echo "- 4 Phase labels (phase-1 through phase-4)"
echo "- 6 Rule-specific labels (color, geometry, visibility, composition, effects, integration)"
echo "- 9 Component labels (heritage, qa-portal, data-collection, etc.)"
echo "- 3 Training/ML labels (feature-analysis, architecture, validation)"
echo ""
echo "🔍 Run 'gh label list' to see all labels." 