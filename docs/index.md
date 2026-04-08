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
First, clone the repository and navigate into the project directory:
```bash
git clone git@github.com:armankhoshnevis/Sensitivity-Analysis-of-Fractional-Constitutive-Models.git
cd Sensitivity-Analysis-of-Fractional-Constitutive-Models
```

### Option A: Python venv & pip (Recommended for Running Locally)
If it is preferred to use standard Python virtual environments locally, `pip` alongside the `requirements.txt` file can be used. Then, execute the following commands:
```bash
python -m venv env

# On Windows:
.\env\Scripts\activate

# On macOS/Linux:
source env/bin/activate

pip install -r requirements.txt
```

### Option B: Conda (Recommended for Running on Clusters)
If it is preferred to run the codes on a cluster, `environment.yml` file is used to ensure exact dependency and Python version matching. Then, execute the following commands:
```bash
module load Miniforge3 # Replace with your specific cluster's module if different
conda env create -f environment.yml
conda activate SA_Project
```

## Quick Run
### Running Locally
Once your environment is activated (via Conda or venv), navigate to the `script` directory and execute the Python files directly from your terminal:

* Global Sensitivity Analysis
```bash
cd script
python fmg_gsa_main.py --HS 20 --GnP_idx 0
python fmg_gsa_vis.py --S 'S1' --E 'Ep' --N 2048 --HS 20
```

* Local Sensitivity Analysis
```bash
python fmg_lsa_main.py --HS 20 --GnP_idx 0 --n_mc 100000 --batch_size 50000
python fmg_lsa_vis.py --E_type 'Ep' --HS 20
```

### Running on a SLURM Cluster
If you are running the inference on a cluster that uses the SLURM workload manager, a sample batch script (`gsa.sh` and `lsa.sh`) is provided. The script is pre-configured to activate the SA_Project conda environment.
```bash
cd script
sbatch gsa.sb
```

**Note:** The script's output and any errors will be automatically logged to standard `.out` and `.err` files in the working directory.

## Documentation
Please refer to this [link](https://armankhoshnevis.github.io/Sensitivity-Analysis-of-Fractional-Constitutive-Models/) for more comprehensive documentations.

## Citation Requirements
If you use this software, please cite it and its corresponding paper, as:

- Software citation:
  - APA style: Khoshnevis, A. (2026). Sensitivity Analysis of Fractional Constitutive Models (Version 1.0.0) [Computer software]. https://github.com/armankhoshnevis/Sensitivity-Analysis-of-Fractional-Constitutive-Models

  - BibTeX entry:<br>
    @software{Khoshnevis_SA_2026, <br>
    author = {Khoshnevis, Arman},<br>
    license = {Apache-2.0},<br>
    month = apr,<br>
    title = {{Sensitivity Analysis of Fractional Constitutive Models}},<br>
    url = {https://github.com/armankhoshnevis/Sensitivity-Analysis-of-Fractional-Constitutive-Models},<br>
    version = {1.0.0},<br>
    year = {2026}<br>
    }

- Paper citation:<br>
@article{khoshnevis2025stochastic, <br>
  title={Stochastic Generalized-Order Constitutive Modeling of Viscoelastic Spectra of Polyurea-Graphene Nanocomposites},<br>
  author={Khoshnevis, Arman and Tzelepis, Demetrios A and Ginzburg, Valeriy V and Zayernouri, Mohsen},<br>
  journal={Engineering Reports},<br>
  volume={7},<br>
  number={9},<br>
  pages={e70367},<br>
  year={2025},<br>
  publisher={Wiley Online Library}<br>
}

## Contributions
This repository is a static archive of the project code. The software is provided "as-is" and is not actively maintained. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
