Careless requires `tensorflow` to run. 

Due to the new cluster and also compatibility woes for `tensorflow`, I followed fixes [here](https://github.com/fasrc/User_Codes/blob/master/AI/TensorFlow/README.md)
Up to the heading: **Pull a TF singularity container**. This link is the FASRC cluster's guide to installing tensorflow on the Rocky 8 OS. 

When these instructions tell you to install `tensorflow`, add `careless` to the command:
```bash
(tf2.12_cuda11) $ pip install --upgrade tensorflow==2.12.* careless tensorflow-probability==0.20.0
```
This ordering is important; `careless` installation brings `tensorflow` along with it, so doing it this way ensures minimal divergence from the instructions. Additionally, the instructions are tailored to `tensorflow 2.12`, but if you install `careless` without specification, you'll get the latest `tensorflow` (`2.15` or something). `careless` only calls for `>=2.8`, so `2.12` is totally fine!

Sometimes, `cuda-nvcc` must be installed: 
```bash
conda install -c nvidia cuda-nvcc
```
To check that tensorflow can connect to the GPU, after activating your mamba environment with tensorflow in it: 

First open an iPython session. 
```bash
$ ipython
```
Then run:
```python
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

