# pymwalib
A Python interface for [MWATelescope/mwalib](https://github.com/MWATelescope/mwalib) that provides a simple
interface for reading MWA raw visibilities and exposing the relevant metadata. pymwalib and mwalib
both support reading data produced by the existing (legacy) MWA correlator and the future MWAX
correlator.

## Prerequisites
* Python >=3.6
* mwalib (pymwalib release major version should match mwalib major version- for prerelease versions <1.0.0, compatibility is via the minor version number 0.N.*). See Installing mwalib section below.
* numpy
 
## Installing mwalib
* Download the relevant release from [MWATelescope/mwalib github releases](https://github.com/MWATelescope/mwalib/releases)
```bash
$ wget https://github.com/MWATelescope/mwalib/releases/download/v0.3.0/libmwalib-0.3.0-linux_x86_64.tar.gz -O libmwalib-0.3.0-linux_x86_64.tar.gz 
```
* Create a directory and extract the libmwalib-X.X.X-linux_x86_64.tar.gz tarball file. (Where X.X.X is the relevant version number).
```bash
$ mkdir -p mwalib
$ tar -xvf libmwalib-0.3.0-linux_x86_64.tar.gz -C mwalib
```
* The next step can be done one of two ways:
  - A) Copy the header and library files into your system `/usr/local/include` and `/usr/local/lib` paths.
```bash
$ sudo cp lib/mwalib.* /usr/local/lib/.
$ sudo cp include/mwalib.h /usr/local/include/.
```
  - OR B) Append the path to the library files to your `LD_LIBRARY` path. `/absolute/path/to/mwalib/lib/directory` is the absolute path to the `lib` directory from the extracted `mwalib` release. NOTE: to make this change permanent for any new login sessions you should add the `export` line to your `.bashrc` file.
```bash
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/absolute/path/to/mwalib/lib/directory
```

## Clone this repository
* Clone master or a specific release / commit- the example below will clone the master branch.
```bash
$ git clone https://github.com/MWATelescope/pymwalib.git pymwalib
```

## Setup virtual environment and install requirements
* Create virtual environment
```bash
$ cd pymwalib
$ python3 -m venv env
```
* Activate the virtual environment
```bash
$ source env/bin/activate
(env)$ 
```
* Install requirements
```bash
(env)$ pip install -r requirements.txt 
```

## Build pymwalib
* Run the setup.py to build the library
```bash
(env)$ python setup.py install
```

## Test
* Run one of the example scripts against an MWA observation (to download MWA Observations, please visit the [MWA ASVO](https://asvo.mwatelescope.org) data portal).
```bash
(env)$ python examples/example01.py -m path_to_metafits.metafits path_to_gpuboxfile01.fits path_to_gpuboxfile02.fits ... 
```

## Docker
### Build the image
You can also build a docker container with pymwalib preinstalled:
```bash
$ docker build . -t pymwalib:latest
```

### Run the container
One way to launch the container is to use docker run, for example:
```
docker run --name my_pymwalib --volume=/host_data:/data --entrypoint="" --rm=true pymwalib:latest python /pymwalib/examples/example01.py -m /data/1101503312.metafits /data/1101503312_20141201210818_gpubox01_00.fits /data/1101503312_20141201210818_gpubox02_00.fits 
```
* This assumes /host_data is a directory on the machine running docker (host) containing the gpubox files and metafits for an observation. 