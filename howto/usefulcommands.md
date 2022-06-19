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

### `rsync`

The `rsync` command is a useful way to transfer files. `rsync` makes one folder match another folder, with the syntax 

```
rsync [source] [destination]
```

#### `rsync` with remote servers

When using `rsync` to grab data off a remote server, the syntax is as follows:

```
rsync username@remote.login.place:/path/to/remote/data /path/to/local/data
```

Note the colon after the domain name, and the leading slash on the remote path.

#### Useful `rsync` things to know

As with all `bash` commands, it's often useful to take a peek at the manual (`man rsync`) or the help message (`rsync --help`). Here are some options and tricks you're likely to use (some of which appear in the command below)

 - `-v` (verbose): print out what files are being transferred
 - `--progress`: also print out the transfer status of the current file
 - `-r` (recursive): copy directories and their contents as well
 - `--partial`: If the job is interrupted in the middle of transferring a file, continue with that file upon resuming
 - `--log-file="filename"`: print the `rsync` log to this file. I believe this file must already exist.

#### `tmux` for background transfers

I think that `tmux` is installed by default on the cluster, though I honestly don't remember. If not, or if you're doing this on your personal computer, see installation instructions [here](https://github.com/tmux/tmux/wiki/Installing). All you should need to know about `tmux` to pull off the below is:

 - type `tmux` to begin a new session
 - Press `CTRL + B` and then press `D` to "detach," e.g., leave the `tmux` session but keep it running.

It is important to use the `serial_requeue` partition for your `salloc` job. I won't get into details, but this is good cluster etiquette, and also lets you create a 9-day-long job! [Read more](https://docs.rc.fas.harvard.edu/kb/running-jobs/). This does mean there is a non-zero chance that your job gets killed at some point; that's ok, just repeat these instructions to continue it. When I did this the first time, it ran the whole 9 days!

The alphabet soup of `rsync` options in the below command is everything that makes up `-a` (archive mode), except the part that lets you preserve permissions, because that seems to make `rsync` mad. Feel free to `rsync --help` to figure out for yourself what they all mean and/or troubleshoot as necessary. Finally, as best I can tell, the logfile specified must already exist; `rsync` won't create a new file for you.

In all:

```
tmux
```

Inside your `tmux` session:

```
salloc -p serial_requeue --mem 20G -t 9-00:00
rsync -rlvhtgoD --log-file="[filename]" --progress --partial --exclude "*.cbf" hekstra@smbcopy.slac.stanford.edu:/data/hekstra/[folder]/ /n/hekstra_lab/data/[folder]/
```

and then detach, `CTRL + B` + `D`

You will not be able to get back into this session to see your job running. However, you can (and should!):

 - confirm via `squeue` that your job is still running, and/or
 - confirm via a `du` command of some type that your destination directory is increasing in size, and/or
 - confirm via your logfile that stuff is happening.

It is possible that setting up email notifications about job status isn't that difficult?
