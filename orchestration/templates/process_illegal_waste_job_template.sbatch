#!/bin/bash
#SBATCH --partition=short-serial
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --time=04:00:00
#SBATCH --mem=24GB
#SBATCH --constraint="epyctwo1024G"

singularity exec --bind $input:/input --bind $state:/state --bind $static:/static --bind $working:/working --bind $output:/output $extraBinds $containerPath /app/exec.sh $finalJobTarget --inputFolder=$inputFolder --outputSRS=$outputSRS