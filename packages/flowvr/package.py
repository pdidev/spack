# Copyright (C) 2020 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# and others. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flowvr(CMakePackage):
    """FlowVR is a middleware library that eases development and execution of
    high performance interactive applications requiring to harness the power of
    computing nodes distributed in a cluster or grid. FlowVR has been used for
    virtual reality application, telepresence, multi-camera real-time 3D
    modeling, in situ visualization, steering of parallel molecular dynamics
    applications, etc. FlowVR reuses and extends the data flow paradigm commonly
    used for scientific visualization environments. An application is seen as a
    set of possibly distributed modules exchanging data. Different module
    assemblies can be specified without modification or recompilation of the
    modules. The application developper does not have to bother about networking
    issues. That's the job of FlowVR to manage and optimize data exchanges
    between modules. FlowVR supports parallel modules, enabling to harness
    existing MPI codes for instance. This feature is commonly used for in-situ
    visualization or computational steering."""

    homepage = "http://flowvr.sourceforge.net/"
    url = "https://gitlab.inria.fr/flowvr/flowvr-ex/-/archive/v2.3.2/flowvr-ex-v2.3.2.tar.bz2"

    maintainers = ['jbigot']

    version(
        '2.3.2', sha256='4543bd2a9e52f363c981a2aafacae4bf5ae7dd96d7757ebf60b809334b4f3932')
    version(
        '2.3.1', sha256='57cdd18363ef8956c317d63e601fb8667015f3480a8a32fedc1370031aebc278')
    version(
        '2.3.0', sha256='eef405c77eacd9eda86383d84a16dd12805b2f8c35c10560813e635fd20dc692')

    variant('mpi-plugin', default=True,
            description='Enable FlowVR-Daemon MPI plugin.')
    variant('contrib',    default=False,
            description='Enable Flowvr Contribs (various components, API extensions, tests, utility tools, etc.)')
    variant('debug',      default=False, description='Enable -DDEBUG flag')
    variant('doc',        default=False,
            description='Enable Doxygen doc for FlowVR')
    variant('glgraph',    default=False, description='Build FlowVR GLGraph')
    variant('gltrace',    default=False, description='Build FlowVR GLTrace')
    variant('python',     default=True,
            description='Build FlowVR Python Module API')
    variant('tests',      default=False, description='Build the testing tree.')

    depends_on('cmake@3:',  type=('build'))
    depends_on('freeglut',  type=('link'))
    depends_on('glew',      type=('link'))
    depends_on('hwloc',     type=('link'))
    depends_on('mpi',       type=('link'),  when='+mpi-plugin')
    depends_on('libxml2',   type=('link'))
    depends_on('libxmu',    type=('link'))
    depends_on('libxslt',   type=('link'))
    depends_on('python@3:', type=('link'),  when='+python')
    depends_on('swig',      type=('build'), when='+python')

    def cmake_args(self):
        return [
            '-DBUILD_FLOWVRD_MPI_PLUGIN:BOOL={:s}'.format(
                'ON' if '+mpi-plugin' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_CONTRIB:BOOL={:s}'.format(
                'ON' if '+contrib' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_DEBUG_MESSAGES:BOOL={:s}'.format(
                'ON' if '+debug' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_DOXYGEN:BOOL={:s}'.format(
                'ON' if '+doc' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_GLGRAPH:BOOL={:s}'.format(
                'ON' if '+glgraph' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_GLTRACE:BOOL={:s}'.format(
                'ON' if '+gltrace' in self.spec else 'OFF'),
            '-DBUILD_FLOWVR_PYTHONMODULEAPI:BOOL={:s}'.format(
                'ON' if '+python' in self.spec else 'OFF'),
            '-DBUILD_TESTING:BOOL={:s}'.format(
                'ON' if '+tests' in self.spec else 'OFF'),
        ]
