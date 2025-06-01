# Golden Arches Integrity

A production-grade AI model to ensure compliance with McDonald's brand integrity rules for the Golden Arches through automated image analysis.

## 🎯 Project Overview

This project implements an end-to-end MLOps pipeline for detecting brand guideline violations in McDonald's Golden Arches imagery, including:

- **Web Interface** for human-in-the-loop data collection and annotation
- **Azure ML Training Pipeline** with production-grade MLOps practices
- **Rule-based Post-processing** combining AI predictions with explicit brand rules
- **Real-time Deployment** for compliance checking at scale

## 🏗️ Architecture

```
├── frontend/          # React + Tailwind UI for annotation
├── backend/           # FastAPI backend with Azure integration
├── ml_pipeline/       # Azure ML training and deployment
├── rule_engine/       # Brand compliance rule implementations
└── docs/             # Documentation and specifications
```

## 🔧 Azure Resources

- **Subscription ID**: e93bc54d-78c1-418a-85a8-ab40fe3e7547
- **Resource Group**: golden-arches
- **ML Workspace**: Golden-Arches
- **Storage Account**: kparches
- **Region**: West US 2

## 📐 Brand Rules Detected

The model evaluates 14 core McDonald's brand integrity rules:

1. Use of only Gold color (RGB: 255,188,13)
2. Backgrounds must not compromise legibility
3. No drop shadows
4. Not used as letters or numbers
5. No rotation
6. Not obscured
7. Not masked with textures
8. Not warped or stretched
9. No over-modification
10. No flipping
11. Only current logo styles allowed
12. Cropping allowed only via approved assets
13. Token assets must follow separate compliance rules
14. Heritage marks detection and routing

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 20+
- Azure CLI with ML extension
- Azure subscription access

### Setup
```bash
# Clone and setup
git clone <repository-url>
cd golden-arches

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Azure ML setup
az ml workspace show --name "Golden-Arches" --resource-group golden-arches
```

### Development
```bash
# Start backend (from backend/)
uvicorn app.main:app --reload

# Start frontend (from frontend/)
npm run dev
```

## 📊 Model Development

- **Model Type**: Vision Transformer (ViT) / YOLOv8 for multi-class classification
- **Training**: Azure ML Compute with GPU support
- **Evaluation**: mAP, F1 score, precision/recall
- **Deployment**: Azure ML Endpoints with monitoring

## 🔐 Authentication

- Azure AD integration for admin access
- Role-based permissions for annotation workflow
- Secure API endpoints with JWT tokens

## 📈 Monitoring

- Azure Application Insights for performance tracking
- Model drift detection and retraining triggers
- Compliance metrics and reporting dashboard

## 🤝 Contributing

This project follows MLOps best practices with automated testing, CI/CD pipelines, and comprehensive documentation.

## 📄 License

Proprietary - McDonald's Corporation 