# PDI spack repository

This is a [spack](https://spack.io/) repository with recipes for PDI, its plugins and dependencies.

The Decl'SION plugin depends on the SIONlib recipe available from https://gitlab.version.fz-juelich.de/SIONlib/spack-repository

## Usage

You can install PDI and all its plugins using the following instructions:

```
# 1. Get Spack
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
# 3. Get SIONlib spack repo
git clone https://gitlab.version.fz-juelich.de/SIONlib/spack-repository.git spack/var/spack/repos/SIONlib
spack repo add spack/var/spack/repos/SIONlib
# 3. Get PDI spack repo
git clone https://github.com/pdidev/spack.git spack/var/spack/repos/pdi
spack repo add spack/var/spack/repos/pdi
# 4. Find already installed dependencies
spack external find --not-buildable
# 5. Install PDI and its plugins
spack install pdiplugin-decl-hdf5 pdiplugin-decl-sion pdiplugin-mpi pdiplugin-pycall pdiplugin-trace pdiplugin-user-code
```

If you only need some of the plugins, you can adapt the last line.
