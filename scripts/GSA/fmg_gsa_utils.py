import numpy as np
import pandas as pd

from SALib.sample import sobol as sobol_sampling
from SALib.analyze import sobol as sobol_analysis

# Define the modulus function for both storage and loss moduli
def modulus_func(x, model_params, model):
    """Calculate the modulus function for a given model.

    Args:
        x (float): Shifted frequency.
        model_params (array-like): The model parameters including the characteristic moduli, time scales, and fractional-order derivatives.
        model (str): The model type ('storage', 'loss', or 'complex').

    Returns:
        Ep (float): The storage modulus if model is 'storage'.
        Epp (float): The loss modulus if model is 'loss'.
        Ecomplex (float): The magnitude of the complex modulus if model is 'complex'.
    """
    E_c1 = model_params[0]
    tau_c1 = model_params[1]
    alpha_1 = model_params[2]
    E_c2 = model_params[3]
    tau_c2 = model_params[4]
    alpha_2 = model_params[5]
    
    num1_Ep = (x * tau_c1)**alpha_1 * np.cos(np.pi * alpha_1 / 2) + (x * tau_c1)**(2 * alpha_1)
    num2_Ep = (x * tau_c2)**alpha_2 * np.cos(np.pi * alpha_2 / 2) + (x * tau_c2)**(2 * alpha_2)
    num1_Epp = (x * tau_c1)**alpha_1 * np.sin(np.pi * alpha_1 / 2)
    num2_Epp = (x * tau_c2)**alpha_2 * np.sin(np.pi * alpha_2 / 2)
    denom1 = 1 + (x * tau_c1)**alpha_1 * np.cos(np.pi * alpha_1 / 2) + (x * tau_c1)**(2 * alpha_1)
    denom2 = 1 + (x * tau_c2)**alpha_2 * np.cos(np.pi * alpha_2 / 2) + (x * tau_c2)**(2 * alpha_2)
    
    Ep = E_c1 * num1_Ep / denom1 + E_c2 * num2_Ep / denom2
    Epp = E_c1 * num1_Epp / denom1 + E_c2 * num2_Epp / denom2
    
    if model == 'storage':
        return Ep
    
    elif model == 'loss':
        return Epp
    elif model == 'complex':
        return np.sqrt(Ep**2 + Epp**2)
    else:
        raise ValueError("Invalid model type. Choose 'storage', 'loss', or 'complex'.")

# Define a function to load the optimized parameters
def load_data(file_path, rows, cols, params_list):
    """Load the optimized model parameters

    Args:
        file_path (str): The path to the Excel file containing the optimized parameters.
        rows (dict): A dictionary containing the start and end rows for reading the optimized parameters.
        cols (dict): A dictionary containing the column indices for reading the optimized parameters.
        params_list (list): A list of parameter names.

    Returns:
        optimized_params_df (pandas.DataFrame): A DataFrame containing the optimized model parameters.
    """
    optimized_params_df = pd.read_excel(
        file_path['opt_path'], usecols=cols['cols_opt'], skiprows=rows['start_row_opt'],
        nrows=rows['end_row_opt'] - rows['start_row_opt'], header=None
    )
    optimized_params_df.columns = params_list

    return optimized_params_df

