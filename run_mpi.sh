#!/bin/bash
#SBATCH --job-name=det_methane_2D  # create a short name for your job
#SBATCH --nodes=3                # node count
#SBATCH --ntasks=336             # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --time=00:30:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-user=ltt@princeton.edu
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --account=mueller

module purge
module load intel-mpi/gcc/2021.13

srun ./PeleC2d.gnu.MPI.ex det.inp