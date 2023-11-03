Careless requires `tensorflow` to run. 

Due to the new cluster and also compatibility woes for `tensorflow`, I followed fixes [here](https://github.com/fasrc/User_Codes/blob/master/AI/TensorFlow/README.md)
Up to the heading: **Pull a TF singularity container**. This link is the FASRC cluster's guide to installing tensorflow on the Rocky 8 OS. 

In the `mamba create` command in the instructions, I install careless as well: 

`mamba create -n tf2.12_cuda11 python=3.10 pip numpy six wheel scipy pandas matplotlib seaborn h5py jupyter jupyterlab careless`


Sometimes, `cuda-nvcc` must be installed: 
```
conda install -c nvidia cuda-nvcc
```
To check that tensorflow can connect to the GPU, after activating your mamba environment with tensorflow in it: 

First open an iPython session. 
```
$ ipython
```
Then run:
```
import tensorflow as tf
tf.config.list_physical_devices('GPU')
```

The output should read:

```
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```
Whereas if there is no GPU, the output reads:
```
[]
```

