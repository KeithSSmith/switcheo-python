#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
try:  # pip version >= 10.0
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # pip version < 10.0
    from pip.req import parse_requirements
    from pip.download import PipSession

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

# tests_require = [
#     'pytest',
#     ]

setup(
    name='switcheo-python',
    python_requires='>=3.6',
    version='0.0.1',
    author='Keith Smith',
    author_email='keith.scotts@gmail.com',
    license='Apache Software License',
    url='https://github.com/KeithSSmith/switcheo-python',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    # tests_require=tests_require,
    description='Python client for the Switcheo DEX API',
    keywords=['switcheo', 'switcheo-api', 'trade', 'bitcoin', 'ethereum', 'neo', 'BTC', 'ETH', 'NEO',
              'QTUM', 'client', 'api', 'wrapper', 'exchange', 'dex', 'crypto', 'currency', 'trading', 'trading-api'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
