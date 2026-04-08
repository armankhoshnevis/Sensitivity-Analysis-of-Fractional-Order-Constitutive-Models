import json
import argparse
import numpy as np
from fmm_gsa_utils import load_data, modulus_func, perform_sensitivity_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--HS', type=int, default=20)
    parser.add_argument('--GnP_idx', type=int, default=0, help='Index of GnP in GnP_list for which to perform sensitivity analysis. GnP_idx = 0, 1, 2, 3 -> 0%, 0.5%, 1%, and 1.5% GnP')
    args = parser.parse_args()
    HS = args.HS
    GnP_idx = args.GnP_idx
    
    # Load the configuration for the FMM model parameters and data paths
    with open(f'../../configs/GSA/{HS}HSWF_FMM_Config.json', 'r') as config_file:
        config = json.load(config_file)

    file_path = config['file_path']
    rows = config['rows']
    cols = config['cols']
    params_list = config['params_list']
    GnP_list = config['GnP_list']

    optimized_params_df = load_data(file_path, rows, cols, params_list)

    # Assign optimized model parameters to mu
    mu = np.array(optimized_params_df.iloc[GnP_idx])

    # Calculate the standard deviation (sigma) as a percentage of the mean (mu)
    std_fctr = 0.05
    sigma = std_fctr * mu

    # Calculate the bounds for the uniform distribution based on the mean (mu) and standard deviation (sigma)
    upper_bound = 1/2 * (np.sqrt(12)*sigma + 2*mu)
    lower_bound = 2 * mu - upper_bound

    if HS == 30 and GnP_idx == 0:
        upper_bound[3] = 0.005
    elif HS == 40 and GnP_idx == 0:
        upper_bound[3] = 0.005

    # Unified frequency range
    w_freq = np.logspace(-8, 2, 500)

    # Calculate the model evaluations for storage, loss, and magnitude of complex moduli using the optimized parameters
    model_params = mu
    Ep_model = [modulus_func(w_value, model_params, 'storage') for w_value in w_freq]
    Epp_model = [modulus_func(w_value, model_params, 'loss') for w_value in w_freq]
    Ecomplex_model = [modulus_func(w_value, model_params, 'complex') for w_value in w_freq]

    # Define the sensitivity analysis problem
    SA_problem = {
        'num_vars': len(params_list),
        'names': params_list,
        'bounds': np.column_stack((lower_bound, upper_bound))
    }

    # Number of realizations (N = 2**m)
    m_min = 5
    m_max = 11
    step = 2
    N_values = [2**i for i in range(m_min, m_max+step, step)]

    # Define column names for the sensitivity indices DataFrames
    column_names = [params_list + [f'{param}_CI' for param in params_list] + ['freq']][0]

    # Perform sensitivity analysis
    perform_sensitivity_analysis(SA_problem, N_values, w_freq, column_names, file_path, HS, GnP_list, GnP_idx)