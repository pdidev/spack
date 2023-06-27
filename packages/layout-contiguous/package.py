from spack import *


class LayoutContiguous(CMakePackage):
    """Library providing additional layouts to be used with `std::mdspan`"""

    git = "https://github.com/Maison-de-la-Simulation/layout-contiguous.git"
    url = "https://github.com/Maison-de-la-Simulation/layout-contiguous/archive/refs/tags/v0.6.0.tar.gz"

    maintainers = ['tpadioleau', 'jbigot']

    version('main',  branch='main')
    version('0.6.0', sha256='3026efba1b58aa39cb35e254e20313f2bc5f4e5e8a42aede7401323b559df54c', extension='tar.gz')
    version('0.3.0', sha256='39dd518a04cb7aaeb8d3a3317810c65b8beb10ea41f54b967c58f24a33384ce5', extension='tar.gz')
    version('0.1.0', sha256='33c9e7f63e787808363ae03b2003b2853553f476d0e2df9c69861d0df043256d', extension='tar.gz')

    depends_on("cmake@3.20:", type='build')
    depends_on("mdspan@0.3", when="@:0.3")
    depends_on("mdspan@0.6", when="@0.6")
    depends_on("googletest", type=('build', 'test'))

    def cmake_args(self):
        args = [
            self.define('BUILD_TESTING', True)
        ]

        return args
