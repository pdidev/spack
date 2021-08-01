# PDI spack repository

This is a [spack](https://spack.io/) repository with recipes for PDI, its plugins and dependencies.

## Usage

You can install PDI and most of its plugins using the following instructions:

```
# 1. Get Spack
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
# 2. Get PDI spack repo
git clone https://github.com/pdidev/spack.git spack/var/spack/repos/pdi
spack repo add spack/var/spack/repos/pdi
# 3. Install PDI and its plugins
spack install pdiplugin-decl-hdf5 pdiplugin-decl-netcdf pdiplugin-flowvr pdiplugin-mpi pdiplugin-pycall pdiplugin-serialize pdiplugin-set-value pdiplugin-trace pdiplugin-user-code
```

If you only need some of the plugins, you can adapt the last line.

### Decl'SION

The Decl'SION plugin depends on the [SIONlib recipe](https://gitlab.jsc.fz-juelich.de/cstao-public/SIONlib/spack-repository).
To install it, you need to run the following lines after the previous ones:
```
# 4. Get SIONlib spack repo
git clone https://gitlab.jsc.fz-juelich.de/cstao-public/SIONlib/spack-repository.git spack/var/spack/repos/SIONlib
spack repo add spack/var/spack/repos/SIONlib
# 5. Install decl-sion plugin
spack install pdiplugin-decl-sion
```

### FTI

The FTI plugin depends on the [FTI recipe](https://github.com/leobago/fti-spack).
To install it, you need to run the following lines after the previous ones:
```
# 4. Get SIONlib spack repo
git clone https://github.com/leobago/fti-spack spack/var/spack/repos/FTI
spack repo add spack/var/spack/repos/FTI
# 5. Install fti plugin
spack install pdiplugin-fti
```
