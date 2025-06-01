#!/usr/bin/env python3
"""
Script to set up GitHub labels for the Golden Arches Integrity project.
This creates a comprehensive labeling system for the project.
"""

import json
from typing import List, Dict


def create_labels_config() -> List[Dict]:
    """Create the labels configuration for GitHub."""
    
    labels = [
        # Priority Labels
        {"name": "priority:critical", "color": "d73a4a", "description": "Critical priority - needs immediate attention"},
        {"name": "priority:high", "color": "ff6b6b", "description": "High priority - important for current milestone"},
        {"name": "priority:medium", "color": "ffa726", "description": "Medium priority - normal development"},
        {"name": "priority:low", "color": "4fc3f7", "description": "Low priority - nice to have"},
        
        # Component Labels
        {"name": "component:frontend", "color": "61dafb", "description": "React frontend application"},
        {"name": "component:backend", "color": "68d391", "description": "FastAPI backend service"},
        {"name": "component:ml-pipeline", "color": "9f7aea", "description": "Azure ML training pipeline"},
        {"name": "component:rule-engine", "color": "f6ad55", "description": "Brand compliance rule engine"},
        {"name": "component:azure", "color": "0078d4", "description": "Azure infrastructure and services"},
        {"name": "component:database", "color": "38b2ac", "description": "Database and data storage"},
        {"name": "component:docs", "color": "48bb78", "description": "Documentation and guides"},
        
        # Issue Types
        {"name": "type:bug", "color": "d73a4a", "description": "Something isn't working"},
        {"name": "type:feature", "color": "a2eeef", "description": "New feature or enhancement"},
        {"name": "type:improvement", "color": "7057ff", "description": "Improvement to existing functionality"},
        {"name": "type:refactor", "color": "fbca04", "description": "Code refactoring"},
        {"name": "type:security", "color": "ee0701", "description": "Security-related issue"},
        {"name": "type:performance", "color": "ff9500", "description": "Performance optimization"},
        
        # ML/AI Specific Labels
        {"name": "ml:experiment", "color": "9f7aea", "description": "Machine learning experiment"},
        {"name": "ml:model-training", "color": "b794f6", "description": "Model training and evaluation"},
        {"name": "ml:data-prep", "color": "d6bcfa", "description": "Data preparation and preprocessing"},
        {"name": "ml:deployment", "color": "805ad5", "description": "Model deployment and serving"},
        {"name": "ml:monitoring", "color": "553c9a", "description": "Model monitoring and drift detection"},
        
        # McDonald's Brand Rules
        {"name": "brand:gold-color", "color": "ffbc0d", "description": "Gold color compliance (RGB: 255,188,13)"},
        {"name": "brand:geometry", "color": "ffd700", "description": "Logo geometry and positioning"},
        {"name": "brand:heritage", "color": "daa520", "description": "Heritage brand marks"},
        {"name": "brand:token", "color": "b8860b", "description": "Token asset compliance"},
        {"name": "brand:background", "color": "f4e04d", "description": "Background legibility rules"},
        
        # Status Labels
        {"name": "status:needs-triage", "color": "ededed", "description": "Needs initial review and prioritization"},
        {"name": "status:in-progress", "color": "0052cc", "description": "Currently being worked on"},
        {"name": "status:blocked", "color": "b60205", "description": "Blocked by external dependency"},
        {"name": "status:ready-for-review", "color": "0e8a16", "description": "Ready for code review"},
        {"name": "status:testing", "color": "1d76db", "description": "In testing phase"},
        {"name": "status:deployed", "color": "28a745", "description": "Deployed to production"},
        
        # Special Labels
        {"name": "good-first-issue", "color": "7057ff", "description": "Good for newcomers"},
        {"name": "help-wanted", "color": "008672", "description": "Extra attention is needed"},
        {"name": "question", "color": "d876e3", "description": "Further information is requested"},
        {"name": "duplicate", "color": "cfd3d7", "description": "This issue or pull request already exists"},
        {"name": "wontfix", "color": "ffffff", "description": "This will not be worked on"},
        
        # Azure Specific
        {"name": "azure:ml-workspace", "color": "0078d4", "description": "Azure ML workspace related"},
        {"name": "azure:blob-storage", "color": "0078d4", "description": "Azure Blob Storage related"},
        {"name": "azure:compute", "color": "0078d4", "description": "Azure compute resources"},
        {"name": "azure:deployment", "color": "0078d4", "description": "Azure deployment and DevOps"},
        
        # Cursor AI
        {"name": "cursor-ai", "color": "ff6b6b", "description": "Generated or assisted by Cursor AI"},
    ]
    
    return labels


