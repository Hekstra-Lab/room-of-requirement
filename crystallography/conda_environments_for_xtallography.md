# Conda environments on the cluster for crystallographic data analysis

This note is for setting up conda environments on the cluster for crystallographic data analysis. 
The first part is intended to supersede [past instructions](https://github.com/Hekstra-Lab/room-of-requirement/blob/master/crystallography/run_careless_rocky8.md) 
for careless installation on the cluster. 

How to set up conda environments on the cluster from scratch for Laue data processing:


go to `/n/hekstra_lab/people/<your directory>`

run the following code to set up `careless` with `tensorflow` configured correctly:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -p `readlink -f .`/anaconda
source anaconda/etc/profile.d/conda.sh
conda init
conda create -yn careless python=3.10
conda activate careless
pip install --upgrade pip
pip install tensorflow[and-cuda]
pip install careless
```

after doing this, you may have to delete stuff in your `~/.bashrc` from previous `conda init` calls, as well as local directories. 
We can also check the `careless` installation by opening up a gpu node and checking the output as in the 
[previous instructions](https://github.com/Hekstra-Lab/room-of-requirement/blob/master/crystallography/run_careless_rocky8.md).


Next, let's make a folder for Hekstra lab packages, and add them to a separate `conda` environment for Laue data processing. 
This code block includes `cog`,`regroup`,`marccd`,`rs-booster`, and `reciprocalspaceship`. I like to install `rs-booster` and `cog` as editable. 

```
mkdir packages
cd packages
conda create -n laue
conda install -c conda-forge pip

git clone https://github.com/Hekstra-Lab/cog.git
cd cog
pip install -e .
cd ..
conda install -c conda-forge cctbx
pip install git+https://github.com/Hekstra-Lab/regroup.git
pip install git+https://github.com/Hekstra-Lab/marccd.git
pip install git+https://github.com/Hekstra-Lab/marccd.git

git clone https://github.com/rs-station/rs-booster.git
cd rs-booster
python -m pip install -e .
cd ..
```
