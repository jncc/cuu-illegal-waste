#!/bin/bash
#SBATCH --job-name "scotwaste-slc"
#SBATCH --account jncc_scotwaste
#SBATCH --partition standard
#SBATCH --qos high
#SBATCH -o $jobWorkingDir/%j.out
#SBATCH -e $jobWorkingDir/%j.err
#SBATCH --time=04:00:00
#SBATCH --mem=32GB

singularity exec --bind $input:/input --bind $state:/state --bind $static:/static --bind $working:/working --bind $output:/output $extraBinds $containerPath /app/exec.sh $finalJobTarget --inputFolder=$inputFolder --outputSRS=$outputSRS