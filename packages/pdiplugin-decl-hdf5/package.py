# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PdipluginDeclHdf5(CMakePackage):
    """Decl'HDF5 plugin enables one to read and write data from HDF5 files in a
    declarative way. Decl'HDF5 does not support the full HDF5 feature set but
    offers a simple declarative interface to access a large subset of it for the
    PDI library"""

    homepage = "https://pdi.julien-bigot.fr/"
    url      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi/-/archive/0.6.5/pdi-0.6.5.tar.bz2"
    git      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi.git"

    maintainers = ['jbigot']

    version('develop', branch='master', no_cache=True)
    version('0.6.5',   sha256='a1100effb62d43556bd5e50d82f51e51710dbafc8d85c5a2e03ba7c168460be9')

    variant('tests', default=False, description = 'Build tests')
    variant('mpi',   default=False, description = 'Enable MPI')

    depends_on('cmake@3.5:',  type=('build'))
    depends_on('pdi@develop', type=('link', 'run'), when='@develop')
    depends_on('pdi@0.6.5',   type=('link', 'run'), when='@0.6.5')
    depends_on('hdf5 ~mpi',   type=('link', 'run'), when='~mpi')
    depends_on('hdf5 +mpi',   type=('link', 'run'), when='+mpi')

    root_cmakelists_dir = 'plugins/decl_hdf5'
    def cmake_args(self):
        args = [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_HDF5_PARALLEL:BOOL={:s}'.format('ON' if '+mpi' in self.spec else 'OFF')
        ]
        return args
    
    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
