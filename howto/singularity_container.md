### How to set your own singularity containers on RC cluster

These are instructions to get singularity containers with your personalized environment on the RC cluster. We are trying to wrap all conda binaries within a singularity container in the `tier0` storage, for two reasons:

1. Compared with your home directory, `tier0` stroage has much lower latency to call when you are working on a computing node. About **5s to 0.7s**, including the container latency. 

2. `tier0` has a strict inodes limit at about 1M. As a reference, I have about 300k small files in my `miniconda3` folder. So it is not pratical for everyone in lab to directly move all their binaries into `tier0`

I have created a singularity image with `reciprocalspaceship` and `jupyter` at `/n/holylfs05/LABS/hekstra_lab/Lab/garden/singularity_images/rs_jupyter.sif`. I will show the steps to create sif file as an example below.

There are plenty of ways to build a singularity image, like building remotely with a definition file or with [docker2singularity](https://github.com/singularityhub/docker2singularity). What i am using here might not be the least painful approach, but I feel it important that you can test the environment intereactively when you build it. 

If you only want to use the existing singularity image, go to the section 4.

#### Prerequisites

You need to have [docker]https://www.docker.com/products/personal/) installed locally and have a valid dockerhub account.

#### 1. Build your environment container with docker locally

At your local command line

```
# 1. Start with a base image
> docker pull continuumio/miniconda3

# 2. run the image
> docker run -it continuumio/miniconda3

# 3. Now you should be inside the container, build your own environment
> pip install reciprocalspaceship
> pip install jupyter
> apt update
> apt -y install netcat
```

The `netcat` package is used to do an automatic search of ports for jupyter.

#### 2. Commit the container into a docker image and push to dockerhub

Follow the above steps

```
> exit
> docker ps -a
> docker commit -m "message" -a "username" <container ID> username/reponame:tag
> docker push username/reponame:tag
```

#### 3. Build the singularity image on the cluster side

Now at the cluster command line, cd into your disired path

```
singularity build --docker-login <imagename.sif> docker://username/reponame:tag
```


#### 4. Start the container and open a jupyter lab inside

Then you can run the container image file with

```
singularity shell <imagename.sif>
```

To open a jupyter lab, within the singularity shell:
```
for myport in {6818..11845}; do ! nc -z localhost ${myport} && break; done
echo "ssh -NL $myport:$(hostname):$myport $USER@login.rc.fas.harvard.edu"
jupyter-notebook --no-browser --port=$myport --ip='0.0.0.0'
```

In a new terminal on your lcoal machine, connect to the cluster using an output of your echo above command, for example

```
ssh -NL 6820:holy7c05314.rc.fas.harvard.edu:6820 user@login.rc.fas.harvard.edu
```

Then in your workstation/laptop browser. Make sure to copy the token from the Jupyter notebook server and update the token below.

### References

1. [Build singularity from docker containers](https://sylabs.io/guides/3.0/user-guide/singularity_and_docker.html)

2. [FASRC singularity tutorial](https://docs.rc.fas.harvard.edu/wp-content/uploads/2021/11/Singularity_Nov_2021.pdf)

3. [FASRC singularity documentation](https://docs.rc.fas.harvard.edu/kb/singularity-on-the-cluster/)

4. [Install netcat on Debian](https://installati.one/debian/10/netcat/)

