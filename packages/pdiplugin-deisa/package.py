from spack import *


class PdipluginDeisa(CMakePackage):
    """The Deisa plugin let one use Deisa through PDI."""

    git = 'https://github.com/GueroudjiAmal/deisa.git'

    version('develop', branch='master')

    depends_on('cmake@3.10:', type=('build'))

    depends_on('pdi@1.5: +python', type=('link', 'run'))
    depends_on('mpi',              type=('build', 'link', 'run'))
    depends_on('py-deisa@0.2.0:',  type=('run'))

    root_cmakelists_dir = 'pdi-plugin'

    def cmake_args(self):
        return [self.define('INSTALL_PDIPLUGINDIR', self.prefix.lib)]

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
