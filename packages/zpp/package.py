# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zpp(CMakePackage):
    """ZPP, the Z Pre-Processor.
       ZPP transforms bash in a pre-processor for F90 source files.
       It offers a set of functions specifically tailored to build clean
       Fortran90 interfaces by generating code for all types, kinds, and array ranks supported by a given compiler."""

    homepage = "https://github.com/jbigot/zpp"
    git      = 'https://github.com/jbigot/zpp.git'

    version('develop', branch='master')
    version('0.3.0',   tag='v0.3.0')

    depends_on('cmake@2.8:', type='build')
    depends_on('git',        type='build')
