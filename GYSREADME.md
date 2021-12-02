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