# Define a function to perform sensitivity analysis
def perform_sensitivity_analysis(SA_problem, N_values, w_freq, column_names, file_path, HS, GnP_list, GnP_idx):
    """Perform sensitivity analysis using the Sobol method and save the results in Excel files.

    Args:
        SA_problem (dict): A dictionary containing the sensitivity analysis problem definition.
        N_values (list): A list of the number of realizations to use for each simulation.
        w_freq (array-like): An array of frequencies at which to evaluate the model.
        column_names (list): A list of column names for the sensitivity indices DataFrames.
        file_path (dict): A dictionary containing the paths for saving the results.
        HS (str): The name of the health state for which to perform sensitivity analysis.
        GnP_list (list): A list of group names for which to perform sensitivity analysis.
        GnP_idx (int): The index of the group name in GnP_list for which to perform sensitivity analysis.

    Returns:
        This function writes sensitivity analysis results to Excel files and does not return a value.
    """
    # Initialize Excel writers for storing the sensitivity indices
    xlsx_wrtr_S1_Ep = pd.ExcelWriter(f'{file_path["save_path"]}/S1_Ep_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    xlsx_wrtr_ST_Ep = pd.ExcelWriter(f'{file_path["save_path"]}/ST_Ep_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    xlsx_wrtr_S1_Epp = pd.ExcelWriter(f'{file_path["save_path"]}/S1_Epp_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    xlsx_wrtr_ST_Epp = pd.ExcelWriter(f'{file_path["save_path"]}/ST_Epp_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    xlsx_wrtr_S1_Ecomplex = pd.ExcelWriter(f'{file_path["save_path"]}/S1_Ecomplex_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    xlsx_wrtr_ST_Ecomplex = pd.ExcelWriter(f'{file_path["save_path"]}/ST_Ecomplex_{HS}_{GnP_list[GnP_idx]}.xlsx', engine='openpyxl')
    
    # Loop over each number of realization
    for N in N_values:
        # Generate realization of model params
        model_params_samples = sobol_sampling.sample(SA_problem, N, calc_second_order=False)

        # Modify the sampled tau_c2 values based on the constraint tau_c2 = tau_c1 * sqrt(E_c1/E_c2)
        model_params_samples[:, 4] = model_params_samples[:, 1] * np.sqrt(model_params_samples[:, 0]/model_params_samples[:, 3])

        # Evaluate Ep, Epp, and E_complex at each frequency for each set of realized model params
        Ep_eval_sobol = np.array([modulus_func(w_freq, model_params, 'storage') for model_params in model_params_samples])
        Epp_eval_sobol = np.array([modulus_func(w_freq, model_params, 'loss') for model_params in model_params_samples])
        Ecomplex_eval_sobol = np.array([modulus_func(w_freq, model_params, 'complex') for model_params in model_params_samples])

        # Perform SA
        Ep_sobol_indices = [sobol_analysis.analyze(SA_problem, Y, calc_second_order=False) for Y in Ep_eval_sobol.T]
        Epp_sobol_indices = [sobol_analysis.analyze(SA_problem, Y, calc_second_order=False) for Y in Epp_eval_sobol.T]
        Ecomplex_sobol_indices = [sobol_analysis.analyze(SA_problem, Y, calc_second_order=False) for Y in Ecomplex_eval_sobol.T]

        # Extract the first and total order sensitivity indices at each frequency
        S1_Ep = np.array([s['S1'] for s in Ep_sobol_indices])
        ST_Ep = np.array([s['ST'] for s in Ep_sobol_indices])
        S1_Epp = np.array([s['S1'] for s in Epp_sobol_indices])
        ST_Epp = np.array([s['ST'] for s in Epp_sobol_indices])
        S1_Ecomplex = np.array([s['S1'] for s in Ecomplex_sobol_indices])
        ST_Ecomplex = np.array([s['ST'] for s in Ecomplex_sobol_indices])

        # Extract the confidence interval at each frequency
        S1_Ep_CI = np.array([s['S1_conf'] for s in Ep_sobol_indices])
        ST_Ep_CI = np.array([s['ST_conf'] for s in Ep_sobol_indices])
        S1_Epp_CI = np.array([s['S1_conf'] for s in Epp_sobol_indices])
        ST_Epp_CI = np.array([s['ST_conf'] for s in Epp_sobol_indices])
        S1_Ecomplex_CI = np.array([s['S1_conf'] for s in Ecomplex_sobol_indices])
        ST_Ecomplex_CI = np.array([s['ST_conf'] for s in Ecomplex_sobol_indices])

        # Concatenate (column-wise) sensitivity indices, confidence intervals, and frequencies arrays
        S1_Ep_concat = np.c_[S1_Ep, S1_Ep_CI, w_freq]
        ST_Ep_concat = np.c_[ST_Ep, ST_Ep_CI, w_freq]
        S1_Epp_concat = np.c_[S1_Epp, S1_Epp_CI, w_freq]
        ST_Epp_concat = np.c_[ST_Epp, ST_Epp_CI, w_freq]
        S1_Ecomplex_concat = np.c_[S1_Ecomplex, S1_Ecomplex_CI, w_freq]
        ST_Ecomplex_concat = np.c_[ST_Ecomplex, ST_Ecomplex_CI, w_freq]

        # Convert sensitivity indices to data frames
        S1_Ep_df = pd.DataFrame(S1_Ep_concat, columns=column_names)
        ST_Ep_df = pd.DataFrame(ST_Ep_concat, columns=column_names)
        S1_Epp_df = pd.DataFrame(S1_Epp_concat, columns=column_names)
        ST_Epp_df = pd.DataFrame(ST_Epp_concat, columns=column_names)
        S1_Ecomplex_df = pd.DataFrame(S1_Ecomplex_concat, columns=column_names)
        ST_Ecomplex_df = pd.DataFrame(ST_Ecomplex_concat, columns=column_names)

        # Save the data frames to separate sheets in the same Excel file
        sheet_name = f'N={N}'
        S1_Ep_df.to_excel(xlsx_wrtr_S1_Ep, sheet_name=sheet_name, index=False)
        ST_Ep_df.to_excel(xlsx_wrtr_ST_Ep, sheet_name=sheet_name, index=False)
        S1_Epp_df.to_excel(xlsx_wrtr_S1_Epp, sheet_name=sheet_name, index=False)
        ST_Epp_df.to_excel(xlsx_wrtr_ST_Epp, sheet_name=sheet_name, index=False)
        S1_Ecomplex_df.to_excel(xlsx_wrtr_S1_Ecomplex, sheet_name=sheet_name, index=False)
        ST_Ecomplex_df.to_excel(xlsx_wrtr_ST_Ecomplex, sheet_name=sheet_name, index=False)

    # Close the Excel writers and save the files
    xlsx_wrtr_S1_Ep.close()
    xlsx_wrtr_ST_Ep.close()
    xlsx_wrtr_S1_Epp.close()
    xlsx_wrtr_ST_Epp.close()
    xlsx_wrtr_S1_Ecomplex.close()
    xlsx_wrtr_ST_Ecomplex.close()