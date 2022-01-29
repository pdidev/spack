# Copyright 2019-2021 Forschungszentrum Juelich GmbH
# Copyright (C) 2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
#
# SPDX-License-Identifier: MIT

from spack import *


class Sionlib(AutotoolsPackage):
    """Scalable I/O library"""

    homepage = "https://www.fz-juelich.de/jsc/sionlib"
    url = "https://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.5"
    list_url = ("https://www.fz-juelich.de/ias/jsc/EN/Expertise/Support/Software/SIONlib/" +
                "sionlib-download_node.html")
    git = "https://gitlab.version.fz-juelich.de/SIONlib/SIONlib.git"

    version("main", branch="main")
    version('1.7.7l', sha256='3b5072d8a32a9e9858d85dfe4dc01e7cfdbf54cdaa60660e760b634ee08d8a4c',
            extension="tar.gz")
    version('1.7.7',  sha256='a73574b1c17c030b1d256c5f0eac5ff596395f8b827d759af83473bf94f74477',
            extension="tar.gz")
    version('1.7.6l', sha256='2c220390ef63d001f8ab02c380087187ea02ad2bfc5956e05ecaa0725a6f9942',
            extension="tar.gz")
    version('1.7.6',  sha256='e85253ed3cd17a3b1c124ccd704caea3ad3c200abfcca9cc0851cb14f5a60691',
            extension="tar.gz")
    version('1.7.5l', sha256='73abc3a7d07275027975928c0d2036c5fff2592ecb00387d0495a76ed48d368b',
            extension="tar.gz")
    version('1.7.5',  sha256='8ba3c2e69a176436fd7acc5a35c1390804acc677c3d0e9ed34f11500bdedc727',
            extension="tar.gz")
    version('1.7.4l', sha256='3dcb61ea6c2bfa765c44c2407aba7d4f91f39b93549e81a60b26782feab51dfe',
            extension="tar.gz")
    version('1.7.4',  sha256='9ccdfdfa23a281b426764c643ae563f91c2811a8176c687c97f1777d28f609e9',
            extension="tar.gz")
    version('1.7.3l', sha256='e247abbb429446e5f3b3d1b5facb4aced04b513f4369c398422639cc50567e38',
            extension="tar.gz")
    version('1.7.3',  sha256='10621c87594296ac82d1f7582db5fd5cd89d0171aab515f299fa4f8ba4cd25b3',
            extension="tar.gz")
    version('1.7.2l', sha256='7d94fc9a285f407e4e80b49fa618a6d68c7c78dacf3ce45512bbffbbd96500ed',
            extension="tar.gz")
    version('1.7.2',  sha256='19234b9d35d096aa3845ad37fec22e2a4215384f6a4cad7c93e1e4d6cdc68bb5',
            extension="tar.gz")
    version('1.7.1l', sha256='6614187a6dbc5003eafde4ca10a377057c6e8163e3d48c7871b193f84705201d',
            extension="tar.gz")
    version('1.7.1',  sha256='ab37dab5c296d9d03f4fc3d02a489a9045543aa836728c79fb27e3b0ed0f0871',
            extension="tar.gz")
    version('1.7.0l', sha256='82d670cc71a905b432deed63f870c8aa7f2c4ac17118eb4c06ae32c3cc1f8604',
            extension="tar.gz")
    version('1.7.0',  sha256='068800fb69345b552f9765d422be90527f15cc2a552bb27c53966c2561461380',
            extension="tar.gz")
    version('1.6.2l', sha256='32c42411b032dd24a806a4778f6fa4bc7d5976429c23035530a687eb1429ef7f',
            extension="tar.gz")
    version('1.6.2',  sha256='887c34e1e37ea4db0cbfcc07bc30001599d338fbabd3dd393b235dc9098e5081',
            extension="tar.gz")
    version('1.6.1l', sha256='02ec67402fb65a7e379699c434cbf7becb99a827230b685c22609731e33ac319',
            extension="tar.gz")
    version('1.6.1',  sha256='99d57756678224dc9279f141ec7aa52068b64ef5cb2fc1790d2fed1a06b6ec5c',
            extension="tar.gz")

    # TODO: not all variants are available for all versions currently, this cannot be expressed in
    #       spack, see: https://github.com/spack/spack/issues/9740

    # Common options
    variant("debug", default=False, description="enable debug logging")
    variant("coverage", default="none",
            description="enable collection of coverage data with selected method",
            values=("none", "gcovr", "kcov"), multi=False)
    variant("parallel", description="which parallel APIs to enable",
            values=any_combination_of("mpi", "omp").with_default("mpi,omp"))
    variant("parutils", default=True,
            description="build parallel utilities (for benchmarking)")

    # 1.7 options
    variant("cxx", default=True, description="build C++ interface")
    variant("fortran", default=True, description="build Fortran interface")
    variant("cuda", default=False, description="CUDA-aware interface")
    variant("msa", default="none",
            description="collector selection plug-in for MSA-aware collective I/O",
            values=("none", "hostname-regex", "deep-est-sdv"), multi=False)

    depends_on("mpi", when="parallel=mpi")
    depends_on("cuda@9:", when="+cuda")

    conflicts("+fortran", when="@:1.7.6 %gcc@10:",
              msg="Fortran interface for sionlib < 1.7.7 cannot be built with GCC >= 10")

    def configure_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("%gcc"):
            args.append("--compiler=gnu")
        elif spec.satisfies("%intel"):
            args.append("--compiler=intel")
        elif spec.satisfies("%pgi"):
            args.append("--compiler=pgi")

        if spec.satisfies("^openmpi"):
            args.append("--mpi=openmpi")
        elif spec.satisfies("^mpich@:1.99"):
            args.append("--mpi=mpich1")
        elif spec.satisfies("^mpich@2.0:2.99"):
            args.append("--mpi=mpich2")
        elif spec.satisfies("^mpich@3.0:"):
            args.append("--mpi=mpich3")
        elif spec.satisfies("^intel-mpi"):
            args.append("--mpi=intel2")

        if "+debug" in spec:
            args.append("--enable-debug")

        coverage = spec.variants["coverage"].value
        if coverage != "none":
            args.append("--enable-{}".format(coverage))

        if "parallel=mpi" not in spec:
            args.append("--disable-mpi")
        if "parallel=omp" not in spec:
            args.append("--disable-omp")

        if "+parutils" not in spec:
            args.append("--disable-parutils")

        if "+cxx" not in spec:
            args.append("--disable-cxx")

        if "+fortran" not in spec:
            args.append("--disable-fortran")

        if "+cuda" in spec:
            args.append("--enable-cuda={}".format(spec["cuda"].prefix))

        msa = spec.variants["msa"].value
        if msa != "none":
            args.append("--msa={}".format(msa))

        return args
