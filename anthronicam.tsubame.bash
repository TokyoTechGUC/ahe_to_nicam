#!/bin/bash
#$ -cwd
#$ -m abe
#$ -N anthronicam
#$ -M alvincgvarquez@gmail.com
#$ -l h_rt=00:10:00
#$ -l cpu_40=1

module load miniconda >& /dev/null
eval "$(/apps/t4/rhel9/free/miniconda/24.1.2/bin/conda shell.bash hook)" 
conda activate /gs/bs/tga-guc-lab/dependencies/dependencies_intel/conda/envs/guconda
export PATH=/gs/bs/tga-guc-lab/dependencies/dependencies_intel/conda/envs/guconda/bin:$PATH
source /gs/bs/tga-guc-lab/dependencies/dependencies_nvhpc/environments.bash

set -eou pipefail

time python anthro_to_ico_files_28km.py
