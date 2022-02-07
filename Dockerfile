# Base our image on the python:3.8.3 image
FROM python:3.8.3

# Update the OS
RUN apt-get -y update; \
    apt-get -y install git \
                       wget \
                       build-essential \
                       python3-dev; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*; \
    apt-get -y autoremove;

# Get mwalib
RUN cd /tmp; \
    mkdir libmwalib; \
    wget "https://github.com/MWATelescope/mwalib/releases/download/v0.13.0/mwalib-v0.13.0-linux_x86_64.tar.gz" -O libmwalib.tar.gz; \
    tar -xzf libmwalib.tar.gz -C libmwalib; \
    cd libmwalib; \
    cp libmwalib.so /usr/local/lib/.; \
    cp libmwalib.a /usr/local/lib/.; \
    cp mwalib.h /usr/local/include/.; \
    cd ..; \
    rm -rf libmwalib; \
    ldconfig;

# Get pymwalib
RUN cd /; \
    git clone "https://github.com/MWATelescope/pymwalib.git"; \
    cd pymwalib; \
    pip install -r requirements.txt; \
    python setup.py install;

# Install requirements for examples
RUN pip install joblib

ENTRYPOINT bash
