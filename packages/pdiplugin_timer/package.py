# Copyright (C) 2026 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import spack_version_info

try:
    from spack_repo.builtin.build_systems.cmake import CMakePackage
except BaseException:
    pass

try:
    from spack.package import *
except BaseException:
    from spack import *

from .pdi import Pdi


class PdipluginTimer(CMakePackage):
    """The timer plugin for the PDI library measures the time spent by PDI and
    its plugins, between user-defined start and stop events."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.12.0.tar.gz"

    if spack_version_info[0] >= 1:
        license("BSD-3-Clause")

        maintainers("jbigot")
    else:
        maintainers = ["jbigot"]

    for v in Pdi.versions:
        if v >= Version("1.12.0"):
            version(str(v), **Pdi.versions[v])

    variant("tests", default=False, description="Build tests")

    if spack_version_info[0] >= 1:
        depends_on("c", type="build")
        depends_on("cxx", type="build")

    depends_on("cmake@3.22.1:", type=("build"))
    # @= (an exact version) only exists from spack 0.20 on
    exact = "@=" if spack_version_info >= (0, 20) else "@"
    for v in Pdi.versions:
        if v >= Version("1.12.0"):
            depends_on("pdi" + exact + str(v), type=("link", "run"), when=exact + str(v))
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/timer"

    def cmake_args(self):
        return [
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

    def setup_run_environment(self, env):
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)
