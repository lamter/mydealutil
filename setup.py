from setuptools import setup, find_packages
import os

import mydealutil


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(name='mydealutil',
      version=mydealutil.__version__,
      keywords='dealutil',
      description='封装一些通用的函数',
      long_description=read("README.md"),
      license='MIT',

      url='https://github.com/lamter/mydealutil',
      author='lamter',
      author_email='lamter.fu@gmail.com',

      packages=find_packages(),
      include_package_data=True,
      install_requires=read("requirements.txt").splitlines(),
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'License :: OSI Approved :: MIT License'],
      )
