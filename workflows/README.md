# 'cuu-illegal-waste'

This code was developed by JNCC under the Copernicus User Uptake Work Package 6 project focussing on monitoring illegal waste using Sentinel-1 imagery. This project is joint-funded by Scottish Government through the JNCC Simple Analysis Ready Data Service Project. 

## Running Luigi script

```sh
luigi --module process_slc_pair ConvertToTif
  --firstInput=/path/to/first/sentinel/1/zip
  --secondInput=/path/to/second/sentinel/1/zip
  --outputBaseFolder=/path/to/output/folder
  --outputSRS=EPSG_CODE i.e. 27700
```

```sh
LUIGI_CONFIG_PATH=./config/process_slc_pair/luigi.cfg PYTHONPATH='.' luigi --module process_slc_pair ConvertToTif --firstInput=./data/incoming/sentinel/1/S1B_IW_SLC__1SDV_20201216T175827_20201216T175854_024731_02F107_7A4B.zip --secondInput=./data/incoming/sentinel/1/S1B_IW_SLC__1SDV_20201228T175827_20201228T175854_024906_02F6B2_FD92.zip --outputBaseFolder=./data/output --outputSRS=27700
```

This will create a folder under the `outputBaseFolder` in the pattern `S1[A|B]_coh_vv_[StartDate]_[EndDate]`.

## Docker container

To build the container, from the base folder run

`docker build -t cuu-illegal-waste:0.1 .`

This makes use of the `jncc/snap-base:0.0.0.17` docker image