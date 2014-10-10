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
    install_requires=['numpy', 'pyyaml'],
    extras_require={'gui': ['mayavi'],
                    'doc': ['sphinx', 'numpydoc']},
    tests_require=['nose'],
    test_suite='nose.collector',
    include_package_data=True,
    scripts=['bin/yeadon'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Physics',
        ],
)
