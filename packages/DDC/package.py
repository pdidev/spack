# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ddc(CMakePackage):
    """DDC is a domain decomposition library."""

    homepage = "https://github.com/Maison-de-la-Simulation/ddc"
    git = "https://github.com/Maison-de-la-Simulation/ddc.git"
    url = ""

    maintainers = ['tpadioleau', 'jbigot']

    test_requires_compiler = True

    version('main', branch='main', submodules=True)

    depends_on("cmake@3.15:", type='build')
    depends_on("mdspan")
    depends_on("pdi")
    depends_on("googletest", type='test')
    depends_on("benchmark", type='test')
