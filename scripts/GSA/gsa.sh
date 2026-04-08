#!/bin/bash --login

#SBATCH --job-name=GSA_FMG

#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00

# Load necessary modules (Adapt these to your specific cluster environment)
ml purge
ml load Miniforge3
ml load powertools

# Activate the conda environment (Make sure the Conda installation guide is followed)
conda activate SA_Project

# Print job information
echo "Job started at $(date)"
echo "Running on host $(hostname)"

# Run the Python script
# Note: Ensure you are in the correct directory or provide absolute paths
python fmg_main.py --HS 20 --GnP_idx 0

# Uncomment the following line to run post-processing in the same job
# python fmg_vis.py --S 'S1' --E 'Ep' --N 2048 --HS 20

echo "Job finished at $(date)"