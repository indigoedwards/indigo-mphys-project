#!/bin/sh
#SBATCH --job-name=indigo-convtest0                # Job name
#SBATCH --output=log_0convtest%j.log           # Standard out and error log
#SBATCH --mail-type=END                   # Specify when to mail (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=jcre500@york.ac.uk         # NB change uid to your username if wanting to send mail

#need ONE of the following two lines:
##SBATCH --partition=teach         # priority queue for class work
#SBATCH --account=pet-double-2024           # specify your project account if NOT doing class work

#customise these according to job size and time required:
#SBATCH --ntasks=13                         # Run 4 tasks...
#SBATCH --cpus-per-task=1                  # ...with each task using 1 core
#SBATCH --time=24:00:00                    # Time limit hrs:min:sec

#actual executable info now:

#tell user what is going on:
echo My working directory is `pwd`
echo Running job on host:
echo -e '\t'`hostname` at `date`
echo -e '\t'using $SLURM_NTASKS cores
echo

##cd
##cd /tmp/users/jcre500/indigo-mphys/bin
##ls
##source activate
source ~/scratch/.venv/bin/activate
#pip list
##module load foss
OMP_NUM_TREADS=$SLURM_NTASKS python3 energy_convergence_testing.py
deactivate

echo
echo Job completed at `date`

