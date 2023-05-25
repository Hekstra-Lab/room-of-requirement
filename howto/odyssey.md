# Working on the Harvard Cluster

Here are some general guidelines and best practices for working on the cluster.

### Contents:
- [Logging In](odyssey.md#Logging-in)
- [Personal Python Environments](odyssey.md#Personal-Python-Environments)
- [Hekstra Lab Storage](odyssey.md#Hekstra-Lab-Storage)
- [Common Software](odyssey.md#Common-Software)
- [Best Practices](odyssey.md#Best-Practices)
- [Launching Jobs](odyssey.md#Launching-Jobs)
- [Practice Datasets](odyssey.md#Practice-Datasets)

----
### Logging In

You can `ssh` into the cluster with the following command:

```bash
ssh username@login.rc.fas.harvard.edu
```
This will give you a login node that can be used to access different filesystems, move data around, write programs/scripts, 
and launch jobs. In general, it is best practices to not use a login node for any real computationally-intensive task and to
reserve any real work for compute nodes. If you are frequently accessing data stored in boston, it can be advantage to ssh to
`boslogin.rc.fas.harvard.edu`, or if you are frequently accessing things in holyoke you should use `holylogin.rc.fas.harvard.edu`.

----
### Personal Python Environments

The Harvard cluster does have an installation of anaconda that is available as a `module` that can be loaded (see [Python](https://docs.rc.fas.harvard.edu/kb/python/) for more details). Personally, I recommend to maintain your own conda/mamba directory in the lab isilon storage. Check this [link](https://github.com/Hekstra-Lab/room-of-requirement/blob/master/howto/move_conda.md) to see why that is the best directory. To install the latest [mamba](https://github.com/mamba-org/mamba) in your lab isilon folder, do

```bash
cd /net/holy-nfsisilon/ifs/rc_labs/hekstra_lab/people/<username>/
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash Mambaforge-Linux-x86_64.sh
```

Follow the prompts, and then you should close and re-open your shell for the changes to take effect. You can then use `conda` or `mamba` as a Python package manager. It may be advisable to run `conda init bash` in order to initialize `conda` as part of your `.bashrc`.

----
### Hekstra Lab Storage

For persistent storage of lab data or personal work, the Hekstra lab has an 8TB allocation on the cluster's Isilon filesystem. This can be accessed at:
- `/net/holy-nfsisilon/ifs/rc_labs/hekstra_lab`

For convenience, it is also aliased as:
- `/n/hekstra_lab`

This filesystem should be used for persistent storage because it is backed up to an external site on a monthly basis, and it maintains daily snapshots of the directories in case anyone needs to recover any deleted files. 

Diffraction images from past data collection trips are all stored in `/n/hekstra_lab/data`. For personal work, you should create a personal subdirectory in `/n/hekstra_lab/people`. For works that have reached some semblance of completion, a subdirectory can be made in `/n/hekstra_lab/projects`.

----
### Common Software

I have also been maintaining a directory with useful applications for crystallographic data processing in the lab's `garden`. 
This directory can be found here:
- `/n/holylfs05/LABS/hekstra_lab/Lab/garden`

I maintain relatively up-to-date versions of DIALS, XDS, phenix, and precognition in there. In order to set up your environment for running `dials` or `precognition`, use one of the following bash scripts:

```bash
# Setup DIALS environment
source /n/holylfs05/LABS/hekstra_lab/Lab/garden/dials/build/setpaths.sh
```
```bash
# Setup Precognition environment
source /n/holylfs05/LABS/hekstra_lab/Lab/garden/precognition/Precognition_5.2_distrib/setup_precognition_env.sh
```
> :warning: Both of the above environments do not play nicely with standard Python distributions.

----
### Best Practices

Although `/n/hekstra_lab` should be used for persistent storage, it is not best to use this filesystem as a working directory for any jobs requiring heavy IO. This is because there is relatively high latency between this filesystem and the compute nodes on the cluster.

For real computation, you should make a scratch directory in the lab's parent directory. I often copy any diffraction images to the scratch directory that I will be working with, because that greatly improves file latency if the files will be accessed frequently. The system administrators reserve the right to move the physical locations of the scratch directories, but by default an environment variable is set that will resolve to the current location: `$SCRATCH`. 

As such, you should make a personal subdirectory within the following for temporary data storage and work:
- `$SCRATCH/hekstra_lab`

> :warning: Files in `$SCRATCH` directories will be deleted if they have not been edited in 3 months. As such, be sure to remember to copy any useful files or results back to the lab's persistent storage when you are done with your work. 

----
### Launching Jobs

Odyssey (or Cannon, whatever it's called these days) uses Slurm as a job scheduler. Here is a general page describing how to
submit jobs on Odyssey: [Running jobs](https://docs.rc.fas.harvard.edu/kb/running-jobs/). Importantly, it also has a list of 
all the partitions available, and their general resources/constraints.

----
### Practice Datasets

If you are interested in getting started processing crystallographic data on the cluster, here are two datasets that can be useful examples:

#### 1) HEWL S-SAD
If you want to play around with data reduction in DIALS, XDS, or some other program, here is the location of a high-quality
HEWL dataset. This room-temperature dataset was collected at 24-ID-C at a low X-ray energy (6553 eV), and you should be able to solve this
structure by sulfur SAD. There are two 1440˚ passes on the crystal, and I personally processed both passes independently in DIALS, and then
merged the two passes in AIMLESS. You should also manually set the beam center to `(290.5, 225.2), and it is helpful to set a maximum resolution for 
strong spots/indexing to 25Å.

`/n/hekstra_lab/data/201907_APS_24IDC/images/301/0_0/`

#### 2) Looped DHFR Laue Dataset
This is a practice dataset for Laue data processing in Precognition. It is very high quality with low mosaicity, because the
dataset was collected with a DHFR crystal in a loop. 

`/n/hekstra_lab/data/201903_APS_BioCARS/e080`
