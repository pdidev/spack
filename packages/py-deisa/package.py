# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other Spack Project Developers,
# Copyright (C) 2021-2022 Commissariat a l'energie atomique et aux energies alternatives (CEA)
# See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeisa(PythonPackage):
    """
    """

    pypi = 'deisa/deisa-0.2.4.tar.gz'

    maintainers = ['GueroudjiAmal']

    version('0.2.4', sha256='e157bf3ebf052cbdcf9f43f42ba7a99a627de6599d6d152dc49945d0e3da4428')


    depends_on('python@3.9:', type=('build', 'run'))
    depends_on('py-dask', type=('run'))
    depends_on('py-distributed@deisa', type=('run'))
    depends_on('py-setuptools@59:', type='build')
    depends_on('py-pyyaml', type=('build', 'run'))
