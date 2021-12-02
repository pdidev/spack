# GYSELA-X's spack recipe

You can install GYSELA and most of its plugins using the following instructions:

```sh
# 1. Get Spack
$ git clone https://github.com/spack/spack.git
$ . spack/share/spack/setup-env.sh
# 2. Get PDI-GYSELA spack repo
$ git clone https://github.com/pdidev/spack.git spack/var/spack/repos/pdi
$ spack repo add spack/var/spack/repos/pdi
# 3. Install gysela (You'll need to know your gitlab username and password)
$ spack install gysela
``` 

When that is done to actually run gysela you need to load the approriate modules

```sh
# Load the approriate spack modules
$ spack load gysela
```


Everything else should be as expected for former gysela users. 

---

Options for installation are :
* `build_type=X` to specify build type. Values are `'Release', 'Timed', 'Deterministic', 'Debug' and 'Scorep'`, defaults to `Release`
* `+pdi` for compilation with PDI for IOs default `off`
* `+pycall` for use of the `pdi-pycall` plugin, requires `+pdi`.
* `gysela_dir=/path/to/desired/installation/dir` defaults to `$HOME/gysela`.


This information is also available by doing `spack info gysela`. 

---

#### If you are working on a supercomputer with packages already present :

##### Option 1: This super computer uses spack
You can tell your local spack instance that there is an upstream spack instance by editing `spack/etc/spack/defaults/upstreams.yaml`.
```yaml
upstreams:
  name-of-spack-instance:
    install_tree: /path/to/spack/opt/spack
```
This will let spack use the already installed packages when it sees fit, which is almost never. You can however force spack to use already installed package by using the flag `--reuse` when calling `spack install`. It is important to note that this is not recommended. Refer to the next section to add packages in a case by case fashion.


#### Option 2: Other cases
If there are packages already present on the machin that you want spack to use _e.g._ MPI, you can specify them as externals through the `packages.yaml` file found in either in a Spack installation’s `etc/spack/` or a user’s `~/.spack/` directory.  Here’s an example of an external configuration:
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
This can be done automatically by calling `spack compiler find` when the compilers are loaded. This is needed if you want to use the Intel compilers. 


## Important Note
---
In its current state, gysela isn't really fit to be a spack package. Currently, it only works because of a forceful copy of the temporary build directory in the user specified path. This means that the spack directory is completely empty. Yet you shouldn't call `spack uninstall gysela` because of the `spack load gysela` it provides.

### Latest Successful configuration with pdi:
Done on the ruche cluster on 02/12/2021:

Command : `spack install gysela +pdi ^openmpi ^netlib-lapack`
Full dependency tree :
```sh
gysela@develop~ipo+pdi~pycall build_type=Release gysela_dir=/gpfs/users/lavandiera/gysela
    netlib-lapack@3.9.1~external-blas~ipo+lapacke+shared~xblas build_type=RelWithDebInfo
    openmpi@4.0.2~atomics~cuda+cxx+cxx_exceptions+gpfs~internal-hwloc~java~legacylaunchers~lustre~memchecker+pmi+pmix~singularity~sqlite3+static~thread_multiple+vt~wrapper-rpath fabrics=psm2 patches=073477a76bba780c67c36e959cd3ee6910743e2735c7e76850ffba6791d498e4,60ce20bc14d98c572ef7883b9fcd254c3f232c2f3a13377480f96466169ac4c8 schedulers=slurm
    pdi@1.4.3~docs+fortran~ipo+python~tests build_type=RelWithDebInfo
        paraconf@0.4.9+fortran~ipo+shared~tests build_type=RelWithDebInfo
            libyaml@0.2.5
        py-pybind11@2.8.1~ipo build_type=RelWithDebInfo
            python@3.8.12+bz2+ctypes+dbm~debug+libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4+uuid+zlib patches=0d98e93189bc278fbc37a50ed7f183bd8aaf249a8e1670a465f0db6bb4f8cf87,4c2457325f2b608b1b6a2c63087df8c26e07db3e3d493caf36a56f0ecf6fb768,f2fd060afc4b4618fe8104c4c5d771f36dc55b1db5a4623785a4ea707ec72fb4
                bzip2@1.0.8~debug~pic+shared
                expat@2.4.1+libbsd
                    libbsd@0.11.3
                        libmd@1.0.3
                gdbm@1.19
                    readline@8.1
                        ncurses@6.2~symlinks+termlib abi=none
                gettext@0.21+bzip2+curses+git~libunistring+libxml2+tar+xz
                    libiconv@1.16 libs=shared,static
                    libxml2@2.9.12~python
                        xz@5.2.5~pic libs=shared,static
                        zlib@1.2.11+optimize+pic+shared
                    tar@1.34
                libffi@3.3 patches=26f26c6f29a7ce9bf370ad3ab2610f99365b4bdd7b82e7c31df41a3370d685c0
                openssl@1.1.1l~docs certs=system
                sqlite@3.36.0+column_metadata+fts~functions~rtree
                util-linux-uuid@2.36.2
        spdlog@1.9.2~ipo+shared build_type=RelWithDebInfo
    pdiplugin-decl-hdf5@1.4.3+fortran~ipo~mpi~tests build_type=RelWithDebInfo
        hdf5@1.10.7~cxx~fortran~hl~ipo~java+mpi+shared~szip~threadsafe+tools api=default build_type=RelWithDebInfo
            pkgconf@1.8.0
    pdiplugin-mpi@1.4.3~ipo~tests build_type=RelWithDebInfo
    pdiplugin-set-value@1.4.3~ipo~tests build_type=RelWithDebInfo
    pdiplugin-trace@1.4.3~ipo~tests build_type=RelWithDebInfo
    pdiplugin-user-code@1.4.3~ipo~tests build_type=RelWithDebInfo
    py-numpy@1.21.4+blas+lapack patches=873745d7b547857fcfec9cae90b09c133b42a4f0c23b6c2d84cf37e2dd816604
        py-setuptools@59.4.0

```