# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Pdi(CMakePackage):
    """PDI is a library that aims to decouple high-performance simulation codes
    from Input/Output concerns. It offers a declarative application programming
    interface that enables codes to expose the buffers in which they store data
    and to notify PDI of significant steps of the simulation. It supports a
    plugin system to make existing libraries such as HDF5, SIONlib or FTI
    available to codes, potentially mixed in a single execution."""

    homepage = "https://pdi.julien-bigot.fr/"
    url      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi/-/archive/0.6.5/pdi-0.6.5.tar.bz2"
    git      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi.git"

    maintainers = ['jbigot']

    version('develop', branch='master', no_cache=True)
    version('0.6.5',   sha256='a1100effb62d43556bd5e50d82f51e51710dbafc8d85c5a2e03ba7c168460be9')
    
    variant('docs',     default=False, description = 'Build documentation')
    variant('tests',    default=False, description = 'Build tests')
    variant('fortran',  default=True,  description = 'Enable Fortran support')
    variant('python',   default=True,  description = 'Enable Python support')
    
    depends_on('cmake@3.5:',                type=('build'))
    depends_on('paraconf +shared',          type=('link', 'run'),          when='-fortran')
    depends_on('spdlog@1.3.1:',             type=('link', 'run'))
    depends_on('cmake@3.10:',               type=('build'),                when='+docs')
    depends_on('doxygen@1.8.13:',           type=('build'),                when='+docs')
    depends_on('paraconf +shared+fortran',  type=('link', 'run'),          when='+fortran')
    depends_on('zpp@1.0.8',                 type=('build'),                when='+fortran')
    depends_on('py-pybind11@2.3.0:',        type=('link'),                 when='+python')
    depends_on('python@3.7:',               type=('build', 'link', 'run'), when='+python')
    depends_on('cmake@3.10:',               type=('build'),                when='+tests')
    depends_on('googletest@1.8.0: +gmock',  type=('link'),                 when='+tests')
    depends_on('paraconf +shared +fortran', type=('link', 'run'),          when='+tests+fortran')
    
    root_cmakelists_dir = 'pdi'
    def cmake_args(self):
        args = [
            '-DBUILD_DOCUMENTATION:BOOL={:s}'.format('ON' if '+docs' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF'),
            '-DBUILD_PYTHON:BOOL={:s}'.format('ON' if '+python' in self.spec else 'OFF')
        ]
        return args
