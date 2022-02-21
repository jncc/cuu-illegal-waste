#!/bin/bash
#SBATCH --partition=short-serial
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --time=04:00:00
#SBATCH --mem=24GB
#SBATCH --constraint="epyctwo1024G"

./process_slc.sh
