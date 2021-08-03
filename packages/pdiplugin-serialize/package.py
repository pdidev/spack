# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PdipluginSerialize(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.julien-bigot.fr/"
    url = "https://gitlab.maisondelasimulation.fr/pdidev/pdi/-/archive/1.3.1/pdi-1.3.1.tar.bz2"
    git = "https://gitlab.maisondelasimulation.fr/pdidev/pdi.git"

    maintainers = ['jbigot']

    version('develop', branch='master', no_cache=True)
    version('1.3.1',   sha256='a4a1f9d4d6ca6790487edf65e3d7c9f5a5d17fb0bcdf81dfab94efc854fcc387')
    version('1.3.0',   sha256='86947c40f025a09ab228360fa002f7241801f5fb70c75f815210d607cf30b200')
    version('1.2.2',   sha256='b93a9165d4b9f1e09790c9be3c950530537cf9a9dc01210afc77e411939bdf41')
    version('1.2.1',   sha256='0c90294fb2bb9ca5f6b957d9d8f68f3a3039fc256ba92f7e5bbe316768b43037')
    version('1.2.0',   sha256='8d5821d473140ea48036e8f03668bf6295d06f8b7561d464cc1b5748bf8d2aa3')
    version('1.1.0',   sha256='8f8a33e1538afde81bb2bbbc3ba8fe3942f0824672a364d0eb2055a0255e8b0c')
    version('1.0.1',   sha256='c35f6d19cecfc3963c08c8d516386c1cd782fcdbe4e39aa91dd01376d2346cb6')
    version('1.0.0',   sha256='57f5bfd2caa35de144651b0f4db82b2a403997799c258ca3a4e632f8ff2cfc1b')

    variant('tests', default=False, description='Build tests')
    
    depends_on('cmake@3.5:',  type=('build'))
    depends_on('googletest@1.8.0: +gmock', type=('link'), when='@1.3: +tests')
    depends_on('pdi@develop', type=('link', 'run'), when='@develop')
    depends_on('pdi@1.2.2',   type=('link', 'run'), when='@1.2.2')
    depends_on('pdi@1.2.1',   type=('link', 'run'), when='@1.2.1')
    depends_on('pdi@1.2.0',   type=('link', 'run'), when='@1.2.0')
    depends_on('pdi@1.1.0',   type=('link', 'run'), when='@1.1.0')
    depends_on('pdi@1.0.1',   type=('link', 'run'), when='@1.0.1')
    depends_on('pdi@1.0.0',   type=('link', 'run'), when='@1.0.0')
    depends_on('pdi@0.6.5',   type=('link', 'run'), when='@0.6.5')
    depends_on('pkgconfig',   type=('build'))

    root_cmakelists_dir = 'plugins/serialize'

    def cmake_args(self):
        return [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
            '-DBUILD_FORTRAN:BOOL={:s}'.format(
                'ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format(
                'ON' if '+tests' in self.spec else 'OFF'),
            '-DBUILD_CFG_VALIDATOR:BOOL=OFF',
        ]

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
