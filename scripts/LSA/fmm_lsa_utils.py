import numpy as np
import sympy as sp
import pandas as pd

def generate_derivatives():
    """Defines symbolic equations and returns lambdified derivative functions.
    Returns:
        funcs_dEp (dict): Dictionary of lambdified functions for derivatives of storage modulus.
        funcs_dEpp (dict): Dictionary of lambdified functions for derivatives of loss modulus.
    """
    # Define model parameters and frequency as symbols
    E_c1, E_c2, tau_c1, tau_c2, alpha_1, alpha_2, beta_1, w_freq = sp.symbols('E_c1 E_c2 tau_c1 tau_c2 alpha_1 alpha_2 beta_1 w_freq')

    # Define the storage and loss moduli
    numerator_Ep_1 = E_c1 * ( (w_freq*tau_c1)**alpha_1 * sp.cos(sp.pi*alpha_1/2) + (w_freq*tau_c1)**(2*alpha_1 - beta_1) * sp.cos(sp.pi*beta_1/2) )
    numerator_Ep_2 = E_c2 * ( (w_freq*tau_c2)**alpha_2 * sp.cos(sp.pi*alpha_2/2) + (w_freq*tau_c2)**(2*alpha_2) )

    numerator_Epp_1 = E_c1 * ( (w_freq*tau_c1)**alpha_1 * sp.sin(sp.pi*alpha_1/2) + (w_freq * tau_c1)**(2*alpha_1 - beta_1) * sp.sin(sp.pi*beta_1/2) )
    numerator_Epp_2 = E_c2 * ( (w_freq*tau_c2)**alpha_2 * sp.sin(sp.pi*alpha_2/2) )
    
    denominator_1 = ( 1 + (w_freq*tau_c1)**(alpha_1-beta_1) * sp.cos(sp.pi * (alpha_1 - beta_1)/2) + (w_freq*tau_c1)**(2*(alpha_1 - beta_1)) )
    denominator_2 = ( 1 + (w_freq*tau_c2)**alpha_2 * sp.cos(sp.pi*alpha_2/2) + (w_freq*tau_c2)**(2*alpha_2) )
    
    Ep = numerator_Ep_1 / denominator_1 + numerator_Ep_2 / denominator_2
    Epp = numerator_Epp_1 / denominator_1 + numerator_Epp_2 / denominator_2
    
    # Compute the derivatives and lambdify them for numerical evaluation
    vars_branch_1 = (E_c1, tau_c1, alpha_1, beta_1, w_freq)
    vars_branch_2 = (E_c2, tau_c2, alpha_2, w_freq)

    funcs_dEp = {
        'E_c1': sp.lambdify(vars_branch_1, sp.diff(Ep, E_c1), 'numpy'),
        'tau_c1': sp.lambdify(vars_branch_1, sp.diff(Ep, tau_c1), 'numpy'),
        'alpha_1':  sp.lambdify(vars_branch_1, sp.diff(Ep, alpha_1), 'numpy'),
        'beta_1': sp.lambdify(vars_branch_1, sp.diff(Ep, beta_1), 'numpy'),
        'E_c2': sp.lambdify(vars_branch_2, sp.diff(Ep, E_c2), 'numpy'),
        'tau_c2': sp.lambdify(vars_branch_2, sp.diff(Ep, tau_c2), 'numpy'),
        'alpha_2':  sp.lambdify(vars_branch_2, sp.diff(Ep, alpha_2), 'numpy')
    }

    funcs_dEpp = {
        'E_c1': sp.lambdify(vars_branch_1, sp.diff(Epp, E_c1), 'numpy'),
        'tau_c1': sp.lambdify(vars_branch_1, sp.diff(Epp, tau_c1), 'numpy'),
        'alpha_1':  sp.lambdify(vars_branch_1, sp.diff(Epp, alpha_1), 'numpy'),
        'beta_1': sp.lambdify(vars_branch_1, sp.diff(Epp, beta_1), 'numpy'),
        'E_c2': sp.lambdify(vars_branch_2, sp.diff(Epp, E_c2), 'numpy'),
        'tau_c2': sp.lambdify(vars_branch_2, sp.diff(Epp, tau_c2), 'numpy'),
        'alpha_2':  sp.lambdify(vars_branch_2, sp.diff(Epp, alpha_2), 'numpy')
    }
    
    print("Derivative functions generated successfully.")
    return funcs_dEp, funcs_dEpp

