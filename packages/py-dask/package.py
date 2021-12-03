# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    pypi = "dask/dask-1.1.0.tar.gz"

    maintainers = ['skosukhin']

    version('2021.11.2')


    variant('array',       default=True, description='Install requirements for dask.array')
    variant('bag',         default=True, description='Install requirements for dask.bag')
    variant('dataframe',   default=True, description='Install requirements for dask.dataframe')
    variant('distributed', default=True, description='Install requirements for dask.distributed')
    variant('diagnostics', default=False, description='Install requirements for dask.diagnostics')
    variant('delayed',     default=True, description='Install requirements for dask.delayed (dask.imperative)')
    variant('yaml',        default=True, description='Ensure support for YAML configuration files')

    conflicts('~bag', when='@2021.3.1:')
    conflicts('+distributed', when='@:0.4.0,0.7.6:0.8.1')
    conflicts('+diagnostics', when='@:0.5.0')
    conflicts('~delayed', when='@2021.3.1:')
    conflicts('+yaml', when='@:0.17.5')
    conflicts('~yaml', when='@2.17.1:')

    depends_on('python@2.7:2.8,3.5:',   type=('build', 'run'))
    depends_on('python@3.5:',           type=('build', 'run'), when='@2.0.0:')
    depends_on('python@3.6:',           type=('build', 'run'), when='@2.7.0:')
    depends_on('python@3.7:',           type=('build', 'run'), when='@2021.3.1:')

    depends_on('py-setuptools',         type='build')

    # Common requirements
    depends_on('py-pyyaml',             type=('build', 'run'), when='@2.17.1:')
    depends_on('py-cloudpickle@1.1.1:', type=('build', 'run'), when='@2021.3.1:')
    depends_on('py-fsspec@0.6.0:',      type=('build', 'run'), when='@2021.3.1:')
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2021.3.1:')
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2021.3.1:')
    depends_on('py-packaging',          type=('build', 'run'), when='@2021.11.2')
    # Requirements for dask.array
    depends_on('py-numpy',              type=('build', 'run'), when='@:0.17.1 +array')
    depends_on('py-numpy@1.10.4:',      type=('build', 'run'), when='@0.17.2: +array')
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='@0.17.3: +array')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.1: +array')
    depends_on('py-numpy@1.15.1:',      type=('build', 'run'), when='@2020.12.0: +array')
    depends_on('py-numpy@1.16.0:',      type=('build', 'run'), when='@2021.3.1: +array')

    depends_on('py-toolz',              type=('build', 'run'), when='@:0.6.1 +array')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +array')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +array')
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0:2021.3.0 +array')

    # Requirements for dask.bag
    depends_on('py-dill',               type=('build', 'run'), when='@:0.7.5 +bag')
    depends_on('py-cloudpickle',        type=('build', 'run'), when='@0.7.6: +bag')
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@0.8.2: +bag')
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@2.13.0:2021.3.0 +bag')

    depends_on('py-fsspec@0.3.3:',      type=('build', 'run'), when='@2.2.0: +bag')
    depends_on('py-fsspec@0.5.1:',      type=('build', 'run'), when='@2.5.0: +bag')
    # The dependency on py-fsspec is non-optional starting version 2021.3.1
    depends_on('py-fsspec@0.6.0:',      type=('build', 'run'), when='@2.8.0:2021.3.0 +bag')

    depends_on('py-toolz',              type=('build', 'run'), when='@:0.6.1 +bag')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +bag')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +bag')
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0:2021.3.0 +bag')

    depends_on('py-partd@0.3.2:',       type=('build', 'run'), when='@0.6.0: +bag')
    depends_on('py-partd@0.3.3:',       type=('build', 'run'), when='@0.9.0: +bag')
    depends_on('py-partd@0.3.5:',       type=('build', 'run'), when='@0.10.2: +bag')
    depends_on('py-partd@0.3.6:',       type=('build', 'run'), when='@0.12.0: +bag')
    depends_on('py-partd@0.3.7:',       type=('build', 'run'), when='@0.13.0: +bag')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='@0.15.0: +bag')
    # The dependency on py-partd is non-optional starting version 2021.3.1
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2.0.0:2021.3.0 +bag')

    # Requirements for dask.dataframe
    depends_on('py-numpy',              type=('build', 'run'), when='@:0.17.1 +dataframe')
    depends_on('py-numpy@1.10.4:',      type=('build', 'run'), when='@0.17.2: +dataframe')
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='@0.17.3: +dataframe')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.1: +dataframe')
    depends_on('py-numpy@1.15.1:',      type=('build', 'run'), when='@2020.12.0: +dataframe')
    depends_on('py-numpy@1.16.0:',      type=('build', 'run'), when='@2021.3.1: +dataframe')

    depends_on('py-pandas@0.16.0:',     type=('build', 'run'), when='+dataframe')
    depends_on('py-pandas@0.18.0:',     type=('build', 'run'), when='@0.9.0: +dataframe')
    depends_on('py-pandas@0.19.0:',     type=('build', 'run'), when='@0.14.0: +dataframe')
    depends_on('py-pandas@0.21.0:',     type=('build', 'run'), when='@1.2.1: +dataframe')
    depends_on('py-pandas@0.23.0:',     type=('build', 'run'), when='@2.11.0: +dataframe')
    depends_on('py-pandas@0.25.0:',     type=('build', 'run'), when='@2020.12.0: +dataframe')

    depends_on('py-toolz',              type=('build', 'run'), when='@:0.6.1 +dataframe')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +dataframe')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +dataframe')
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0:2021.3.0 +dataframe')

    depends_on('py-partd@0.3.2:',       type=('build', 'run'), when='@0.6.0: +dataframe')
    depends_on('py-partd@0.3.3:',       type=('build', 'run'), when='@0.9.0: +dataframe')
    depends_on('py-partd@0.3.5:',       type=('build', 'run'), when='@0.10.2: +dataframe')
    depends_on('py-partd@0.3.7:',       type=('build', 'run'), when='@0.13.0: +dataframe')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='@0.15.0: +dataframe')
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2.0.0: +dataframe')
    # The dependency on py-partd is non-optional starting version 2021.3.1
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2.0.0:2021.3.0 +dataframe')

    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@0.8.2:2.6.0 +dataframe')

    depends_on('py-fsspec@0.3.3:',      type=('build', 'run'), when='@2.2.0: +dataframe')
    depends_on('py-fsspec@0.5.1:',      type=('build', 'run'), when='@2.5.0: +dataframe')
    # The dependency on py-fsspec is non-optional starting version 2021.3.1
    depends_on('py-fsspec@0.6.0:',      type=('build', 'run'), when='@2.8.0:2021.3.0 +dataframe')

    # Requirements for dask.distributed
    depends_on('py-dill',               type=('build', 'run'), when='@:0.7.5 +distributed')
    depends_on('py-pyzmq',              type=('build', 'run'), when='@:0.7.5 +distributed')
    depends_on('py-distributed',        type=('build', 'run'), when='@0.8.2: +distributed')
    depends_on('py-distributed@1.9:',   type=('build', 'run'), when='@0.9.0: +distributed')
    depends_on('py-distributed@1.10:',  type=('build', 'run'), when='@0.10.0: +distributed')
    depends_on('py-distributed@1.14:',  type=('build', 'run'), when='@0.12.0: +distributed')
    depends_on('py-distributed@1.15:',  type=('build', 'run'), when='@0.13.0: +distributed')
    depends_on('py-distributed@1.16:',  type=('build', 'run'), when='@0.14.1: +distributed')
    depends_on('py-distributed@1.20:',  type=('build', 'run'), when='@0.16.0: +distributed')
    depends_on('py-distributed@1.21:',  type=('build', 'run'), when='@0.17.0: +distributed')
    depends_on('py-distributed@1.22:',  type=('build', 'run'), when='@0.18.0: +distributed')
    depends_on('py-distributed@2.0:',   type=('build', 'run'), when='@2.0.0: +distributed')
    depends_on('py-distributed@2020.12.0:', type=('build', 'run'), when='@2020.12.0: +distributed')
    depends_on('py-distributed@2021.6.2:',  type=('build', 'run'), when='@2021.6.2: +distributed')

    # Requirements for dask.diagnostics
    depends_on('py-bokeh@1.0.0:',       type=('build', 'run'), when='@2.0.0: +diagnostics')
    depends_on('py-bokeh@1.0.0:1,2.0.1:', type=('build', 'run'), when='@2.26.0: +diagnostics')

    # Requirements for dask.delayed
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@2.7.0: +delayed')
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@2.13.0:2021.3.0 +delayed')

    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.8.1: +delayed')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +delayed')
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0:2021.3.0 +delayed')

    # Support for YAML configuration files
    # The dependency on py-pyyaml is non-optional starting version 2.17.1
    depends_on('py-pyyaml',             type=('build', 'run'), when='@0.18.0:2.17.0 +yaml')

    @property
    def import_modules(self):
        modules = ['dask']

        if self.spec.satisfies('@0.9.0:'):
            modules.append('dask.bytes')

        if self.spec.satisfies('@:0.20.2'):
            modules.append('dask.store')

        if '+array' in self.spec:
            modules.append('dask.array')

        if '+bag' in self.spec:
            modules.append('dask.bag')

        if self.spec.satisfies('@:0.7.5 +distributed'):
            modules.append('dask.distributed')

        if '+dataframe' in self.spec:
            modules.append('dask.dataframe')
            if self.spec.satisfies('@0.8.2:'):
                modules.append('dask.dataframe.tseries')
            if self.spec.satisfies('@0.12.0:'):
                modules.append('dask.dataframe.io')

        if '+diagnostics' in self.spec:
            modules.append('dask.diagnostics')

        return modules
