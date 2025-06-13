# Copyright (C) 2020-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import spack_version_info

try:
    from spack.package import *
except BaseException:
    from spack import *

from .pdi import Pdi


class PdipluginDeclNetcdf(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.8.0.tar.gz"

    if spack_version_info[0] >= 1:
        license("BSD-3-Clause")

        maintainers("jbigot")
    else:
        maintainers = ["jbigot"]

    for v in Pdi.versions:
        version(str(v), **Pdi.versions[v])

    variant("tests", default=False, description="Build tests")
    variant("mpi", default=True, description="Enable parallel NetCDF")

    if spack_version_info[0] >= 1:
        depends_on("c", type="build")
        depends_on("cxx", type="build")

    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("cmake@3.10:", type=("build"), when="@1.5:")
    depends_on("cmake@3.10:", type=("build"), when="+tests")
    depends_on("cmake@3.5:", type=("build"), when="@:1.4.3")
    depends_on("fmt@6.1.2:", type=("link"), when="@1.5")
    depends_on("googletest@1.8: +gmock", type=("link"), when="@1.3:1.7 +tests")
    depends_on("netcdf-c@4.7.3:4", type=("link"), when="@1.8:")
    depends_on("netcdf-c@4.6:4", type=("link"), when="@1.5:")
    depends_on("netcdf-c@4.6.2:4+mpi", type=("link"), when="+mpi")
    depends_on("netcdf-c@4", type=("link"))
    for v in Pdi.versions:
        depends_on("pdi@" + str(v), type=("link", "run"), when="@" + str(v))
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/decl_netcdf"

    def url_for_version(self, version):
        return Pdi.version_url(version)

    def cmake_args(self):
        return [
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            self.define_from_variant("BUILD_HDF5_PARALLEL", "mpi"),
            self.define_from_variant("BUILD_NETCDF_PARALLEL", "mpi"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

    def setup_run_environment(self, env):
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)
