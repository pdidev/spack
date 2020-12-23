# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PdipluginTrace(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.julien-bigot.fr/"
    url      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi/-/archive/0.6.5/pdi-0.6.5.tar.bz2"
    git      = "https://gitlab.maisondelasimulation.fr/pdidev/pdi.git"

    maintainers = ['jbigot']

    version('develop', branch='master', no_cache=True)
    version('0.6.5',   sha256='a1100effb62d43556bd5e50d82f51e51710dbafc8d85c5a2e03ba7c168460be9')

    depends_on('cmake@3.5:',  type=('build'))
    depends_on('pdi@develop', type=('link', 'run'), when='@develop')
    depends_on('pdi@0.6.5',   type=('link', 'run'), when='@0.6.5')

    root_cmakelists_dir = 'plugins/trace'
    def cmake_args(self):
        return [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
        ]
    
    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
