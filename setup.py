from setuptools import setup, find_packages

# Note: the version should match the mwalib version at the MAJOR version number level
setup(name='pymwalib',
      version='0.5.0',
      install_requires=[
          'numpy',
      ],
      packages=find_packages())
