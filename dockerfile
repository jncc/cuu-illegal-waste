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
    gdal-bin

# Setup python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
    && pip3 install virtualenv

# --------- Place machine build layers before this line ---------

# Install snap toolbox scripts.
COPY  SLCCoh_Scot_CommandLine.xml /app/toolchain/SLCCoh_Scot_CommandLine.xml

# Copy workflow requirements
COPY process_slc_pair/requirements.txt /app/workflows/

# Remove static gpt memory configuration
#RUN rm /app/snap/bin/gpt.vmoptions

# Build virtual env
COPY process_slc_pair/install-venv.sh /app/workflows
RUN chmod +x /app/workflows/install-venv.sh \
    && /app/workflows/install-venv.sh \
    && rm -f /app/workflows/install-venv.sh

# Create processing paths
RUN mkdir /input/ \
    && mkdir /static/ \
    && mkdir /state/ \
    && mkdir /working/ \
    && mkdir /output/ 

# Copy the singularity test script
#COPY app/test-luigi.sh ./

# Initialise startup script
COPY process_slc_pair/exec.sh /app/exec.sh
RUN chmod +rx /app/exec.sh
COPY process_slc_pair/CopyState.py ./

# Copy the workflow
COPY process_slc_pair/workflow ./workflows

# Copy workflow config
COPY process_slc_pair/config/luigi.cfg /app/workflows
RUN chmod +r ./workflows/luigi.cfg

# Copy container readme
COPY process_slc_pair/README.md ./

ENTRYPOINT ["/app/exec.sh"]
