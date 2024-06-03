FROM jncc/snap-base-dev:1.0.12

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
RUN apt-get update && apt-get -y install \
    python3 \
    python3-pip \
    gdal-bin

# --------- Place machine build layers before this line ---------

# Install snap toolbox scripts.
COPY SLCCoh_Scot_CommandLine.xml /app/toolchain/SLCCoh_Scot_CommandLine.xml

# Copy workflow requirements
COPY workflows/requirements.txt /app/workflows/

# Remove static gpt memory configuration
#RUN rm /app/snap/bin/gpt.vmoptions

# Build virtual env
COPY workflows/install-venv.sh /app/workflows
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
COPY workflows/exec.sh /app/exec.sh
RUN chmod +rx /app/exec.sh
COPY workflows/CopyState.py ./

# Copy the workflow
COPY workflows/process_slc_pair ./workflows/process_slc_pair

# Copy workflow config
COPY workflows/config/process_slc_pair/luigi.cfg.template /app/workflows/luigi.cfg
RUN chmod +r ./workflows/luigi.cfg

# Copy container readme
COPY workflows/README.md ./

ENTRYPOINT ["/app/exec.sh"]
