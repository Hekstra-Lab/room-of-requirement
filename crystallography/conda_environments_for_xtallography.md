# Mamba environments on the cluster for crystallographic data analysis

This note describes how to set up a Mamba environment for crystallographic data analysis on the cluster. Previous instructions used Conda; we now use Mamba, which is faster and is provided by FASRC through the Python module.

## Setup

Load the FASRC Python module to make Mamba available:

```bash
module load python
```

Create and activate `xtalenv1` with Python 3.12, then install `careless` with CUDA support:

```bash
mamba create -n xtalenv1 python=3.12
mamba activate xtalenv1
pip install --upgrade pip
pip install 'careless[cuda]'
```

## Add Hekstra Lab packages to `xtalenv1`

Create a `packages` directory to keep local repositories used for editable installations in one place:

```bash
mkdir packages
cd packages
mamba install -c conda-forge pip
```

Clone `cog` and install it as an editable package:

```bash
git clone https://github.com/Hekstra-Lab/cog.git
cd cog
pip install -e .
cd ..
```

Install `cctbx`, `regroup`, and `marccd` into `xtalenv1`:

```bash
mamba install -c conda-forge cctbx
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

## Future sessions

The environment only needs to be created once. For future sessions, load Python and activate the existing environment:

```bash
module load python
mamba activate xtalenv1
```

