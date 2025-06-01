
# Golden Arches Integrity – GitHub Issues

---

## ✅ `golden-arches-integrity` Model Training: Project Setup

```
### Train the `golden-arches-integrity` model on Azure

We need to train a model on Azure to evaluate Golden Arches image compliance with brand rules. Follow Azure best practices for ML Ops.

**Tasks:**
- Set up Azure ML workspace
- Use Azure Storage for datasets
- Set up compute clusters
- Define training pipeline (AutoML or custom)
- Apply responsible AI guardrails

**Labels:** `model-training`, `azure`, `mlops`, `priority:high`
```

---

## 🖼️ Image Collection Web UI with Cursor AI

```
### Build web UI for image collection and organization (Cursor AI)

Cursor should generate a web interface to collect and organize assets (images, logos, usage samples) for training the model.

**Requirements:**
- Upload, tag, and preview images
- Assign rule tags (e.g., "drop shadow", "cropped", "compliant")
- Visual inspection tools
- Export as Azure-compatible dataset

**Labels:** `cursor-ai`, `ui`, `data-prep`, `priority:medium`
```

---

## 🧠 Rule Awareness: Encode Brand Integrity Rules

```
### Encode Golden Arches brand integrity rules into structured definitions

Translate these image rules into structured, enforceable logic for training and inference.

**Examples:**
- No colors other than `#FFBC0D`
- No flipping, rotating, obscuring
- Enforce Clearspace rules
- Identify improper cropping vs. approved assets
- Handle Heritage Brand Marks

**Labels:** `rule-engine`, `compliance`, `priority:high`
```

---

## 🧪 Image Preprocessing Pipeline

```
### Create preprocessing pipeline for image integrity model

Before training, images should be normalized, labeled, and validated for quality and clarity.

**Tasks:**
- Resize/crop
- Normalize color values
- Tag known violations and edge cases
- Remove low-quality samples

**Labels:** `preprocessing`, `pipeline`, `priority:medium`
```

---

## 🧭 Identify Heritage Brand Marks

```
### Train model to detect Heritage Brand Marks

These are outdated or stylized logos that need different evaluation rules. They should not be flagged as incorrect but routed to a heritage check pipeline.

**Tasks:**
- Build classifier for Heritage marks
- Maintain asset database of heritage logos
- Route matches to alternate rule check

**Labels:** `heritage`, `rule-routing`, `priority:low`
```

---

## 📂 Dataset Versioning + Labeling

```
### Implement dataset versioning and labeling

Use a Git-friendly format or Azure ML Datasets to version labeled training data.

**Tasks:**
- Use tagging schema (e.g., `shadow`, `rotation`, `background-noise`)
- Store dataset metadata in Cursor UI
- Enable data refresh and auditability

**Labels:** `data-labeling`, `versioning`, `priority:medium`
```

---

## 🔎 Evaluate Environment Context in Image

```
### Detect environment context around Golden Arches

Ensure the model can assess:
- Background noise
- Text/object occlusion
- Placement relative to other branding elements
- Use of token assets

**Labels:** `context-detection`, `priority:medium`
```

---

## 🔄 Compliance Scoring Engine

```
### Build a scoring engine to evaluate brand integrity

Generate a numeric or categorical score to reflect how well an image follows brand integrity rules.

**Output examples:**
- ✅ Fully compliant
- ⚠️ Minor violation (e.g., poor background)
- ❌ Major violation (e.g., flipped logo)

**Labels:** `scoring`, `evaluation`, `priority:high`
```

---

## 🚀 Deploy Model on Azure for Inference

```
### Deploy model to Azure for real-time or batch inference

Use Azure ML or Azure Functions to expose model via API for compliance checks.

**Tasks:**
- Export trained model
- Containerize (if needed)
- Deploy to Azure endpoint
- Add input validation + rate limiting

**Labels:** `deployment`, `azure`, `api`, `priority:high`
```

---

## 📊 Reporting Dashboard (optional)

```
### Create dashboard for compliance review

Optional: Build a simple dashboard to visualize image scores and common violations.

**Labels:** `dashboard`, `reporting`, `priority:low`
```
