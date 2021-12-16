# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ddc(CMakePackage):
    """DDC is a domain decomposition library."""

    homepage = "https://github.com/Maison-de-la-Simulation/ddc"
    git = "https://github.com/Maison-de-la-Simulation/ddc.git"
    url = "https://github.com/Maison-de-la-Simulation/ddc/archive/refs/tags/v0.0.0.tar.gz"

    maintainers = ['tpadioleau', 'jbigot']

    test_requires_compiler = True

    version('main', branch='main')
    version('0.0.0', sha256='0d832e17266f87166eea25ea0b35644e319e751b36153cd2739e293a7dc75a80', extension='tag.gz')

    variant('tests', default=True, description='Build the tests')
    variant('benchmarks', default=False, description='Build the benchmarks')
    variant('pdi_wrapper', default=True, description='Build the PDI wrapper')

    depends_on("cmake@3.15:", type='build')
    depends_on("mdspan")
    depends_on("pdi", when='+pdi_wrapper')
    depends_on("googletest", type='test', when='+tests')
    depends_on("benchmark", type='test', when='+benchmarks')

    def cmake_args(self):
        args = [
            '-DDDC_mdspan_DEPENDENCY_POLICY=INSTALLED',
            self.define_from_variant('BUILD_TESTING', 'tests'),
            self.define_from_variant('BUILD_BENCHMARKS', 'benchmarks'),
            self.define_from_variant('DDC_BUILD_PDI_WRAPPER', 'pdi_wrapper')
        ]
        if '+tests' in self.spec:
            args.append('-DDDC_GTest_DEPENDENCY_POLICY=INSTALLED')
        if '+benchmarks' in self.spec:
            args.append('-DDDC_benchmark_DEPENDENCY_POLICY=INSTALLED')

        return args
