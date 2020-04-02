# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pdi(CMakePackage):
    """PDI is a library that aims to decouple high-performance simulation codes from
       Input/Output concerns.
       It offers a declarative application programming interface that enables codes to
       expose the buffers in which they store data and to notify PDI of significant
       steps of the simulation.
       It supports a plugin system to make existing libraries such as HDF5, SIONlib or
       FTI available to codes, potentially mixed in a single execution."""

    homepage = "https://pdi.julien-bigot.fr/"
    git      = 'https://gitlab.maisondelasimulation.fr/jbigot/pdi.git'
    
    root_cmakelists_dir = 'pdi'

    version('develop', branch='master')


    variant('shared',   default=True,  description = 'Build shared libraries rather than static ones')
    variant('unstable', default=False, description = 'Build all features by default including those not stable yet')
    variant('docs',     default=False, description = 'Build documentation')
    variant('tests',    default=False, description = 'Build tests')
    variant('fortran',  default=False, description = 'Enable Fortran support')
    variant('python',   default=False, description = 'Enable Python support')
    variant('indent',   default=False, description = 'Enable automatic code indentation')

    depends_on('cmake@3.5:',         type='build')
    depends_on('cmake@3.10:',        type='build', when='+docs')
    depends_on('cmake@3.10:',        type='build', when='+test')
    depends_on('git',                type='build')
    depends_on('pdi.paraconf')
    depends_on('pdi.bpp')
    depends_on('astyle@3.1.0:',      type='build', when='+indent')
    depends_on('doxygen@1.8.13:',    type='build', when='+docs')
    depends_on('py-pybind11@2.3.0:', type='build', when='+python')
    depends_on('python',             when='+python')
    depends_on('googletest@1.8.0:',  when='+tests')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={:s}'.format('OFF' if '-shared' in self.spec else 'ON'),
            '-DENABLE_UNSTABLE:BOOL={:s}'.format('ON' if '+unstable' in self.spec else 'OFF'),
            '-DBUILD_DOCUMENTATION:BOOL={:s}'.format('ON' if '+docs' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DENABLE_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF'),
            '-DENABLE_PYTHON:BOOL={:s}'.format('ON' if '+python' in self.spec else 'OFF'),
            '-DENABLE_INDENT:BOOL={:s}'.format('ON' if '+indent' in self.spec else 'OFF')
        ]
        return args
