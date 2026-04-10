import json
import numpy as np

import sys
import os
sys.path.append(os.path.abspath("../.."))
from scripts.LSA.fmg_lsa_utils import (
    generate_derivatives,
    load_parameter_bounds,
    run_monte_carlo,
    save_statistics_npz
)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--HS', type=int, default=20, help='HSWF content percentage (e.g., 20 for 20% HSWF)')
    parser.add_argument('--GnP_idx', type=int, default=0, help='Index of GnP in GnP_list for which to perform sensitivity analysis. GnP_idx = 0, 1, 2, 3 -> 0%, 0.5%, 1%, and 1.5% GnP')
    parser.add_argument('--n_mc', type=int, default=100_000, help='Number of Monte Carlo samples to run for sensitivity analysis')
    parser.add_argument('--batch_size', type=int, default=50_000, help='Batch size for Monte Carlo sampling to manage memory usage')
    args = parser.parse_args()
    
    HS = args.HS
    GnP_idx = args.GnP_idx
    n_mc = args.n_mc
    batch_size = args.batch_size

    # Load configuration for the specified HSWF content and GnP
    with open(f'../../configs/LSA/{HS}HSWF_FMG_Config.json', 'r') as config_file:
        config = json.load(config_file)

    file_path = config['file_path']
    rows = config['rows']
    cols = config['cols']
    params_list = config['params_list']
    GnP_list = config['GnP_list']

    # Define frequency range for analysis
    w_freq = np.logspace(-8, 2, 500)

    # Generate funciton for derivative based sensitivity analyis
    funcs_dEp, funcs_dEpp = generate_derivatives()

    # Load parameter bounds for Monte Carlo sampling
    param_bounds = load_parameter_bounds(file_path, rows, cols, gnp_index=GnP_idx, std_fctr=0.05)

    # Run Monte Carlo sampling and compute sensitivity indices
    results = run_monte_carlo(
        funcs_dEp, 
        funcs_dEpp, 
        param_bounds, 
        params_list, 
        w_freq, 
        n_mc=n_mc, 
        batch_size=batch_size
    )

    # Save indices results to .npz file
    save_statistics_npz(results, params_list, w_freq, HS, GnP_list[GnP_idx], file_path)