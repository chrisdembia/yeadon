#!/usr/bin/env python

from setuptools import setup, find_packages

exec(open('yeadon/version.py').read())

setup(
    name='yeadon',
    version=__version__,
    author='Chris Dembia',
    author_email='chris530d@gmail.com',
    url="https://github.com/chrisdembia/yeadon/",
    description='Estimates the inertial properties of a human.',
    long_description=open('README.rst').read(),
    keywords="human inertia yeadon sports biomechanics gymnastics",
    license='LICENSE.txt',
    packages=find_packages(),
    # NOTE : The minimum versions correspond to those in Ubuntu 20.04 LTS.
    install_requires=['numpy>=1.16.5',
                      'pyyaml>=5.3.1'],
    extras_require={'gui': ['mayavi>=4.7.1'],
                    'doc': ['sphinx>=1.8.5', 'numpydoc>=0.7.0']},
    tests_require=['nose>=1.3.7'],
    test_suite='nose.collector',
    include_package_data=True,
    scripts=['bin/yeadon'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Physics',
        ],
)
