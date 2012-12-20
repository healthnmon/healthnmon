# vim: tabstop=4 shiftwidth=4 softtabstop=4

#          (c) Copyright 2012 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import gettext
import glob
import os

from setuptools import find_packages

# In order to run the i18n commands for compiling and
# installing message catalogs, we use DistUtilsExtra.
# Don't make this a hard requirement, but warn that
# i18n commands won't be available if DistUtilsExtra is
# not installed...

#try:
#    from DistUtilsExtra.auto import setup
#except ImportError:
#    from setuptools import setup
#    print 'Warning: DistUtilsExtra required to use i18n builders. '
#    print 'To build healthnmon with support for message catalogs, you need '
#    print '  https://launchpad.net/python-distutils-extra >= 2.18'

from setuptools import setup
print 'Warning: DistUtilsExtra required to use i18n builders. '
print 'To build healthnmon with support for message catalogs, you need '
print '  https://launchpad.net/python-distutils-extra >= 2.18'

gettext.install('healthnmon', unicode=1)

from healthnmon import version

nova_cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc

    class local_BuildDoc(BuildDoc):

        def run(self):
            for builder in ['html', 'man']:
                self.builder = builder
                self.finalize_options()
                BuildDoc.run(self)

    nova_cmdclass['build_sphinx'] = local_BuildDoc
except Exception:

    pass


def find_data_files(destdir, srcdir):
    package_data = []
    files = []
    for d in glob.glob('%s/*' % (srcdir,)):
        if os.path.isdir(d):
            package_data += find_data_files(
                os.path.join(destdir,
                             os.path.basename(d)), d)
        else:
            files += [d]
    package_data += [(destdir, files)]
    return package_data


setup(
    name='healthnmon',
    version=version.canonical_version_string(),
    description='Healthnmon project provides health and \
    monitoring service for cloud',
    author='healthnmon',
    author_email='healthnmon@lists.launchpad.net',
    url='https://launchpad.net/healthnmon/',
    cmdclass=nova_cmdclass,
    packages=find_packages(exclude=['bin', 'smoketests']),
    include_package_data=True,
    test_suite='nose.collector',
    scripts=['bin/healthnmon', 'bin/healthnmon-manage'],
    py_modules=[],
)
