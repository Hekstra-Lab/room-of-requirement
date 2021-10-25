### How to get a _good_ version of vim on the cluster
These are instructions to get a version of vim on the cluster with X11 clipboard support, python3, and jedi-vim. 
Firstly, deactivate conda so you drop down to the base python3 install on the cluster.
This is important, because this version has access to python devtools.
Then compile vim with this script:

```bash
#!/bin/bash
#
#SBATCH -p shared # partition (queue)
#SBATCH -N 1 # a single node
#SBATCH -n 4 # four cores
#SBATCH --mem 12G # memory pool for all cores
#SBATCH -t 0-2:00 # time (D-HH:MM)


INSTALL_DIR=/n/home04/kmdalton/opt
NPROC=4

# Modern gcc
module load gcc/10.2.0-fasrc01

cd $INSTALL_DIR

git clone https://github.com/vim/vim.git
cd vim/src

make distclean #This is just in case
./configure --with-features=huge \
    --enable-multibyte \
    --prefix=$INSTALL_DIR \
    --enable-python3interp \
    --with-python-config-dir=$(python3-config --configdir)  | tee config_log.txt

make 
make -j $NPROC install

PURPLE='\033[0;35m'
NC='\033[0m'
echo -e "${PURPLE}Add the following line to your .bashrc to use this version of vim:${NC}"
echo "export PATH=$INSTALL_DIR/bin:\$PATH"
```

Add the `$INSTALL_DIR/bin` to your path. 

Next, activate the conda environment you plan to use with vim (for me this is `careless`). 
Then use the next script to install jedi, pathogen, and jedi-vim. 

```bash
# Install latest jedi python autocomplete library
pip install --upgrade jedi

# Install Pathogen vim plugin manager
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

# Install jedi-vim python autocompletion library for vim
git clone --recursive https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim

PURPLE='\033[0;35m'
NC='\033[0m'
echo -e "${PURPLE}Prepend your .vimrc with the following line:${NC}"
echo "execute pathogen#infect()"
```

Finally, add "execute pathogen#infect()" to the beginning of your `.bashrc`. 
