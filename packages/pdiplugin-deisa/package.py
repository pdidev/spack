from spack import *


class PdipluginDeisa(CMakePackage):
    """The Deisa plugin let one use Deisa through PDI."""

    git = 'https://github.com/GueroudjiAmal/deisa.git'

    version('develop', branch='master')

    depends_on('cmake@3.10:', type=('build'))

    depends_on('pdi+python@1.4.3', type=('link', 'run'))
    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('pdiplugin-mpi', type=('build', 'link', 'run'))
    depends_on('py-distributed@deisa', type=('run'))
    depends_on('py-dask@2021.11.2:', type=('run'))
    depends_on('py-dask-ml@2021.11.30:', type=('run'))
    depends_on('py-xarray', type=('run'))

    def cmake_args(self):
        args = [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
        ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
