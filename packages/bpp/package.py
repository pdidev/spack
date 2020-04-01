# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bpp(CMakePackage):
    """BPP, the Bash Pre-Processor.
       BPP is useful in order to build clean Fortran90 interfaces. It allows to
       generate Fortran code for all types, kinds, and array ranks supported by the
       compiler."""

    homepage = "https://gitlab.maisondelasimulation.fr/jbigot/bpp"
    git      = 'https://gitlab.maisondelasimulation.fr/jbigot/bpp.git'


    version('develop', branch='master')
    version('0.3.0',   tag='v0.3.0')

    depends_on('cmake@2.8:', type='build')
    depends_on('git',        type='build')