def load_parameter_bounds(file_path, rows, cols, gnp_index, std_fctr=0.05):
    """Loads Excel data and calculates uniform distribution bounds.
    Args:
        file_path (dict): Dictionary containing paths to Excel files.
        rows (dict): A dictionary containing the start and end rows for reading the optimized parameters.
        cols (dict): A dictionary containing the column indices for reading the optimized parameters.
        gnp_index (int): Index for the GnP parameter set to extract means from.
        std_fctr (float): Standard deviation factor for calculating bounds.
    Returns:
        bounds (list): List of tuples containing (a, b) bounds for uniform distribution.
    """
    optimized_params_df = pd.read_excel(
        file_path['opt_path'], usecols=cols['cols_opt'], skiprows=rows['start_row_opt'],
        nrows=rows['end_row_opt'] - rows['start_row_opt'], header=None
    )
    data = optimized_params_df.to_numpy()

    mus = data[gnp_index]
        
    bounds = []
    for mu in mus:
        sigma = std_fctr * mu
        upper_bound = 0.5 * (np.sqrt(12) * sigma + 2 * mu)
        lower_bound = 2 * mu - upper_bound
        bounds.append((lower_bound, upper_bound))
    
    print("Parameter bounds calculated successfully.")
    return bounds

def run_monte_carlo(funcs_dEp, funcs_dEpp, bounds, params_list, w_freq, n_mc=10**3, batch_size=50_000):
    """Executes the MC simulation and returns result arrays.
    Args:
        funcs_dEp (dict): Dictionary of lambdified functions for derivatives of storage modulus.
        funcs_dEpp (dict): Dictionary of lambdified functions for derivatives of loss modulus.
        bounds (list): List of tuples containing lower and upper bounds for uniform distribution.
        w_freq (ndarray): Array of frequency values used in the simulation.
        n_mc (int): Number of Monte Carlo iterations.
    Returns:
        realized_indices (dict): Dictionary containing arrays of sensitivity indices for all moduli.
    """
    (lower_bound1, upper_bound1), (lower_bound2, upper_bound2), (lower_bound3, upper_bound3), (lower_bound4, upper_bound4) = bounds[:4]
    (lower_bound5, upper_bound5), (lower_bound6, upper_bound6), (lower_bound7, upper_bound7) = bounds[4:]
    
    # Initialize arrays to store normalized sensitivity indices for each modulus, parameter and frequency
    realized_indices = {
        'Ep': {p: np.zeros((n_mc, len(w_freq))) for p in params_list},
        'Epp': {p: np.zeros((n_mc, len(w_freq))) for p in params_list},
        'Ecomplex': {p: np.zeros((n_mc, len(w_freq))) for p in params_list},
    }

    # Process samples in batches
    print(f"Starting Monte Carlo simulation with {n_mc} iterations...")
    for start_idx in range(0, n_mc, batch_size):
        end_idx = min(start_idx + batch_size, n_mc)
        b_size = end_idx - start_idx
        
        # Generate random variables
        E_c1 = np.random.uniform(lower_bound1, upper_bound1, b_size).reshape(-1, 1)
        tau_c1 = np.random.uniform(lower_bound2, upper_bound2, b_size).reshape(-1, 1)
        alpha_1 = np.random.uniform(lower_bound3, upper_bound3, b_size).reshape(-1, 1)
        beta_1 = np.random.uniform(lower_bound4, upper_bound4, b_size).reshape(-1, 1)
        E_c2 = np.random.uniform(lower_bound5, upper_bound5, b_size).reshape(-1, 1)
        tau_c2 = np.random.uniform(lower_bound6, upper_bound6, b_size).reshape(-1, 1)
        alpha_2 = np.random.uniform(lower_bound7, upper_bound7, b_size).reshape(-1, 1)

        # Calculate moduli for the current parameter realization
        numerator_Ep_1 = E_c1 * ( (w_freq*tau_c1)**alpha_1 * np.cos(np.pi*alpha_1/2) + (w_freq*tau_c1)**(2*alpha_1 - beta_1) * np.cos(np.pi*beta_1/2) )
        numerator_Ep_2 = E_c2 * ( (w_freq*tau_c2)**alpha_2 * np.cos(np.pi*alpha_2/2) + (w_freq*tau_c2)**(2*alpha_2) )
        
        numerator_Epp_1 = E_c1 * ( (w_freq*tau_c1)**alpha_1 * np.sin(np.pi*alpha_1/2) + (w_freq * tau_c1)**(2*alpha_1 - beta_1) * np.sin(np.pi*beta_1/2) )
        numerator_Epp_2 = E_c2 * ( (w_freq*tau_c2)**alpha_2 * np.sin(np.pi*alpha_2/2) )

        denominator_1 = ( 1 + (w_freq*tau_c1)**(alpha_1-beta_1) * np.cos(np.pi*(alpha_1 - beta_1)/2) + (w_freq*tau_c1)**(2*(alpha_1 - beta_1)) )
        denominator_2 = ( 1 + (w_freq*tau_c2)**alpha_2 * np.cos(np.pi*alpha_2/2) + (w_freq*tau_c2)**(2*alpha_2) )

        Ep = numerator_Ep_1 / denominator_1 + numerator_Ep_2 / denominator_2
        Epp = numerator_Epp_1 / denominator_1 + numerator_Epp_2 / denominator_2
        Ecomplex = np.sqrt(Ep**2 + Epp**2)

        # Calculate normalized local sensitivity indices
        for p, xv in zip(params_list, [E_c1, tau_c1, alpha_1, beta_1, E_c2, tau_c2, alpha_2]):
            if p in ['E_c1', 'tau_c1', 'alpha_1', 'beta_1']:
                args = (E_c1, tau_c1, alpha_1, beta_1, w_freq)
            else:
                args = (E_c2, tau_c2, alpha_2, w_freq)
            
            dEp_val = funcs_dEp[p](*args)
            dEpp_val = funcs_dEpp[p](*args)
            
            realized_indices['Ep'][p][start_idx:end_idx, :] = dEp_val * xv / Ep
            realized_indices['Epp'][p][start_idx:end_idx, :] = dEpp_val * xv / Epp
            realized_indices['Ecomplex'][p][start_idx:end_idx, :] = (xv / Ecomplex) * np.sqrt(dEp_val**2 + dEpp_val**2)

        print(f"Completed {end_idx} / {n_mc} iterations")
    
    print("Monte Carlo simulation completed successfully.")
    return realized_indices

