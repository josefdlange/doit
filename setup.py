# encoding: utf-8
from setuptools import setup, find_packages

import doit


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name='doit-tasks',
    version=doit.__version__,
    description="Tasks on the command line",
    long_description=readme,
    author='Josef Lange',
    author_email='josef.d.lange@me.com',
    license=license,
    install_requires=['clint>=0.3.1'],
    packages=['doit'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ),
    entry_points={
        'console_scripts': [
            'doit = doit.command:main',
        ],
    }
)
