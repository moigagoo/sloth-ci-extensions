﻿from setuptools import setup

import docker_exec as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description=ext.__description__,
    long_description=ext.__long_description__,
    author_email=ext.__author_email__,
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['%s.%s' % (package, ext.__name__)],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.2',
        'docker-py'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )