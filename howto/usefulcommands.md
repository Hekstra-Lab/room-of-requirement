# Useful Commands in `bash`
Collective memory for how we overcame issues on the Harvard cluster

### Setting Default Permissions

If you are collaborating with people in a directory, it is often useful to
make sure that file permissions are inherited such that new folders have
read/write permissions to everyone in a UNIX group. Here is how you do that.

Let's say you have a directory called `projects/`:

```
mkdir projects
```

We can make sure that the directory has the correct permissions, and then we
can use `setfacl` to change the default permissions for any new files and subdirectories:

```
chmod g+rwx projects
setfacl -d -m g::rwx projects
```

### Transferring files

The `rsync` command is a useful way to transfer files. `rsync` makes one folder match another folder, with the syntax 

```
rsync [source] [destination]
```

As with all `bash` commands, it's often useful to take a peek at the manual (`man rsync`) or the help message (`rsync --help`) but my goal here is to compile some of the more useful options and tricks.

#### Common `rsync` flags

 - `-v` (verbose): print out what files are being transferred
 - `--progress`: also print out the transfer status of the current file
 - `-r` (recursive): copy directories and their contents as well
 - `--partial`: If the job is interrupted in the middle of transferring a file, continue with that file upon resuming

```
tmux
salloc -p serial_requeue --mem 20G -t 9-00:00
rsync -rlvhtgoD --log-file="~/rsynclog.log" --progress --partial --exclude "*.cbf" hekstra@smbcopy.slac.stanford.edu:/data/hekstra/20220506_BL12_1/ /n/hekstra_lab/data/20220506_SSRL_BL12_1/
```
and then detach, `CTRL + B` + `D`
