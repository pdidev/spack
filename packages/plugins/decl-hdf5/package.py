# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PdipluginDeclHdf5(CMakePackage):
    """Decl'HDF5 plugin enables one to read and write data from HDF5 files in a declarative way.
    Decl'HDF5 does not support the full HDF5 feature set but offers a simple declarative interface
    to access a large subset of it for the PDI library"""

    homepage = "https://pdi.julien-bigot.fr/"
    git      = 'https://gitlab.maisondelasimulation.fr/jbigot/pdi.git'

    version('develop', branch='master')
    version('0.6.1', tag='0.6.1')
    version('0.6.0', tag='0.6.0')

    root_cmakelists_dir = 'plugins/decl_hdf5'

    variant('indent',        default=False, description = 'Enable automatic code indentation')
    variant('tests',         default=False, description = 'Build tests')
    variant('cfg_validator', default=False, description = 'Configuration validation')
    variant('fortran',       default=False, description = 'Enable Fortran support')
    variant('mpi',           default=False, description = 'Enable MPI')

    depends_on('cmake@3.5:',             type='build')
    depends_on('git',                    type='build')
    depends_on('spdlog@1.3.1:',          type='build')
    depends_on('pdi',                    type=('build', 'link', 'run'))
    depends_on('pdi +fortran',           type=('build', 'link', 'run'), when='+fortran')
    depends_on('astyle@3.1:',            type='build', when='+indent')
    depends_on('py-pybind11@2.3.0:',     type='build')
    depends_on('python@3.7:',            type=('build', 'link', 'run'))
    depends_on('hdf5 +cxx~mpi',          type=('build', 'link', 'run'), when='~mpi')
    depends_on('hdf5 +cxx~mpi+fortran',  type=('build', 'link', 'run'), when='~mpi+fortran')
    depends_on('hdf5 +cxx+mpi',          type=('build', 'link', 'run'), when='+mpi')
    depends_on('hdf5 +cxx+mpi+fortran',  type=('build', 'link', 'run'), when='+mpi+fortran')
    depends_on('mpi',                    type=('build', 'link', 'run'), when='+mpi')
    depends_on('pdiplugin-mpi',          type=('build', 'link', 'run'), when='+mpi')
    depends_on('pdiplugin-mpi +fortran', type=('build', 'link', 'run'), when='+mpi+fortran')

    def cmake_args(self):
        args = [
            '-DBUILD_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF'),
            '-DBUILD_INDENT:BOOL={:s}'.format('ON' if '+indent' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_CFG_VALIDATOR:BOOL={:s}'.format('ON' if '+cfg_validator' in self.spec else 'OFF'),
            '-DBUILD_HDF5_PARALLEL:BOOL={:s}'.format('ON' if '+mpi' in self.spec else 'OFF')
        ]
        return args

