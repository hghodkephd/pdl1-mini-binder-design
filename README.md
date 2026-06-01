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

## Workflow Overview

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

## Repository Structure

```text
pdl1-mini-binder-design/
├── README.md
├── data/
│   ├── structures/
│   ├── sequences/
│   └── results/
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

Contains project inputs, intermediate outputs, and analysis results.

Typical contents include:

```text
data/
├── structures/
│   ├── pdb4zq.ent
│   ├── pdl1_clean.pdb
│   └── pdl1_interface_session.pse
├── sequences/
└── results/
    ├── proteinmpnn/
    └── ...
```

Large generated outputs should be handled carefully. Raw model outputs, large trajectory files, and model weights should generally not be committed unless they are small, curated, and necessary for reproducibility or portfolio presentation.

---

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

---

### `scripts/`

Contains reusable scripts extracted from notebook workflows.

Example:

- `portfolio_page3_extract_passed_structures_for_viewer.py`  
  Extracts selected structures for downstream visualization in the portfolio project.

---

### `portfolio_pages/`

Contains curated outputs that support the separate public portfolio website.

This folder may include:

- selected structures
- figures
- summary CSVs
- tables
- viewer-ready files
- exported analysis artifacts

The live HTML pages are maintained separately in the `hg-portfolio` repository. This folder exists to preserve the computational outputs that feed those pages.

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

---

### ProteinMPNN entropy analysis

ProteinMPNN sequence sampling can identify positions where the model is highly confident versus positions where multiple amino acids appear tolerated.

This can inform experimental library design:

- low-entropy positions → fix
- high-entropy positions → diversify

The goal is to compress library size while enriching for sequences that are more likely to fold and remain compatible with the designed scaffold.

---

### Parameter sensitivity

The project also explores how RFdiffusion settings affect output quality. The practical goal is to understand how to tune design parameters to get more useful candidates from limited compute.

---

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

---

## Reproducibility Notes

Some workflows depend on Google Colab GPU availability and external model repositories. Large model weights and generated bulk outputs are not intended to be tracked directly in this repository.

Recommended practice:

- keep code, notebooks, configs, and curated small outputs in GitHub
- keep large intermediate files, model caches, and trajectories outside Git
- clear notebook outputs before committing when possible
- use `portfolio_pages/` only for curated assets needed to support public presentation

---

## Author

Harshad Ghodke, PhD

Experimental protein engineer and molecular biophysicist building direct fluency with computational protein design workflows.
