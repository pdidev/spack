# Copyright (C) 2020-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

try:
    from spack.package import *
except BaseException:
    from spack import *
from spack.pkg.pdi.pdi import Pdi


class PdipluginSerialize(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.8.0.tar.gz"

    maintainers = ['jbigot']

    for v in Pdi.versions:
        version(str(v), **Pdi.versions[v])

    variant('tests', default=False, description='Build tests')

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on('cmake@3.16.3:', type=('build'), when='@1.8:')
    depends_on('cmake@3.10:', type=('build'), when='@1.5:')
    depends_on('cmake@3.10:', type=('build'), when='+tests')
    depends_on('cmake@3.5:', type=('build'), when='@:1.4.3')
    depends_on('googletest@1.8: +gmock', type=('link'), when='@1.3:1.7 +tests')
    for v in Pdi.versions:
        depends_on('pdi@' + str(v), type=('link', 'run'), when='@' + str(v))
    depends_on('pkgconfig', type=('build'))

    root_cmakelists_dir = 'plugins/serialize'

    def url_for_version(self, version):
        return Pdi.version_url(version)

    def cmake_args(self):
        return [
            '-DINSTALL_PDIPLUGINDIR:PATH={:s}'.format(self.prefix.lib),
            self.define_from_variant('BUILD_TESTING', 'tests'),
        ]

    def setup_run_environment(self, env):
        env.prepend_path('PDI_PLUGIN_PATH', self.prefix.lib)
