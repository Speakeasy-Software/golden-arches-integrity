#!/bin/bash
# GitHub CLI commands to set up Golden Arches Integrity project
# Run this script after creating the GitHub repository

echo '🏷️  Setting up GitHub labels...'
gh label create "priority:critical" --color "d73a4a" --description "Critical priority - needs immediate attention" --force
gh label create "priority:high" --color "ff6b6b" --description "High priority - important for current milestone" --force
gh label create "priority:medium" --color "ffa726" --description "Medium priority - normal development" --force
gh label create "priority:low" --color "4fc3f7" --description "Low priority - nice to have" --force
gh label create "component:frontend" --color "61dafb" --description "React frontend application" --force
gh label create "component:backend" --color "68d391" --description "FastAPI backend service" --force
gh label create "component:ml-pipeline" --color "9f7aea" --description "Azure ML training pipeline" --force
gh label create "component:rule-engine" --color "f6ad55" --description "Brand compliance rule engine" --force
gh label create "component:azure" --color "0078d4" --description "Azure infrastructure and services" --force
gh label create "component:database" --color "38b2ac" --description "Database and data storage" --force
gh label create "component:docs" --color "48bb78" --description "Documentation and guides" --force
gh label create "type:bug" --color "d73a4a" --description "Something isn't working" --force
gh label create "type:feature" --color "a2eeef" --description "New feature or enhancement" --force
gh label create "type:improvement" --color "7057ff" --description "Improvement to existing functionality" --force
gh label create "type:refactor" --color "fbca04" --description "Code refactoring" --force
gh label create "type:security" --color "ee0701" --description "Security-related issue" --force
gh label create "type:performance" --color "ff9500" --description "Performance optimization" --force
gh label create "ml:experiment" --color "9f7aea" --description "Machine learning experiment" --force
gh label create "ml:model-training" --color "b794f6" --description "Model training and evaluation" --force
gh label create "ml:data-prep" --color "d6bcfa" --description "Data preparation and preprocessing" --force
gh label create "ml:deployment" --color "805ad5" --description "Model deployment and serving" --force
gh label create "ml:monitoring" --color "553c9a" --description "Model monitoring and drift detection" --force
gh label create "brand:gold-color" --color "ffbc0d" --description "Gold color compliance (RGB: 255,188,13)" --force
gh label create "brand:geometry" --color "ffd700" --description "Logo geometry and positioning" --force
gh label create "brand:heritage" --color "daa520" --description "Heritage brand marks" --force
gh label create "brand:token" --color "b8860b" --description "Token asset compliance" --force
gh label create "brand:background" --color "f4e04d" --description "Background legibility rules" --force
gh label create "status:needs-triage" --color "ededed" --description "Needs initial review and prioritization" --force
gh label create "status:in-progress" --color "0052cc" --description "Currently being worked on" --force
gh label create "status:blocked" --color "b60205" --description "Blocked by external dependency" --force
gh label create "status:ready-for-review" --color "0e8a16" --description "Ready for code review" --force
gh label create "status:testing" --color "1d76db" --description "In testing phase" --force
gh label create "status:deployed" --color "28a745" --description "Deployed to production" --force
gh label create "good-first-issue" --color "7057ff" --description "Good for newcomers" --force
gh label create "help-wanted" --color "008672" --description "Extra attention is needed" --force
gh label create "question" --color "d876e3" --description "Further information is requested" --force
gh label create "duplicate" --color "cfd3d7" --description "This issue or pull request already exists" --force
gh label create "wontfix" --color "ffffff" --description "This will not be worked on" --force
gh label create "azure:ml-workspace" --color "0078d4" --description "Azure ML workspace related" --force
gh label create "azure:blob-storage" --color "0078d4" --description "Azure Blob Storage related" --force
gh label create "azure:compute" --color "0078d4" --description "Azure compute resources" --force
gh label create "azure:deployment" --color "0078d4" --description "Azure deployment and DevOps" --force
gh label create "cursor-ai" --color "ff6b6b" --description "Generated or assisted by Cursor AI" --force

echo '🎯 Setting up project milestones...'
gh api repos/:owner/:repo/milestones -f title="Phase 1: Foundation Setup" -f description="Set up core infrastructure, Azure resources, and basic backend" -f due_on="2024-02-15T00:00:00Z" -f state="open"
gh api repos/:owner/:repo/milestones -f title="Phase 2: Data Collection & UI" -f description="Build web interface for image collection and annotation" -f due_on="2024-03-15T00:00:00Z" -f state="open"
gh api repos/:owner/:repo/milestones -f title="Phase 3: Rule Engine Development" -f description="Implement all 14 McDonald's brand compliance rules" -f due_on="2024-04-15T00:00:00Z" -f state="open"
gh api repos/:owner/:repo/milestones -f title="Phase 4: ML Model Training" -f description="Train and validate the brand compliance AI model" -f due_on="2024-05-15T00:00:00Z" -f state="open"
gh api repos/:owner/:repo/milestones -f title="Phase 5: Production Deployment" -f description="Deploy to production with monitoring and CI/CD" -f due_on="2024-06-15T00:00:00Z" -f state="open"

echo '✅ GitHub project setup complete!'