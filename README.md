# De Novo Mini Binder Design Against PD-L1

This repository documents an end-to-end computational protein design workflow for de novo mini binder generation against human PD-L1.

The project uses a modern protein design pipeline:

```text
Target preparation → RFdiffusion → ProteinMPNN → ESMFold validation → analysis/filtering → interaction/MD analysis
```

The purpose of this repository is not to claim experimentally validated binders. It is a practical workflow project: building direct fluency with computational protein design tools from the perspective of an experimental protein engineer.

---

## Project Goals

This project has three main goals:

1. Build hands-on fluency with modern AI-assisted protein design tools.
2. Understand how parameter choices affect RFdiffusion and downstream design quality.
3. Develop a practical analysis framework for triaging computational designs before experimental testing.

The central scientific question is:

> Given current computational protein design tools, how can an experimental scientist generate, filter, and prioritize plausible mini binder candidates for downstream testing?

---

## Scientific Context

PD-L1 is an immune checkpoint ligand that binds PD-1 and suppresses T-cell activation. The PD-1/PD-L1 interaction is a major therapeutic target in oncology.

In this project, PD-L1 is used as a realistic benchmark target because:

- High-resolution structures are available.
- The PD-1 binding interface is well characterized.
- De novo binder design against PD-L1 has been demonstrated in published work.
- The target provides a meaningful biological and therapeutic context for evaluating computational design workflows.

---

## Important Caveat

The designs in this repository are computational candidates only.

Passing the in silico filters means that a designed sequence is predicted to fold into a structure similar to the intended RFdiffusion backbone. It does **not** mean that the protein binds PD-L1.

Experimental validation would require gene synthesis, protein expression, purification, and binding/biophysical assays such as SPR, BLI, ELISA, SEC, DLS, or thermal stability measurements.

---

## Scientific Workflow Overview

```text
PD-L1 target structure
        ↓
Target preparation
        ↓
RFdiffusion backbone generation
        ↓
Geometry filtering
        ↓
ProteinMPNN sequence design
        ↓
ESMFold structure prediction
        ↓
RMSD / pLDDT validation
        ↓
Candidate ranking
        ↓
Interaction fingerprinting and MD-style exploratory analysis
        ↓
Portfolio-ready figures, structures, and summaries
```

---

## Working Model: What Lives Where

This project uses three working locations, each with a distinct purpose.

```text
GitHub repository
= code, notebooks, scripts, documentation, and small curated portfolio-support outputs

Local Mac project folder
= the working copy of the GitHub repo, plus local ignored data in data/

Google Colab / Google Drive
= temporary compute and staging, not the permanent source of truth
```

### GitHub

GitHub tracks the project brain:

- README and documentation
- notebooks
- reusable scripts
- configuration files, if added
- small curated outputs needed to support portfolio pages
- `data/README.md`, which explains how the local data folder is used

GitHub should **not** be used for bulk generated data, model weights, MD trajectories, large ESMFold/RFdiffusion outputs, or temporary Colab artifacts.

### Local Mac folder

The local working folder is:

```text
~/AIML/pdl1-mini-binder-design/
```

This is the main project workspace. It contains both Git-tracked project files and the local `data/` folder.

The `data/` folder stays inside the project directory for convenience, but its contents are ignored by Git. This allows notebooks and scripts to use simple relative paths while preventing large generated files from being committed.

### Colab and Google Drive

Google Colab is treated as a disposable compute environment.

The intended workflow is:

```text
GitHub/Mac repo → clone or pull in Colab → run compute → save outputs temporarily to Drive → bring selected outputs back to the Mac repo
```

Google Drive is useful as temporary staging for Colab runs. It is not treated as the permanent archive for this project.

---

## Repository Structure

```text
pdl1-mini-binder-design/
├── README.md
├── .gitignore
├── data/
│   └── README.md
├── notebooks/
│   ├── 01_target_preparation.ipynb
│   ├── 02_rfdiffusion_binder_generation_clean.ipynb
│   ├── 03_proteinmpnn_sequence_design.ipynb
│   ├── 04_esmfold_validation_clean.ipynb
│   ├── 05_analysis_and_filtering.ipynb
│   ├── environment.yml
│   └── test_local_env.ipynb
├── scripts/
│   └── portfolio_page3_extract_passed_structures_for_viewer.py
└── portfolio_pages/
```

---

## Directory Notes

### `data/`

The `data/` directory is kept inside the project folder for local use, but its contents are ignored by Git.

Use `data/` for:

- downloaded structures
- local inputs
- RFdiffusion outputs
- ProteinMPNN outputs
- ESMFold predictions
- intermediate CSVs
- logs
- molecular dynamics files
- scratch outputs

Only `data/README.md` is tracked.

This setup keeps paths simple while preventing large project outputs from entering GitHub.

Example local layout:

```text
data/
├── structures/
├── sequences/
├── results/
├── intermediate/
├── cache/
└── scratch/
```

### `notebooks/`

Contains the main computational workflow notebooks.

Current workflow notebooks:

- `01_target_preparation.ipynb`  
  Prepares the PD-L1 target structure and identifies interface/hotspot residues.

- `02_rfdiffusion_binder_generation_clean.ipynb`  
  Generates de novo binder backbones using RFdiffusion.

- `03_proteinmpnn_sequence_design.ipynb`  
  Designs amino acid sequences for generated backbones using ProteinMPNN.

