## How to move your binaries to places with lower latency

These are instructions to move your binaries (like conda or other python environments) to paths with lower latency. Most people by default put their conda folders in personal home directory (like `n/home0*/username`) in Boston data center. However, according to the [diagram](https://docs.rc.fas.harvard.edu/wp-content/uploads/2022/03/FAS-RC-Network-Diagram-24-March-2022.png), most computing nodes live in Holyoke data center. So when you reqeust computing resources and start jobs on holyoke computing nodes, every time you call a function in your conda environment, you have to communicate between boston data center and holyke center which is of high latency. This latency is extremely sensible when you start a new python kernal, or get an error and have to trace back, which is common and annoying. So it is necessary to find a better home for our conda files and other binaries. 

### 1. Where to Move?

Fortunately, we have two more lab storage paths in holyoke data center, the `holy-isilon` permenant storage and `holy-scratch` fast-io storage (`tier0` is also good but not suitable for conda files due to small inodes limits). Here is the stats of latency after moving conda files to these paths, test with `time ipython --version` on `holygpu2c0701` node:

|  | home directory  | holy-isilon  | holy-scratch  |
|:-:|:-:|:-:|:-:|
| latency  |  ~5.7s | ~0.89s |  ~0.56s |

Both lab storages could give much lower latency. However, although `holy-scratch` gives lower latency, **`holy-isilon` is more recommended**. because `holy-scartch` is a fast-io path where files will be cleaned if not touched for 90 days. It is not appropriate to move comparatively stable environment files to `holy-scratch` or you have to touch all files every 90 days.

So conclusion: as a good cluster citizen who wants lower latency, move your conda files to `holy-isilon` lab permenant storage.

For our hekstra lab, the path is: `/net/holy-nfsisilon/ifs/rc_labs/hekstra_lab/people/username/`

### 2. How to move?

If you want to keep you current conda files:

1. Move you conda folde to target path, for example:
   ```bash
   rsync -avp ~/miniconda3 <holy-scratch path>/miniconda3
   ```
   This will do copy with progress bar. You can clean the origin folder after this is done.

2. Change the conda init block in `~/.bashrc` to:
   ```bash
   if [[ $(hostname) != *login* ]]; then
    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('<holy-scratch path>/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
    else
        if [ -f "<holy-scratch path>/miniconda3/etc/profile.d/conda.sh" ]; then
            . "<holy-scratch path>/miniconda3/etc/profile.d/conda.sh"
        else
            export PATH="<holy-scratch path>/miniconda3/bin:$PATH"
        fi
    fi
    unset __conda_setup
    # <<< conda initialize <<<
    fi
   ```
   This `if` block makes `conda init` only happen when you are not on a login node, as it is now slow to call conda on a boston login node.
   
3. Alternatively, you can leave the `~/.bashrc` unchanged and make a symbolic link in your home directory with the same name pointing to your new holy-scratch folder, like:
    ```bash
    ln -s <holy-scratch path>/miniconda3/ ~/miniconda3
    ```

If you want to install the conda from sractch (not tested): 

1. Choose whatever conda version you like (anaconda, miniconda, mamba...), download the binary

2. Install the conda binary to your `holy-scratch` path with `-PREFIX` flag, for example:
   
   ```bash
   bash ***conda***.sh -p <holy-scratch path>/<conda_folder_name>/
   ```

3. Run conda init 
