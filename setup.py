#!/usr/bin/env python

import os
import sys

from setuptools import setup

version = "0.0.1"

with open('README.md') as readme_file:
    readme = readme_file.read()

history=''
# with open('CHANGELOG.md') as history_file:
#     history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as req_file:
    requirements = req_file.read().rstrip('\n').split('\n')

long_description = readme + '\n\n' + history

# if sys.argv[-1] == 'publish':
#     os.system('python setup.py sdist upload')
#     os.system('python setup.py bdist_wheel upload')
#     sys.exit()

# if sys.argv[-1] == 'tag':
#     os.system("git tag -a %s -m 'version %s'" % (version, version))
#     os.system("git push --tags")
#     sys.exit()


if sys.argv[-1] == 'readme':
    print(long_description)
    sys.exit()



setup(
    name='atp',
    version=version,
    description=('Algorithmic Trading Platform'),
    long_description=long_description,
    author='Yohannes Libanos',
    # packages=[
    #     'atp.data','atp.lib'#,'algotrade.compute','algotrade.portfolio'
    # ],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    package_dir={'atp': 'atp'},

    # entry_points={
        # 'autobahn.asyncio.wamplet': [
        #     'backend = algotrade.dataservice.socket:DataService'
        # ],
    #     'apt':'apt/main:main'
    #     'console_scripts': [
    #         'apt = apt.main:main',
    #     ]
    # },
    include_package_data=True,
    install_requires=requirements,
    # extras_require={
    #     ':sys_platform=="win32" and python_version=="2.7"': [
    #         'PyYAML>=3.10'
    #     ],
    #     ':sys_platform!="win32" or python_version!="2.7"': [
    #         'ruamel.yaml>=0.10.12'
    #     ]
    # },
    license='BSD',
    zip_safe=False,
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        # 'Development Status :: 3 - Alpha',
        # 'Environment :: Console',
        # 'Intended Audience :: Developers',
        'Natural Language :: English',
        # 'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    keywords=(
        'Algo Trade, Quantitative Finance, Trading Platform, Python, Trading'
    )
)
