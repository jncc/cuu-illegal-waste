# 'cuu-illegal-waste'

This code was developed by JNCC under the Copernicus User Uptake Work Package 6 project focussing on monitoring illegal waste using Sentinel-1 imagery. This project is joint-funded by Scottish Government through the JNCC Simple Analysis Ready Data Service Project. 

## Running Luigi script

```sh
luigi --module process_slc_pair ConvertToTif
  --inputFolder=S1B_20201110T175829_20201122T175828
  --outputSRS=EPSG_CODE i.e. 27700
```

```sh
LUIGI_CONFIG_PATH=./config/process_slc_pair/luigi.cfg PYTHONPATH='.' luigi --module process_slc_pair ConvertToTif --inputFolder=S1B_20201110T175829_20201122T175828 --outputSRS=27700
```

This will create a folder under the `/output` in the pattern `S1[A|B]_coh_vv_[StartDate]_[EndDate]`.

Working paths are controlled via the `luigi.cfg` file `paths` dictionary i.e. 

```
paths = {"input":"/input",
            "state":"/state",
            "static":"/static",
            "working":"/working",
            "output":"/output",
            "scripts": "/app/toolchain/scripts",
            "toolchain": "/app/toolchain",
            "executable": "/app/snap/bin/gpt",
            "toolchainXML": "SLCCoh_Scot_CommandLine.xml"
            }
```

This workflow is being desinged to be run as a container under docker or singularity container so best practice would be to mount the following folders to the container;

  - `/input` the base directory that contains Sentinel 1 scene pair folders with the form `S1[A|B]_[START-YYYYMMDDThhmmss]_[END-YYYYMMDDThhmmss]` (i.e. `S1B_20201110T175829_20201122T175828`)
  - `/output` the base directory where outputs should be written to which will create folders of the form `S1[A|B]_coh_vv_[StartDate-YYYYMMDD]_[EndDate-YYYYMMDD]` (i.e. `S1B_coh_vv_20201110_20201122`).
 
## Docker container 

To build the container, from the base folder run

`docker build -t cuu-illegal-waste:0.1 .`

This makes use of the `jncc/snap-base:0.0.0.17` docker image