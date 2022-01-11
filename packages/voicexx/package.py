from spack import *


class Voicexx(CMakePackage):
    """"""

    homepage = "https://gitlab.maisondelasimulation.fr/gysela-developpers/voicexx"
    git = "https://gitlab.maisondelasimulation.fr/gysela-developpers/voicexx.git"
    url = ""

    maintainers = ['gdgirard', 'tpadioleau', 'jbigot']

    test_requires_compiler = True

    version('main',  branch='main', submodules=True)

    variant('benchmarks', default=False, description='Build the benchmarks.')
    variant('deprecated', default=False, description='Enable deprecated code.')

    depends_on("lapack")
    depends_on("fftw precision=double -mpi")
    depends_on("paraconf@0.4.14:")
    depends_on("pdi")
    depends_on('pdiplugin-decl-hdf5', type='run')
    depends_on('pdiplugin-set-value', type='run')
    depends_on('pdiplugin-trace', type='run')
    depends_on("cmake@3.15:", type='build')
    depends_on('googletest +gmock', type='test')
    depends_on("benchmark", type='test', when='+benchmarks')
