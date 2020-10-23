#Script Name: ProcessSLC_Scotland_fromInput
#Date Created: 16/09/2020
#Date Modified: 16/09/2020
#Author: JNCC
#Licence: MIT Licence
#Abstract: Script written for the Copernicus User Uptake project on illegal waste

#!/bin/bash
#SBATCH --partition=short-serial
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --time=30
#SBATCH --mem=24000
#SBATCH --ntasks=4

/snap/bin/gpt gpt SLCCoh_Scot_CommandLine.xml -Pinput1=$INPUT1 -Pinput2=$INPUT2 -Poutput=$OUTPUT
