FROM jncc/snap-base:0.0.0.17

# Setup app folder
WORKDIR /app

# Configure apt
RUN apt-get update && apt-get -y install \ 
    apt-utils \
    build-essential \
    software-properties-common \
    git \
    bc 

# Install packages from apt
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
    && apt-get update && apt-get -y install \
    python3.7 \
    python-setuptools \
    python3-pip \
    python-gdal \
    gdal-bin

# Setup python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
    && pip3 install virtualenv

# --------- Place machine build layers before this line ---------

# Install snap toolbox scripts.
COPY  SLCCoh_Scot_CommandLine.xml /app/toolchain/SLCCoh_Scot_CommandLine.xml

# Copy workflow requirements
COPY workflows/requirements.txt /app/workflows/

# Remove static gpt memory configuration
#RUN rm /app/snap/bin/gpt.vmoptions

# Build virtual env
COPY workflows/install-venv.sh /app/workflows
RUN chmod +x ./workflows/install-venv.sh \
    && ./workflows/install-venv.sh \
    && rm -f ./workflows/install-venv.sh

# Create processing paths
RUN mkdir /input/ \
    && mkdir /static/ \
    && mkdir /state/ \
    && mkdir /working/ \
    && mkdir /output/ 

# Copy the singularity test script
#COPY app/test-luigi.sh ./

# Initialise startup script
COPY app/exec.sh ./
RUN chmod +rx /app/exec.sh
COPY app/CopyState.py ./

# Copy the workflow
COPY workflows ./workflows

# Copy workflow config
COPY config/app/workflows/luigi.cfg /app/workflows
RUN chmod +r ./workflows/luigi.cfg

# Copy container readme
COPY workflows/README.md ./

ENTRYPOINT ["/app/exec.sh"]
