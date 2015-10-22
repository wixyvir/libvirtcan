from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='virtimg',

    version='1.0.0',

    description='A virtual disk images operations manager on top of qemu and libguestfs',
    url='http://gitlab/docker/tools',
    author='Cyprien DIOT',
    author_email='cyprien.diot@pmsipilot.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='libvirt guestfs qemu qcow2',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['sh'],
    package_data={
        'DESCRIPTION.rst': ['DESCRIPTION.rst'],
    },
    extras_require={
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'virtimg=virtimg.virtimg:cli_entrypoint',
        ],
    },
)
