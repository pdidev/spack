ARG BASE_IMAGE=spack/ubuntu-xenial

FROM ${BASE_IMAGE}

ARG COMPILER
ARG PARALLELISM=1
ARG SPACK_INSTALL_ARGS

ENV COMPILER=${COMPILER:-"gcc@5.4.0"}
ENV SPACK_INSTALL_ARGS=${SPACK_INSTALL_ARGS:-"--show-log-on-error --fail-fast"}

SHELL ["/usr/local/bin/spack-env", "/bin/bash", "-c"]

RUN apt-get -yqq update \
 && apt-get -yqq install --no-install-recommends \
    cmake \
    libopenmpi-dev \
    openmpi-bin \
 && rm -rf /var/lib/apt/lists/*

COPY tests/compiler_install /
RUN spack external find \
 && bash /compiler_install \
 && rm /compiler_install

RUN git clone https://github.com/leobago/fti-spack /opt/spack-fti
RUN spack repo add /opt/spack-fti

RUN git clone https://gitlab.version.fz-juelich.de/SIONlib/spack-repository.git /opt/spack-SIONlib
RUN spack repo add /opt/spack-SIONlib

RUN mkdir /opt/spack-pdi
COPY repo.yaml /opt/spack-pdi/
COPY packages /opt/spack-pdi/packages/
RUN spack repo add /opt/spack-pdi

RUN mkdir /opt/spack-environment
COPY tests/spack.yaml /opt/spack-environment/

RUN cd /opt/spack-environment \
 && spack env activate . \
 && spack external find \
 && spack config add config:install_tree:root:/opt/software \
 && spack config add config:view:/opt/view \
 && spack config add "packages:all:compiler:[${COMPILER}]" \
 && spack config add 'packages:all:target:[x86_64]'

RUN cd /opt/spack-environment \
 && spack env activate . \
 && spack concretize

RUN cd /opt/spack-environment \
 && spack env activate . \
 && for N in {2..${PARALLELISM}} \
  ; do spack install ${SPACK_INSTALL_ARGS} --only dependencies \
  & done \
 && spack install ${SPACK_INSTALL_ARGS} --only dependencies \
 || tail -n +1 -- /tmp/root/spack-stage/spack-stage-*/spack-*-out.txt \
 && spack uninstall -y pdi
