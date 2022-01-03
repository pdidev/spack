# Copyright (C) 2021 Commissariat a l'energie atomique et aux energies alternatives (CEA)
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import inspect
import os


class Gysela(CMakePackage):
    """The Gysela 5D code models the electrostatic branch of the Ion Temperature
    Gradient turbulence in tokamak plasmas.

    Gysela is a 5D full-f and flux-driven gyrokinetic code. As such, it evolves in
    time the five-dimensional (3D in configuration space, 2D in velocity space)
    ion distribution function. For now, Gysela assumes electrons to be adiabatic
    and considers a global simplified magnetic geometry (concentric toroidal
    magnetic flux surfaces with circular cross-sections). The code simulates the
    full ion distribution function without any scale separation between
    equilibrium and fluctuations (”full-f”).

    From the physics point of view, the other peculiarities of the Gysela code are
    the presence of an ion-ion collision operator accounting for neoclassical
    transport, and the existence of versatile sources (heat, momentum, …) which
    sustain the mean profiles on confinement times (“flux-driven”).

    From the numerical point of view, Gysela is based on a semi-lagrangian scheme,
    hence is name: GYSELA 5D is an acronym for GYrokinetic SEmi-LAgrangian in 5
    Dimensions. Two solvers are at the heart of Gysela: a Vlasov solver for
    computing ions advections and a Poisson solver for computing the magnetic
    field."""

    homepage = "https://gyseladoc.gforge.inria.fr"

    url = "https://gitlab.maisondelasimulation.fr/gysela-developpers/gysela/-/archive/release-v37.0/gysela-release-v37.0.tar.gz"
    git = "git@gitlab.maisondelasimulation.fr:gysela-developpers/gysela.git"

    version('develop', branch='master-spack', no_cache=True)
    # 37.0 Doesn't work because of shebang limit.
    # version('37.0',  sha256='0cab6b92de1d976f5c15f64272e41dcf93536860dce25e70084f86254571e0b8')
    # Comes with its own Zpp,

    variant('pdi',        default=False, description='Build with PDI for IOs')
    variant('deisa',      default=False, description='Build with the deisa PDI plugin')
    variant('numpy',      default=True, description='Link to numpy for validate_data')
    variant('gysela_dir', default=os.environ.get('HOME')+'/gysela',
            description='Where to put gysela')
    variant('build_type', default='Release', description='CMake build type',
            values=('Release', 'Timed', 'Deterministic', 'Debug', 'Scorep'))

    depends_on('cmake@3.5:',          type=('build'))
    depends_on('mpi',                 type=('build', 'link', 'run'))
    # Has sometimes  issues when lapack is provided by open-blas.
    # Use ^netlib-lapack or ^intel-mkl when calling spack install.

    depends_on('lapack',              type=('link', 'run'))
    depends_on('zpp',                 type=('build'))
    depends_on('hdf5',                type=('link', 'run'))

    # For validate_data only.
    depends_on('py-numpy',            type=('run'), when='+numpy')

    depends_on('pdi +fortran',
               type=('build', 'link', 'run'), when='+pdi')
    depends_on('pdiplugin-decl-hdf5', type=('run'), when='+pdi')
    depends_on('pdiplugin-mpi',       type=('run'), when='+pdi')
    depends_on('pdiplugin-pycall',    type=('run'), when='+pdi')
    depends_on('pdiplugin-set-value', type=('run'), when='+pdi')
    depends_on('pdiplugin-trace',     type=('run'), when='+pdi')
    depends_on('pdiplugin-user-code', type=('run'), when='+pdi')
    depends_on('pdiplugin-deisa',     type=('link', 'run'),
               when='+deisa')  # Probably only needs run

    root_cmakeslists_dir = 'src'

    def cmake_args(self):
        stage_dir = str(self.stage.source_path)

        args = [
            '-Wno-dev',
            '-DUSE_PDI={:s}'.format('ON' if '+pdi' in self.spec else 'OFF'),
            '-DHDF5_USE_EMBEDDED=OFF',
        ]
        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                inspect.getmodule(self).make(*self.install_targets)
            elif self.generator == 'Ninja':
                inspect.getmodule(self).ninja(*self.install_targets)

            # With how the CMAKE/MAKE are done for gysela, everything gets lost in spack's temporary
            # staging dirs.
            # This piece of code ensures that the whole git (not including the build dir) is
            # available in the user specified path with gysela_dir=/path/to/desired/install/dir/.

            # target directory
            TARGET_DIR = str(self.spec.variants['gysela_dir'].value)
            # Dir where the files end up
            stage_dir = str(self.stage.source_path)

            # Copy the files and creates TARGET_DIR if it doesn't exist.
            from distutils.dir_util import copy_tree
            copy_tree(stage_dir, TARGET_DIR)
