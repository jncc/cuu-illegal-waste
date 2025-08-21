# 'cuu-illegal-waste'

This code was developed by JNCC under the Copernicus User Uptake Work Package 6 project focussing on monitoring illegal waste using Sentinel-1 imagery. This project is joint-funded by Scottish Government through the JNCC Simple Analysis Ready Data Service Project. 

## Running Luigi script

There are two endpoints fo the workflow, the first is `TransferOutputs` which just generates the output and exits. The second endpoint `CleanupCompletedProducts` essentially will do the same but then will remove the input folder and working files for the pair provided to the container. The Luigi script takes in two arguments alongside its config file which contains a set of defaults that are designed to work with a containerized version of this workflow.

```sh
luigi --module process_slc_pair TransferOutputs
  --inputFolder=S1B_20201110T175829_20201122T175828
  --outputSRS=27700
  --local-scheduler
```

`inputFolder` is the name of the folder pair, the layout of which contains two Sentinel 1 SLC scenes covering the same area for consecutive passes. Each input folder should be of the form `S1[A|B|C]_[START-YYYYMMDDThhmmss]_[END-YYYYMMDDThhmmss]` (i.e. `S1B_20201110T175829_20201122T175828`) such that the overal `input` folder looks like the following;

    input/
    ├── S1B_20201029T175829_20201110T175829
    │   ├── S1B_IW_SLC__1SDV_20201029T175829_20201029T175856_024031_02DAD5_7692.SAFE
    │   ├── S1B_IW_SLC__1SDV_20201029T175829_20201029T175856_024031_02DAD5_7692.SAFE
    ├── S1B_20201110T175829_20201122T175828/
    │   ├── S1B_IW_SLC__1SDV_20201110T175829_20201110T175856_024206_02E040_D8A8.SAFE
    │   ├── S1B_IW_SLC__1SDV_20201122T175828_20201122T175855_024381_02E5CA_0DC7.SAFE
    ├── ...

Each Pair folder should contain two inputs matching the name (i.e. start and end date for capture), these can be symlinks or the real folder as appropriate.

`outputSRS` is the EPSG code that the output should be reprojected to, i.e. 27700 is EPSG:27700 or OSGB.

Working paths and other configurable items are controlled via a `luigi.cfg` file `paths` dictionary i.e. 

```
paths = {"input":"/input",
            "state":"/state",
            "static":"/static",
            "working":"/working",
            "output":"/output",
            "scripts": "/app/toolchain/scripts",
            "toolchain": "/app/toolchain",
            "executable": "/usr/local/esa-snap/bin/gpt",
            "toolchainXML": "SLCCoh_Scot_CommandLine.xml"
            }
```

These shouldn't be altered unless you are running the workflow outside of this container, but can be specified using the `LUIGI_CONFIG_PATH` environment variable i.e.

```sh
LUIGI_CONFIG_PATH=./config/process_slc_pair/luigi.cfg PYTHONPATH='.' luigi --module process_slc_pair TransferOutputs --inputFolder=S1B_20201110T175829_20201122T175828 --outputSRS=27700 --local-scheduler
```

Running this workflow will create a GeoTiff under the `/output` in the pattern `S1[A|B|C]_coh_vv_[StartDate]_[EndDate].tif`.

`/output` is the base directory where final outputs should be written to. The SNAP outputs can also be found in the `/working` directory under folders with pattern `S1[A|B]_coh_vv_[StartDate-YYYYMMDD]_[EndDate-YYYYMMDD]` (i.e. `S1B_coh_vv_20201110_20201122`) if `CleanupCompletedProducts` has not been run. State files can also be found here which are useful for debugging.

    output/
    ├── S1B_coh_vv_20201029_20201110.tif
    ├── S1B_coh_vv_20201110_20201122.tif
    working/
    ├── S1B_20201029T175829_20201110T175829
    │   ├── working
    │   │   ├── S1B_coh_vv_20201029_20201110
    │   │   │   ├── S1B_coh_vv_20201029_20201110.data
    │   │   │   │   ├── vector_data
    │   │   │   │   │   ├── ground_control_points.csv
    │   │   │   │   │   ├── pins.csv
    │   │   │   │   ├── coh_VV_29Oct2020_10Nov2020.hdr
    │   │   │   │   ├── coh_VV_29Oct2020_10Nov2020.img
    │   │   │   ├── S1B_coh_vv_20201029_20201110.dim
    │   │   │   ├── S1B_coh_vv_20201029_20201110.tif
    │   │   │   ├── S1B_coh_vv_20201029_20201110_tmp1.tif
    │   │   ├── S1B_coh_vv_20201110_20201122
    │   │   │   ├── ...
    │   ├── state
    │   │   |── TransferOutputs.json
    │   │   ├── ConvertToTif.json
    │   │   ├── GetConfiguration.json
    │   │   ├── ProcessSLCPair.json
    ├── S1B_20201110T175829_20201122T175828
    │   ├── working
    |   │   ├── ...
    │   ├── state
    |   │   ├── ...
 
The final output of this workflow is a Cloud Optimised GeoTiff file which is a reprojected form of the `.img` file in the `.data` folder.

## Docker container 

To build the container, from the base folder run

`docker build -t cuu-illegal-waste:0.1 .`

This makes use of the `jncc/snap-base:1.0.5-SNAP-12.0.0` docker image

### Example:

```
docker run -i -v /data/input:/input -v /data/output:/output -v /data/state:/state -v /data/static:/static -v data/working:/working jncc/cuu-illegal-waste CleanupCompletedProducts   --inputFolder=S1B_20201110T175829_20201122T175828 --outputSRS=27700 --local-scheduler
```