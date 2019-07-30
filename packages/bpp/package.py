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
#     spack install bpp
#
# You can edit this file again by typing:
#
#     spack edit bpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Bpp(CMakePackage):
    """BPP, the Bash Pre-Processor.
       BPP is useful in order to build clean Fortran90 interfaces. It allows to
       generate Fortran code for all types, kinds, and array ranks supported by the
       compiler."""

    homepage = "https://gitlab.maisondelasimulation.fr/jbigot/bpp"
    url      = 'https://gitlab.maisondelasimulation.fr/jbigot/bpp/-/archive/master/bpp-master.tar.gz'
    git      = 'https://gitlab.maisondelasimulation.fr/jbigot/bpp.git'


    version('develop', branch='master')
    version('0.3.0',   tag='v0.3.0')

    depends_on('cmake@2.8:', type='build')

