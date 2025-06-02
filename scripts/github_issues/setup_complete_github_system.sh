#!/bin/bash
# Master script to setup complete GitHub Issues system for Golden Arches training

echo "🎯 Setting up complete GitHub Issues system for Golden Arches AI Training..."
echo ""

# Check if GitHub CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI is not installed. Please install it first:"
    echo "   https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI. Please run:"
    echo "   gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

echo "📋 Step 1: Setting up comprehensive labels..."
if [ -f "./setup_comprehensive_labels.sh" ]; then
    chmod +x ./setup_comprehensive_labels.sh
    ./setup_comprehensive_labels.sh
else
    echo "❌ setup_comprehensive_labels.sh not found in current directory"
    exit 1
fi

echo ""
echo "📋 Step 2: Creating Phase 1 Issues (Infrastructure & Data Foundation)..."
if [ -f "./create_phase1_issues.sh" ]; then
    chmod +x ./create_phase1_issues.sh
    ./create_phase1_issues.sh
else
    echo "❌ create_phase1_issues.sh not found in current directory"
    exit 1
fi

echo ""
echo "📋 Step 3: Creating Phase 2 Issues (Rule-Specific Training Development)..."
if [ -f "./create_phase2_issues.sh" ]; then
    chmod +x ./create_phase2_issues.sh
    ./create_phase2_issues.sh
else
    echo "❌ create_phase2_issues.sh not found in current directory"
    exit 1
fi

echo ""
echo "📋 Step 4: Creating Phase 3 Issues (Model Optimization & Unification)..."
if [ -f "./create_phase3_issues.sh" ]; then
    chmod +x ./create_phase3_issues.sh
    ./create_phase3_issues.sh
else
    echo "❌ create_phase3_issues.sh not found in current directory"
    exit 1
fi

echo ""
echo "📋 Step 5: Creating Phase 4 Issues (Production Integration & Validation)..."
if [ -f "./create_phase4_issues.sh" ]; then
    chmod +x ./create_phase4_issues.sh
    ./create_phase4_issues.sh
else
    echo "❌ create_phase4_issues.sh not found in current directory"
    exit 1
fi

echo ""
echo "📊 Step 6: Checking current status..."
echo ""
echo "📋 Current Issues Summary:"
gh issue list --state open --limit 20
echo ""

echo "🏷️ Current Labels Summary:"
gh label list | grep -E "(phase-|color-rules|geometry-rules|heritage|qa-portal)" | head -10
echo ""

echo "✅ Complete GitHub Issues system setup finished!"
echo ""
echo "📊 Summary of Created Issues:"
echo "- Phase 1: 4 issues (Infrastructure & Data Foundation)"
echo "- Phase 2: 6 issues (Rule-Specific Training Development)"
echo "- Phase 3: 3 issues (Model Optimization & Unification)"
echo "- Phase 4: 3 issues (Production Integration & Validation)"
echo "- Total: 16 comprehensive issues"
echo ""
echo "🔍 Next steps:"
echo "1. Review created issues: gh issue list"
echo "2. Assign issues to team members as needed"
echo "3. Create project boards for phase tracking"
echo "4. Set up milestone tracking for each phase"
echo "5. Begin Phase 1 implementation"
echo ""
echo "📖 Useful commands:"
echo "- View all issues: gh issue list"
echo "- View Phase 1 issues: gh issue list --label phase-1"
echo "- View high priority issues: gh issue list --label priority:high"
echo "- View all labels: gh label list"
echo ""
echo "🎉 Golden Arches AI Training GitHub Issues system is ready!" 