def create_milestones_config() -> List[Dict]:
    """Create milestones configuration for the project."""
    
    milestones = [
        {
            "title": "Phase 1: Foundation Setup",
            "description": "Set up core infrastructure, Azure resources, and basic backend",
            "due_on": "2024-02-15T00:00:00Z",
            "state": "open"
        },
        {
            "title": "Phase 2: Data Collection & UI",
            "description": "Build web interface for image collection and annotation",
            "due_on": "2024-03-15T00:00:00Z",
            "state": "open"
        },
        {
            "title": "Phase 3: Rule Engine Development",
            "description": "Implement all 14 McDonald's brand compliance rules",
            "due_on": "2024-04-15T00:00:00Z",
            "state": "open"
        },
        {
            "title": "Phase 4: ML Model Training",
            "description": "Train and validate the brand compliance AI model",
            "due_on": "2024-05-15T00:00:00Z",
            "state": "open"
        },
        {
            "title": "Phase 5: Production Deployment",
            "description": "Deploy to production with monitoring and CI/CD",
            "due_on": "2024-06-15T00:00:00Z",
            "state": "open"
        }
    ]
    
    return milestones


def generate_github_cli_setup() -> str:
    """Generate GitHub CLI commands to set up labels and milestones."""
    
    labels = create_labels_config()
    milestones = create_milestones_config()
    
    commands = []
    commands.append("#!/bin/bash")
    commands.append("# GitHub CLI commands to set up Golden Arches Integrity project")
    commands.append("# Run this script after creating the GitHub repository")
    commands.append("")
    
    # Add labels
    commands.append("echo '🏷️  Setting up GitHub labels...'")
    for label in labels:
        cmd = f'gh label create "{label["name"]}" --color "{label["color"]}" --description "{label["description"]}" --force'
        commands.append(cmd)
    
    commands.append("")
    commands.append("echo '🎯 Setting up project milestones...'")
    
    # Add milestones
    for milestone in milestones:
        cmd = f'gh api repos/:owner/:repo/milestones -f title="{milestone["title"]}" -f description="{milestone["description"]}" -f due_on="{milestone["due_on"]}" -f state="{milestone["state"]}"'
        commands.append(cmd)
    
    commands.append("")
    commands.append("echo '✅ GitHub project setup complete!'")
    
    return "\n".join(commands)


def main():
    """Main function to generate GitHub setup files."""
    
    # Create labels configuration
    labels = create_labels_config()
    with open("scripts/github_issues/labels.json", "w") as f:
        json.dump(labels, f, indent=2)
    
    # Create milestones configuration
    milestones = create_milestones_config()
    with open("scripts/github_issues/milestones.json", "w") as f:
        json.dump(milestones, f, indent=2)
    
    # Generate setup script
    setup_script = generate_github_cli_setup()
    with open("scripts/github_issues/setup_github.sh", "w") as f:
        f.write(setup_script)
    
    print(f"✅ Created GitHub setup files:")
    print(f"   📁 scripts/github_issues/labels.json ({len(labels)} labels)")
    print(f"   📁 scripts/github_issues/milestones.json ({len(milestones)} milestones)")
    print(f"   📁 scripts/github_issues/setup_github.sh (setup script)")
    
    # Print summary
    print(f"\n📊 Labels Summary:")
    label_categories = {}
    for label in labels:
        category = label["name"].split(":")[0] if ":" in label["name"] else "general"
        label_categories[category] = label_categories.get(category, 0) + 1
    
    for category, count in sorted(label_categories.items()):
        print(f"   {category}: {count} labels")


if __name__ == "__main__":
    main() 