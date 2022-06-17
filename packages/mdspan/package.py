# Copyright (C) 2020-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mdspan(CMakePackage):
    """Reference implementation of mdspan targeting C++23."""

    homepage = "https://github.com/Kokkos/mdspan"
    git = "https://github.com/Kokkos/mdspan.git"
    url = "https://github.com/kokkos/mdspan/archive/refs/tags/mdspan-0.3.0.tar.gz"

    maintainers = ['crtrott']

    version('stable',  branch='stable')
    version('0.3.0', sha256='275ac02b456a31a5b8c0cb773fca3fe59f6df8a441124dcc1e7a88ef8069f974', extension='tar.gz')
    version('0.2.0', sha256='1ce8e2be0588aa6f2ba34c930b06b892182634d93034071c0157cb78fa294212', extension='tar.gz')
    version('0.1.0', sha256='24c1e4be4870436c6c5e80d38870721b0b6252185b8288d00d8f3491dfba754b', extension='tar.gz')

    depends_on("cmake@3.14:", type='build')

    variant('cxx_standard', default='DETECT', description="Override the default CXX_STANDARD to compile with.",
            values=('DETECT', '14', '17', '20'))

    def cmake_args(self):
        args = [
            self.define_from_variant('MDSPAN_CXX_STANDARD', 'cxx_standard')
        ]

        return args
