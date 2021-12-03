from spack import *

class PdipluginDeisa(CMakePackage):
    
    
    git = 'https://github.com/GueroudjiAmal/deisa.git'

    version('develop', branch='master', no_cache=True)

    depends_on('cmake@3.5:',         type=('build'))

    depends_on('pdi+python@1.4.3',     type=('link', 'run'))
    depends_on('mpi',                  type=('build','link','run'))
    depends_on('py-distributed@deisa', type=('run'))
    depends_on('py-dask',              type=('run'))

    def cmake_args(self):
        args = [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
        ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.append_path('PDI_PLUGIN_PATH', self.prefix.lib)
