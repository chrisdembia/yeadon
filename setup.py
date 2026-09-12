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
    # NOTE : The minimum versions correspond to those in Ubuntu 24.04 LTS.
    install_requires=[
        'numpy>=1.26.4',
        'pyyaml>=6.0.1',
    ],
    extras_require={
        'gui': ['mayavi>=4.8.1'],
        'doc': [
            'numpydoc>=1.6.0',
            'sphinx>=7.2.6',
        ]
    },
    tests_require=['nose>=1.3.7'],
    test_suite='nose.collector',
    include_package_data=True,
    entry_points={'console_scripts': ['yeadon=yeadon.app:run']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
