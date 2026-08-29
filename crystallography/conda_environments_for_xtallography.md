# Mamba environments on the cluster for crystallographic data analysis

This note describes how to set up a Mamba environment for crystallographic data analysis on the cluster. Previous instructions used Conda; we now use Mamba, which is faster and is provided by FASRC through the Python module.

## Setup

Load the FASRC Python module to make Mamba available:

```bash
module load python
```

To make Mamba available automatically in future sessions, add the Python module to your `~/.bashrc`:

```bash
echo 'module load python' >> ~/.bashrc
```

This only needs to be done once. In future login sessions, the Python module will be loaded automatically.

Create `xtalenv1` with Python 3.12, NumPy 1.26, and CCTBX, then activate the environment:

```bash
mamba create -n xtalenv1 python=3.12 numpy=1.26 cctbx -c conda-forge
mamba activate xtalenv1
```

NumPy is constrained to version 1.26 because `marccd 0.3` requires NumPy `<2.0`. Installing CCTBX together with the NumPy constraint allows Mamba to resolve compatible versions of the scientific Python dependencies.

Upgrade `pip` and install `careless` with CUDA support:

```bash
pip install --upgrade pip
pip install 'careless[cuda]'
```

## Add Hekstra Lab packages to `xtalenv1`

Local repositories used for editable installations should be stored in persistent Tier 1 lab storage. Navigate to your directory in the Hekstra Lab Tier 1 storage and create a `packages` directory:

```bash
cd /n/lab_storage/hekstra_lab/people/<your directory>
mkdir packages
cd packages
```

Clone `cog` and install it as an editable package:

```bash
git clone https://github.com/Hekstra-Lab/cog.git
cd cog
pip install -e .
cd ..
```

Install `regroup` and `marccd` into `xtalenv1`:

```bash
pip install git+https://github.com/Hekstra-Lab/regroup.git
pip install git+https://github.com/Hekstra-Lab/marccd.git
```

Clone `rs-booster` and install it as an editable package:

```bash
git clone https://github.com/rs-station/rs-booster.git
cd rs-booster
python -m pip install -e .
cd ..
```

## Check the installation

Check that the installed Python packages have compatible dependencies:

```bash
pip check
```

A correctly resolved installation should report:

```text
No broken requirements found.
```

## Future sessions

Because `module load python` is in your `~/.bashrc`, Mamba will be available automatically in future sessions. You only need to activate the existing environment:

```bash
mamba activate xtalenv1
```

