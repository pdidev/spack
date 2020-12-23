# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Paraconf(CMakePackage):
    """Paraconf is a library that provides a simple query language to access a
    Yaml tree on top of libyaml."""

    homepage = "https://github.com/pdidev/paraconf"
    url      = "https://github.com/pdidev/paraconf/archive/0.4.9.tar.gz"

    maintainers = ['jbigot']

    version('0.4.9', sha256='e99a01584e07e4d09b026fcd9a39500fbdbc3074a2598a4bc89f400825094c5a')

    variant('shared',  default=True,  description = 'Build shared libraries rather than static ones')
    variant('fortran', default=True,  description = 'Enable Fortran support')
    variant('tests',   default=False, description = 'Build tests')

    depends_on('cmake@3.5:', type='build')
    depends_on('libyaml@0.2.2:', type=('link', 'run'))

    root_cmakelists_dir = 'paraconf'
    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={:s}'.format('ON' if '+shared' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF')
        ]
        return args
