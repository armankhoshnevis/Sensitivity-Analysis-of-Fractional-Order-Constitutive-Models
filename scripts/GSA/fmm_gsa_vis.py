import json
import argparse
import numpy as np

from fmm_gsa_vis_utils import (
    plot_sensitivity_indices,
    read_excel_range,
    plot_Linf_grouped
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--S', type=str, help='Sensitivity index type (S1 or ST)')
    parser.add_argument('--E', type=str, help='Modulus type (Ep, Epp, or Ecomplex)')
    parser.add_argument('--N', type=int, help='Number of samples (N = 2**m)')
    parser.add_argument('--HS', type=int, help='Value of Hard Segment Weight Fraction (e.g., 20, 30, or 40)')
    args = parser.parse_args()
    
    w_freq = np.logspace(-8, 2, 500)
    
    with open(f'../../configs/GSA/{args.HS}HSWF_FMM_Config.json', 'r') as config_file:
        config = json.load(config_file)
    
    GnP_list = config['GnP_list']
    params_list = config['params_list']
    file_path = config['file_path']
    
    plot_sensitivity_indices(
        S=args.S,
        E=args.E,
        N=args.N,
        HS=args.HS,
        w_freq=w_freq,
        GnP_list=GnP_list,
        params_list=params_list,
        file_path=file_path
    )

    filename = "../../results/GSA/GSA_FMM.xlsx"

    Linf_Ep_20HS  = read_excel_range(filename=filename, cell_range="C8:I9")
    Linf_Ep_30HS  = read_excel_range(filename=filename, cell_range="C15:I16")
    Linf_Ep_40HS  = read_excel_range(filename=filename, cell_range="C22:I23")

    Linf_Epp_20HS = read_excel_range(filename=filename, cell_range="M8:S9")
    Linf_Epp_30HS = read_excel_range(filename=filename, cell_range="M15:S16")
    Linf_Epp_40HS = read_excel_range(filename=filename, cell_range="M22:S23")

    Linf_Ecomplex_20HS = read_excel_range(filename=filename, cell_range="W8:AC9")
    Linf_Ecomplex_30HS = read_excel_range(filename=filename, cell_range="W15:AC16")
    Linf_Ecomplex_40HS = read_excel_range(filename=filename, cell_range="W22:AC23")

    Linf_Ep_mean = np.vstack([Linf_Ep_20HS[0, :],  Linf_Ep_30HS[0, :],  Linf_Ep_40HS[0, :]])
    Linf_Ep_std = np.vstack([Linf_Ep_20HS[1, :],  Linf_Ep_30HS[1, :],  Linf_Ep_40HS[1, :]])

    Linf_Epp_mean = np.vstack([Linf_Epp_20HS[0, :], Linf_Epp_30HS[0, :], Linf_Epp_40HS[0, :]])
    Linf_Epp_std = np.vstack([Linf_Epp_20HS[1, :], Linf_Epp_30HS[1, :], Linf_Epp_40HS[1, :]])

    Linf_Ecomplex_mean = np.vstack([Linf_Ecomplex_20HS[0, :], Linf_Ecomplex_30HS[0, :], Linf_Ecomplex_40HS[0, :]])
    Linf_Ecomplex_std = np.vstack([Linf_Ecomplex_20HS[1, :], Linf_Ecomplex_30HS[1, :], Linf_Ecomplex_40HS[1, :]])

    # Note: Specify the ylabel and save path manually
    plot_Linf_grouped(
        Linf_Ep_mean,
        Linf_Ep_std,
        ylabel=r"$||\bar{S}_{E^{\prime}}||_{L_{\infty}}$",
        save_path="../../results/GSA/GSA_Linf_Ep_FMM"
    )