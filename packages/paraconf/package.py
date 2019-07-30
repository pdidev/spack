# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install paraconf
#
# You can edit this file again by typing:
#
#     spack edit paraconf
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Paraconf(CMakePackage):
    """Paraconf is a library that provides a simple query language to
       access a Yaml tree on top of libyaml."""

    homepage = "https://gitlab.maisondelasimulation.fr/jbigot/libparaconf"
    url      = 'https://gitlab.maisondelasimulation.fr/jbigot/libparaconf/-/archive/master/libparaconf-master.tar.gz'
    git      = 'https://gitlab.maisondelasimulation.fr/jbigot/libparaconf.git'


    version('develop', branch='master')
    version('0.4.0',   tag='0.4.0')

    variant('shared',  default=True,   description = 'Build shared libraries rather than static ones')
    variant('profile', default='User', values=('User', 'Devel'), description = 'Profile to use for PDI distribution build', multi=False)
    variant('fortran', default=True,   description = 'Enable Fortran support')
    variant('tests',   default=False,  description = 'Build tests')

    depends_on('cmake@3.5:',     type='build')
    depends_on('libyaml@:0.2.2', type='build')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={:s}'.format('ON' if '+shared' in self.spec else 'OFF'),
            '-DDIST_PROFILE:STRING={:s}'.format(self.spec.variants['profile'].value),
            '-DBUILD_TESTING:BOOL={:s}'.format('ON' if '+tests' in self.spec else 'OFF'),
            '-DENABLE_FORTRAN:BOOL={:s}'.format('ON' if '+fortran' in self.spec else 'OFF')
        ]
        return args
