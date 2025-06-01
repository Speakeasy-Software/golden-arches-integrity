#!/usr/bin/env python3
"""
Script to create GitHub issues from the golden-arches-github-issues.md file.
This script parses the markdown and creates properly formatted GitHub issues.
"""

import re
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitHubIssue:
    """Represents a GitHub issue."""
    title: str
    body: str
    labels: List[str]
    assignees: List[str] = None
    milestone: str = None
    priority: str = "medium"


class IssueParser:
    """Parse issues from markdown format."""
    
    def __init__(self, markdown_file: str):
        self.markdown_file = Path(markdown_file)
        self.issues: List[GitHubIssue] = []
    
    def parse_issues(self) -> List[GitHubIssue]:
        """Parse all issues from the markdown file."""
        content = self.markdown_file.read_text()
        
        # Split by issue sections (looking for ## followed by emoji and title)
        issue_sections = re.split(r'\n## [🎯🖼️🧠🧪🧭📂🔎🔄🚀📊]', content)
        
        for section in issue_sections[1:]:  # Skip the header
            issue = self._parse_single_issue(section)
            if issue:
                self.issues.append(issue)
        
        return self.issues
    
    def _parse_single_issue(self, section: str) -> GitHubIssue:
        """Parse a single issue from a markdown section."""
        lines = section.strip().split('\n')
        if not lines:
            return None
        
        # Extract title (first line)
        title_line = lines[0].strip()
        title = re.sub(r'^[🎯🖼️🧠🧪🧭📂🔎🔄🚀📊]\s*', '', title_line)
        
        # Find the code block with issue details
        in_code_block = False
        issue_content = []
        labels = []
        
        for line in lines[1:]:
            if line.strip() == '```':
                if in_code_block:
                    break
                in_code_block = True
                continue
            
            if in_code_block:
                issue_content.append(line)
                
                # Extract labels
                if line.startswith('**Labels:**'):
                    labels_text = line.replace('**Labels:**', '').strip()
                    labels = [label.strip('` ') for label in labels_text.split(',')]
        
        # Clean up the issue content
        body = '\n'.join(issue_content)
        body = re.sub(r'\*\*Labels:\*\*.*', '', body).strip()
        
        # Determine priority from labels
        priority = "medium"
        for label in labels:
            if "priority:high" in label:
                priority = "high"
            elif "priority:low" in label:
                priority = "low"
        
        return GitHubIssue(
            title=title,
            body=body,
            labels=labels,
            priority=priority
        )
    
    def export_to_json(self, output_file: str):
        """Export issues to JSON format for GitHub CLI or API."""
        issues_data = []
        
        for issue in self.issues:
            issue_dict = {
                "title": issue.title,
                "body": issue.body,
                "labels": issue.labels,
                "priority": issue.priority
            }
            if issue.assignees:
                issue_dict["assignees"] = issue.assignees
            if issue.milestone:
                issue_dict["milestone"] = issue.milestone
            
            issues_data.append(issue_dict)
        
        with open(output_file, 'w') as f:
            json.dump(issues_data, f, indent=2)
        
        print(f"Exported {len(issues_data)} issues to {output_file}")
    
    def generate_github_cli_commands(self, output_file: str):
        """Generate GitHub CLI commands to create issues."""
        commands = []
        
        for issue in self.issues:
            labels_str = ','.join(issue.labels) if issue.labels else ''
            
            # Escape quotes in title and body
            title = issue.title.replace('"', '\\"')
            body = issue.body.replace('"', '\\"').replace('\n', '\\n')
            
            cmd = f'gh issue create --title "{title}" --body "{body}"'
            if labels_str:
                cmd += f' --label "{labels_str}"'
            
            commands.append(cmd)
        
        with open(output_file, 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('# GitHub CLI commands to create Golden Arches Integrity issues\n\n')
            for cmd in commands:
                f.write(cmd + '\n\n')
        
        print(f"Generated {len(commands)} GitHub CLI commands in {output_file}")


def main():
    """Main function to parse and export issues."""
    # Path to the markdown file
    markdown_file = "/Users/svenmesecke/golden-arches/golden-arches-github-issues.md"
    
    if not Path(markdown_file).exists():
        print(f"Error: {markdown_file} not found")
        return
    
    # Parse issues
    parser = IssueParser(markdown_file)
    issues = parser.parse_issues()
    
    print(f"Parsed {len(issues)} issues from {markdown_file}")
    
    # Create output directory
    output_dir = Path("scripts/github_issues")
    output_dir.mkdir(exist_ok=True)
    
    # Export to different formats
    parser.export_to_json(output_dir / "issues.json")
    parser.generate_github_cli_commands(output_dir / "create_issues.sh")
    
    # Print summary
    print("\n📊 Issues Summary:")
    priority_counts = {}
    label_counts = {}
    
    for issue in issues:
        priority_counts[issue.priority] = priority_counts.get(issue.priority, 0) + 1
        for label in issue.labels:
            label_counts[label] = label_counts.get(label, 0) + 1
    
    print(f"  Priority breakdown: {priority_counts}")
    print(f"  Most common labels: {dict(sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[:5])}")


if __name__ == "__main__":
    main() 