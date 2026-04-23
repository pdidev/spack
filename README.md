# PDI spack repository

This is a [spack](https://spack.io/) repository with recipes for [PDI](https://pdi.dev) and its plugins.
It can be installed in just two steps: 1. [setup spack](#setup-spack) and 2. [install](#install-pdi).

## Setup Spack

To use it, you should first setup spack:
```sh
# 1. Get and enable Spack
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
# 2. Get and enable this spack repo
git clone https://github.com/pdidev/spack.git spack/var/spack/repos/pdi
spack repo add spack/var/spack/repos/pdi
```

## Install PDI

You can install PDI and most of its plugins using the following instructions after you've [done the setup](#setup):
```sh
# Install PDI and most of its plugins
spack install pdiplugin-decl-hdf5 pdiplugin-decl-netcdf pdiplugin-mpi pdiplugin-pycall pdiplugin-serialize pdiplugin-set-value pdiplugin-trace pdiplugin-user-code
```

If you only need some of the plugins, you can adapt the last line.
