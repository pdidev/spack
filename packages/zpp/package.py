# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Zpp(PythonPackage):
    """ZPP, the Z Pre-Processor. ZPP transforms bash in a pre-processor for F90
    source files. It offers a set of functions specifically tailored to build
    clean Fortran90 interfaces by generating code for all types, kinds, and
    array ranks supported by a given compiler."""

    homepage = "https://github.com/jbigot/zpp"

    maintainers = ['jbigot']

    version('1.0.8', sha256='dc5f423f019f1af92ff020372b458ab539890d2de2133bb9602cce419486faea')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    
    def url_for_version(self, version):
        fixed=''
        if version > Version('1.0.7') and version <= Version('1.0.9'):
            fixed = '-fixed'
        url = 'https://files.pythonhosted.org/packages/source/z/zpp/zpp-{version}{fixed}.tar.gz'
        return url.format(version=version, fixed=fixed)
