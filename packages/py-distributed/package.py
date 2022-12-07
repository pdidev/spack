# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other Spack Project Developers,
# Copyright (C) 2021-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

#    homepage = "https://distributed.dask.org/"
#    pypi = "distributed/distributed-2.10.0.tar.gz"
    git = "https://github.com/GueroudjiAmal/distributed.git"
    # 'distributed.dashboard.components' requires 'bokeh', but 'bokeh' is not listed as
    # a dependency. Leave out of 'import_modules' list to avoid unnecessary dependency.
    import_modules = [
        'distributed', 'distributed.deploy', 'distributed.comm',
        'distributed.comm.tests', 'distributed.protocol', 'distributed.cli',
        'distributed.dashboard', 'distributed.http', 'distributed.http.tests',
        'distributed.http.scheduler', 'distributed.http.scheduler.prometheus',
        'distributed.http.worker', 'distributed.diagnostics'
    ]
    version('deisa', branch='main', no_cache=True)

#    version('2021.6.2', sha256='d7d112a86ab049dcefa3b21fd1baea4212a2c03d22c24bd55ad38d21a7f5d148')
#    version('2021.4.1', sha256='4c1b189ec5aeaf770c473f730f4a3660dc655601abd22899e8a0662303662168')
#    version('2020.12.0', sha256='2a0b6acc921cd4e0143a7c4383cdcbed7defbc4bd9dc3aab0c7f1c45f14f80e1')
#    version('2.10.0', sha256='2f8cca741a20f776929cbad3545f2df64cf60207fb21f774ef24aad6f6589e8b')
#    version('1.28.1', sha256='3bd83f8b7eb5938af5f2be91ccff8984630713f36f8f66097e531a63f141c48a')

    depends_on('python@2.7:2.8,3.5:', when='@:1', type=('build', 'run'))
    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.6:8.0', type=('build', 'run'))
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@:2.16.0')
    depends_on('py-cloudpickle@1.3.0:',
               type=('build', 'run'), when='@2.17.0:2.20.0')
    depends_on('py-cloudpickle@1.5.0:', type=('build', 'run'), when='@2.21.0:')
    depends_on('py-contextvars', type=('build', 'run'),
               when='@2020: ^python@:3.6')
    depends_on('py-msgpack', type=('build', 'run'), when='@:2.10.0')
    depends_on('py-msgpack@0.6.0:', type=('build', 'run'), when='@2.11.0:')
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@:1')
    depends_on('py-sortedcontainers@:1,2.0.2:', type=('build', 'run'))
    depends_on('py-tblib', type=('build', 'run'), when='@:2.10.0')
    depends_on('py-tblib@1.6.0:', type=('build', 'run'), when='@2.11.0:')
    depends_on('py-toolz@0.7.4:', type=('build', 'run'), when='@:2.12.0')
    depends_on('py-toolz@0.8.2:', type=('build', 'run'), when='@2.13.0:')
    depends_on('py-tornado@5:', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-tornado@6.0.3:', type=('build', 'run'), when='^python@3.8:')
    depends_on('py-zict@0.1.3:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-futures', when='@:1 ^python@2.7:2.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='@:1 ^python@2.7:2.8',
               type=('build', 'run'))

    def patch(self):
        filter_file('^dask .*', '', 'requirements.txt')
