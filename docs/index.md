# Sensitivity-Analysis-of-Fractional-Constitutive-Models

This repository provides a computational framework for conducting sensitivity analysis on fractional-order constitutive models. In particular, this repository focuses on a derivative-based local sensitivity analysis (LSA) and a variance-based (Sobol' indices) global sensitivity analysis (GSA) for constitutive models consist of parallel Fractional Maxwell Model (FMM) and Fractional Maxwell Gel (FMG) models capturing the dynamic viscoelastic response of neat and nanocomposite polyureas. The framework relies on in-house Python code for LSA and SALib package for GSA.

## Repository Structure
* **`configs/`**: Configuration files defining model parameters and their bounds for sensitivity analysis, and simulation settings.
* **`dataset/`**: Optimized model parameters.
* **`docs/`**: Markdown source files for the MkDocs documentation site.
* **`notebooks/`**: Interactive Jupyter notebooks detailing the workflow—from data preprocessing and model implementation to final visualizations.
* **`results/`**: Exported sensitivity indices and plots.
* **`scripts/`**: Python main scripts and modules for LSA and GSA for both models.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/armankhoshnevis/Sensitivity-Analysis-of-Fractional-Constitutive-Models.git](https://github.com/armankhoshnevis/Sensitivity-Analysis-of-Fractional-Constitutive-Models.git)
cd Sensitivity-Analysis-of-Fractional-Constitutive-Models
pip install -r requirements.txt