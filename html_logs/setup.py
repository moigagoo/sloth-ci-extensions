from setuptools import setup

import html_logs as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description='Additional HTML logs for Sloth CI apps',
    long_description='This Sloth CI extension adds an extra HTML logger to Sloth CI apps.',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['%s.%s' % (package, ext.__name__)],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.2'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
