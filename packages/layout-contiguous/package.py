from spack import *


class LayoutContiguous(CMakePackage):
    """Library providing additional layouts to be used with `std::mdspan`"""

    git = "https://github.com/Maison-de-la-Simulation/layout-contiguous.git"
    url = "https://github.com/Maison-de-la-Simulation/layout-contiguous/archive/refs/tags/v0.1.0.tar.gz"

    maintainers = ['tpadioleau', 'jbigot']

    version('main',  branch='main')
    version('0.1.0', sha256='33c9e7f63e787808363ae03b2003b2853553f476d0e2df9c69861d0df043256d', extension='tag.gz')

    depends_on("cmake@3.21:", type='build')
    depends_on("mdspan@0.2:")
