import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

setup(
    name="django-nopassword",
    version='0.6.0',
    url='http://github.com/relekang/django-nopassword',
    author='Rolf Erik Lekang',
    author_email='me@rolflekang.com',
    description='Authentication backend for django that uses email verification instead of passwords',
    packages=find_packages(exclude='tests'),
    tests_require=['tox'],
    cmdclass={'test': Tox},
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ]
)
