# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fti(CMakePackage):
    """FTI stands for Fault Tolerance Interface and is a library that aims to give computational scientists the means to perform fast and efficient multilevel checkpointing in large scale supercomputers."""

    homepage = "https://fault-tolerance-interface.readthedocs.io"
    git      = 'https://github.com/leobago/fti.git'

    version('develop', branch='master')
    version('1.4', tag='1.4')

    variant('doc',      default=False, description="Enables the generation of a Doxygen documentation")
    variant('examples', default=False, description="Enables the generation of examples")
    variant('fortran',  default=False, description="Enables the generation of the Fortran wrapper for FTI")
    variant('fiio',     default=False, description="Enables the I/O failure injection mechanism")
    variant('hdf5',     default=False, description="Enables the HDF5 checkpoints for FTI")
    variant('ime',      default=False, description="Enables the IME native API")
    variant('lustre',   default=False, description="Enables Lustre Support")
    variant('sion',     default=False, description="Enables the parallel I/O SIONlib for FTI")
    variant('tests',    default=False, description="Enables the generation of tests")
    variant('tutorial', default=False, description="Enables the generation of tutorial files")

    depends_on('cmake@3.3.2:',  type=('build'))
    depends_on('zlib',          type=('link', 'run'))
    depends_on('mpi',           type=('build', 'link', 'run'))
    depends_on('hdf5 +mpi',     type=('build', 'link', 'run'))
    depends_on('doxygen',       type=('build'),                when='+doc')
    depends_on('sionlib@1.7.2', type=('build', 'link', 'run'), when='+sion')

    def cmake_args(self):
        args = [
            '-DENABLE_DOCU:BOOL={:s}'.format('ON' if '+doc' in self.spec else 'OFF'),
            '-DENABLE_EXAMPLES:BOOL={:s}'.format('ON' if '+examples' in self.spec else 'OFF'),
            '-DENABLE_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF'),
            '-DENABLE_FI_IO:BOOL={:s}'.format('ON' if '+fiio' in self.spec else 'OFF'),
            '-DENABLE_HDF5:BOOL={:s}'.format('ON' if '+hdf5' in self.spec else 'OFF'),
            '-DENABLE_IME_NATIVE:BOOL={:s}'.format('ON' if '+ime' in self.spec else 'OFF'),
            '-DENABLE_LUSTRE:BOOL={:s}'.format('ON' if '+lustre' in self.spec else 'OFF'),
            '-DENABLE_SIONLIB:BOOL={:s}'.format('ON' if '+sion' in self.spec else 'OFF'),
            '-DENABLE_TESTS:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DENABLE_TUTORIAL:BOOL={:s}'.format('ON' if '+tutorial' in self.spec else 'OFF'),
        ]
        return args
