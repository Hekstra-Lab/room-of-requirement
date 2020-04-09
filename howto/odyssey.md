# Working on the Harvard Cluster

### Logging in
You can `ssh` into the cluster with the following command:

```bash
ssh username@login.rc.fas.harvard.edu
```
This will give you a login node that can be used to access different filesystems, move data around, write programs/scripts, 
and launch jobs. In general, it is best practices to not use a login node for any real computationally-intensive task and to
reserve any real work for compute nodes. 

### Launching jobs
Odyssey (or Cannon, whatever it's called these days) uses Slurm as a job scheduler. Here is a general page describing how to
submit jobs on Odyssey: [Running jobs](https://docs.rc.fas.harvard.edu/kb/running-jobs/). Importantly, it also has a list of 
all the partitions available, and their general resources/constraints.

### Hekstra lab filesystems and useful directories
There are two filesystems that can be used for persistent data storage. The `ifs` filesystem can be convenient for long-term
storage of data that you would like to access outside of the cluster. This filesystem can be mounted on your local computer. 
The `lfs` filesystem has better performance, and is the preferred location for long-term storage of data that you will be 
accessing for doing real computation. I have been using `lfs` for the main storage of diffraction images, although images from
a few trips are stored on `ifs`.

Persistent data storage:
- `/n/holylfs/LABS/hekstra_lab`
- `/net/rcstorenfs02/ifs/rc_labs/hekstra_lab`

For real computation, you should make a scratch directory in the lab's parent directory. I often copy any diffraction images
to the scratch directory that I will be working with, because that greatly improves file latency if the files will be accessed
frequently. The system administrators reserve the right to move the physical locations of the scratch directories, but by default
an environment variable is set that will resolve to the current location: `$SCRATCH`.

Temporary data storage and work:
- `$SCRATCH/hekstra_lab`

I have also been maintaining a directory with useful applications for crystallographic data processing in the lab's `garden`. 
This directory can be found here:
- `/n/holylfs/LABS/hekstra_lab/garden`

I maintain relatively up-to-date versions of DIALS, XDS, phenix, and precognition in there. In order to set up your environment for
running `dials` or `precognition`, use one of the following bash scripts:

```bash
# Setup DIALS environment
source /n/holylfs/LABS/hekstra_lab/garden/dials/build/setpaths.sh

# Setup Precognition environment
source /n/holylfs/LABS/hekstra_lab/garden/precognition/Precognition_5.2_distrib/setup_precognition_env.sh
```

Just a warning... both of the above environments do not play nicely with standard Python distributions.

### Practice Datasets

#### 1) HEWL S-SAD
If you want to play around with data reduction in DIALS, XDS, or some other program, here is the location of a high-quality
HEWL dataset. This room-temperature dataset was collected at 24-ID-C at a low X-ray energy (6553 eV), and you should be able to solve this
structure by sulfur SAD. There are 1440˚ passes on the crystal, and I personally processed both passes independently in DIALS, and then
merged the two passes in AIMLESS. You should also manually set the beam center to 290.5, 225.2, and it is helpful to set a maximum resolution for 
strong spots/indexing to 25Å.

`/n/holylfs/LABS/hekstra_lab/data/201907_APS_24IDC/images/301/0_0/`

#### 2) Looped DHFR Laue Dataset
This is a practice dataset for Laue data processing in Precognition. It is very high quality with low mosaicity, because the
dataset was collected with a DHFR crystal in a loop. 

`/n/holylfs/LABS/hekstra_lab/data/201903_APS_BioCARS/e080`