- `04_esmfold_validation_clean.ipynb`  
  Predicts structures from designed sequences and compares them to intended backbones.

- `05_analysis_and_filtering.ipynb`  
  Merges design metrics, ranks candidates, and applies structural filters.

Some workflows are intended for Google Colab, especially GPU-dependent steps. Local notebooks are mainly used for organization, analysis, and portfolio preparation.

### `scripts/`

Contains reusable scripts extracted from notebook workflows.

Example:

- `portfolio_page3_extract_passed_structures_for_viewer.py`  
  Extracts selected structures for downstream visualization in the portfolio project.

### `portfolio_pages/`

Contains curated outputs that support the separate public portfolio website.

This folder may include:

- selected structures
- figures
- summary CSVs
- tables
- viewer-ready files
- exported analysis artifacts

The live HTML pages are maintained separately in the `hg-portfolio` repository. This folder preserves the computational outputs that feed those pages.

---

## Code / Data Operating Workflow

### Editing code and notebooks

Use the local Mac repo as the main editing environment:

```text
~/AIML/pdl1-mini-binder-design/
```

Typical workflow:

```bash
cd ~/AIML/pdl1-mini-binder-design
git status
git add -A
git commit -m "Describe the change"
git push
```

### Running compute in Colab

Colab should pull code from GitHub rather than acting as the source of truth.

Typical Colab pattern:

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
!git clone https://github.com/hghodkephd/pdl1-mini-binder-design.git /content/pdl1-mini-binder-design
%cd /content/pdl1-mini-binder-design
```

Large outputs produced in Colab should be saved temporarily to Google Drive, then copied back to the local Mac project folder if they need to be preserved.

### Bringing outputs back into Git

Only curated, small outputs should be copied into tracked folders such as `portfolio_pages/`.

Do not commit bulk raw outputs unless there is a specific reason.

A useful rule:

```text
Can I explain why this exact file belongs in GitHub?
    yes → keep it tracked
    no  → leave it in data/ or another ignored local output location
```

---

## Current Status

### Completed

- PD-L1 target preparation
- Interface and hotspot residue identification
- RFdiffusion binder backbone generation
- ProteinMPNN sequence design
- ESMFold structure prediction
- Structural validation using pLDDT and RMSD
- Candidate filtering and ranking
- Portfolio-support structure extraction

### In progress

- Parameter sensitivity analysis across RFdiffusion conditions
- Interaction fingerprinting of selected designs
- MD-style exploratory analysis of structural stability and contact persistence
- Portfolio pages explaining the workflow at an accessible technical level

### Planned

- Programmatic extraction of interaction pairs across selected systems
- Contact persistence / rotamer residence analysis
- Cleaner separation of reusable Python utilities from notebooks
- Expanded documentation of design decisions, failure modes, and practical lessons

---

## Key Analysis Concepts

### Structural validation

Designed sequences are evaluated by predicting their structures from sequence alone and comparing those predictions to the intended design backbones.

Primary filters:

- Mean pLDDT > 80
- Cα RMSD to designed backbone < 2.0 Å

Passing these filters indicates fold recapitulation, not target binding.

### ProteinMPNN entropy analysis

ProteinMPNN sequence sampling can identify positions where the model is highly confident versus positions where multiple amino acids appear tolerated.

This can inform experimental library design:

- low-entropy positions → fix
- high-entropy positions → diversify

The goal is to compress library size while enriching for sequences that are more likely to fold and remain compatible with the designed scaffold.

### Parameter sensitivity

The project also explores how RFdiffusion settings affect output quality. The practical goal is to understand how to tune design parameters to get more useful candidates from limited compute.

### Interaction fingerprinting and MD-style analysis

Selected designs are being examined for interaction patterns, side-chain contacts, aromatic stacking, contact persistence, and short-timescale structural behavior.

These analyses are exploratory and are intended to illustrate how computationally selected candidates can be further triaged before experimental testing.

---

## Tools Used

- RFdiffusion — de novo backbone generation
- ProteinMPNN — inverse folding / sequence design
- ESMFold — sequence-based structure prediction
- BioPython — structure parsing and analysis
- PyMOL — structure visualization
- OpenMM — molecular simulation exploration
- Python / Jupyter / Google Colab
- GitHub Pages — portfolio presentation

---

## Relationship to Portfolio

This repository contains the computational work and curated outputs.

The public-facing project pages live in the separate portfolio repository:

```text
https://github.com/hghodkephd/hg-portfolio
```

The portfolio pages translate selected results from this repo into accessible explanations for a broader technical audience.

The intended separation is:

```text
pdl1-mini-binder-design/
= computational workflow, notebooks, scripts, and curated support outputs

hg-portfolio/
= public-facing HTML pages served by GitHub Pages
```

---

## Reproducibility Notes

Some workflows depend on Google Colab GPU availability and external model repositories. Large model weights and generated bulk outputs are not intended to be tracked directly in this repository.

Recommended practice:

- keep code, notebooks, configs, and curated small outputs in GitHub
- keep local data and generated results in `data/`, which is ignored by Git
- use Google Drive only as temporary Colab staging
- clear notebook outputs before committing when possible
- use `portfolio_pages/` only for curated assets needed to support public presentation

---

## Author

Harshad Ghodke, PhD

Experimental protein engineer and molecular biophysicist building direct fluency with computational protein design workflows.
