# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other Spack Project Developers,
# Copyright (C) 2021-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeisa(PythonPackage):
    """
    """

    pypi = 'deisa/deisa-0.2.1.tar.gz'

    maintainers = ['GueroudjiAmal']

    version('0.2.1', sha256='c91b8cfcf890f26e24d643ed3eaeae7a5e46bb5db92bd3295fd7d1b7e39bf97b')


    depends_on('python@3.9:', type=('build', 'run'))
    depends_on('py-dask', type=('run'))
    depends_on('py-distributed@deisa', type=('run'))
    depends_on('py-setuptools@59:', type='build')
    depends_on('py-pyyaml', type=('build', 'run'))
