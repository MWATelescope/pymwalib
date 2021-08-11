from distutils.core import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymwalib',
    packages=['pymwalib'],
    version='0.9.1',
    license='mpl-2.0',
    description='A Python interface for mwalib, a library to read Murchison Widefield Array (MWA) raw visibilities, '
                'voltages and metadata into a common structure',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Greg Sleap',
    author_email='greg.sleap@curtin.edu.au',
    url='https://github.com/MWATelescope/pymwalib',
    download_url='https://github.com/MWATelescope/pymwalib/archive/refs/tags/v0.9.1.tar.gz',
    keywords=['MWA', 'radioastronomy'],
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
