#/bin/bash
set -e

git clone https://github.com/leobago/fti-spack /opt/spack-fti
spack repo add /opt/spack-fti
git clone https://gitlab.version.fz-juelich.de/SIONlib/spack-repository.git /opt/spack-SIONlib
spack repo add /opt/spack-SIONlib
spack repo add /opt/spack-pdi
mkdir /opt/spack-environment
cd /opt/spack-environment
cp /opt/spack-pdi/tests/spack-${MPIIMPL}.yaml spack.yaml

COMPILER_NAME="$(echo ${COMPILER} | sed 's/@.*//')"
COMPILER_VERSION="$(echo ${COMPILER} | sed 's/^[^@]*//')"

case "${COMPILER_NAME}" in
"clang")
    COMPILER_NAME=llvm
;;
intel|oneapi)
    COMPILER_NAME=intel-oneapi-compilers
;;
esac
COMPILERPKG="${COMPILER_NAME}${COMPILER_VERSION}"

echo "Checking if install is required for compiler ${COMPILER_NAME} (${COMPILER_VERSION})"
if ! spack compilers | grep "${COMPILERPKG}" &>/dev/null
then
    echo "Installing compiler ${COMPILER_NAME} (${COMPILER_VERSION})"
    spack spec "${COMPILERPKG}"
    for N in $(seq 2 ${PARALLELISM})
    do spack install ${SPACK_INSTALL_ARGS} "${COMPILERPKG}" &
    done
    spack install ${SPACK_INSTALL_ARGS} "${COMPILERPKG}" || \
            { tail -n +1 -- /tmp/root/spack-stage/spack-stage-*/spack-*-out.txt && false; }
    wait || \
            { tail -n +1 -- /tmp/root/spack-stage/spack-stage-*/spack-*-out.txt && false; }
    spack load "${COMPILERPKG}"
    spack compiler find
else
    echo "No install required for ${COMPILER_NAME} (${COMPILER_VERSION})"
fi

spack env activate .
spack config add config:install_tree:root:/opt/software
spack config add config:view:/opt/view
spack config add "packages:all:compiler:[${COMPILER}]"
spack config add "config:concretization:together"
spack add pdiplugin-decl-hdf5 pdiplugin-decl-netcdf pdiplugin-flowvr pdiplugin-mpi pdiplugin-pycall pdiplugin-serialize pdiplugin-set-value pdiplugin-trace pdiplugin-user-code pdiplugin-decl-sion pdiplugin-fti

spack concretize
for N in $(seq 2 ${PARALLELISM})
do spack install ${SPACK_INSTALL_ARGS} &
done
spack install ${SPACK_INSTALL_ARGS} || \
        { tail -n +1 -- /tmp/root/spack-stage/spack-stage-*/spack-*-out.txt && false; }
wait || \
        { tail -n +1 -- /tmp/root/spack-stage/spack-stage-*/spack-*-out.txt && false; }