def save_statistics_npz(realized_indices, params, w_freq, HS, GnP, file_path):
    """Calculates mean and standard deviation of sensitivity indices, and L1 norm of mean sensitivity indices, followed by saving to a compressed NumPy archive.
    Args:
        realized_indices (dict): Dictionary containing arrays of sensitivity indices for all moduli.
        params (list): List of parameter names.
        w_freq (ndarray): Array of frequency values used in the simulation.
        HS (int): Heat treatment condition.
        GnP (str): GnP loading condition.
        file_path (dict): Dictionary containing paths to save the data."""
    log_w_freq = np.log(w_freq)
    save_data = {}
    for key in ['Ep', 'Epp', 'Ecomplex']:
        mean_std_indices = np.zeros((len(params)*2 + 1, len(w_freq)))
        l1_array = np.zeros(len(params))
        
        for idx, p in enumerate(params):
            mean_sensitivity_index = np.mean(realized_indices[key][p], axis=0)
            std_sensitivity_index = np.std(realized_indices[key][p], axis=0, ddof=1)

            mean_std_indices[idx*2, :] = mean_sensitivity_index
            mean_std_indices[idx*2 + 1, :] = std_sensitivity_index

            l1_array[idx] = np.trapezoid(np.abs(mean_sensitivity_index), x=log_w_freq)
            
        save_data[f'all_lsi_{key}_{HS}HS_{GnP}'] = mean_std_indices
        save_data[f'L1_lsi_{key}_{HS}HS_{GnP}'] = l1_array

    np.savez_compressed(file_path['save_path'] + f'/{HS}HS_{GnP}.npz', **save_data)
    print(f"Statistics saved successfully to {file_path['save_path']}/{HS}HS_{GnP}.npz")