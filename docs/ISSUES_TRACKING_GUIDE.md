# Golden Arches Integrity - Issues Tracking Guide

## 🎯 Overview

This guide outlines the comprehensive issues tracking system for the Golden Arches Integrity project. Our system is designed to handle the unique requirements of an AI/ML project focused on McDonald's brand compliance.

## 📋 Issue Categories

### 🏷️ Labels System

Our labeling system is organized into several categories:

#### Priority Labels
- `priority:critical` - Needs immediate attention (production issues)
- `priority:high` - Important for current milestone
- `priority:medium` - Normal development priority
- `priority:low` - Nice to have features

#### Component Labels
- `component:frontend` - React UI application
- `component:backend` - FastAPI service
- `component:ml-pipeline` - Azure ML training
- `component:rule-engine` - Brand compliance rules
- `component:azure` - Azure infrastructure
- `component:database` - Data storage
- `component:docs` - Documentation

#### Issue Types
- `type:bug` - Something isn't working
- `type:feature` - New functionality
- `type:improvement` - Enhancement to existing features
- `type:refactor` - Code restructuring
- `type:security` - Security-related issues
- `type:performance` - Performance optimization

#### ML/AI Specific
- `ml:experiment` - Machine learning experiments
- `ml:model-training` - Model training and evaluation
- `ml:data-prep` - Data preparation and preprocessing
- `ml:deployment` - Model deployment and serving
- `ml:monitoring` - Model monitoring and drift detection

#### McDonald's Brand Rules
- `brand:gold-color` - Gold color compliance (RGB: 255,188,13)
- `brand:geometry` - Logo geometry and positioning
- `brand:heritage` - Heritage brand marks
- `brand:token` - Token asset compliance
- `brand:background` - Background legibility rules

#### Status Labels
- `status:needs-triage` - Needs initial review
- `status:in-progress` - Currently being worked on
- `status:blocked` - Blocked by external dependency
- `status:ready-for-review` - Ready for code review
- `status:testing` - In testing phase
- `status:deployed` - Deployed to production

## 🎯 Project Milestones

### Phase 1: Foundation Setup (Feb 2024)
- Azure infrastructure setup
- Backend API development
- Basic rule engine framework
- Testing infrastructure

### Phase 2: Data Collection & UI (Mar 2024)
- React frontend development
- Image upload and annotation system
- User authentication
- Asset management interface

### Phase 3: Rule Engine Development (Apr 2024)
- Implement all 14 McDonald's brand rules
- Color compliance checking
- Geometry analysis
- Heritage mark detection

### Phase 4: ML Model Training (May 2024)
- Dataset preparation and labeling
- Model architecture selection
- Training pipeline on Azure ML
- Model evaluation and validation

### Phase 5: Production Deployment (Jun 2024)
- Production deployment to Azure
- Monitoring and alerting setup
- CI/CD pipeline implementation
- Documentation and training

## 📊 Issue Templates

### Bug Report Template
Use for reporting bugs and issues:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Feature Request Template
Use for new features and enhancements:
- Problem statement
- Proposed solution
- Component impact analysis
- Success criteria
- McDonald's brand rule relevance

### ML Experiment Template
Use for tracking machine learning experiments:
- Experiment objective
- Dataset information
- Model architecture
- Training configuration
- Target metrics
- Results and observations

## 🔄 Workflow Process

### 1. Issue Creation
1. Choose appropriate template
2. Fill in all required fields
3. Add relevant labels
4. Assign to milestone if applicable
5. Set initial priority

### 2. Triage Process
1. Review new issues weekly
2. Validate requirements
3. Assign priority and components
4. Add to appropriate milestone
5. Assign team members

### 3. Development Workflow
1. Move to `status:in-progress` when starting
2. Create feature branch
3. Implement solution
4. Update to `status:ready-for-review`
5. Code review process
6. Move to `status:testing`
7. Deploy and mark `status:deployed`

### 4. ML Experiment Workflow
1. Create ML experiment issue
2. Set up Azure ML experiment
3. Document hypothesis and approach
4. Run experiments and log results
5. Update issue with findings
6. Close with summary and next steps

## 🛠️ Tools and Integration

### GitHub CLI Setup
Run the setup script to configure your repository:
```bash
# Set up labels and milestones
./scripts/github_issues/setup_github.sh

# Create issues from markdown
./scripts/github_issues/create_issues.sh
```

### Azure DevOps Integration
- Link GitHub issues to Azure ML experiments
- Track model performance metrics
- Monitor deployment status

### Automation
- Auto-label issues based on file paths
- Auto-assign based on component expertise
- Auto-close issues when PRs are merged

## 📈 Metrics and Reporting

### Key Metrics to Track
- Issues opened/closed per week
- Time to resolution by priority
- Component-specific issue trends
- ML experiment success rates
- Brand rule compliance coverage

### Weekly Reports
- Sprint progress against milestones
- Blocker identification and resolution
- Team velocity and capacity planning
- Technical debt accumulation

## 🎯 McDonald's Brand Rule Tracking

### Rule-Specific Issue Management
Each of the 14 McDonald's brand rules has dedicated tracking:

1. **Gold Color Only** (`brand:gold-color`)
   - RGB validation: 255,188,13
   - Color tolerance testing
   - Edge case handling

2. **Background Legibility** (`brand:background`)
   - Contrast ratio validation
   - Background noise detection
   - Readability assessment

3. **No Drop Shadows** (`brand:geometry`)
   - Shadow detection algorithms
   - False positive reduction
   - Edge case documentation

4. **Geometry Rules** (`brand:geometry`)
   - Rotation detection
   - Aspect ratio validation
   - Warping identification

5. **Heritage Marks** (`brand:heritage`)
   - Historical logo recognition
   - Classification accuracy
   - Special handling rules

### Compliance Tracking
- Track implementation status for each rule
- Monitor accuracy metrics per rule
- Document edge cases and exceptions
- Plan improvement iterations

## 🚀 Getting Started

### For Developers
1. Review this guide
2. Set up GitHub CLI
3. Run setup scripts
4. Create your first issue
5. Follow the workflow process

### For ML Engineers
1. Use ML experiment templates
2. Link to Azure ML workspace
3. Document all experiments
4. Track model performance
5. Report findings in issues

### For Project Managers
1. Monitor milestone progress
2. Review weekly metrics
3. Identify blockers early
4. Coordinate cross-team dependencies
5. Ensure brand rule coverage

## 📞 Support

For questions about the issues tracking system:
- Check the documentation first
- Ask in GitHub Discussions
- Contact the project maintainers
- Review existing issues for similar problems

---

**Last Updated**: January 2024  
**Version**: 1.0  
**Maintainer**: Golden Arches Integrity Team 