# De Novo Mini Binder Design Against PD-L1

Building an end-to-end computational protein design workflow for de novo mini binder generation against human PD-L1 using RFdiffusion → ProteinMPNN → structure prediction/validation pipelines.

This project serves two purposes:

1. Develop hands-on fluency with modern AI-assisted protein design tools
2. Document the process from the perspective of an experimental scientist transitioning from directing AI-enabled protein engineering programs to directly executing computational workflows

Rather than acting as a polished tutorial, this repository functions as a computational design campaign notebook: assumptions, failures, design choices, debugging, and iterative refinement are documented alongside code and results.

---

## Scientific Objective

PD-L1 (Programmed Death Ligand-1) suppresses T-cell activation through interaction with PD-1 and is a major therapeutic target in cancer immunotherapy.

Goal:

Design small (~50–80 amino acid) de novo protein binders that:

- Fold into stable structures
- Occupy the PD-1 interaction surface on PD-L1
- Reproduce designed structures during validation
- Serve as candidate computationally designed binders

---

## Workflow

```text
Target structure (PD-L1)

        ↓

Target preparation
(PDB parsing, interface identification)

        ↓

RFdiffusion
Generate de novo backbone scaffolds

        ↓

ProteinMPNN
Design sequences for generated backbones

        ↓

ESMFold / AlphaFold
Predict structures from sequence

        ↓

Structural comparison
(RMSD, pLDDT, interface metrics)

        ↓

Candidate ranking and analysis
```

---

## Repository Structure

### notebooks/

Computational workflow notebooks

- `00_environment_test.ipynb`
- `01_target_preparation.ipynb`
- `02_rfdiffusion_binder_generation.ipynb`
- `03_proteinmpnn_sequence_design.ipynb`
- `04_alphafold_validation.ipynb`
- `05_analysis_and_filtering.ipynb`

Notes:

- Some notebooks run locally
- GPU-intensive workflows run in Google Colab (T4 GPU)

---

### data/

Project inputs and outputs

```text
data/
├── structures/
├── sequences/
└── results/
```

---

### figures/

Generated figures and visualizations

Examples:

- PD-L1 interface characterization
- Structure comparison plots
- Design performance metrics
- Final candidate ranking

---

### scripts/

Reusable utility functions and analysis scripts

---

### docs/

Project notes and experimentalist-oriented explanations

Examples:

- Computational design logbook
- Environment notes
- Explanations of workflow decisions
- Lessons learned

---

## Current Status

### Completed

- Environment setup
- PD-L1 target preparation
- RFdiffusion workflow setup
- Initial binder generation
- Geometry-based design filtering

### In progress

- Refinement of hotspot residue selection
- ProteinMPNN sequence design
- Structural validation workflow

### Planned

- Candidate ranking
- Portfolio visualization
- Final report generation

---

## Key Results

Project ongoing.

Results and figures will be added as computational campaigns progress.

---

## Motivation

I previously led and collaborated with teams applying AI-guided protein engineering and high-throughput experimental workflows but had limited direct hands-on experience executing modern computational design pipelines.

This repository documents the process of building direct operational fluency at the keyboard while maintaining an experimentalist's perspective on hypothesis generation, design-build-test-learn cycles, and interpretation.

---

## Tools

- RFdiffusion — de novo backbone generation
- ProteinMPNN — inverse folding / sequence design
- ESMFold / AlphaFold — structure prediction
- BioPython — structure parsing and analysis
- PyMOL — visualization
- Python / Jupyter / Google Colab
