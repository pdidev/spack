# Copyright (C) 2020-2026 Commissariat a l'energie atomique et aux energies alternatives (CEA)
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


class Paraconf(CMakePackage):
    """Paraconf is a library that provides a simple query language to access a
    Yaml tree on top of libyaml."""

    homepage = "https://github.com/pdidev/paraconf"
    url = "https://github.com/pdidev/paraconf/archive/1.0.3.tar.gz"

    if spack_version_info[0] >= 1:
        license("MIT")

        maintainers("jbigot")
    else:
        maintainers = ["jbigot"]

    version("1.0.3", sha256="462c487b1c9681ad0fd04cde611a9b9d969c3ab2504e2573c5ca88d1b7afa203")

    variant("shared", default=True, description="Build shared libraries rather than static ones")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("tests", default=False, description="Build tests")

    if spack_version_info[0] >= 1:
        depends_on("c", type="build")
        depends_on("cxx", type="build")
        depends_on("fortran", type="build", when="+fortran")

    depends_on("cmake@3.22:", type=("build"))
    depends_on("pkgconfig", type=("build"))
    depends_on("libyaml@0.2.2:", type=("link", "run"))

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PARACONF_BUILD_TESTING", "tests"),
            self.define_from_variant("PARACONF_BUILD_FORTRAN", "fortran"),
        ]
