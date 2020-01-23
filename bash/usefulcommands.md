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

