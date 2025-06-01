#!/bin/bash
# GitHub CLI commands to create Golden Arches Integrity issues

gh issue create --title "Image Collection Web UI with Cursor AI" --body "### Build web UI for image collection and organization (Cursor AI)\n\nCursor should generate a web interface to collect and organize assets (images, logos, usage samples) for training the model.\n\n**Requirements:**\n- Upload, tag, and preview images\n- Assign rule tags (e.g., \"drop shadow\", \"cropped\", \"compliant\")\n- Visual inspection tools\n- Export as Azure-compatible dataset" --label "cursor-ai,ui,data-prep,priority:medium"

gh issue create --title "Rule Awareness: Encode Brand Integrity Rules" --body "### Encode Golden Arches brand integrity rules into structured definitions\n\nTranslate these image rules into structured, enforceable logic for training and inference.\n\n**Examples:**\n- No colors other than `#FFBC0D`\n- No flipping, rotating, obscuring\n- Enforce Clearspace rules\n- Identify improper cropping vs. approved assets\n- Handle Heritage Brand Marks" --label "rule-engine,compliance,priority:high"

gh issue create --title "Image Preprocessing Pipeline" --body "### Create preprocessing pipeline for image integrity model\n\nBefore training, images should be normalized, labeled, and validated for quality and clarity.\n\n**Tasks:**\n- Resize/crop\n- Normalize color values\n- Tag known violations and edge cases\n- Remove low-quality samples" --label "preprocessing,pipeline,priority:medium"

gh issue create --title "Identify Heritage Brand Marks" --body "### Train model to detect Heritage Brand Marks\n\nThese are outdated or stylized logos that need different evaluation rules. They should not be flagged as incorrect but routed to a heritage check pipeline.\n\n**Tasks:**\n- Build classifier for Heritage marks\n- Maintain asset database of heritage logos\n- Route matches to alternate rule check" --label "heritage,rule-routing,priority:low"

gh issue create --title "Dataset Versioning + Labeling" --body "### Implement dataset versioning and labeling\n\nUse a Git-friendly format or Azure ML Datasets to version labeled training data.\n\n**Tasks:**\n- Use tagging schema (e.g., `shadow`, `rotation`, `background-noise`)\n- Store dataset metadata in Cursor UI\n- Enable data refresh and auditability" --label "data-labeling,versioning,priority:medium"

gh issue create --title "Evaluate Environment Context in Image" --body "### Detect environment context around Golden Arches\n\nEnsure the model can assess:\n- Background noise\n- Text/object occlusion\n- Placement relative to other branding elements\n- Use of token assets" --label "context-detection,priority:medium"

gh issue create --title "Compliance Scoring Engine" --body "### Build a scoring engine to evaluate brand integrity\n\nGenerate a numeric or categorical score to reflect how well an image follows brand integrity rules.\n\n**Output examples:**\n- ✅ Fully compliant\n- ⚠️ Minor violation (e.g., poor background)\n- ❌ Major violation (e.g., flipped logo)" --label "scoring,evaluation,priority:high"

gh issue create --title "Deploy Model on Azure for Inference" --body "### Deploy model to Azure for real-time or batch inference\n\nUse Azure ML or Azure Functions to expose model via API for compliance checks.\n\n**Tasks:**\n- Export trained model\n- Containerize (if needed)\n- Deploy to Azure endpoint\n- Add input validation + rate limiting" --label "deployment,azure,api,priority:high"

gh issue create --title "Reporting Dashboard (optional)" --body "### Create dashboard for compliance review\n\nOptional: Build a simple dashboard to visualize image scores and common violations." --label "dashboard,reporting,priority:low"

