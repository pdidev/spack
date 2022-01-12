# PDI spack repository

This is a [spack](https://spack.io/) repository with recipes for:
[DDC](https://github.com/Maison-de-la-Simulation/ddc),
Deisa,
[Gysela](https://gyselax.github.io/),
[layout-contiguous](https://github.com/Maison-de-la-Simulation/layout-contiguous),
[PDI](https://pdi.dev) and its plugins.

Each of thiese can be installed in a few simple steps:
1. [setup spack](#step-1-setup),
2. [(optional): reuse already installed packages](#step-2-optional-reuse-already-installed-packages),
3. [(optional): setup a non-default compiler](#step-3-optional-setup-a-non-default-compiler),
4. [install](#step-4-installation):
   * [install Gysela](#gysela),
   * [install DDC](#ddc),
   * [install Deisa](#deisa),
   * [install layout-contiguous](#layout-contiguous),
   * [install PDI and most of its plugins](#pdi-and-most-of-its-plugins),
     - [install PDI Decl'SION plugin](#pdi-declsion-plugin),
     - [install PDI FTI plugin](#pdi-fti-plugin),


## Step #1: Setup

To use it, you should first setup spack:
```sh
# 1. Get and enable Spack
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
# 2. Get and enable this spack repo
git clone https://github.com/pdidev/spack.git spack/var/spack/repos/pdi
spack repo add spack/var/spack/repos/pdi
```


## Step #2 (optional): reuse already installed packages

### Option #2.1: Reuse already installed packages on super-computers that use spack

You can tell your local spack instance that there is an upstream spack instance by editing `spack/etc/spack/defaults/upstreams.yaml`.
```yaml
upstreams:
  name-of-spack-instance:
    install_tree: /path/to/spack/opt/spack
```

This will let spack use the already installed packages when it sees fit, (which is almost never).
You can however force spack to use already installed package by using the flag `--reuse` when calling `spack install`.


**For example on [Ruche](https://mesocentre.pages.centralesupelec.fr/user_doc/ruche/09_softwares/)**, you can do:
```sh
cat<<EOF > spack/etc/spack/defaults/upstreams.yaml
upstreams:
  ruche-system:
    install_tree: /gpfs/softs/spack/opt/spack/
EOF
```


### Option #2.2: Reuse already installed packages on super-computers that does not use spack

If there are packages already present on the machine that you want spack to use _e.g._ MPI, you can specify them as externals through the `packages.yaml` file found in either in a Spack installation’s `etc/spack/` or a user’s `~/.spack/` directory.  Here’s an example of an external configuration:
```yaml
packages:
  openmpi:
    externals:
    - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64"
      prefix: /opt/openmpi-1.4.3
    - spec: "openmpi@1.4.3%gcc@4.4.7 arch=linux-debian7-x86_64+debug"
      prefix: /opt/openmpi-1.4.3-debug
    - spec: "openmpi@1.6.5%intel@10.1 arch=linux-debian7-x86_64"
      prefix: /opt/openmpi-1.6.5-intel
```
Is it recommended to only put MPI implementations, CMake and `openssl` as externals and let spack take care of the rest.


## Step #3 (optional): setup a non-default compiler

For compilers, you can specify them in the user's `~/.spack/linux/compilers.yaml`. 
```yaml
compilers:
- compiler:
    spec: gcc@4.8.5
    paths:
      cc: /usr/bin/gcc
      cxx: /usr/bin/g++
      f77: /usr/bin/gfortran
      fc: /usr/bin/gfortran
    flags: {}
    operating_system: centos7
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
```

This can be done automatically by calling `spack compiler find` when the compilers are loaded.
This is needed if you want to use the Intel compilers. 


**For example on [Ruche](https://mesocentre.pages.centralesupelec.fr/user_doc/ruche/09_softwares/)**, you can do:
```sh
spack load gcc@9.2.0
spack compiler find
spack unload gcc@9.2.0
```


## Step #4: Installation

Then depending on what you want to install, go to the following:
* [install Gysela](#gysela),
* [install DDC](#ddc),
* [install Deisa](#deisa),
* [install layout-contiguous](#layout-contiguous),
* [install PDI and most of its plugins](#pdi-and-most-of-its-plugins),
  - [install PDI Decl'SION plugin](#pdi-declsion-plugin),
  - [install PDI FTI plugin](#pdi-fti-plugin),


### DDC

You can install [DDC](https://github.com/Maison-de-la-Simulation/ddc) using the following instructions after you've [done the setup](#setup):
```sh
# Install DDC
spack install ddc
```


### Deisa

You can install Deisa using the following instructions after you've [done the setup](#setup):
```sh
# Install Deisa
spack install deisa
```


### Gysela

#### Gysela Options

Before installing Gysela, you choose select the set of options that suit you by adding elements to your spec:
* `build_type=X` to specify build type, valid values are `'Release', 'Timed', 'Deterministic', 'Debug' and 'Scorep'` (defaults to `Release`),
* `+pdi` for compilation with PDI for IOs (defaults to `off`),
* `gysela_dir=/path/to/put/gysela` to choose where to install Gysela (defaults to `$HOME/gysela`).
This information is also available by doing `spack info gysela`. 

Gysela sometimes has issues when lapack is provided by open-blas.
It is thus recommended to add `^intel-mkl` (or `^netlib-lapack`) when calling spack install.

To check what you will actually install, you can run:
```sh
# Get info about what you will install with Gysela
spack solve gysela ${SPEC_ELEMENTS}
```

#### Gysela Installation proper

**Warning:** 
Since Gysela is not publicly available for download, you will need a ssh key properly installed to download it.

You can install Gysela using the following instructions after you've [done the setup](#setup):
```sh
# Install Gysela
spack install gysela ${SPEC_ELEMENTS}
```


**For example on [Ruche](https://mesocentre.pages.centralesupelec.fr/user_doc/ruche/09_softwares/)**, you can do:
```sh
# Install Gysela
export GYSELA_INSTALLDIR="${HOME}/gysela_spack"
spack install --reuse gysela %gcc@9.2.0 +pdi "gysela_dir=${GYSELA_INSTALLDIR}" "^intel-mkl"
```

#### Execution of spack-installed Gysela

To actually run Gysela you need to move to the installation directory selected in the previous section and load the module.

```sh
# move to the installation directory
cd "${GYSELA_INSTALLDIR}/wk"
# load the appropriate spack modules
spack load gysela
# now you can run
./subgys
```


### layout-contiguous

You can install [layout-contiguous](https://github.com/Maison-de-la-Simulation/layout-contiguous) using the following instructions after you've [done the setup](#setup):
```sh
# Install layout-contiguous
spack install layout-contiguous
```


### PDI and most of its plugins

You can install PDI and most of its plugins using the following instructions after you've [done the setup](#setup):
```sh
# Install PDI and most of its plugins
spack install pdiplugin-decl-hdf5 pdiplugin-decl-netcdf pdiplugin-flowvr pdiplugin-mpi pdiplugin-pycall pdiplugin-serialize pdiplugin-set-value pdiplugin-trace pdiplugin-user-code
```

If you only need some of the plugins, you can adapt the last line.


#### PDI Decl'SION plugin

PDI Decl'SION plugin depends on the [SIONlib recipe](https://gitlab.jsc.fz-juelich.de/cstao-public/SIONlib/spack-repository).
To install it, you need to use the following instructions after you've [done the setup](#setup):
```sh
# 1. Get SIONlib spack repo
git clone https://gitlab.jsc.fz-juelich.de/cstao-public/SIONlib/spack-repository.git spack/var/spack/repos/SIONlib
spack repo add spack/var/spack/repos/SIONlib
# 2. Install decl-sion plugin
spack install pdiplugin-decl-sion
```


#### PDI FTI plugin

PDI FTI plugin depends on the [FTI recipe](https://github.com/leobago/fti-spack).
To install it, you need to use the following instructions after you've [done the setup](#setup):
```sh
# 1. Get SIONlib spack repo
git clone https://github.com/leobago/fti-spack spack/var/spack/repos/FTI
spack repo add spack/var/spack/repos/FTI
# 2. Install fti plugin
spack install pdiplugin-fti
```
